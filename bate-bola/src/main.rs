#![allow(warnings)]

// Bibliotecas externas:
extern crate pancurses;
extern crate fastrand;
// Módulos internos ao projeto:
mod graficos;
mod modelos;
mod estatisticas;

// Importando ferramentas externa:
use pancurses::{
   initscr, start_color, use_default_colors, noecho,
   curs_set, Window, init_pair, COLOR_BLUE, COLOR_YELLOW, COLOR_RED,
   COLOR_WHITE, nocbreak
};
// Utilitários referentes as funções internas:
use graficos::{roda_jogo, Tabuleiro};
use estatisticas::{BarraMetadados, BolaMetadados};
use modelos::{Dimensao, Barra, Ponto, Bola, Direcao};

// velocidade(tempo em miliseg de cada novo quadro).
pub const TAXA_DE_QUADROS: i32 = 100;
// quantidade limite de toques no chão.
pub const TOQUES_LIMITE: u8 = 3;
pub const MOVIMENTACAO: usize = 1;

fn main() {
   let mut tabuleiro = Tabuleiro::inicia();
   let dim = tabuleiro.dimensao();
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
      &mut barra, &mut bola, &mut tabuleiro, &mut barmdt, &mut ballmdt
   );
   println!(
      "--- Dados da Barra --- \n{}\n\n--- Dados da Bola ---\n{}\n",
      barmdt, ballmdt
   );
}

#[cfg(test)]
mod tests {
   extern crate pancurses;

   use pancurses::{napms, endwin};

   #[test]
   fn criacao_de_um_tabuleiro() {
      let (board, size) = super::criacao_e_configuracao_da_janela();
      board.refresh();
      napms(2000);
      endwin();
   }
}
