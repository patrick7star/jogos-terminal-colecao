#!/bin/python3 -BO

# Biblioteca padrão do Python:
from platform import system as sistema
from pathlib import (Path)
from sys import argv
from random import choice
from curses import (
   KEY_RIGHT, KEY_LEFT,
   KEY_DOWN, KEY_UP, KEY_ENTER
)
# Biblioteca do jogo:
from codigo.tabuleiro import *
from codigo.pecas import *
from codigo.motor import *
from codigo.ponto import Direcao
# Bibliote externas:
from biblioteca_externa.utilitarios.lib import tela

# Dependendo da plataforma, modificar a permisão do script principal, ou 
# instalar depedendências.
if sistema() == "Windows":
   from subprocess import (Popen, DEVNULL, PIPE)
   from sys import stdout as saida

   pip_instalacao = Popen(
      ["powershell", "pip install windows-curses"],
      bufsize = 0, stdout=PIPE
   )
   pip_instalacao.wait()
   (dados, _) = pip_instalacao.communicate()
   dados = dados.decode(encoding="latin1")
   if __debug__:
      print("conteudo '%s'", dados)
   if "Requirement already sastified" in dados:
      print("'windows-curses' já está instalado.")
   else:
      print("instalação feita com sucesso.")

elif sistema() == "Linux":
   from os import (chmod, getenv)
   from stat import (S_IXGRP, S_IRWXU, S_IXOTH)
   from os.path import join as JoinPath
   # muda a permição do arquivo script que lança
   # estes jogo. Só clicar e jogar.
   try:
      chmod("setup.py", S_IRWXU | S_IXGRP | S_IXOTH)
   except FileNotFoundError:
      caminho = JoinPath(
         getenv("PYTHON_CODES"), 
         "velha/setup.py"
      )
      chmod(caminho, S_IRWXU | S_IXGRP | S_IXOTH)

# Fazendo com que o teclado também funcione para marcar posições, navegando 
# através do jogo.
def converte_em_direcoes(code: int) -> Direcao:
   assert isinstance(code, int)

   if code == KEY_UP:
      return Direcao.CIMA
   elif KEY_DOWN == code:
      return Direcao.BAIXO
   elif KEY_LEFT == code:
      return Direcao.ESQUERDA
   elif KEY_RIGHT == code:
      return Direcao.DIREITA
   else:
      return None

def roda_o_jogo(jogador: Jogadores, tabuleiro: Tabuleiro) -> None:
   assert isinstance(jogador, Jogadores)
   assert isinstance(tabuleiro, Tabuleiro)
   global uso_do_teclado

   # Roda o jogo até não houver mais jogadas.
   while jogadas_restantes() != 0:
      # Desenha todo tabuleiro e seus objetos.
      tabuleiro.renderiza()
      # Pega 'input' do teclado.
      tecla = tabuleiro.janela.getch()
      KEY_SPACEBAR = ' '

      # escape da partida.
      if tecla == ord('s') or tecla == ord('S'):
         break

      # Uso do teclado para jogar, caso contrário do mouse.
      if uso_do_teclado:
         # Pega possível tecla direcional, e converte-a na sua 
         # respectiva Direção.
         seta = converte_em_direcoes(tecla)
         local = tabuleiro.seletor.atual

         if seta is not None:
            tabuleiro.seletor.move(seta)
            continue
         elif (tecla == KEY_ENTER) or (tecla == KEY_SPACEBAR):
            try:
               tabuleiro.coloca_peca(jogador, local)

            except LocalJaPreenchidoError:
               # Tentar novamente, vagão já preenchido.
               tabuleiro.informa_algo("posição já preenchida!")
               continue
      else:
         # coordenadas do mouse relativo a janela.
         coord = tabuleiro.posicoes()

         try:
            local = tabuleiro.posicao_clicada(coord)
            tabuleiro.coloca_peca(jogador, local)

         except ForaTabuleiroError:
            # Tentar novamente, vagão já preenchido.
            tabuleiro.informa_algo("fora do tabuleiro!")
            continue
         except LocalJaPreenchidoError:
            tabuleiro.informa_algo("posição já marcada")
            continue

      try:
         adiciona_peca(jogador, numeracao_em_coord(local))
      except LocalJaPreenchidoError:
         # voltar para o começo do laço, e tentar novamente.
         continue
      finally:
         alguma_peca_venceu = (
            peca_vitoriosa(Jogadores.XIS) or
            peca_vitoriosa(Jogadores.BOLA)
         )
         if alguma_peca_venceu:
            tabuleiro.marca_vitoria(fileira_ganha())
            break

         # obtem evento do mouse/teclado.
         jogador = jogador.alternar()

   # Encerra a "interface do curses".
   tabuleiro.desmancha_tabuleiro()

def visualizacao_resultado_da_partida() -> None:
   "Mostra resultado do jogo e demais informações."
   if peca_vitoriosa(Jogadores.XIS):
      o_vencedor = r'"xis" GANHOU.'
   elif peca_vitoriosa(Jogadores.BOLA):
      o_vencedor = r'"bola" GANHOU.'
   else:
      o_vencedor = "jogo EMPATADO."

   # Cria tela de desenho.
   t = tela.Tela(12, 300, grade=False)
   # Cabeçalho sobre os jogadores.
   t.escreve(0, 0, "1º jogador: 'X'\t2º jogador: 'O'")
   # Desenha o vencedor.
   (linha, coluna) = (4, 10)
   t.escreve(linha, coluna, o_vencedor)
   t.enquadra(
      linha-2, coluna-3,
      altura = 4,
      largura = len(o_vencedor) + 4
   )
   # screenshot miniaturizado sobre os jogo em geral.
   t.escreve(0, 40, "como o jogo terminou:")
   tabuleiro_screenshot = tabuleiro_str().split('\n')

   while tabuleiro_screenshot.count('') > 0:
      tabuleiro_screenshot.remove('')

   arg1 = tabuleiro_screenshot[0]
   arg2 = tabuleiro_screenshot[1]
   arg3 = tabuleiro_screenshot[2]
   arg4 = tabuleiro_screenshot[3]
   arg5 = tabuleiro_screenshot[4]
   arg6 = tabuleiro_screenshot[5]
   arg7 = tabuleiro_screenshot[6]
   t.lista_strings(2, 43, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

   # Risco de divisão do resultado.
   t.risca(1, 34, 9, simbolo='|', horizontal=False)
   # visualizando tela o resultado geral.
   print(t)

   # Registrando no banco de screenshots do tabuleiro.
   # Considerando-se uma execução do diretório velha, por enquanto...
   CAMINHO_BD = Path("../data/velha/resultados.txt")
   resultado_bd = open(CAMINHO_BD, mode="at")
   print(t, file=resultado_bd)


# Ativa o modo teclado para jogar.
qtd_args = len(argv)
uso_do_teclado = (qtd_args == 2 and "--teclado" == argv[1])
# Instância o tabuleiro para o jogo(inicializa a "interface gráfica").
board = Tabuleiro()
# Seleciona peça de forma aleatória.
player = choice([Jogadores.XIS, Jogadores.BOLA])

if (not uso_do_teclado):
   board.desativa_seletor()

# Inicializa execução ...
roda_o_jogo(player, board)
visualizacao_resultado_da_partida()
