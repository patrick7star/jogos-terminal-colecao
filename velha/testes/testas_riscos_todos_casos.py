""" teste de para ver ser risca todas fileiras,
sejam elas horizontais ou verticais. """

import os, sys
from time import sleep
sys.path.append("..")
import codigo.tabuleiro as TB


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
...

tabuleiro = TB.Tabuleiro('*')

# marcando todos pontos:
marca_pontos_centrais(tabuleiro)

# marca linhas e colunas:
for l in range(1, 8 + 1):
   tabuleiro.marca_vitoria(l)
   sleep(0.2)
...

sleep(1)

# agora apenas as diagonais.
tabuleiro.janela.erase()
tabuleiro.__init__('*')  # chamando novamente o construtor.
marca_pontos_centrais(tabuleiro)
tabuleiro.marca_vitoria(7)
tabuleiro.marca_vitoria(8)

tabuleiro.desmancha_tabuleiro()
