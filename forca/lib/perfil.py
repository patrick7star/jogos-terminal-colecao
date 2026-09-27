# Perfil da jogada. Basicamente uma 
# info sobre o que ocorreu, e como 
# acabou à partida.
# Aqui pegará a palavra-chave; o tempo
# que a partida durou; seus erros e 
# acertos.

# bibliotecas do Python:
import shelve, sys, pickle
from time import time
# minha biblioteca:
from .external_lib.arvore import matriciar_str,imprime_matriz
from lib.moldura_str import emoldura

# o que pode ser importado:
__all__ = ["Perfil","armazena","faz_backup","mostra_partidas",
           "arq_aglomerado"]
# dados:
# nome do banco de dados.
if sys.platform == 'linux':
	nome_bdd = "./data/partidas"
	arq_aglomerado = './data/aglomerado.dat'
elif sys.platform == 'win32':
	nome_bdd = '.\\data\\partidas_win'
	arq_aglomerado = '.\\data\\aglomerado.dat'

# Faz um recorte da parte realmente
# importante da captura de tela, após 
# o término do jogo.
def recorte_importante(tela):
	matriz = matriciar_str(tela)
	m,n = len(matriz), len(matriz[0])
	ultima_coluna, ultima_linha = (0,0)
	L1, C1 = (None, 80)
	for i in range(m):
		for j in range(n):
			# analizando apenas caractéres na tabela
			# ascii.
			if matriz[i][j].isascii():
				# pegando posição última na coluna.
				if ultima_coluna < j:
					ultima_coluna = j
				# obtendo linha limite do que realmente
				# importada na captura.
				ultima_linha = i
				# registrando coluna mais a esquerda
				# contendo.
				if j < C1: C1 = j
				# pegando primeira linha com caractéres.
				if not L1: L1 = i

	# escrevendo recorte da tela.
	_str = ''
	for i in range(L1-1,ultima_linha+1):
		for j in range(C1-1, ultima_coluna+1):
			_str += matriz[i][j]
		_str += '\n'
	#imprime_matriz(matriz)
	return _str

# classe para armazenar perfil da partida.
class Perfil:
	"""
	 Classe principalmente para registrar dados 
	da partida. Os métodos deles são auxiliares
	nesta tarefa.
	"""
	# variáveis auxiliares:
	acionada_mj =  False
	ti = None
	acionada_mt = False

	# método construtor.
	def __init__(self, A, E, pC, dica):
		# sequência com acertos feitos na partida.
		self.acertos = tuple(A) 
		# sequência com erros cometidos durante a partida.
		self.erros = tuple(E)
		# marca jogada, a peça utilizada e seu tempo.
		self.jogadas = {}
		#"self.tempo" - gerando durante a execução 
		# de um método. Colocada aqui para dizer que
		# há instâncias implícitas.
		self.palavra_chave = pC
		# dica da partida.
		self.dica = dica

	# marca o tempo da partida.
	def marca_tempo(self):
		"marca tempo do perfil."
		if len(self.jogadas) == 0: ... 
		else:
			self.tempo = sum(t for s,t in self.jogadas.values())
	# variáveis de estado da função.
	#self.marca_tempo.acionada = False

	# marca a jogada da partida e demais dados.
	def marca_jogada(self, peca=None):
		"marca uma info da jogada feita."
		if Perfil.acionada_mj:
			# quantidade de jogadas já registradas.
			q = len(self.jogadas) + 1
			# tempo final de registro da jogada.
			tf = time()-Perfil.ti
			# a composição das jogadas são: qual sua
			# ordem como chave no dicionário; o valor
			# um par ordenada, sendo o primeiro elemento
			# a peça jogada, e o segundo, o tempo levado
			# pelo jogador para fazer-lô.
			self.jogadas[q]=(peca, tf)
			# neutralizando função novamente para 
			# novos registros.
			Perfil.acionada_mj = False
		else:
			# se for a primeira vez que essa 
			# função é acionada, então...
			Perfil.ti = time()
			Perfil.acionada_mj = True

	# pega o resultado.
	def marca_resultado(self, resultado):
		"verifica o resultado do jogo."
		def converte_bool(valor):
			if valor: return "venceu"
			return "perdeu"
		# será um valor lógico.
		self.resultado = converte_bool(resultado)

	# imprime a info do perfil, todos seus dados
	# devidamente legendados.
	def __str__(self):
		string = ''
		if "ordem" in self.__dict__:
			string = "ordem: %iª\n" % self.ordem
		string += "acertos: %s\n" % str(self.acertos).upper()[1:-1:1]
		string += "erros: %s\n" % str(self.erros).upper()[1:-1:1]
		string += "jogadas:\n"
		for (c,v) in self.jogadas.items():
			string += '%10iª » \'%s\', %0.3f seg\n' % (c,v[0].upper(),v[1])
		string += 'palavra-chave: "%s" \n' % self.palavra_chave
		string += 'dica: "%s" \n' % self.dica
		# atributos criados ao executar métodos 
		# da classe.
		if 'resultado' in self.__dict__:
			string += 'resultado: %s\n'%self.resultado
		if 'tempo' in self.__dict__:
			string += 'tempo total: %0.2f seg\n' % self.tempo
		if "captura_tela" in self.__dict__:
			string += 'captura do tabuleiro ao fim:\n' + recorte_importante(self.captura_tela)
		return emoldura(string)
		#return string

# armazena um perfil no banco de dados.
def armazena(perfil):
	# abre banco de dados.
	banco = shelve.open(nome_bdd)
	# cria atributo para perfil, registrando
	# que partida foi essa.
	perfil.ordem = len(list(banco.keys())) + 1
	# registra no banco com tal ordem definida acima.
	banco['%iº'%(len(banco)+1)] = perfil
	banco.close()

# busca e mostra todas jogadas.
def mostra_partidas():
	# função ordena as chaves, especificamente,
	# do banco de dados.
	def ordena_ordinais(lista):
		nova = [int(x.strip('º')) for x in lista]
		nova.sort(reverse=True)
		return ['{0}º'.format(n) for n in nova]
	# abrindo banco de dados.
	bdd = shelve.open(nome_bdd)
	# se for maior que dez, mostrar apenas os dez últimos.
	if len(bdd) >= 8:
		print('as cinco últimas partidas do total de %i:'%len(bdd),end=' ')
		chaves = ordena_ordinais(list(bdd.keys()))[0:8]
		print('{','; '.join(chaves),'\b}')
	else:
		print('todas partidas realizadas, totalizam %i:'%len(bdd),end=' ')
		chaves = ordena_ordinais(list(bdd.keys()))
		print(', '.join(chaves))
	for c in chaves: print(bdd[c])
	bdd.close()

# adiciona novos contatos, independente da plataforma.
def faz_backup():
	# lendo todos dados do arquivo.
	arq = open(arq_aglomerado,mode='rb')
	perfils = []
	try:
		while True: perfils.append(pickle.load(arq))
	except EOFError: ...
	arq.close()

	# Verifica se os perfils são iguais. Independente
	# da ordem dada.
	def perfils_iguais(p1, p2):
		# proposições.
		A = p1.acertos == p2.acertos
		B = p1.erros == p2.erros
		C = p1.tempo == p2.tempo 
		D = p1.resultado == p2.resultado 
		E = p1.palavra_chave == p2.palavra_chave
		F = p1.dica == p2.dica
		G = p1.jogadas == p2.jogadas
		return A and B and C and D and E and F and G
	# verifica se o perfil pertence a lista
	# de perfils.
	def perfil_pertence(perfil, lista):
		# se a lista estiver vázi, já retornar como 
		# não pertence.
		if len(lista) == 0: return False
		for p in lista:
			if perfils_iguais(p, perfil): return True
		return False 
	banco = shelve.open(nome_bdd)
	for p in banco.values():
		# se não houver tal perfil, adicionar.
		if not perfil_pertence(p, perfils): 
			# atribuindo uma nova ordem.
			p.ordem = len(perfils) + 1
			perfils.append(p)
	banco.close()
	# reescrevendo o arquivo, com perfils novos 
	# adicionados.
	arq = open(arq_aglomerado,mode='wb')
	for p in perfils: pickle.dump(p, arq)
	arq.close()

# execução de testes:
if __name__ == '__main__':
	P = Perfil({'a', 'b','c','i','x'},{'e','k','m'},'abacaxi','é uma fruta')
	P.marca_resultado(False)
	#print(P)
	armazena(P)

	p = Perfil({'a', 'b','c','i','x'},{'e','k','m'},'abacaxi','é uma fruta')
	
	p.marca_tempo() # abrindo tempo total.

	p.marca_jogada('a')
	input('aperte ENTER quando puder:')
	p.marca_jogada('a')

	p.marca_jogada('b')
	input('aperte ENTER quando puder:')
	p.marca_jogada('b')

	p.marca_jogada('c')
	input('aperte ENTER quando puder:')
	p.marca_jogada('c')

	p.marca_jogada('i')
	input('aperte ENTER quando puder:')
	p.marca_jogada('i')

	p.marca_jogada('k')
	input('aperte ENTER quando puder:')
	p.marca_jogada('k')

	p.marca_jogada('e')
	input('aperte ENTER quando puder:')
	p.marca_jogada('e')

	p.marca_jogada('x')
	input('aperte ENTER quando puder:')
	p.marca_jogada('x')

	p.marca_jogada('m')
	input('aperte ENTER quando puder:')
	p.marca_jogada('m')

	p.marca_tempo() # fechando tempo total.
	#print(p)
	p.marca_resultado(True)
	armazena(p)

	bdd = shelve.open(nome_bdd)
	print('chaves=',bdd)
	print('quantidade=',str(len(bdd)))
	for x in bdd.keys(): print(bdd[x])
	bdd.close()
