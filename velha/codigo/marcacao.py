

"""
Desenhando os traços gráficos(uma simples
animaçãozinha) representando a vitória.
"""

# do próprio programa:
from codigo.ponto import *
# biblioteca padrão do Python:
from curses import (window, napms, color_pair)
from unittest import (TestCase, main)
from time import sleep
from math import sqrt

# tempo de espera da pausa.
PAUSA = 60 # milisegundos
TRACO_H = '='
TRACO_V = '&'

__all__ = ["risca_linha", "risco_entre_pontos"]

def desenha_ponto(janela: window, y: int, x: int, 
  caractere: str) -> None:
   assert len(caractere) == 1
   (Y, X) = janela.getmaxyx()
   if y >= Y or x >= X:
      return None
   janela.addch(y, x, caractere, color_pair(5))
   napms(PAUSA)
   janela.refresh()
...

# risca uma linha reta entre dois pontos, estando
# tais alinhados.
def risca_linha(janela: window, A: Ponto, B: Ponto) -> None:
   # detectando o tipo de linha.
   mesma_linha = (A.x != B.x) and (A.y == B.y)
   mesma_coluna = (A.y != B.y) and (A.x == B.x)
   primeira_diagonal = (A.x < B.x and B.y > A.y)
   segunda_diagonal = (A.x > B.x and B.y > A.y)

   if __debug__:
      vertical = "vertical?" + str(mesma_coluna)
      horizontal = "horizontal?" + str(mesma_linha)
      janela.addstr(1, 1, horizontal, color_pair(5))
      janela.addstr(2, 1, vertical, color_pair(3))
      janela.refresh()
   ...
   if mesma_linha:
      dx = abs(A.x - B.x)
      for x in range(0, dx):
         desenha_ponto(janela, A.y, A.x + x, TRACO_H)
   elif mesma_coluna:
      dy = abs(A.y - B.y)
      for y in range(0, dy):
         desenha_ponto(janela, A.y + y, B.x, TRACO_V)
   else:
      raise Exception("caso não abordado para tal.")
...

# verifica se o Ponto pertence a Linha.
def pertence_a_linha(A: Ponto, linha: iter) -> bool:
   pass 

# projeta uma linha reta que intersecta tal Ponto.
def projecao(P: Ponto) -> iter:
   (Y, X) = (P.y, P.x)
   k = 30
   for y in range(Y, Y + k):
      for x in range(X, X + k):
         yield(Ponto(y, x))
   ...
...

def risco_entre_pontos(janela:window, A: Ponto, B: Ponto) -> None:
   "cuida dos riscos diagonais necessários."
   primeira_diagonal = (A.x < B.x and B.y > A.y)
   segunda_diagonal = (A.x > B.x and B.y > A.y)
   # comprimentos do retângulo formado pelos Pontos.
   dy = abs(A.y - B.y); dx = abs(A.x - B.x)
   c = int(A.distancia(B))

   if primeira_diagonal:
      x = A.x; y = A.y
      for p in range(0, c):
         # aumenta taxa de variação se estiver muito distante.
         if p % 5 != 0:
            x += dx // dy
            y += 1
         else:
            x -= 1
            y -= 1
         desenha_ponto(janela, y, x, 'X')
      ...
   elif segunda_diagonal:
      y = A.y; x = A.x
      for p in range(0, c - 15):
         if p % 5 != 0:
            x -= dx // dy
            y += 1
         else:
            x += 1
            y -= 1
         desenha_ponto(janela, y, x, 'X')
      ...
   ...
...

# importação necessária para testes.
if __name__ == "codigo.marcacao":
   from codigo.tabuleiro import (Tabuleiro, Quadrantes)

class Riscagem(TestCase):
   def riscosRetosHorizontais(self):
      t = Tabuleiro()
      t.desativa_seletor()
      t.desenha_tudo()
      entradas = [
         (Quadrantes.PRIMEIRO, Quadrantes.TERCEIRO),
         (Quadrantes.QUARTO, Quadrantes.SEXTO),
         (Quadrantes.SETIMO, Quadrantes.NONO),
      ]
      for (q1, q2) in entradas:
         (A, B) = t.grade.limites(q1)
         dy = abs(A.y - B.y) // 2
         (C, D) = t.grade.limites(q2)
         (P, Q) = (
            Ponto(A.y + dy, A.x),
            Ponto(C.y + dy, D.x)
         )
         risca_linha(t.janela, P, Q)
      ...
      t.desmancha_tabuleiro()
      # avaliação manual.
      self.assertTrue(True)
   ...
   def riscosRetosVerticais(self):
      t = Tabuleiro()
      t.desativa_seletor()
      t.desenha_tudo()
      entradas = [
         (Quadrantes.PRIMEIRO, Quadrantes.SETIMO),
         (Quadrantes.SEGUNDO, Quadrantes.OITAVO),
         (Quadrantes.TERCEIRO, Quadrantes.NONO),
      ]
      for (q1, q2) in entradas:
         (A, B) = t.grade.limites(q1)
         dx = abs(A.x - B.x) // 2
         (C, D) = t.grade.limites(q2)
         (P, Q) = (
            Ponto(A.y, A.x + dx),
            Ponto(D.y, A.x + dx)
         )
         risca_linha(t.janela, P, Q)
      ...
      t.desmancha_tabuleiro()
      # avaliação manual.
      self.assertTrue(True)
   ...
   def riscoDiagonalPrincipal(self):
      t = Tabuleiro()
      t.desativa_seletor()
      t.desenha_tudo()
      (A, _) = t.grade.limites(Quadrantes.PRIMEIRO)
      (_, B) = t.grade.limites(Quadrantes.NONO)
      risco_entre_pontos(t.janela, A, B)
      t.desmancha_tabuleiro()
      # avaliação manual.
      self.assertTrue(False)
   ...
   def riscoDiagonalSecundaria(self):
      t = Tabuleiro()
      t.desativa_seletor()
      t.desenha_tudo()
      (A, B) = t.grade.limites(Quadrantes.TERCEIRO)
      P = Ponto(A.y, B.x)
      del A, B
      (A, B) = t.grade.limites(Quadrantes.SETIMO)
      Q = Ponto(B.y, A.x)
      risco_entre_pontos(t.janela, P, Q)
      t.desmancha_tabuleiro()
      # avaliação manual.
      self.assertTrue(False)
   ...
   def todosRiscosPossiveis(self):
      t = Tabuleiro()
      t.desativa_seletor()
      t.desenha_tudo()
      # riscos horizontais:
      entradas = [
         (Quadrantes.PRIMEIRO, Quadrantes.TERCEIRO),
         (Quadrantes.QUARTO, Quadrantes.SEXTO),
         (Quadrantes.SETIMO, Quadrantes.NONO),
      ]
      for (q1, q2) in entradas:
         (A, B) = t.grade.limites(q1)
         dy = abs(A.y - B.y) // 2
         (C, D) = t.grade.limites(q2)
         (P, Q) = (
            Ponto(A.y + dy, A.x),
            Ponto(C.y + dy, D.x)
         )
         risca_linha(t.janela, P, Q)
      ...
      del entradas, q1, q2
      # riscos verticais.
      entradas = [
         (Quadrantes.PRIMEIRO, Quadrantes.SETIMO),
         (Quadrantes.SEGUNDO, Quadrantes.OITAVO),
         (Quadrantes.TERCEIRO, Quadrantes.NONO),
      ]
      for (q1, q2) in entradas:
         (A, B) = t.grade.limites(q1)
         dx = abs(A.x - B.x) // 2
         (C, D) = t.grade.limites(q2)
         (P, Q) = (
            Ponto(A.y, A.x + dx),
            Ponto(D.y, A.x + dx)
         )
         risca_linha(t.janela, P, Q)
      ...
      del entradas, q1, q2
      # diagonal principal.
      (A, _) = t.grade.limites(Quadrantes.PRIMEIRO)
      (_, B) = t.grade.limites(Quadrantes.NONO)
      risco_entre_pontos(t.janela, A, B)
      del A, B
      # diagonal secundária.
      (A, B) = t.grade.limites(Quadrantes.TERCEIRO)
      P = Ponto(A.y, B.x)
      del A, B
      (A, B) = t.grade.limites(Quadrantes.SETIMO)
      Q = Ponto(B.y, A.x)
      risco_entre_pontos(t.janela, P, Q)

      t.desmancha_tabuleiro()
      # avaliação manual.
      self.assertTrue(False)
   ...
...

if __name__ == "__main__":
   main()
