# algebralineartdd

Desenvolvimento de ferramentas para a disciplina de álgebra linear do mestrado em modelagem matemática computacional do CEFET-MG utilizando metodologia TDD.

## Visão geral da estrutura

A base de código está organizada em módulos Python separados por temas da disciplina e um conjunto de testes automatizados escritos com `pytest`.

```
algebralineartdd/
├── matriz/
├── polinomios/
├── produto_interno/
├── sistemas_lineares/
└── testes/
```

* `matriz/`: implementa a classe `MatrizBiDimensional`, responsável por operações matriciais (soma, subtração, multiplicação escalar e matricial), cálculo de determinante por cofatores ou permutações, transformação em forma escada linha reduzida e obtenção de matriz inversa. O módulo também define exceções específicas para inconsistências de dimensão, termos inválidos e matrizes singulares.【F:matriz/matriz.py†L1-L210】【F:matriz/exceptions.py†L1-L11】
* `polinomios/`: contém utilitários para avaliar polinômios matriciais, como a função `p_de_A`, que recebe os coeficientes do polinômio e uma matriz NumPy para produzir o resultado.【F:polinomios/polinomios.py†L1-L8】
* `produto_interno/`: reúne funções de álgebra linear relacionadas a produto interno, norma, ângulo entre vetores, projeções, ortogonalização e ortonormalização por Gram-Schmidt. As implementações utilizam funções auxiliares para tornar o funcional linear configurável, permitindo reutilização com produtos internos alternativos.【F:produto_interno/produto_interno.py†L1-L44】
* `sistemas_lineares/`: define a classe `SL`, que encapsula um sistema linear `Ax = b` baseado na classe de matriz própria. O módulo oferece validações, cálculo da matriz aumentada, resolução por forma escada ou regra de Cramer, além de detecção de sistemas insolúveis via comparação de postos.【F:sistemas_lineares/sistemas_lineares.py†L1-L86】【F:sistemas_lineares/exceptions.py†L1-L8】

## Testes automatizados

Os testes vivem em `testes/` e cobrem cada módulo principal com cenários positivos e negativos. Eles validam os comportamentos expostos, como operações matriciais, verificação de exceções, aplicação de produtos internos personalizados e resolução de sistemas lineares. Para executar todos os testes, utilize:

```bash
pip install -r requirements.txt
pytest
```

## Dicas para quem está começando

1. **Comece pela classe de matrizes**: ela é a base para sistemas lineares e outras operações. Analise como os métodos públicos se apoiam em utilitários privados para formar escada, calcular determinantes e montar inversas.【F:matriz/matriz.py†L39-L150】【F:matriz/matriz.py†L150-L209】
2. **Leia os testes primeiro**: eles demonstram exemplos concretos de uso e deixam claro o comportamento esperado, incluindo exceções e propriedades importantes.【F:testes/test_matriz_bidimensional.py†L1-L120】【F:testes/test_sistemas_lineares.py†L1-L120】
3. **Experimente no REPL**: após entender os testes, execute pequenos experimentos no Python interativo para reforçar o aprendizado, reutilizando os mesmos casos.
4. **Use o `funcional_linear` para expandir**: o módulo de produtos internos permite injetar outras definições de produto interno. Tente implementar um funcional diferente para compreender como as projeções e ortogonalizações se adaptam.【F:produto_interno/produto_interno.py†L10-L44】
5. **Pratique o ciclo TDD**: ao adicionar novos recursos, escreva primeiro um teste em `testes/`, implemente a funcionalidade correspondente e garanta que toda a suíte continua verde.

Essa organização modular e orientada a testes facilita a evolução incremental da base sem perder a confiança na corretude matemática das implementações.
