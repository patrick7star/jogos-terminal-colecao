#![allow(unused_variables)]

// Bibliotecas externas:
extern crate pancurses;
extern crate fastrand;
// Módulos internos ao projeto:
mod graficos;
mod modelos;
mod estatisticas;

// Importando ferramentas externa:
use pancurses::{
   initscr, start_color, use_default_colors, newwin, noecho,
   curs_set, Window
};
// Utilitários referentes as funções internas:
use graficos::{roda_jogo};
use estatisticas::{BarraMetadados, BolaMetadados};
use modelos::{Dimensao, Barra, Ponto, Bola, Direcao};

// cor transparente:
pub const TRANSPARENTE: i16 = -1;
// velocidade(tempo em miliseg de cada novo quadro).
pub const TAXA_DE_QUADROS: i32 = 150;
// quantidade limite de toques no chão.
pub const TOQUES_LIMITE: u8 = 3;
pub const MOVIMENTACAO: usize = 2;

// execução de testes...
fn main() {
   /* ativando unicode characteres...
   let local = LcCategory::all;
   setlocale(local, "pt.UTF-8"); */

   let (tabuleiro, dim) = criacao_e_configuracao_da_janela();
   let mut barra = Barra::nova(
      fastrand::u16(5..19), '=',
      Ponto {
         x:dim.largura/2, 
         y:dim.altura-5
      },
      dim
   );
   // isntânciando bolas:
   let mut bola = Bola::nova(
      // direção de partida.
      Direcao::Sudoeste,
      // ponto de partida.
      Ponto { 
         x: fastrand::u16(2..dim.largura-2), 
         y: fastrand::u16(1..dim.altura-7) 
      },
      // dimensão do tabuleiro inserida.
      dim 
   );
   // Prá coleta de dados:
   let mut barmdt = BarraMetadados::gera(barra.comprimento as u8);
   let mut ballmdt = BolaMetadados::gera();
   
   // executando o jogo...
   let dados = roda_jogo(
      &mut barra, &mut bola, &tabuleiro, &mut barmdt, &mut ballmdt
   );
   println!(
      "--- Dados da Barra --- \n{}\n\n--- Dados da Bola ---\n{}\n",
      barmdt, ballmdt
   );
}

fn criacao_e_configuracao_da_janela() -> (Window, Dimensao)
{
   let tabuleiro = initscr();
   // dimensão da janela.
   let dim_j:Dimensao = Dimensao {
      altura: tabuleiro.get_max_y() as u16,
      largura: tabuleiro.get_max_x() as u16,
   };
   // Obtendo dimensão do tabuleiro.
   let dim:Dimensao = Dimensao {
      altura: tabuleiro.get_max_y() as u16,
      largura: tabuleiro.get_max_x() as u16,
   };

   // Configuração da janela:
   tabuleiro.keypad(true);
   tabuleiro.nodelay(true);
   curs_set(0);
   // noecho();
   // Inicia coloração.
   // start_color();
   // use_default_colors();

   (tabuleiro, dim)
}
