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
