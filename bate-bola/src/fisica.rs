/** Cuida de alguns algoritmos de computação relacionada a física do jogo.
 */

// Utilitários referentes as funções internas:
use crate::modelos::{Direcao, Barra, Bola};

/** Altera rota da bolinha após colisão levando em conta seu sentido atual,
 *  assim com o da barra.
 */
pub fn colisao_bola_barra(bo:&mut Bola, ba:&mut Barra)
{
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

/* Da um impulso na direção para que fica ainda mais caótica o movimento da 
 * bolinha. Envia a direção dado para que possa entrar em 'códigos de desvio' 
 * sem precisar alterar mais e gerar muita gambiarra.
 */
fn impulsiona_bola(bl:&mut Bola, dir: Direcao) -> Direcao {
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
