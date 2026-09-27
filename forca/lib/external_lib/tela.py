"""
 Acessório importantissímo para gerar os gráficos
no console de tal biblioteca. Na verdade o potencial
de reutilização de tal biblioteca é o máximo possível.
"""

# bibliotecas:
import os, sys, copy

class Tela:
	"""
	 Tal classe é muito útil para impressão na tela.
	Ela oferece um monte de ferramentas para você
	personalizar o máximo tal impressão: de "rabiscar
	o terminal" para produzir desenhos; também escrever
	palavras; listar-las também de várias maneiras. É
	realmente algo para ser reutilizado em várias outras
	aplicações para fazer impressões.
	"""
	# construtor.
	def __init__(self, L, C):
		dimensao = os.get_terminal_size()
		# Número de colunas do gráfico.
		# Lembre-se que, o máximo é algo menor
		# ou igual a dimensão do terminal.
		# A segunda linha é o número de linhas.
		if C > dimensao.columns or C <= 20:
			self.colunas = dimensao.columns - 3
		else: self.colunas = C

		if L > dimensao.lines or L <= 5:
			self.linhas = dimensao.lines - 3
		else: self.linhas = L

		# Matriz que representa a tela do programa.
		# Ela terá as dimensões dos dados passados,
		# ou o padrão do terminal.
		self.simbolo = ' '
		self.matriz = [[self.simbolo for i in range(self.colunas)] for j in range(self.linhas)]

	# sobrecarregando impressão do objeto.
	# Será formada uma string, formatada coma 
	# uma tabela, ou seja, quebra de linha 
	# na última coluna.
	def __str__(self, borda=False):
		string = ''
		for i in range(self.linhas):
			for j in range(self.colunas):
				string += self.matriz[i][j]
			# adicionando quebra de linha.
			string +='\n'
		return string
	
	# O programa parte inicialmente na horizontal, porém
	# "delisgando" tal função, ele vai para vertical. O
	# símbolo padrão é uma "hashtag", porém também pode 
	# ser mudado. A posição(linha e coluna) determinando
	# de onde partir, se houver algo na frente, será 
	# transcrito. O comprimento é o quanto rabíscar, se 
	# tal, esbarrar com o limite da tela, será continuado
	# uma linha abaixo, ou lateral, dependendo de como
	# foi definido a direção.
	def rabisca(self,L,C,comprimento,simbolo='$',horizontal=True):
		# se for horizontal, bem,... rabiscar horizontalmente.
		if horizontal:
			for j in range(comprimento):
				# se exceder o limite de colunas, continar 
				# o processo na linha abaixo.
				if (j+C) > (self.colunas-1): 
					self.matriz[L+1][j-comprimento] = simbolo
				else: self.matriz[L][C+j] = simbolo
		else:
			# no outro caso, desenhar na vertical.
			for i in range(comprimento):
				if (i+L) > (self.linhas-1):
					self.matriz[i-comprimento][C+1] = simbolo
				else: self.matriz[L+i][C] = simbolo
			
	# Limpa tela rabiscada ou não, traz tudo 
	# zerado novamente, sem qualquer coisa. Se 
	# a borda estiver ativada, deixa apenas ela.
	def limpa(self):
		"limpa toda tela, rabiscos, listas, caractéres e mais."
		for i in range(self.linhas):
			for j in range(self.colunas):
				self.matriz[i][j] = self.simbolo

	# Escreve uma letra em determinada posição da 
	# tela. A posição tem que ser válida, do caso
	# contrário nada acontecerá. Existe um símbolo
	# padrão de preenchimento, porém, se for dado 
	# algum, ele será substituído.
	def marca(self, L,C,simbolo='x'):
		# verificando se a posição passada é 
		# válida.
		p = L >= 0 and L <= (self.linhas-1)
		q = C >= 0 and C <= (self.colunas-1)
		# se for marcar na matriz.
		if p and q: self.matriz[L][C] = simbolo

	# Escreve uma string dada a posição. Se a 
	# posição não for válida, ele não escreve 
	# a string, com ser válido, digo ela não
	# transbordar a dimensão da tela.
	def escreve(self, L,C, string):
		# proposições:
		# se não transbordará em colunas.
		A = (C+len(string)) <= self.colunas-1
		# se não transbordará em linhas.
		B = L <= self.linhas-1
		# verifica se o tamanho da string dado 
		# a posição onde colocar-lá não transborda.
		if A and B:
			for (j, c) in enumerate(string):
				self.matriz[L][C+j] = c

	# Lista um monte de strings na ordem que 
	# foram dadas. Se alguma tranbordar tanto
	# colunas como linhas, serão cortadas.
	def lista_strings(self, L, C, * strings):
		filtro = []
		# Vamos considerar todas strings como 
		# válidas, não cortando para encaxar
		# o número de linhas. Posteriormente, 
		# vamos eliminar as que quebram o 
		# número de colunas.
		for s in strings:
			if C + len(s) <= self.colunas-1:
				filtro.append(s)
		# escrevendo cada uma das strings na forma
		# de lista.
		for i,s in enumerate(filtro): 
			self.escreve(L+i,C,s)

	# Imprime a tela, porém apagando a outra impressão
	# para parecer que ela está em tempo real sendo 
	# constantemente atualizada.
	def imprime(self, borda=True):
		'''
		 Imprime a matriz que representa a tela no terminal.
		Se algo já foi impresso anteriormente no terminal, será
		apgado, incluse uma impressão de tela feita anteriormente.
		Vem coma uma opção ativada(default keyword), porém,
		pode ser alternada. Esta em especifíco defino, se a 
		borda da tela será impressa ou não.
		'''
		# limpa tela.
		# para sistema específico.
		if sys.platform == 'win32': os.system('cls')
		elif sys.platform == 'linux': os.system('clear')

		# circunscrevendo à tela.
		# símbolo da borda.
		S = '*'

		# nova matriz cópia da outra.
		M = copy.deepcopy(self.matriz)

		# Adicionando linhas para serem bordas.
		# borda superior. Se, a opção foi acionada.
		if borda:
			M.insert(0,[S for i in range(self.colunas)])
			# borda esquerda e direita.
			for i in range(len(M)):
				M[i].insert(0,S)
				M[i].append(S)
			# borda inferior.
			M.append([S for i in range(self.colunas+2)])

		# imprimindo matriz.
		for i in range(len(M)):
			for j in range(len(M[i])): print (M[i][j], end='')
			print("")
		# deleta matriz copiada só por preucação.
		del M

	# Cria um retângulo dado dois pontos(duas
	# coordenadas).
	def circunscreve(self, * coordenadas):
		# simplificando coordenadas.
		try:
			(l1,c1,l2,c2) = (coordenadas[0][0],coordenadas[0][1],
								  coordenadas[1][0], coordenadas[1][1])
		except: sys.exit('erro de sintaxe!'.upper())
		# proposições:
		# Verificando... primeiro, se há duas coordenadas.
		# Segundo, se cada coordenada têm apenas dois valores.
		p1 = len(coordenadas) == len(coordenadas[0]) == len(coordenadas) == 2
		# Ambos pares distintos.
		p2 = coordenadas[0] != coordenadas[1]
		# tem que está superior no caso das linhas, e, 
		# a esquerda no caso das colunas; digo, o/a 
		# primeiro(a)/ponto coordenada em relação ao segundo.
		p3 = (c1 < c2) and (l1 < l2)
		# verifica se ambos os pontos estão no limite do quadro.
		p4 = ((0 <= l1 <= self.linhas) and (0<=c1<= self.colunas) and
			  (0 <= l2 <= self.linhas) and (0 <= c2 <= self.colunas))
		# verifica transbordamento da coluna.
		p5 = ((0<=l1<=self.linhas) and (0<=c1<=self.colunas) and 
			  (0<=l2<=self.linhas) and (c2 > self.colunas))
		# verica um transbordamento das linhas.
		p6 = ((0<=l1<=self.linhas) and (0<=c1<=self.colunas) and 
			(l2 > self.linhas) and (0 <= c2 <= self.colunas))

		if p3 and p1 and p2 and p4:
			# comprimentos:
			v, h = abs(l1-l2),abs(c1-c2)
			# lado superior do retângulo.
			self.rabisca(l1,c1, h)
			# lado esquerdo do retângulo.
			self.rabisca(l1,c1,v,horizontal=False)
			# lado inferior do retângulo.
			self.rabisca(l2,c1,h+1) # acrescenta um, pois... bem corrige o erro.
			# lado direito do retângulo.
			self.rabisca(l1, c2,v,horizontal=False)
		else:
			if not p3:
				# se o 1º ponto estiver mais "distante" que 
				# o 2º, usar da recursividade chamando 
				# a função com parâmetros permutados.
				self.circunscreve((l2,c2),(l1,c1))
			elif not p4:
				if p5 and (not p6):
					# comprimentos dos lados:
					v,h = abs(l1-l2),abs(self.colunas-c1)
					# escrevendo lado superior...
					self.rabisca(l1,c1,h)
					# ... agora, escrvendo lado inferior...
					self.rabisca(l2,c1, h)
					#... por fim, barra esquerda.
					self.rabisca(l1,c1, v,horizontal=False)

				elif (not p5) and p6:
					# comprimentos dos lados:
					(v,h) = abs(self.linhas-l1), abs(c1-c2)
					# escrevendo lado superior...
					self.rabisca(l1,c1,h)
					#... agora, barra esquerda ...
					self.rabisca(l1,c1, v,horizontal=False)
					# ... por fim, barra direita.
					self.rabisca(l1,c2, v,horizontal=False)

				else:
					# comprimentos dos lados:
					h,v = abs(c1-self.colunas), abs(l1-self.linhas)
					# escrevendo lado superior...
					self.rabisca(l1,c1,h)
					#... agora, barra esquerda ...
					self.rabisca(l1,c1, v,horizontal=False)

	# enquadra de determinado ponto. Faz o mesmo
	# que o circunscreve, porém, será preciso apenas
	# o primeiro ponto/coordenada, e se quiser
	# passar altura ou largura do retângulo, que já 
	# tem tamanhos definidos.
	def enquadra(self, L, C, altura=4, largura=5):
		self.circunscreve((L,C), (L+altura,C+largura))

# execuções de teste.
if __name__ == "__main__":

	# criando instância da tela.
	t = Tela(L=4,C=950)	
	
	# testando função de "escrever" na tela.
	t.rabisca(10,10,10,'*')
	t.rabisca(11,11,7)
	t.rabisca(8,15,14,'@',horizontal=False)
	# mostrando tela...
	print(t)

	# testando desvio de tela.
	t.rabisca(19, 37, 11, 'X', False)
	t.rabisca(4,50, 26, 'H');
	# mostrando tela...
	print(t)

	# testando função de limpar tela dos rabíscos.
	t.limpa()
	print(t)

	# marcando na tabela alguns símbolos, em 
	# algumas posições.
	t.marca(0,0,'I')
	t.marca(60,60,'J') # não será impresso(posição inválida).
	
	t.marca(3, 37,'X')
	t.marca(3, 38,'Y')
	t.marca(3, 39,'Z')
	
	t.marca(3, 27,'A')
	t.marca(4, 27,'b')
	t.marca(5, 27,'c')

	t.marca(1,1)
	t.marca(2,2)
	t.marca(3,4)
	print(t)

	# escrevendo na tela algumas strings.
	t.escreve(15, 17, 'string 1')
	t.escreve(23, 45, 'string 2')
	t.escreve(7, 10, "string 3")
	print(t)
	
	# lista strings na tela de forma manual...
	t.escreve(23, 6, "isso é a 1º string.")
	t.escreve(24,6, "esta é a segunda.")
	t.escreve(25,6, "aqui está a terceira...")
	t.escreve(26, 6, "colocamos aqui uma quarta:[]")
	print(t)

	# função que lista todas strings, filtras as 
	# não cábiveis.
	t.lista_strings(5, 49, 'primeiro non-sense.', 'segundo non-sense.', 'terceiro nonsense.')
	print(t)

	t.imprime()

	# testando transbordamento, tanto vertical
	# como horizontal.
	#t.lista_strings(26, 40, 'isso é uma string não tão gigante')
	#t.imprime()