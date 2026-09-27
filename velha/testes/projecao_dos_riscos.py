
""" trabalhando em cima da diagonal secundária
tudo sobre sua geração é bem díficil. """

# biblioteca padrão do Python:
from math import sqrt, floor
from time import sleep
import curses
from sys import path
# meu módulos:
path.append("..")
import codigo.tabuleiro as TB
import biblioteca_externa.espiral as BEE

# marca todos pontos centrais.
def marca_pontos_centrais(tabuleiro):
   cor = TB.color_pair(1)
   tabuleiro.janela.addch(*tabuleiro.q1,'@',cor)
   tabuleiro.janela.addch(*tabuleiro.q2,'@',cor)
   tabuleiro.janela.addch(*tabuleiro.q3,'@',cor)
   tabuleiro.janela.addch(*tabuleiro.q4,'@',cor)
   tabuleiro.janela.addch(*tabuleiro.q5,'@',cor)
   tabuleiro.janela.addch(*tabuleiro.q6,'@',cor)
   tabuleiro.janela.addch(*tabuleiro.q7,'@',cor)
   tabuleiro.janela.addch(*tabuleiro.q8,'@',cor)
   tabuleiro.janela.addch(*tabuleiro.q9,'@',cor)
   tabuleiro.janela.refresh()
   sleep(1)

tabuleiro = TB.Tabuleiro('+')

# marcas pontos de cada local.
marca_pontos_centrais(tabuleiro)

# principal:
coords =[]
for (y,x) in BEE.espiral(tabuleiro.q3):
   if tabuleiro.q7 in TB.projecao((y,x),tabuleiro.q7):
      coords.append((y,x))
   TB.risca(tabuleiro.janela,(y,x),tabuleiro.q7)

curses.napms(3000)  # três segundo de duração.
tabuleiro.desmancha_tabuleiro()

# verifica quais das coordenadas acertaram o 
# ponto desejado.
B = tabuleiro.q7
for A in coords:
   print(
      "está dentro(col=%i, lin=%i)?"
      %(A[1], A[0]), 
      tabuleiro.q7 in TB.projecao(A,B)
   )
...
