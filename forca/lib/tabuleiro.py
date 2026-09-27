"""
   Agora aqui, terá a tela baseado no módulo curses do Python. As funções 
 estão aqui embutidas para não sobrecarregar o código-fonte principal com 
 muito entulho. Isto prejudica na leitura.
"""

# bibliotecas do Python:
import os
from curses import *

# dimensão do tabuleiro.
dimensao = os.get_terminal_size()
LINHAS, COLUNAS = dimensao.lines, dimensao.columns


# desenha forca.
def desenha_forca(janela):
	# paleta de cores.
	init_pair(3, COLOR_YELLOW, COLOR_BLACK)
	# haste da forca.
	janela.hline(3, 8,'#',10, color_pair(3))
	# tronco da forca.
	janela.vline(3, 8,'#', 12, color_pair(3))
	# base da forca.
	janela.hline(15, 5, '#', 8, color_pair(3))
	# gancho da forca.
	janela.addch(4,17,'#', color_pair(3))

# mostrando dica do jogo.
def campo_dica(dica, janela):
	texto_i = 'dica de jogo: %s' % dica
	# calculando coluna onde alocar.
	x = 60 - (len(texto_i) + 2)
	janela.addstr(2,x, texto_i)

# Letreiro das letras acertadas, e erradas.
# retorna string representando campo vázio
# de determinada palavra-chave da partida
# no momento. Útil tanto para o letreiro 
# das letras corretas como incorretas.
def campo_vazio(string):
	aux = ''
	for c in string: aux += '_ '
	return aux

# Função que marca o corpo do boneco a cada
# nova chamada. O corpo será desenhado de 
# acordo com a posição da forca. E não fará
# nenhuma nova aplicação após 7 chamadas,
# que é o número de erros aceito de acordo
# com as regras do jogo.
def marca_forca(janela):
	# todas os membros a marcar na ordem crescente
	# da esquerda para direta.
	marcacoes = [(5,17,'O'), (6,17,'|'),(6,16,'/'),
					(6,18,'\\'),(7,17,'|'),(8,16,'/'),
					(8,18,'\\')]
	# definindo limite até sete chamadas.
	if marca_forca.chamadas_feitas <= 7:
		global tabuleiro
		janela.addch(*(marcacoes[marca_forca.chamadas_feitas-1]))
		marca_forca.chamadas_feitas += 1
# atribuindo variável de estado da função.
marca_forca.chamadas_feitas = 1

# Função preenche campos de acertos e erros. Dado
# tais conjuntos contendo os conteúdo, pega eles
# e preenche campos vázios, nas determinadas posições
# para dá a impressão que estão sendo preenchidos 
# de acrodo com as jogadas.
def marca_letreiro(acertos, erros, pC, janela):
	# primeiro cuidando dos erros...
	# por ser uma tarefa mais trivial, é claro!
	_erros = ""
	for i in range(7):
		try:
			_erros += '%s '%sorted(list(erros))[i]
		except IndexError:
			_erros += '_ '
	# agora os acertos, que terá que ser 
	# preenchidos nos "campos vázios" de acordo
	# com a palavra chave.
	_acertos = ''
	for x in pC:
		if x in acertos: _acertos += '%s ' % x
		else: _acertos += '_ '
	# escreve todas strings geradas nas específicas
	# posições no tabuleiro.
	pa, pe = [6,30], [8,30]
	# recalculando as posições de acordo com a
	# dimensão da tela no momento.
	#proposições:
	x1 = len(_acertos) + pa[1] > COLUNAS
	x2 = len(_erros) + pe[1] > COLUNAS
	if x1 or x2:
		if x1:
			excesso = len(_acertos) + pa[1] - COLUNAS
			pa[1] -= excesso + 2 # duas à mais(... ou há menos!), por segunrança.
		elif x2:
			excesso = len(_erros) + pe[1] - COLUNAS
			pe[1] -= excesso + 2 # mais duas para dá segurança.
	janela.addstr(pa[0], pa[1], _acertos.upper(),A_BOLD)
	janela.addstr(pe[0], pe[1], _erros.upper(),A_BOLD)

# Esta aqui escreve(atualiza) o placar do jogo.
def marca_placar(acertos, erros, janela):
	# paletas de cores necessárias:
	init_pair(1, COLOR_GREEN, COLOR_BLACK)
	init_pair(2, COLOR_RED, COLOR_BLACK)
	# marca o placar numérico quantos os acertos.
	modelo_acertos = 'acertos:%2i' % len(acertos)
	modelo_erros = 'erros:%2i' % len(erros)
	#modelo = 'acertos: %i \t erros: %i' % (len(acertos), len(erros))
	janela.addstr(15, 25, modelo_acertos, color_pair(1) | A_BOLD)
	c = 25 + len(modelo_acertos) + 10 # acertando coluna.
	janela.addstr(15, c, modelo_erros, color_pair(2) | A_BOLD)
	# sobreescrevendo "pontuação" com cor diferente.
	janela.addstr(15,25+len(modelo_acertos)-1,str(len(acertos)))
	janela.addstr(15,c+len(modelo_erros)-1,str(len(erros)))
# atualiza a tela após uma jogada, renovando o 
# letreiro, e o placar do jogo.
def atualiza_tela(acertos, erros, pC,dica, janela):
	marca_letreiro(acertos, erros, pC, janela)
	marca_placar(acertos, erros, janela)
	campo_dica(dica, janela)

# Função apaga todo a parte do tabuleiro que não serve
# mais pois é fim de jogo, e, mantém o estado da
# forca, onde ela parou.
def limpa_tabuleiro(qtd_erros, janela):
	janela.erase() # limpa todo o quadro do terminal.
	# reseta o número de execuções realizadas.
	marca_forca.chamadas_feitas = 1 
	# escreve os erros cometidos novamente,...
	# baseado no corpo do boneco enforcado.
	for i in range(qtd_erros): marca_forca(janela)

# gera quadro de resultado da partida.
def quadro_resultado(lin: int, col: int, *strings):
   # String com maior comprimento.
   comprimento = max([len(s) for s in strings]) + 2
   # criando nova janela.
   nova_janela = newwin(len(strings)+3, comprimento, lin, col)
   # desenhando borda.
   nova_janela.border(0,0,0,0,0,0,0,0)

   for (i,s) in enumerate(strings):
      nova_janela.addstr(i+1, 1,s)
   nova_janela.refresh()

#  Filtra tela após termino do jogo.
def captura_tela(janela):
	#converte byte-string para string.
	def bytestr_to_str(bs):
		_str = ''
		for c in bs: _str += chr(c)
		return _str
	string = ""
	for l in range(1, LINHAS-1):
		string += bytestr_to_str(janela.instr(l,1,COLUNAS-2)) + '\n'
	return string

# == == == == == == == == == == == === == == == == == == == == == == == ===
#                          Testes Unitários
# == == == == == == == == == == == === == == == == == == == == == == == ===
import unittest, curses

class CoresDoCurses(unittest.TestCase):
   def runTest(self):
      print("curses.COLOR_BLUE:", curses.COLOR_BLUE)
      print("curses.COLOR_YELLOW:", curses.COLOR_YELLOW)
      print("curses.COLOR_RED:", curses.COLOR_RED)
      print("curses.COLOR_CYAN:", curses.COLOR_CYAN)
      print("curses.COLOR_GREEN:", curses.COLOR_GREEN)
      print("curses.COLOR_BLACK:", curses.COLOR_BLACK)

class DefinindoUmNovoPar(unittest.TestCase):
   def runTest(self):
      J = initscr()
      start_color()
      print("Total de cores:", curses.COLORS)
      #init_pair(93, COLOR_YELLOW, COLOR_BLUE)
      endwin()
