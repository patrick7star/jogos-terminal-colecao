
# bibloteca padrão do Python:
from time import sleep
import curses
from sys import path
# minha lib:
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

# pontos.
marca_pontos_centrais(tabuleiro)

# referência a janela do tabuleiro.
janela = tabuleiro.janela

# riscando apenas pontos válidos.
coords = []
for ponto in BEE.espiral(tabuleiro.q3):
   if tabuleiro.q7 in TB.projecao(ponto,tabuleiro.q7):
      coords.append(ponto)

for ponto in coords: 
   TB.risca(janela,ponto, tabuleiro.q7)

tabuleiro.desmancha_tabuleiro()

print("quantidade de coords. achadas=%i"%len(coords))
print("\ncoordenas:")
for C in coords:
   print("LIN=%i COL=%i"%(C[0],C[1]))
