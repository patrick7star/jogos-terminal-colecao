
# o que será importado:
__all__ = ["Direcao", "Ponto", "Dimensao"]

from math import (sqrt)

# outro nome para o mesmo objeto.
class Ponto:
   "representação do 'Ponto', posições (y, x)"
   def __init__(self, vertical: int, horizontal: int):
      self._y = vertical
      self._x = horizontal
   ...
   def __str__(self):
      return "({}, {})".format(self._y, self._x)
   def __add__(self, ponto):
      if not isinstance(ponto, Ponto):
         raise ValueError("'%s' não é do tipo 'Ponto'" % type(ponto))
      return Ponto(self._y + ponto.y, self._x + ponto.x)
   def __sub__(self, ponto):
      if not isinstance(ponto, Ponto):
         raise ValueError("'%s' não é do tipo 'Ponto'" % type(ponto))
      return Ponto(self._y - ponto.y, self._x - ponto.x)
   ...
   # só delega as funções acimas que já fazem
   # quase todo o trabalho.
   def __iadd__(self, ponto):
      return self + ponto
   def __isub__(self, ponto):
      return self - ponto
   # encapsulamento ...
   def valor_x(self):
      return self._x
   def valor_y(self):
      return self._y
   x = property(valor_x, doc="coordenada X(horizontal)")
   y = property(valor_y, doc="coordenada Y(vertical)")
   def distancia(self, Q) -> float:
      (xq, yq) = (Q.x, Q.y)
      dx = self.x - xq
      dy = self.y - yq
      return sqrt(pow(dx, 2) + pow(dy, 2))
   ...
...

class Dimensao(Ponto):
   " comprimento físico de algum objeto. "
   def __getitem__(self, indice) -> int:
      tipo = type(indice)
      if tipo == int:
         if indice == 0:
            return self.y
         elif indice == 1:
            return self.x
         else:
            raise IndexError("só válido índices 1 e 0.")
      elif tipo == str:
         if indice == "altura" or indice == "height":
            return self.y
         elif indice == "largura" or indice == "width":
            return self.x
         else:
            raise KeyError(
               "só são válidas as chaves 'altura/height'" +
               " e 'largura/width'."
            )
         ...
      else:
         raise LookupError("índice dado inválido(inteiro/str)")
   ...
   # as áreas são determinantes de comparação:
   # verifica se as áreas da instância de do 
   # argumento(outra Dimensão), tem áreas
   # diferentes ou iguais, fazendo assim, a 
   # avaliação de ordem entre eles.
   def __le__(self, d: Ponto) -> bool:
      return d[0] * d[1] >= self[0] * self[1]
   def __ge__(self, d: Ponto) -> bool:
      aI = self["altura"] * self["width"]
      aA = self["height"] * self["largura"]
      return aI >= aA
   ...
   def __getattr__(self, atributo):
      if atributo in ("height", "altura"):
         return self[0]
      elif atributo in ("width", "largura"):
         return self[1]
      else:
         raise AttributeError(
            "{} é incompátivel com 'Dimensão'."
            .format(atributo)
         )
      ...
   def __str__(self):
      return "Dimensão: {}x{}".format(self[0], self[1])
...

from enum import (IntEnum, auto)

class Direcao(IntEnum):
   DIREITA = auto()
   ESQUERDA = auto()
   CIMA = auto()
   BAIXO = auto()
   
   def inverso(self) -> IntEnum:
      "retorna a direção oposta da atual."
      match self:
         case Direcao.DIREITA:
            return Direcao.ESQUERDA
         case Direcao.ESQUERDA:
            return Direcao.DIREITA
         case Direcao.CIMA:
            return Direcao.BAIXO
         case Direcao.BAIXO:
            return Direcao.CIMA
      ...
   ...
...

import unittest

class TesteDimensao(unittest.TestCase):
   def instanciaBasica(self):
      iD = Dimensao(13, 42)
      self.assertEqual(iD[0], 13)
      self.assertEqual(iD[1], 42)
      print(iD)
   ...
   def comparacao(self):
      d = Dimensao(13, 42)
      D = Dimensao(11, 52)
      self.assertTrue(D >= d)
      self.assertFalse(D == d)
      print(D, d, sep='\n')
   ...
   def todosMeiosDeAcesso(self):
      D = Dimensao(20, 72)
      self.assertEqual(D.altura, D["altura"])
      self.assertEqual(D["width"], D[1])
      self.assertTrue(
         D["height"] == D[0] == D.altura and
         D["largura"] == D[1] == D.largura
      )
      print(D)
   ...
...

if __name__ == "__main__":
   unittest.main()
