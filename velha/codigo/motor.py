
"""
 Motor do jogo; aqui ficará todos os procedimentos de verificação de
 vitória, reposição de peças; pontuação do placar e etc...
"""


# o que pode ser importado:
__all__ = [
  "peca_vitoriosa", "adiciona_peca", "jogadas_restantes", "Fileira",
  "LocalJaPreenchidoError", "tabuleiro_str", "fileira_ganha",
  "numeracao_em_coord"
]

# exceções:
class LocalJaPreenchidoError(Exception):
   def __str__(self):
      msg = "este local já foi preenchido por uma peça."
      return msg
...

# matriz contendo todas peças. no ínicio estará apenas como "null".
matriz = [
   [None for i in range(3)]
   for j in range(3)
]

# tabuleiro em texto, seu molde.
tabuleiro_molde= """
   |     |
 {} |  {}  | {}
===+=====+====
 {} |  {}  | {}
===+=====+====
 {} |  {}  | {}
   |     |
"""
# novo molde do mapa do resultado, porém, usando separadores Unicode.
tabuleiro_unicode = (
   tabuleiro_molde
   .replace('|', '\u2551')
   .replace('=', '\u2550')
   .replace('+', '\u256C')
)

from codigo.pecas import Jogadores
# verifica vitória de uma peça.
def peca_vitoriosa(peca: Jogadores) -> bool:
   assert isinstance(peca, Jogadores)
   "verifica se peça é a vencedora"
   # apelido para variável global para melhor a legibilidade e
   # a codificação.
   m = matriz
   # todas proposições que validam uma vitória para tal peça.
   if m[0][0] == m[0][1] == m[0][2] == peca:
      return True  # primeira linha.

   elif m[1][0] == m[1][1] == m[1][2] == peca:
      return True # segunda linha.

   elif m[2][0] == m[2][1] == m[2][2] == peca:
      return True # terceira linha.

   elif m[0][0] == m[1][0] == m[2][0] == peca:
      return True # primeira coluna.

   elif (m[0][1] == m[1][1]==m[2][1]==peca):
      return True # segunda coluna.

   elif m[0][2] == m[1][2] == m[2][2] == peca:
      return True # terceira coluna.

   elif m[0][0] == m[1][1] == m[2][2] == peca:
      return True # diagonal principal.

   elif m[0][2]==m[1][1]== m[2][0] == peca:
      return True # diagonal secundaria.

   else:
      return False
...

# Adiciona uma peça na matriz. Você adiciona apenas numa posição, ou
# seja, não pode sobreescrever peça já posicionada.
def adiciona_peca(peca: Jogadores, coordenada) -> None:
   (linha,coluna) = coordenada
   # proposições de 'peça válida' e 'lacuna vaga':
   peca_valida = (peca != None) and isinstance(peca, Jogadores)
   lacuna_vaga = (matriz[linha][coluna] == None)

   if peca_valida and lacuna_vaga:
      matriz[linha][coluna] = peca
   else:
      raise LocalJaPreenchidoError()
...

# traduz um local numa coordenada legível pela matriz.
def numeracao_em_coord(local):
   """ retorna uma coordenada exclusiva para
   matriz, então será adicionada uma peça nela."""
   try:
      if local == 1: return (0,0)
      elif local == 2: return (0,1)
      elif local == 3: return (0,2)
      elif local == 4: return (1,0)
      elif local == 5: return (1,1)
      elif local == 6: return (1,2)
      elif local == 7: return (2,0)
      elif local == 8: return (2,1)
      elif local == 9: return (2,2)
      else: pass
   except:
      return numeracao_em_coord(local % 9 + 1)
...

from array import array as Array
def tabuleiro_str():
   """
   retorna uma versão string do "tabuleiro" de tic-toc-toe, tendo
   peças adicionadas, ou não, e isto independe se a partida está
   finalizada.
   """
   pecas_posicionais = Array('u')
   for i in range(3):
      for j in range(3):
         peca = matriz[i][j]
         if peca is None:
            pecas_posicionais.append(' ')
         else:
            pecas_posicionais.append(peca[0])
      ...
   ...
   #return tabuleiro_molde.format(*pecas_posicionais)
   return tabuleiro_unicode.format(*pecas_posicionais)
...

def jogadas_restantes():
   """ retorna a contagem de jogadas restantes"""
   return sum(M.count(None) for M in matriz)
...

# biblioteca padrão.
from enum import (auto, IntEnum)

class Fileira(IntEnum):
   HORIZONTAL_SUPERIOR = auto()
   HORIZONTAL_MEDIO = auto()
   HORIZONTAL_INFERIOR= auto()
   VERTICAL_ESQUERDA = auto()
   VERTICAL_MEDIA = auto()
   VERTICAL_DIREITA = auto()
   DIAGONAL_PRINCIPAL = auto()
   DIAGONAL_SECUNDARIA = auto()
...

def fileira_ganha():
   """
   retorna o número da fileira ganha no jogo. A numeração é a seguinte:
   1ª linha superior; 2ª linha do meio; 3ª linha inferior; 4ª coluna
   da esquerda; 5ª coluna do meio; 6ª coluna da direita; 7ª diagonal
   principal e 8ª diagonal secundária.
   """
   if peca_vitoriosa(Jogadores.XIS):
      peca = Jogadores.XIS
   elif peca_vitoriosa(Jogadores.BOLA):
      peca = Jogadores.BOLA
   else:
      raise Exception("não há vencedor; jogo empatado!")

   if matriz[0][0] == matriz[0][1] == matriz[0][2] == peca:
      return Fileira.HORIZONTAL_SUPERIOR

   elif matriz[1][0] == matriz[1][1] == matriz[1][2] == peca:
      return Fileira.HORIZONTAL_MEDIO

   elif matriz[2][0] == matriz[2][1] == matriz[2][2] == peca:
      return Fileira.HORIZONTAL_INFERIOR

   elif matriz[0][0] == matriz[1][0] == matriz[2][0] == peca:
      return Fileira.VERTICAL_ESQUERDA

   elif (matriz[0][1] == matriz[1][1]==matriz[2][1]==peca):
      return Fileira.VERTICAL_MEDIA

   elif matriz[0][2] == matriz[1][2] == matriz[2][2] == peca:
      return Fileira.VERTICAL_DIREITA

   elif matriz[0][0] == matriz[1][1] == matriz[2][2] == peca:
      # diagonal principal.
      return Fileira.DIAGONAL_PRINCIPAL

   else:
      # diagonal secundaria.
      return Fileira.DIAGONAL_SECUNDARIA
...
