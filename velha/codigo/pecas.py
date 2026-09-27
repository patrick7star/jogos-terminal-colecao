
""" fabricante de peças """

# meus módulos.
from biblioteca_externa.moldura_str import (imprime, matriciar)

# o que pode ser importado.
__all__ = ["Jogadores"]

# obtem a matriz de tanto a bola, como
# o xis.
CAMINHO_BOLA = "dados/bola.txt"
CAMINHO_XIS = "dados/xis.txt"
CAMINHO_QUADRADO = "dados/quadrado.txt"
...

# lê a formatação das peças dentro dos arquivos.
try:
   with (open(CAMINHO_BOLA, 'rt') as arq_i,
     open(CAMINHO_XIS) as arq_ii,
     open(CAMINHO_QUADRADO,'rt') as arq
   ):
      bola_matriz = matriciar(arq_i.read())
      xis_matriz = matriciar(arq_ii.read())
      quadrado_matriz = matriciar(arq.read())
   ...
except FileNotFoundError:
   CAMINHO_BOLA = "../dados/bola.txt"
   CAMINHO_XIS = "../dados/xis.txt"
   CAMINHO_QUADRADO = "../dados/quadrado.txt"
   with (
     open(CAMINHO_BOLA, 'rt') as arq_i,
     open(CAMINHO_XIS) as arq_ii,
     open(CAMINHO_QUADRADO,'rt') as arq
   ):
      bola_matriz = matriciar(arq_i.read())
      xis_matriz = matriciar(arq_ii.read())
      quadrado_matriz = matriciar(arq.read())
   ...
...

from enum import (Enum, auto)
from random import choice

class Jogadores(Enum):
   """
   enumerador com tupla do símbolo da peça, assim como a peça em sí,
   uma matriz com caractéres formando ascii-art dela.
   """
   # seleciona formato de peça de forma randômica.
   BOLA = ('O', choice((bola_matriz, quadrado_matriz)))
   XIS = ('X', xis_matriz)

   def alternar(self):
      "o valor oposto da instância de menu usada."
      match self:
         case Jogadores.BOLA:
            return Jogadores.XIS
         case Jogadores.XIS:
            return Jogadores.BOLA
      ...
   ...

   def __getitem__(self, indice: int):
      "indexar dados(uma tupla) que os braços do Enum retém."
      if indice >= 2:
         raise IndexError("enum só tem dois valores.")
      return self.value[indice]
   ...
...
