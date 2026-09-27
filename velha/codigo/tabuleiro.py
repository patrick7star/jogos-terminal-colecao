
# biblioteca do Python:
from curses import *
from math import floor, sqrt
from random import randint
# meus módulos:
if __name__ == "__main__":
   import sys
   sys.argv.append("..")
import biblioteca_externa.espiral as BEE
from codigo.motor import (Fileira, LocalJaPreenchidoError)
from codigo.ponto import *

# o que pode ser importado?
__all__ = ["Quadrantes", "GradePixelada", 'Tabuleiro',"ForaTabuleiroError"]


# algumas exceções:
class ForaTabuleiroError(Exception):
   " exceção de que está fora do tabuleiro "
   def __str__(self):
      return "coordenada está fora da área do tabuleiro"
...

from enum import (IntEnum, auto)
# enumerador que representa, individualmente,
# cada quadrante da tabela.
class Quadrantes(IntEnum):
   """
   A contagem começa do superior esquerdo, indo à direita, e para
   baixo quando alcança a última coluna:

               1º 2º 3º
               4º 5º 6º
               7º 8º 9º
   """
   PRIMEIRO = 1
   SEGUNDO  = auto()
   TERCEIRO  = auto()
   QUARTO  = auto()
   QUINTO  = auto()
   SEXTO  = auto()
   SETIMO = auto()
   OITAVO  = auto()
   NONO  = auto()
...

from codigo.pecas import Jogadores
from random import choice
# tipo de peça que é desenhada lá.
MatrizPeca = list[list[str]]

class Tabuleiro:
   def __init__(self):
      # personalização do interface gráfica.
      self.janela = initscr()
      #configurando janela ...
      start_color()
      #use_default_colors()
      mousemask(True) # habilita mouse.
      curs_set(0)  # tira o cursor.
      self.janela.keypad(True) # ativa outras teclas não númericas.

      # paletas de cores:
      init_pair(1, COLOR_MAGENTA, COLOR_WHITE)
      init_pair(2, COLOR_GREEN, COLOR_WHITE)
      init_pair(3, COLOR_RED, COLOR_WHITE)
      init_pair(4, COLOR_BLUE, COLOR_WHITE)
      init_pair(5, COLOR_YELLOW, COLOR_WHITE)
      init_pair(6, COLOR_WHITE, COLOR_WHITE)

      # definindo uma cor do plano de fundo.
      self.janela.bkgd(' ', color_pair(6))

      # dimensão do terminal.
      self.LIN, self.COL = self.janela.getmaxyx()
      # comprimento das barras formando os tabuleiros.
      self.barra_h, self.barra_v = self.COL-35, self.LIN-5
      # impondo limite caso a tela se redimensiona
      # bastante.
      if self.barra_v >= 20 and self.barra_h >= 53:
         self.barra_h = 55
         self.barra_v = 22
      ...
      # canto superior esquerdo do retângulo onde
      # fica a tabela formando o tabuleiro.
      Y = (self.LIN // 2) - (self.barra_v // 2)
      X = (self.COL // 2) - (self.barra_h // 2)
      # criando grade ao invés de tantas variáveis acima.
      self.posicao = Ponto(Y, X)
      dimensao = Dimensao(self.barra_v, self.barra_h)
      self.grade = GradePixelada(self.posicao, dimensao)
      # marcação dos lugares já marcados.
      self.lugares_marcados = {}
      # cursor para movimentação via
      # teclas direcionais.
      self.seletor = Cursor()
      self.seletor_ativado = True
      # info na barra de status.
      self.mensagem = None
      self.lugar = Ponto(self.LIN - 1, 4)
   ...

   def marca_vitoria(self, fileira):
      " marca o 'tiro' de vitória do vencedor. "
      # compr. da barra horizontais e verticais.
      comprimento = self.barra_h + 5
      comprimentoV = self.barra_v + 2
      cor = color_pair(5)  # coloração da barra.
      coordenada = self.grade.quadrante_coordenada

      # importando funções essenciais. Aqui, pois
      # no cabeçalho do módulo entre em conflito,
      # porque o módulo lá importa coisas daqui também,
      # então entra-se numa importação circular.
      from codigo.marcacao import (
         risco_entre_pontos,
         risca_linha
      )

      if (fileira == Fileira.HORIZONTAL_SUPERIOR
      or fileira == Fileira.HORIZONTAL_MEDIO
      or fileira == Fileira.HORIZONTAL_INFERIOR):
         if fileira == Fileira.HORIZONTAL_SUPERIOR:
            q1 = Quadrantes.PRIMEIRO
            q2 = Quadrantes.TERCEIRO
         elif fileira == Fileira.HORIZONTAL_MEDIO:
            q1 = Quadrantes.QUARTO
            q2 = Quadrantes.SEXTO
         else:
            q1 = Quadrantes.SETIMO
            q2 = Quadrantes.NONO
         (A, B) = self.grade.limites(q1)
         dy = abs(A.y - B.y) // 2
         (C, D) = self.grade.limites(q2)
         (P, Q) = (
            Ponto(A.y + dy, A.x),
            Ponto(C.y + dy, D.x)
         )
         risca_linha(self.janela, P, Q)
      elif (fileira == Fileira.VERTICAL_ESQUERDA
      or fileira == Fileira.VERTICAL_MEDIA
      or fileira == Fileira.VERTICAL_DIREITA):
         if fileira == Fileira.VERTICAL_ESQUERDA:
            q1 = Quadrantes.PRIMEIRO
            q2 = Quadrantes.SETIMO
         elif fileira == Fileira.VERTICAL_MEDIA:
            q1 = Quadrantes.SEGUNDO
            q2 = Quadrantes.OITAVO
         else:
            q1 = Quadrantes.TERCEIRO
            q2 = Quadrantes.NONO
         (A, B) = self.grade.limites(q1)
         dx = abs(A.x - B.x) // 2
         (C, D) = self.grade.limites(q2)
         (P, Q) = (
            Ponto(A.y, A.x + dx),
            Ponto(D.y, A.x + dx)
         )
         risca_linha(self.janela, P, Q)
         ...
      elif fileira == Fileira.DIAGONAL_PRINCIPAL:
         (A, _) = self.grade.limites(Quadrantes.PRIMEIRO)
         (_, B) = self.grade.limites(Quadrantes.NONO)
         risco_entre_pontos(self.janela, A, B)
      else:
         (A, B) = self.grade.limites(Quadrantes.TERCEIRO)
         P = Ponto(A.y, B.x)
         del A, B
         (A, B) = self.grade.limites(Quadrantes.SETIMO)
         Q = Ponto(B.y, A.x)
         risco_entre_pontos(self.janela, P, Q)
      ...
   ...

   def _desenha_matriz(self, peca: Jogadores, posicao: Ponto) -> None:
      matriz_str_peca = peca[1]
      # dimensão das peças.
      matriz_str_peca = peca[1]
      (m, n) = len(matriz_str_peca), len(matriz_str_peca[0])

      # determinando a cor...
      match peca:
         case Jogadores.XIS:
            cor_selecionado = color_pair(3)  # X é vermelho.
         case Jogadores.BOLA:
            cor_selecionado = color_pair(4)  # O é azul.
            #cor = color_pair(2)  # [] é verde.
         case _:
            raise Exception("nunca chega até aqui")
      ...

      # desenhando e pintando, pixel por pixel...
      for i in range(m):
         for j in range(n):
            self.janela.addch(
               # ajustando posição usando dimensão da peça.
               i + (m // 2 - 1) + posicao.y,
               j + (n // 2 + 1) + posicao.x,
               matriz_str_peca[i][j], 
               cor_selecionado
            )
         ...
      ...
   ...

   def coloca_peca(self, peca: Jogadores, local: Quadrantes) -> None:
      " informa a peça, e o quadrante que irá desenha-la."
      assert isinstance(local, Quadrantes)
      assert isinstance(peca, Jogadores)
      posicao = self.grade.quadrante_coordenada(local)

      # verifa se posição já não possui algo.
      if local not in self.lugares_marcados:
         # registrando o lugar como já marcado.
         self.lugares_marcados[local] = peca
      else:
         raise LocalJaPreenchidoError()

      self._desenha_matriz(peca, posicao)
   ...

   def posicao_clicada(self, coord: Ponto) -> Quadrantes:
      """
      denuncia que local no tabuleiro o mouse
      clicou, eventuamente, retornando tal local.
      """
      assert(isinstance(coord, Ponto))
      resultado = self.grade.quadrante(coord)
      if resultado is None:
         # sobe uma exceção por coordenada inválida.
         raise ForaTabuleiroError()
      return resultado
   ...

   def posicoes(self) -> Ponto:
      """
      obtem a coordenada do clique na janela, e seu respectivo
      local no tabuleiro.
      """
      try:
         coordenada = getmouse()
         # invertendo para colocar mais palatável
         # ao tipo de input do programa.
         coord_mouse = (coordenada[2],coordenada[1])
         return Ponto(*coord_mouse)
      except:
         return None
   ...

   def desmancha_tabuleiro(self) -> None:
      # última visualizada no Tabuleiro.
      napms(1_000)
      # renderiza uma última vez.
      # self.renderiza()
      endwin()
   ...
   def informa_algo(self, mensagem: str) -> None:
      self.mensagem = mensagem
...

# elementos que formarão barras do tabuleiro.
SIMBOLO = '&'
BARRA_VERTICAL = '|'
BARRA_HORIZONTAL = '='
# métodos para fazer o Tabuleiro algo mais
# dinâmico, e não só uma folha estática, onde
# um rabisco é dicífil de apagar e impossível
# de desfazer. Algo como uma 'tela', com objetos
# sendo gerados constantemente.
class Tabuleiro(Tabuleiro):
   """
   tenta um método de renderização, ao invés de simplesmente ficar
   simplesmente rabiscando a tela uma vez só.
   """
   def desenha_barras(self) -> bool:
      # 'a' de altura e 'c' de comprimento(miniretângulos).
      (a, c) = (self.barra_v // 3, self.barra_h // 3)
      (Y, X) = (self.posicao.y, self.posicao.x)
      if not hasattr(self, "janela"):
         return False
      # formando barras horizontais:
      self.janela.hline(
         Y + a, X,
         BARRA_HORIZONTAL,
         self.barra_h,
         color_pair(1)
      )
      self.janela.hline(
         Y + 2 * a, X,
         BARRA_HORIZONTAL,
         self.barra_h,
         color_pair(1)
      )
      # formando barras verticais:
      self.janela.vline(
         Y, X + c,
         BARRA_VERTICAL,
         self.barra_v,
         color_pair(1)
      )
      self.janela.vline(
         Y, X + 2 * c,
         BARRA_VERTICAL,
         self.barra_v,
         color_pair(1)
      )
      # as grades foram desenhadas com sucesso.
      return True
   ...

   def redesenha_pecas(self) -> bool:
      "desenhando todas peças já colocadas."
      chave_valor = self.lugares_marcados.items()
      for (quadrante, peca) in chave_valor:
         posicao = self.grade.quadrante_coordenada(quadrante)
         self._desenha_matriz(peca, posicao)
      ...
   ...
   def desativa_seletor(self) -> None:
      self.seletor_ativado = False
   def desenha_seletor(self) -> bool:
      quadrante = self.seletor.atual
      # retângulo definindo o quadrante.
      (A, B) = self.grade.limites(quadrante)
      # dimensões do quadrante.
      altura = abs(A.y - B.y)
      largura = abs(A.x - B.x)
      # cor do seletor.
      cor = color_pair(3)
      # parte horizontal.
      for x in range(0, largura):
         X = (A.x + x)
         self.janela.addch(A.y, X, '+', cor)
         self.janela.addch(B.y, X, '+', cor)
      # parte vertical.
      for y in range(0, altura):
         Y = (A.y + y)
         self.janela.addch(Y, A.x, '+', cor)
         self.janela.addch(Y, B.x, '+', cor)
      # confirma desenho.
      return True
   ...
   def desenha_status(self) -> None:
      if (self.mensagem is None) or (self.lugar is None):
         return None
      posicao = self.lugar
      cor = color_pair(randint(1, 6))
      self.janela.addstr(
         posicao.y, posicao.x,
         self.mensagem, cor
      )
      # desativando novamente, apenas
      # uma visualização permitida por erro.
      self.mensagem = None
   ...
   def renderiza(self) -> None:
      self.janela.erase()
      # renderizando o tabuleiro e todos seus objetos que o compõem.
      self.desenha_barras()
      self.redesenha_pecas()
      if __debug__:
         self.grade.mostra_pontos(self.janela)
      if self.seletor_ativado:
         self.desenha_seletor()
      self.desenha_status()
      self.janela.refresh()
   ...
...

# Tupla contendo os pontos supeior-esquerdo e inferior-direito, nesta
# ordem, acima podemos abstratamente determinar um retângulo qualquer.
Retangulo = (Ponto, Ponto)

class GradePixelada:
   """
   Quadrado que ajuda ajusta a delimitar os quadrantes respectivos do
   Tabuleiro, dando suas coordenadas, e posicionando-o certo na tela
   do terminal. É basicamente a área de desenha das peças e traços de
   vitória, porem de forma mais organizada.
   """
   def __init__(self, posicao: Ponto, tamanho: Dimensao):
      # canto superior esquerdo do retângulo onde
      # fica a tabela formando o tabuleiro.
      (Y, X) = (posicao.y, posicao.x)
      (A, L) = (tamanho["altura"], tamanho[1])
      # fragmentos, dimensão de cada quadrante. Na
      # verdade é a Grade inteira, apenas divida em
      # três partes iguais de cada dimensão.
      (a, l) = (A // 3, L // 3)
      # retângulos delimitante de cada quadrante.
      # Uma tupla, contendo apenas dois Pontos, sendo
      # o primeiro representação do ponto superior
      # esquerdo, já o outro é a representação do
      # ponto inferior direito, formando assim um
      # retângulo. A contagem de quadrantes se dá
      # no superior esquerdo na primeira coluna
      # (o primeiro) até o inferior direito na última
      # coluna(o nono).
      # linha superior:
      self.Q1 = (posicao, Ponto(Y + a, X + l))
      self.Q2 = (Ponto(Y, X + l), Ponto(Y + a, X + 2*l))
      self.Q3 = (Ponto(Y, X + 2*l), Ponto(Y + a, X + 3*l))
      # linha do meio:
      self.Q4 = (Ponto(Y + a, X), Ponto(Y + 2*a, X + l))
      self.Q5 = (Ponto(Y + a, X + l), Ponto(Y + 2*a, X + 2*l))
      self.Q6 = (Ponto(Y + a, X + 2*l), Ponto(Y + 2*a, X + 3*l))
      # linha inferior:
      self.Q7 = (Ponto(Y + 2*a, X), Ponto(Y + 3*a, X + l))
      self.Q8 = (Ponto(Y + 2*a, X + l), Ponto(Y + 3*a, X + 2*l))
      self.Q9 = (Ponto(Y + 2*a, X + 2*l), Ponto(Y + 3*a, X + 3*l))
   ...
   def quadrante(self, p: Ponto) -> Quadrantes:
      assert isinstance(p, Ponto)
      retangulos = [
         self.Q1, self.Q2, self.Q3,
         self.Q4, self.Q5, self.Q6,
         self.Q7, self.Q8, self.Q9
      ]
      quadrantes = tuple(Quadrantes)
      for (indice, (P, Q)) in enumerate(retangulos):
         if GradePixelada.delimitado_por(P, Q, p):
            return quadrantes[indice]
      ...
      # se chegar até aqui, então a posição
      # dada é inválida.
      return None
   ...
   @staticmethod
   def delimitado_por(A: Ponto, B: Ponto, P: Ponto) -> bool:
      return (
         A.x < P.x < B.x and
         A.y < P.y < B.y
      )
   ...
   def quadrante_coordenada(self, retangulo: Quadrantes) -> Ponto:
      " retorna a coordenada do respectivo Quadrante."
      match retangulo:
         case Quadrantes.PRIMEIRO:
            return self.Q1[0]
         case Quadrantes.SEGUNDO:
            return self.Q2[0]
         case Quadrantes.TERCEIRO:
            return self.Q3[0]
         case Quadrantes.QUARTO:
            return self.Q4[0]
         case Quadrantes.QUINTO:
            return self.Q5[0]
         case Quadrantes.SEXTO:
            return self.Q6[0]
         case Quadrantes.SETIMO:
            return self.Q7[0]
         case Quadrantes.OITAVO:
            return self.Q8[0]
         case Quadrantes.NONO:
            return self.Q9[0]
      ...
   ...
   def mostra_pontos(self, janela) -> None:
      todos_pontos = [
         self.Q1, self.Q2, self.Q3,
         self.Q4, self.Q5, self.Q6,
         self.Q7, self.Q8, self.Q9,
      ]
      for (P, Q) in todos_pontos:
         (a, b) = (P.y, P.x)
         (c, d) = (Q.y, Q.x)
         janela.addch(a, b, 'X', color_pair(2))
         janela.addch(c, d, 'X', color_pair(2))
      ...
   ...
   def limites(self, qual: Quadrantes) -> Retangulo:
      match qual:
         case Quadrantes.PRIMEIRO:
            return self.Q1
         case Quadrantes.SEGUNDO:
            return self.Q2
         case Quadrantes.TERCEIRO:
            return self.Q3
         case Quadrantes.QUARTO:
            return self.Q4
         case Quadrantes.QUINTO:
            return self.Q5
         case Quadrantes.SEXTO:
            return self.Q6
         case Quadrantes.SETIMO:
            return self.Q7
         case Quadrantes.OITAVO:
            return self.Q8
         case Quadrantes.NONO:
            return self.Q9
      ...
   ...
...

class Cursor:
   "selector permite navegar no tabuleiro pelas setas direcinais."
   def __init__(self) -> None:
      # o quandrante em sí, com um valor inicial
      # mas seguirá o valor da sequência, baseado
      # no índice(também abaixo).
      self._atual = Quadrantes.QUINTO
      # todos quadrantes, numerados de cima
      # para baixo, da esquerda para direita.
      self.mapa_quadrantes = tuple(Quadrantes)
      # começa no meio.
      self.posicao = 4
   ...
   def move(self, direcao: Direcao) -> None:
      match direcao:
         case Direcao.DIREITA:
            # evitando overflow do cursor.
            if self.posicao not in (2, 5, 8):
               self.posicao += 1
         case Direcao.ESQUERDA:
            if self.posicao not in (0, 3, 6):
               self.posicao -= 1
         case Direcao.CIMA:
            if self.posicao > 2:
               self.posicao -= 3
         case Direcao.BAIXO:
            if self.posicao < 6:
               self.posicao += 3
      ...
      self._atual = self.mapa_quadrantes[self.posicao]
   ...
   def _get_atual(self):
      return self._atual
   atual = property(_get_atual, None, None, None )
...

from unittest import (TestCase)
import random, sys

class PrototipoDoJogo(TestCase):
   def runTest():
      t = Tabuleiro()

      for i in range(9):
         aleatorio = random.randint(1,9)
         t.coloca_peca(xis_matriz, aleatorio)

      tecla = t.janela.getch()
      coord = None
      try:
         coord = getmouse()
      except:
         coord = 'erro pelo caminho'
         pass
      else:
         pass
      t.janela.refresh()
      endwin()

      print("coordenas ==> %s"%coord)
      E = sys.exc_info()
      print("exeção:\n%s\n%s\n%s"%(E[0],E[1],E[2]))
      raise ForaTabuleiroError()
