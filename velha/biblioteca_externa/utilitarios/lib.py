
"""
importa todos módulos atualmente importante
para aqui, então serão exportados. Os códigos
dados como "mortos", pois foram criados
otimizações, ou descontinuados não serão
exportados novamente. Muitos destes módulos
reescritos com otimizações, ganharão o nome
original, e como já dito, exportado.
"""

if __debug__:
   print("fonte de importação:",__name__)

if __name__ == "__main__":
   import src.barra_de_progresso as barra_de_progresso
   import src.espiral as espiral
   import src.legivel as legivel
   import src.romanos as romanos
   import src.silhueta as silhueta
   # sendo renomeada com a versão otimizada,
   # pelo menos até o momento.
   import src.tela_i as tela
   import src.arvore_ii as arvore
else:
   from .src import barra_de_progresso
   from .src import espiral
   from .src import legivel
   from .src import romanos
   from .src import silhueta
   # sendo renomeada com a versão otimizada,
   # pelo menos até o momento.
   from .src import tela_i
   from .src import arvore_ii
   # renomeando ...
   tela = tela_i
   arvore = arvore_ii

# ainda não terminado.
#import numeros_por_extenso

# não usado muito, então dado como
# descontinuado.
#import aritmetica

# re-exportando ...
__all__ = [
   "arvore",
   "barra_de_progresso",
   "espiral",
   "legivel",
   "romanos",
   "silhueta",
   "tela"
]
