extern crate fastrand;
extern crate pancurses;

// Biblioteca externas.
use pancurses::*;
// Biblioteca do Rust:
use std::time::{Instant, Duration};
// Módulos propriamente implementados.
use super::modelos::{ Bola, Dimensao, Direcao, Barra, Parede };
use crate::{ MOVIMENTACAO, TOQUES_LIMITE, TAXA_DE_QUADROS };
use super::estatisticas::{BarraMetadados, BolaMetadados};


pub struct Tabuleiro {
   // Tela virtual do ncurses que é efetuado o desenho.
   tela: Window,

   // Dimensão dela. Pode ser menor do que o ncurses ocupa.
   dimensao: Dimensao,

   // Taxa de quadros por segundo.
   taxa: i32,
}

impl Tabuleiro
{
   pub fn inicia() -> Self 
   {
      let tabuleiro = initscr();
      // Obtendo dimensão do tabuleiro.
      let dimensao = Dimensao {
         altura: tabuleiro.get_max_y() as u16,
         largura: tabuleiro.get_max_x() as u16,
      };

      Tabuleiro::configura_janela(&tabuleiro);
      Tabuleiro::inicia_paleta_de_cores();
      tabuleiro.draw_box(0, 0);

      Self { tela: tabuleiro, dimensao:dimensao, taxa:TAXA_DE_QUADROS }
   }

   pub fn dimensao(&self) -> Dimensao
      { self.dimensao }

   pub fn tela<'x>(&'x mut self) -> &'x Window
      { &self.tela }

   pub fn entrada(&self) -> Option<Input>
      { self.tela.getch() }

   pub fn renderiza(&mut self)
   {
      self.tela.draw_box(0, 0);
      self.tela.refresh();
      napms(self.taxa);
      self.tela.clear();
   }

   pub fn mensagem_centralizada(&mut self, texto: &str)
   {
      let d = self.dimensao;
      #[allow(non_snake_case)]
      let (C, A) = (d.largura, d.altura); 
      let length = texto.len() as u16;
      let y = A / 2;
      let x = (C - length) / 2;

      self.tela.attrset(A_BOLD);
      self.tela.color_set(2);
      self.tela.mv(y as i32, x as i32);
      self.tela.addstr(texto);
      self.tela.color_set(0);
      self.tela.attrset(A_NORMAL);
   }

   fn configura_janela(janela: &Window)
   {
      curs_set(0);
      noecho();
      cbreak();
      start_color();
      use_default_colors();
      janela.keypad(true);
      janela.nodelay(true);
   }

   fn inicia_paleta_de_cores()
   {
      const TRANSPARENTE: i16 = 0;

      init_pair(0, COLOR_WHITE, TRANSPARENTE);
      init_pair(1, COLOR_RED, TRANSPARENTE);
      init_pair(2, COLOR_YELLOW, TRANSPARENTE);
      init_pair(3, COLOR_BLUE, TRANSPARENTE);
   }
}

/* Desenha a cobrinha onde quer que ela vá. Com a array de direções que são 
 * dado para ela "virar" a cada novo passo. Retorna todos os dados que foram 
 * gerados durante tanta iteração.
 */
pub fn roda_jogo(
   barra:&mut Barra, bola:&mut Bola, tabuleiro:&mut Tabuleiro,
   barmetadata: &mut BarraMetadados, ballmetadata: &mut BolaMetadados
){
   // Quantia de colisões abaixo.
   let mut toques_no_chao: u8 = 0;
   // Quantia de choques com a barra.
   let mut qtd_rebates_barra: u16 = 0;
   // Variável para obter tempo.
   let ti = Instant::now();
   let dados_brr = barmetadata;
   let dados_bl = ballmetadata;

   // Desativado no modo debug, pois tira foco do principal.
   if !(cfg!(debug_assertions))
      { animacao_de_abertura(tabuleiro); }

   // laço que executa o jogo.
   'unico: loop {
      // Verifica se houve uma derrota.
      colisoes_monitoramento(
         bola, barra,
         &mut toques_no_chao,
         &mut qtd_rebates_barra
      );

      if toques_no_chao > TOQUES_LIMITE { break }

      // Coletando dados antes do "evento".
      dados_brr.qtd_rebatidas = qtd_rebates_barra;
      dados_brr.atualiza(
         barra,
         (barra.esqueleto.posicao, barra.esqueleto.sentido)
      );
      // renomeando para legibilidade.
      let pos = bola.esqueleto.posicao;
      let sent = bola.esqueleto.sentido;
      let (bateu, parede):(bool, Parede) = bola.colidiu();
      if bateu { 
         // colocar ambos.
         dados_bl.atualiza(
            Some((pos, sent)), 
            Some((pos, parede, sent))
         ); 
      } 
      // apenas colocar localização e vetor-sentido.
      else
         { dados_bl.atualiza(Some((pos, sent)), None); }

      // implemetando rebote caso bate na barra.
      colisao_bola_barra(bola, barra);
      // move a bola e a barra:
      bola.move_n_vezes(MOVIMENTACAO);
         // está baseado na direção dada.
      match controle_do_jogo(tabuleiro, barra, dados_brr)
      { 
         Some(instrucao) => 
            { barra.move_n_vezes(instrucao, MOVIMENTACAO); }
         None => {break 'unico}
      };
      // Desenha bola e barra:
      bola.desenha_bola(tabuleiro.tela());
      barra.desenha_barra(tabuleiro.tela());
      // informação barra de status.
      /*barra_status(
         barra, bola, tabuleiro, 
         &toques_no_chao, 
         &qtd_rebates_barra,
         ti.elapsed()
      );*/
      tabuleiro.renderiza();
   }

   // Desativado no modo debug, pois é irrelevante.
   if (cfg!(debug_assertions))
      { animacao_de_inercia_pos_termino(tabuleiro, bola, barra); }
   endwin();
}
// Implementando fora do módulo a função de plotar os objetos do jogo:
impl Bola {
   pub fn desenha_bola(&self, tabuleiro:&Window)
   {
      // nomeando a coordenada de modo mais legível...
      let l:i32 = self.esqueleto.posicao.y as i32;
      let c:i32 = self.esqueleto.posicao.x as i32;
      // desenhando objeto propriamente...
      tabuleiro.attrset(A_BOLD);
      tabuleiro.color_set(1);
      tabuleiro.mvaddch(l,c,self.esqueleto.forma);
      tabuleiro.attrset(A_NORMAL);
      tabuleiro.color_set(0);
   }
}

impl Barra {
   // desenha na tela a cobrinha.
   pub fn desenha_barra(&self, tabuleiro:&Window) {
      // apelidando variáveis importantes...
      let l:i32 = self.esqueleto.posicao.y as i32;
      let c:i32 = self.esqueleto.posicao.x as i32;
      // só move respeitando o limite da parede. 
      // string formando barra a ser "impressa".
      let formato:String = {
         self.esqueleto.forma
         .to_string()
         .repeat(self.comprimento as usize)
      };
      // desenha.
      tabuleiro.attrset(A_BOLD);
      tabuleiro.color_set(2);
      tabuleiro.mvaddstr(l, c, formato.as_str());
      tabuleiro.color_set(0);
      tabuleiro.attrset(A_NORMAL);
   }
}

/* escrevendo simetria reflexiva para o tipo
 * direção. */
impl Direcao {
   pub fn simetrica(&self) -> Self {
      match *self {
         Direcao::Norte => Direcao::Sul,
         Direcao::Sul => Direcao::Norte,
         Direcao::Leste => Direcao::Oeste,
         Direcao::Oeste => Direcao::Leste,
         Direcao::Noroeste => Direcao::Sudoeste,
         Direcao::Nordeste => Direcao::Sudeste,
         Direcao::Sudeste => Direcao::Nordeste,
         Direcao::Sudoeste => Direcao::Noroeste,
      }
   }
}


/* Altera rota da bolinha após colisão
 * levando em conta seu sentido atual,
 * assim com o da barra.
 */
pub fn colisao_bola_barra(bo:&mut Bola, ba:&mut Barra) {
   // verifica se tocou o campo da barra.
   if ba.foi_acertada(bo.esqueleto.posicao) { 
      // apelido com direção atual.
      let sentido = bo.esqueleto.sentido;
      /* aplicando dado viciado ao determinar direção,
       * então 70% das colisão refletem na direção
       * simétrica. */
      if fastrand::u8(1..10) <= 7 {
         bo.esqueleto.sentido = match sentido { 
            Direcao::Sul => {
               // 20% na direção convêncional.
               if fastrand::u8(1..10) <= 8 { 
                  impulsiona_bola(bo, sentido.simetrica())
               }
               // 80% vai precisamente as diagonais.
               else {
                  match fastrand::bool() {
                     true => { 
                        impulsiona_bola(bo, Direcao::Nordeste)
                     },
                     false => { 
                        impulsiona_bola(bo, Direcao::Noroeste)
                     },
                  }
               }
            },
            _ => sentido.simetrica()
         };
      }
      /* 30% dos demais casos; eles serão tratados todos
       * podendo ou não ir na direção "convêncional"
       * ou perpendicular a barra. O "norte" e "sul"
       * tem tratamentos especiais para não permitir
       * um "loop" de rebotes. */
      else {
         bo.esqueleto.sentido = match sentido {
            // tratando colisão superior da barra.
            Direcao::Sudeste => {
               match fastrand::bool() {
                  true => Direcao::Norte,
                  false => impulsiona_bola(bo, Direcao::Noroeste),
               }
            },
            Direcao::Sudoeste => {
               match fastrand::bool() {
                  true => Direcao::Norte,
                  false => impulsiona_bola(bo, Direcao::Nordeste),
               }
            },
            Direcao::Sul => {
               match fastrand::bool() {
                  true => impulsiona_bola(bo, Direcao::Noroeste),
                  false => impulsiona_bola(bo, Direcao::Nordeste),
               }
            },
            // agora da parte inferior...
            Direcao::Nordeste => {
               match fastrand::bool() {
                  false => impulsiona_bola(bo, Direcao::Sul),
                  true => impulsiona_bola(bo, Direcao::Sudoeste),
               }
            },
            Direcao::Noroeste => {
               match fastrand::bool() {
                  false => impulsiona_bola(bo, Direcao::Sul),
                  true => impulsiona_bola(bo, Direcao::Sudeste),
               }
            },
            // para não ficar num laço-infinito cima-baixo.
            Direcao::Norte => {
               match fastrand::bool() {
                  false => impulsiona_bola(bo,Direcao::Sudoeste),
                  true => impulsiona_bola(bo, Direcao::Sudeste),
               }
            },
            // caso contrário direção convencional.
            _ => sentido,
         };
      }
   }
}

/* Representa informações no "rodapé" da tela, tipo: o tempo de jogo, colisões 
 * da bolinha com as paredes; colisão com a barra, e etc... */
pub fn mostra_barra_status(
   brr:&Barra, bl:&Bola, janela:&Window, qtd:&u8, qtd_i:&u16, 
   t:Duration
){
   // dimensão da janela.
   let dim = Dimensao {
      altura: janela.get_max_y() as u16,
      largura: janela.get_max_x() as u16
   };
   let _debaixo:bool = {
      brr.esqueleto.posicao.x > 3
   };
   // escrevendo legendas e info sobre o jogo.
   janela.mv( (dim.altura-1) as i32, 0);
   janela.addstr(format!("dimensao do tabuleiro: {}", bl.area));
   janela.addstr(format!( "\ttempo decorrido:{:3.2}seg", t.as_secs()));
   janela.mv( (dim.altura-2) as i32, 0);
   janela.addstr(format!("toques no chao:{:3.3}", *qtd));
   janela.addstr(format!("\tnum. de rebatidas: {}", *qtd_i)); 
}

/* Conta a quantia de vezes que a bola bate no "piso" do tabuleiro, e passa tal
 * valor a referência passada. */
pub fn colisoes_monitoramento(bl:&Bola, brr:&Barra, 
contador:&mut u8, rebatidas:&mut u16) {
   if bl.esqueleto.posicao.y == bl.area.altura-1
      { *contador += 1; }
   if brr.foi_acertada(bl.esqueleto.posicao)
      { *rebatidas += 1; }
}

/* Da um impulso na direção para que fica ainda mais caótica o movimento da 
 * bolinha. Envia a direção dado para que possa entrar em 'códigos de desvio' 
 * sem precisar alterar mais e gerar muita gambiarra.
 */
fn impulsiona_bola(bl:&mut Bola, dir:Direcao) -> Direcao{
   // trabalhando dado a direção.
   match dir {
      Direcao::Nordeste | Direcao::Sudeste => {
         // mudando de direção em ante-mão.
         bl.esqueleto.sentido = dir;
         /* seleciona se vai fazer uma curva ou,
          * acelera na direção dada. Ambas opções
          * com 50% de chance de ocorrer, no
          * fim, quanto mais rebatidas, ocorre
          * metade de cada tipo. */
         match fastrand::bool() {
            // curva mais a trajetória.
            true => bl.esqueleto.posicao.x += 1,
            // damos um passo para que assemelhe a aceleração.
            false => bl.r#move(),
         };
         /* e mais um deslocamento a direção horizontal
          * para que no próximo movimento, sem ser 
          * aqui a bola "curve" mais. Porém este
          * encurvamento extra será aleatório(não toda vez). */
         match fastrand::bool() {
            true => { bl.esqueleto.posicao.x += 1; },
            false => (),
         };
      },
      Direcao::Noroeste | Direcao::Sudoeste => {
         bl.esqueleto.sentido = dir;
         // alternativas no cara ou coroa:
         match  fastrand::bool() {
            // curvar mais a direção.
            true => bl.esqueleto.posicao.x -= 1,
            // aplicar uma aceleração.
            false => bl.r#move(),
         };
         // pode ou não entortar mais à trajetória.
         match fastrand::bool() {
            true => { bl.esqueleto.posicao.x -= 1; },
            false => (),
         };
      },
      Direcao::Norte => {
         bl.esqueleto.sentido = dir;
         /* ou acontece uma aceleração, ou 
          * ele desvia um pouco para esquerda. */
         match fastrand::bool() {
            true => bl.esqueleto.posicao.y -= 1,
            false => bl.esqueleto.posicao.x -= 1,
         };
      },
      // as demais, não fazer nada por enquanto...
      _ => (),
   };
   return dir;
}

/** O joystick do jogo. Aqui ele além mudar a direção da barra, coleta dados
 *  dos movimentos feitos. Caso o comando seja de sair do jogo, ele retorna
 *  um 'null(none)'. Assim indica ao loop extero que foi solicitada o
 *  interrompimento da partida.
 */
fn controle_do_jogo(board: &Tabuleiro, bar: &mut Barra, data: &mut BarraMetadados)
  -> Option<Direcao>
{
   match board.entrada()
   {
      Some(Input::KeyRight) => {
         // pegando comandos dado a barra.
         data.total_comandos_dados += 1;
         // acelerar se o comando for igual a direção atual.
         if bar.esqueleto.sentido == Direcao::Leste
            { bar.r#move(Direcao::Leste); }
         Some(Direcao::Leste)
      },
      Some(Input::KeyLeft) => {
         // contando comandos dado a barra.
         data.total_comandos_dados += 1;
         // acelerar se o comando for igual a direção atual.
         if bar.esqueleto.sentido == Direcao::Oeste
            { bar.r#move(Direcao::Oeste); }
         Some(Direcao::Oeste)
      },
      // também termina o laço.
      Some(Input::Character(ch)) => {
         if ch == 's' { None }
         else { Some(bar.esqueleto.sentido) }
      },
      Some(_) | None =>
         Some(bar.esqueleto.sentido)
   }
}

fn animacao_de_inercia_pos_termino
 (tabuleiro: &mut Tabuleiro, bola: &mut Bola, barra: &mut Barra) 
{
   const PERIODO: Duration = Duration::new(14,500); 
   let contador:Instant = Instant::now();
   let dim = tabuleiro.dimensao();

   while contador.elapsed() < PERIODO 
   {
      // implemetando rebote caso bate na barra.
      colisao_bola_barra(bola, barra);
      // mensagem de termino.
      mensagem_termino(tabuleiro);
      // move a bola e a barra:
      bola.r#move();
      barra.r#move(barra.esqueleto.sentido);
      // desenha bola e barra:
      bola.desenha_bola(tabuleiro.tela());
      barra.desenha_barra(tabuleiro.tela());
      tabuleiro.renderiza();
   }
}

fn mensagem_termino(t: &mut Tabuleiro) 
{
   t.tela().attrset(A_BLINK);
   t.tela().attrset(A_BOLD);
   t.tela().color_set(3);
   t.mensagem_centralizada("O Jogo Acabou!");
   // redefinindo novamente...
   t.tela().color_set(0);
   t.tela().attrset(A_NORMAL);
}

/// Mensagem de ínicio, para prepara-se do jogo.
fn animacao_de_abertura(t: &mut Tabuleiro)
{
   let texto = "o jogo inicia em ";

   for numero in 1..=3
   {
      let panfleto = format!("{texto} ...{numero}");
      t.tela().addstr(&panfleto);
      t.tela().refresh();
      napms(1_000);
   }
}
