#!/usr/bin/python3.8 -B 

"""
   Vamos refazer o jogo da forca, porém agora utilizando a bilioteca 
 curses, para melhor animação do jogo.
"""
# Minha biblioteca:
from lib import (motor, perfil, tabuleiro)
# Bibliotecas do Python:
import sys, pickle, os
from curses import (
   napms, window, start_color, initscr, init_pair, curs_set, noecho,
   use_default_colors, endwin
) 
from time import time

(LINHAS, COLUNAS) = tabuleiro.LINHAS, tabuleiro.COLUNAS


def mostra_partidas_aglomerado() -> None:
   "Mostra as partidas realizadas anteriormentes, ou uma parte dela."
   partidas=[]

   try:
      with open(perfil.arq_aglomerado, "rb") as arquivo:
         try:
            while True:  
               partidas.append(pickle.load(arquivo))
         except EOFError: ... 
         except io.UnsupportedOperation:
            print('o arquivo está vázio.')
            sys.exit()
         finally:
            # Déz últimas partidas feitas em ordem decrescente
            sublista = partidas[-1:-10:-1]; sublista.reverse()
            quantia = len(partidas)

            print('\nQuantia de partidas realizadas:%5i' % quantia)
            # Se houver mais de dez registros de partidas.
            if t:=len(partidas) > 10:
               # Exibindo quantas irão sair na saída do terminal.
               formatacao = ( 
                  "Mostrando partidas:" + 
                  ", ".join([
                     str(p.ordem) + 'º' 
                     for p in sublista
                  ])
               )
               print(formatacao, end='\n\n')
               # mostrar apenas dez, e os dez últimos feitos.
               for p in sublista: print(p)
            else:
               # caso contrário, mostrar tudo.
               for p in partidas: print(p)
   except FileNotFoundError:
      print('arquivo não existe.')

def instancia_e_configura_uma_janela() -> window:
   "Instancia e cria uma janela para o jogo."
   janela = initscr()

   # Configuração da janela. Desabilitando o 'eco', escodendo o cursor,
   # usando as cores de fundo do terminal.
   noecho() 
   curs_set(False) 
   start_color()
   use_default_colors()
   # Desenha uma tela na borda do jogo.
   janela.border(0,0,0,0,0,0,0,0)

   return janela

def execucao_do_jogo() -> None:
   # Mostrando o resultado do jogo.
   RESULTADOS_MSG = (
      'você venceu o jogo!', 
      'você perdeu o jogo!', 
      "jogo abandonado"
   )
   janela = instancia_e_configura_uma_janela() 
   # buscando palavra-chave do jogo.
   motor.palavra_chave = motor.palavra_aleatoria()
   # perfilando partida.
   p = perfil.Perfil(
      motor.acertos, motor.erros, 
      motor.palavra_chave, 
      motor.dica
   )
   p.marca_tempo()

	# roda o bloco enquanto o jogo não estiver finalizado.
   while (not motor.partida_finalizada()):
      # formando o tabuleiro.
      tabuleiro.desenha_forca(janela)
      tabuleiro.atualiza_tela(
         motor.acertos, motor.erros, 
         motor.palavra_chave, motor.dica, 
         janela
      )
      # entrada da "peça" jogada.
      p.marca_jogada() # começa a registrar a jogada.

		# colocando a opção de abandonar o jogo.
      try:
         jogada = chr(janela.getch())
      except KeyboardInterrupt:
         p.marca_tempo()
         tabuleiro.quadro_resultado(
            5, 29, RESULTADOS_MSG[2].upper(),
            'tempo decorrido:%2.2f' %p.tempo,
            'palavra correta: "%s".'% p.palavra_chave,
            'erros: %i cometidos'%len(p.erros),
            'dica do jogo: "%s"'%p.dica
         )
         beep() # emite um sinal ao acionar isto.
         janela.refresh() # atualiza para escrita na tela.
         napms(3000)
         del p # apaga dado desnecesário.
         sys.exit('saindo do jogo... feito.')

		# Faz uma jogada, e, registra se foi aceita. Falso se não, pois é 
      # inválida a entrada ou, a tecla já foi digitada. E, o caso contrário 
      # é o valor lógico verdadeiro.
      resultado = motor.joga(jogada)
		# Registra tempo da jogada.
      p.marca_jogada(peca=jogada)
		# Se for "True" então foi uma jogada acertada. Caso contrário, então 
      # foi um, erro, ou seja vamos marca-lo. Porém..., se a peça já foi 
      # registrada com errada, não marcar.
      if not resultado:
         tabuleiro.marca_forca(janela)
		# Última atualização de tela.
      tabuleiro.atualiza_tela(motor.acertos, motor.erros, 
            motor.palavra_chave, motor.dica, janela)
      # Termina a conometragem da partida.
      p.marca_tempo()
      # Marca o resultado.
      p.marca_resultado(motor.e_vitorioso())
      # Marca a tela do jogo.
      p.captura_tela = tabuleiro.captura_tela(janela)
      # Atualizando acertos e erros.
      p.acertos = motor.acertos
      p.erros = motor.erros

   # Armazenada info da partida.
   perfil.armazena(p)
   # Apagando tudo do tabuleiro, menos a estrutura da forca. A contagem de 
   # erros é para mostrar até onde o boneco foi.
   tabuleiro.limpa_tabuleiro(len(motor.erros), janela)

   if motor.e_vitorioso(): 
      # colocando reultado com informações importantes.
      tabuleiro.quadro_resultado(
         5, 29, RESULTADOS_MSG[0].upper(),
         'tempo decorrido: %0.2f seg' % p.tempo,
         'palavra correta: "%s".'% p.palavra_chave,
         'erros: %i cometidos'%len(p.erros),
         'dica do jogo: "%s"'%p.dica
      )
   else: 
      # Exibindo mensagem do resultado da partida. Info básica sobre o jogo:
      tabuleiro.quadro_resultado(
         5, 29, RESULTADOS_MSG[1].upper(),
         'tempo decorrido: %0.2f seg' % p.tempo,
         'palavra correta: "%s".'% p.palavra_chave,
         'acertos: %i realizados'%len(p.acertos),
         'dica do jogo: "%s"'%p.dica
      )

   # faz o backup do registro, independente da plataforma.
   perfil.faz_backup()
   # breve pausa para visualizar resultado.
   napms(7000)
   janela.refresh() # último impressão da tela.
   endwin() # encerra tela de jogo.

def menu_do_programa() -> None:
   if len(sys.argv) == 2 and sys.argv[1] == '--partidas-feitas':
      # Lista na saída do terminal as partidas realizadas conforme 
      # programada anteriormente.
      mostra_partidas_aglomerado()
      sys.exit('partidas realizadas acima.'.upper())

   elif len(sys.argv) == 2 and sys.argv[1] == '--comandos':
      TEXTO_DE_AJUDA = """
     --partidas-feitas\tMostra todas, ou pelo menos, as últimas 
                        partidas realizadas no jogo recentemente.\n
      --ajuda\t\tMostra essa tela de ajuda.
      \n"""
      print(TEXTO_DE_AJUDA)
      sys.exit('')

# == == == == == == == == == == == === == == == == == == == == == == == ===
#                          Execução do Programa
# == == == == == == == == == == == === == == == == == == == == == == == ===
if __name__ == '__main__':
	# execuntado pelo "wrapper" que defaz 
	# bagunça na tela após erros, e, ainda 
	# ativa automáticamente a coloração.
	#wrapper(executa)
	# visualização prévia da captura de tela futura.
	#print(_str)

   menu_do_programa()
   execucao_do_jogo()
