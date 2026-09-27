'''
    Aqui o programa conterá uma função que permite
listar tanto diretórios, como arquivos na forma de
árvores, ou seja, seus ramos terão linhas, e também,
espaçamentos mostrando a profundidade de cada diretório
dado uma pasta raíz.
'''
#só pode ser importado:
__all__ = ['arvore']

# ********* bibliotecas **********
from os import listdir, chdir, system
from random import randint
import string
from sys import platform
# ************* dados ***********
'''
desabilitando, pois gera "saída" indesejada 
no código não relevante. Isto é uma copia 
para está biblioteca, funções aqui não são 
todas úteis para o código que a ascrecentou 
na biblioteca.

# conforme a plataforma em execução.
buffer = 'temporario.txt'
if platform == 'win32': 
  # no caso do windows.
  caminho = 'C:\\Users\\SAVIO\\AppData\\Local\\Temp'
  arqBuffer = caminho+'\\'+buffer
elif platform == 'linux': 
  # no caso de linux.
  caminho = '/tmp'
  arqBuffer = caminho+'/'+buffer

#criando arquivo... não existente inicialmente.
try:
  arq = open(arqBuffer, mode='x')
except FileExistsError:
  print('o arquivo "%s" já existe, então apenas continuando...'%arqBuffer)

'''

# ************ funções ****************

# gera uma árvore, imprimindo cada diretório, com
# determinado recuo no arquivo, para simular uma
# falsa hierárquia.
def trilha_dirs(caminho):
    #lista dos diretórios desta raíz.
    dirs = []
    #print(listdir(path=caminho))
    for pasta in listdir(path = caminho):
        #tenta acessar diretório, caso não
        #seja possível, de modo nenhum, a
        #conclusão é que não é um diretório.
        try:
            if platform == 'win32':
              listdir(caminho+'\\'+pasta)
            elif platform == 'linux':
              listdir(caminho+'/'+pasta)
            dirs.append(pasta)
        except: pass
            #print('"%s" não é um diretório, nem um vázio.' %pasta)
    #delimitando o recuo de espaços.
    espacos = 2
    #0x20 espaço vázio em hexadecimal.
    recuo = (chr(0x20) * espacos) * trilha_dirs.profundidade
    #listando pasta em ramos.
    for d in dirs:
        #limite de profundidade. Definida em 8.
        if trilha_dirs.profundidade > 8: 
          trilha_dirs.profundidade = 0
          continue
        #se houver subdiretórios, voltar a fazer
        #tudo baseado em recursão.
        if platform == 'win32':
          novo_caminho = caminho + '\\' + d
        elif platform == 'linux':
          novo_caminho = caminho + '/' + d
        #texto limitado.
        texto_limitado = '%s|__ "%s [...]"' % (recuo, d[0:20])
        #texto não limitado.
        texto = '%s|__ "%s"' % (recuo, d)
        if len(listdir(novo_caminho)) > 0:
            if len(d) > 20: print(texto_limitado,file=open(arqBuffer,'a'))
            else: print(texto,file=open(arqBuffer,'a'))
            #um espaço à frente para cada profundidade.
            trilha_dirs.profundidade += 1
            trilha_dirs(novo_caminho)
        else:
            if len(d) > 20: print(texto_limitado, file=open(arqBuffer,'a'))
            else: print(texto,file=open(arqBuffer, 'a'))
            #volta par a formatção do primeiro diretório.
            #diminui o recuo para zero.
            trilha_dirs.profundidade = 0

#função gera string aleatórias de extensão "".tmp".
def gera_str_aleatoria(comprimento):
    x, Str = 1,''
    while x <= comprimento:
        opcoes = [string.ascii_uppercase, string.ascii_lowercase,
                    string.digits]
        escolha = opcoes[randint(0,len(opcoes)-1)]
        Str += escolha[randint(0,len(escolha)-1)]
        x+=1
    return 'temporario_' + Str + '.tmp'

# função retorna uma a string com todo o diretório
# até uma certa profundidade, listado como àrvore.
def arvore(caminho, mostra_arquivos=False):
    #caso a opção visualizar arquivos esteja
    #disabilitada, que é o padrão.
    if not mostra_arquivos:
      #armazenando raíz também no arquivo temporário.
      print(caminho,file=open(arqBuffer,'a'))
      #definindo profundidade em um, já
      #que o caminho(raíz) é zero.
      trilha_dirs.profundidade = 1
      #executando procedimento, e criando
      #árvores de caminhos.
      trilha_dirs(caminho)
      #filtrando conteúdo do arquivo.
      conteudo = open(arqBuffer, 'r').read()
      # deletando linha em branco.
      conteudo = conteudo.split('\n')
      conteudo.pop(-1)
      conteudo = '\n'.join(conteudo[0:])
      #novo nome para arquivo temporário para
      #que não atrapalhe na execução de um
      #próximo.
      if platform == 'win32':
        nome_antigo = arqBuffer.split('\\')[-1]
      elif platform == 'linux':
        nome_antigo = arqBuffer.split('/')[-1]
      novo_nome = gera_str_aleatoria(21)
      #print(nome_antigo, ' ==> ', novo_nome)
      if platform == 'win32':
        system('ren %s %s' % (arqBuffer, novo_nome))
      elif platform == 'linux':
        system('mv %s /tmp/%s' % (arqBuffer, novo_nome))
      #retornando string com árvore impressa.
      return ' ᐅ ' + conteudo

# transforma string numa matriz, de acordo com 
# a formatação dela.
def matriciar_str(_str):
   # todas as linhas.
   linhas = _str.split('\n')
   # linha com maior caractéres.
   n = max(len(s) for s in linhas)
   # Criando matriz. O resto, por uniformização
   # será preenchido os espaços em brancos da 
   # strings que não completam a matriz, com 
   # trêmulas.
   matriz = [list(s + '¨' * (n-len(s))) for s in linhas]
   # preenchendo também os resto dos espaços em
   # brancos.
   for i in range(len(matriz)):
      for j in range(len(matriz[0])):
         if matriz[i][j].isspace():
            matriz[i][j] = '¨'
   return matriz

# imprime matriz, para uma boa visualização do que ocorre.
def imprime_matriz(matriz):
   print("mostrando com está indo a matriz:")
   m, n = len(matriz), len(matriz[1])
   for i in range(m): 
      for j in range(n):
         print(matriz[i][j],end='')
      print('')
   print('\t\t---- ---- FIM --- ----')

# está função conserta os demais galhos.
def conserta(_str):
   matriz = matriciar_str(_str)
   # dimensões da matriz.
   (m,n) = len(matriz), len(matriz[0])
   # marcando colunas contendo mais de três
   # barras verticais.
   mais = {j:0 for j in range(n)}
   for j in range(n):
      for i in range(m):
         if matriz[i][j] == '|':
            mais[j] += 1

   for coluna in mais.keys():
      def posicao_valida(i, j):
         palavra_ij = 0
         for j in range(n):
            if matriz[i][j].isascii():
               palavra_ij = j
      if mais[coluna] >= 2:
         for i in range(m):
            if matriz[i][coluna] == '¨':
               matriz[i][coluna] = '|'
   # processo de limpeza do código.
   for i in range(m):
      for j in range(n):
         if matriz[i][j] == '¨':
            matriz[i][j] = ' '
   return matriz 

# execução:   
if __name__ == '__main__':
    #print(gera_str_aleatoria(15))
    caminho = "/home/savio/Documents"
    str_arv = arvore(caminho)
    print(str_arv)
    imprime_matriz(matriciar_str(str_arv))
    
    imprime_matriz(conserta(str_arv))
    imprime_matriz(conserta(arvore('/etc')))
    #print(arvore('/etc'))