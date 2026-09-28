"""
   A antiga base de códigos do 'bate-bola' tem testes integrados. Como mexi com
 todo o código, eles atrapalham a execução dos códigos unitários feitos 
 recentemente. Acho que o Rust, pelo menos do que conheço até o momento, não
 permite executar ambos quando alguma está incompleto. Então surge este script
 que apenas muda o nome do diretório 'tests', assim meio que desabilita os 
 códigos dos testes integrados. E não, não pretendo apenas excluir em todo este
 processo de refatoração.
   Tal script funciona da seguinte maneira. Se o diretório estiver normal ao
 ser iniciado, será renomeado com o sufixo 'off' de desativado. Se ele for 
 executado quando já está com tal sufixo, então ele retira-o, ativando os 
 testes novamente.
"""
from pathlib import (Path)


diretorio = Path("tests")
outro_diretorio = Path("tests-off")

if diretorio.exists():
   print(
      "O diretório 'tests' existe, portanto os testes intregrais estão " +
      "habilitados."
   )
   diretorio.rename("tests-off")
   print("Os testes integrais foram desabilitados.")

else:
   if outro_diretorio.exists():
      print(
         "O diretório 'tests' não existe, logo, os testes intregrais estão " +
         "deshabilitados."
      )
      outro_diretorio.rename("tests")
      print("Os testes integrais foram habilitados novamente.")
   else:
      print("Não existe nenhum teste integral neste projeto Rust!")
      exit(1)
