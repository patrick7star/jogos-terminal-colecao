# Cobrinha
Programa escrito em Rust, que usa o `ncurses` com ambiente gráfico, no jogo da cobrinha.
Funciona tanto com as setas, como o teclado númerico desligado(também setas). Já tem partidas
anteriores registradas, e as realizadas, mesmo que no modo **debug** serão também registradas
para futuramente se possa visualizar a partida.
#### Partida da cobrinha
![partida simples](https://github.com/patrick7star/jogos-terminal-colecao/blob/main/data/jogo-da-cobrinha-demonstração-i.png)
#### o resultado dela após o termino.
![resultado da partida acima](https://github.com/patrick7star/jogos-terminal-colecao/blob/main/data/jogo-da-cobrinha-resultado-i.png)

# Forca
## descrição dos elementos do jogo-da-forca

<!-- adicionando versões compátiveis. -->
<h3> versões:&nbsp &nbsp
<a href="https://github.com/TheAlgorithms/">
    <img src="https://img.shields.io/pypi/pyversions/tomlkit.svg?logo=python&logoColor=white" height="15">
</a>
</h3>

Um jogo da forca simples feito em Python, com a biblioteca "semigráfica": `ncurses`. O jogo é bem intuitívo quando inicializado, têm: dois campos(um para letras de acerto, outro para erros); a forca e o bonequinho que vai aparecendo; também o campo da pontuação, que basicamente conta as letras acertas e erradas; e o campo de dica com o tema da palavra perguntada. Ao ganhar ou perder, aparece um campo com algumas informações básicas da partida jogada, sabe, o tempo de duração as teclas apertadas na sequência,... se venceu ou não a partida, a verdadeira palavra que estava se buscando e etc.

## registros das partidas
Todas as partidas realizadas são registradas, com todos dados de final de partida mencionados acima. Um disparo da tela para ver como ficou o "tabuleiro" final, independente do resultado, é também gravado no "banco de dados". Para acessar-lô, visualizar todas suas jogadas, então digite o setup(no caso **forca.py**) do programa a  executar, e o argumento ***últimas_partidas_feitas***, ficaria assim no bash: 
  - `./forca.py últimas_partidas_feitas`

## sobre as palavras-chaves
O jogo pega e gera as palavras-chaves que são usadas no jogo dos arquivos no diretório `/data/palavras`. Lá existem vários arquivos, com nomes que são as dicas do jogo, dentro deles estão listadas todas palavras-chaves do jogo. Daí fica fácil presumir que para adicionar novas palavras, é só abrir tais arquivos e adicionar novas palavras, uma por linha, e de preferência de acordo com o tema(nome do arquivo). O mesmo vale para uma nova classe de palavras, porém neste caso ao ínvés de abrir um arquivo existente, você criaria um novo com as palavras relacionadas - lembrando novamente, uma em cada linha - no subdiretório `palavras`, o programa pegária cada _dica(arquivo)_ e suas palavras relacionads em tempo de execução, assim "ampliando o vocábulario" do programa.

# Jogo da Velha '#'
Jogo da velha, usando uma "interface gráfica" do terminal(ncurses), funciona quase inteiramente via mouse, porém futuramente também funcionará via teclado


### imagem de uma partida.
![partida simples](https://github.com/patrick7star/estritamente-para-transferencia/blob/main/velha-partida.png)
#### o resultado dela após o termino.
![resultado da partida acima](https://github.com/patrick7star/estritamente-para-transferencia/blob/main/velha-partida-resultado.png)


# Bate-Bola
Um joguinho simples, ou pelo menos sua casca com toda iteração sobre o `ncurses`. O jogo é algo como há uma `barra` flutuante, que fica de um lado para o outro, de modo udimensional, já a `bola`(esta não udimensional) fica batendo por tantos cantos da tela, e sendo refletida, ela não respeita alguma gravidade ou perda de energética; e ela também interage e reflete com a barra. A regra é: bateu 3 vezes no "chão", abaixo da barra relativo ao observador que comanda, o jogo terminal. A informação com dados de todas partidas é mostrado na tela, e guardada em disco para futuros acessos e processamento de dados.

## Especifícações
Foi no Linux, porém isso não possíbilita que funcione em qualquer outro sistema, pois o núcleo não usa nada muito além da biblioteca padrão do Rust. Talvez as bibliotecas-externas tenha alguma restrição, apesar de serem muitos relevantes. A tela trabalha com uma dimensão de caractéres na faixa dos 16-bits, algo maior talvez tenha algum problema. Isto está sendo dito, pois a tela do jogo onde os dois principais objetos locomovem-se, expande-se com a tela do 'temrinal'.
