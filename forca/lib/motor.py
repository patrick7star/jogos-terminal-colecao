"""
 Motor do jogo, verifica se há vitória, faz uma jogada, contêm em sí mesmo,
 ou importa, todas a variáveis importantes da partida.
"""

# Bibliotecas padrão do Python:
import os, random, sys
from pathlib import (Path)

# Conjunto contendo todas as letras acertadas durante a partida.
acertos = set([])
# Conjunto contendo todas as letras erradas nas jogadas.
erros = set([])
# Palavra-chave da partida no momento.
# Será conseguida de maneira aleatória,
# de acordo com o banco de dados do
# momento.
palavra_chave = 'forca'
#variável que armazena dica de jogo.
dica = None
# frequência repetições.
frequencia = []

# Função que realiza a jogada. Será adicionada
# a peça no conjunto de "erros" caso 
# a letra(peça) não seja da "palavra-chave",
# e adicionada no conjunto "acertos" casa 
# seja uma letra da variável.
def joga(peca):
	if peca in palavra_chave:
		acertos.add(peca)
		# registrando sua frequência...
		frequencia.append(peca)
		# retorna "verdadeiro" para: foi uma 
		# jogada acertada.
		return True
	else: 
		# se já foi marcada como errada, então
		# retorna verdadeira.
		if peca in erros: return True
		erros.add(peca)
		# registrando sua frequência...
		frequencia.append(peca)
		# retorna "falso" para: foi uma 
		# jogada errada.
		return False

# verifica se o jogador ganhou o jogo.
def e_vitorioso():
	# Se houver um espaço em branco na palavra-chave
	# já a joga. Isto, para burlar o espaços em brancos
	# no futuro, que contabilizam como letras.
	if ' ' in palavra_chave and len(acertos) == 0: joga(' ')
	# A verificação se dá como verdade, verificando
	# a igualdade entre o número de letras acertadas
	# e todas as letras(não repetidas) da palavra-chave.
	return len(acertos) == len(set(palavra_chave))

# Verifica se o jogo foi finalizado, primeiro
# verificando se o jogador é vitorioso, ou
# se já foi derrotado por cometer demasiados
# erros na partida.
def partida_finalizada():
	# verifica se há um vitorioso.
	if e_vitorioso(): return True
	# verificando se o número de erros é igual a 
	# sete, que é o número máximo de erros permitidos.
	if len(erros) == 7: return True
	# caso nenhum acima acione, então o jogo
	# não está finalizado ainda.
	return False

# trata palavra. Se houver vogáis acentuadas
# a função os torna comuns.
def trata_vogais(palavra):
	_palavra = ''
	for c in palavra:
		if c in 'áàãâä': _palavra += 'a'
		elif c in 'éèẽêë': _palavra += 'e'
		elif c in 'óòõôö': _palavra += 'o'
		elif c in 'íìĩïî': _palavra += 'i'
		elif c in 'úùũûü': _palavra += 'u'
		elif c == 'ç': _palavra += 'c'
		else: _palavra += c
	return _palavra

def palavra_aleatoria() -> str:
   "Função colhe uma palavra aleatória do banco de dados do programa."
   global dica

   # Caminho padrão ao banco de dados. Está numa variável, pois pode mudar.
   if sys.platform == 'linux':
      caminho = Path('../data/forca/palavras/')
   if sys.platform == 'win32':
      #caminho = '.\\data\\palavras\\'
      raise OSError("não ainda pensando neste sistema!")
   # lista com todos arquivos no banco de dados.
   diretorio = os.listdir(path=caminho)
   # palavra do arquivo.
   tema = random.choice(diretorio)
   # escolhendo um dentre todos eles.
   nome_arq = caminho.joinpath(tema)
   # marcando a dica do programa.
   dica = tema[0:tema.index('.')].replace('_', ' ')
   # Abrindo um arquivo selecionado aleatóriamente
   # e colhendo uma palavra, de maneira aleatória 
   # também, dentre todas lá.
   arq = open(nome_arq, mode='r',encoding='utf-8')
   palavras = arq.read().split('\n')
   arq.close()

   return trata_vogais(random.choice(palavras)).lower()

if __name__ == '__main__':
	# muitas palavras aleatórias selecionadas...
	for i in range(50): print(palavra_aleatoria())
