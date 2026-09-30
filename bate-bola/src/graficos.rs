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
use crate::fisica::{colisao_bola_barra};

trait Figura { fn desenha(&self, tabuleiro: &Window); }

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

impl Figura for Bola 
{
   fn desenha(&self, screen: &Window)
   {
      // nomeando a coordenada de modo mais legível...
      let l:i32 = self.esqueleto.posicao.y as i32;
      let c:i32 = self.esqueleto.posicao.x as i32;

      // desenhando objeto propriamente...
      screen.attrset(A_BOLD);
      screen.color_set(1);
      screen.mvaddch(l,c,self.esqueleto.forma);
      screen.attrset(A_NORMAL);
      screen.color_set(0);
   }
}
impl Figura for Barra
{
   fn desenha(&self, tabuleiro: &Window)
   {
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
      bola.desenha(tabuleiro.tela());
      barra.desenha(tabuleiro.tela());
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
      bola.desenha(tabuleiro.tela());
      barra.desenha(tabuleiro.tela());
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
