import numpy as np
import random


def gene_palin(valores_possiveis: list) -> str:
    """
    Gera um gene aleatório para o problema dos palíndromos. Um gene é uma letra do alfabeto.

    Args:
        `valores_possiveis` (`list`): lista contendo os valores possíveis para o gene, que são as letras do alfabeto em minúsculas.

    Returns:
        `str`: Um gene aleatório, que é uma letra do alfabeto em minúsculas.

    Examples:
    ```python
        >>> gene_palin()
        'a'
    ```
    """
    gene = random.choice(valores_possiveis)

    return gene


def cria_candidato_palin(n: int, valores_possiveis: list) -> list:
    """
    Cria um candidato para o problema dos palíndromos.

    Args:
        `n` (`int`): inteiro que representa o número de letras do candidato.
        `valores_possiveis` (`list`): lista contendo os valores possíveis para o gene, que são as letras do alfabeto em minúsculas.

    Returns:
        `list`: Uma lista representando um candidato, que é uma sequência de letras.

    Examples:
    ```python
        >>> cria_candidato_palin(5)
        ['a', 'b', 'c', 'b', 'a']
    ```
    """

    candidato = []
    for _ in range(n):
        gene = gene_palin(valores_possiveis)
        candidato.append(gene)

    return candidato


def populacao_palin(tamanho: int, n: int, valores_possiveis: list) -> list:
    """
    Cria uma população para o problema dos palíndromos.

    Args:
        `tamanho` (`int`): inteiro que representa o tamanho da população.
        `n` (`int`): inteiro que representa o número de letras de cada indivíduo.

    Returns:
        `list`: Uma lista contendo indivíduos, onde cada indivíduo é uma lista de letras.

    Examples:
    ```python
        >>> populacao_palin(3, 5)
        [['a', 'b', 'c', 'b', 'a'], ['d', 'e', 'f', 'e', 'd'], ['g', 'h', 'i', 'h', 'g']]
    ```
    """
    populacao = []
    for _ in range(tamanho):
        individuo = cria_candidato_palin(n, valores_possiveis)
        populacao.append(individuo)

    return populacao


def funcao_objetivo_palin(individuo: list) -> int:
    """
    Computa a função objetivo para um indivíduo no problema dos palíndromos.

    Args:
        `individuo` (`list`): lista representando um indivíduo do problema, onde cada elemento é uma letra.

    Returns:
        `int`: Um valor inteiro representando o fitness do indivíduo, que é a quantidade de letras que formam um palíndromo.

    Examples:
    ```python
        >>> funcao_objetivo_palin(['a', 'b', 'c', 'b', 'a'])
        2
        >>> funcao_objetivo_palin(['a', 'b', 'c', 'd', 'e'])
        0
    ```
    """
    n = len(individuo)
    fitness = 0

    for i in range(n // 2):
        if individuo[i] == individuo[n - 1 - i]:
            fitness += 1

    if not any(c in individuo for c in "aeiou"):
        fitness -= 1

    if fitness < 0:
        fitness = 0

    return fitness


def funcao_objetivo_pop_palin(populacao: list) -> list:
    """
    Computa a função objetivo para uma população no problema dos palíndromos.

    Args:
        `populacao` (`list`): lista contendo os indivíduos do problema, onde cada indivíduo é uma lista de letras.

    Returns:
        `list`: Uma lista contendo os valores de fitness de cada indivíduo na população.

    Examples:
    ```python
        >>> populacao = [['a', 'b', 'c', 'b', 'a'], ['d', 'e', 'f', 'e', 'd']]
        >>> funcao_objetivo_pop_palin(populacao)
        [2, 2]
    ```
    """
    fitness = []
    for individuo in populacao:
        fit = funcao_objetivo_palin(individuo)
        fitness.append(fit)

    return fitness


def selecao_roleta_max(populacao: list, fitness: list) -> list:
    """
    Realiza seleção da população pela roleta

    Args:
        `populacao` (`list`): lista contendo os indivíduos do problema, onde cada indivíduo é uma lista de letras.
        `fitness` (`list`): lista contendo os valores de fitness de cada indivíduo na população.

    Returns:
        `list`: Um indivíduo selecionado da população com base na roleta.

    Examples:
    ```python
        >>> populacao = [['a', 'b', 'c', 'b', 'a'], ['d', 'e', 'f', 'e', 'd']]
        >>> fitness = [2, 2]
        >>> selecao_roleta_max(populacao, fitness)
        ['a', 'b', 'c', 'b', 'a']
    ```
    """
    total_fitness = sum(fitness)
    if total_fitness == 0:
        return random.choice(populacao)

    probabilidade = [f / total_fitness for f in fitness]

    roleta = np.random.choice(len(populacao), p=probabilidade)
    roleta = populacao[roleta]

    return roleta


def cruzamento_palin(pai1: list, pai2: list, taxa_crossover=0.7) -> list:
    """
    Realiza o cruzamento entre dois indivíduos do problema dos palíndromos.

    Args:
        `pai1` (`list`): primeiro pai, uma lista representando um indivíduo do problema.
        `pai2` (`list`): segundo pai, uma lista representando um indivíduo do problema.
        `taxa_crossover` (`float`): probabilidade de cruzamento entre os pais.

    Returns:
        `list`: Um filho resultante do cruzamento entre os dois pais.

    Examples:
    ```python
        >>> pai1 = ['a', 'b', 'c', 'b', 'a']
        >>> pai2 = ['d', 'e', 'f', 'e', 'd']
        >>> cruzamento_palin(pai1, pai2)
        ['a', 'b', 'f', 'e', 'd']
    ```
    """
    if random.random() < taxa_crossover:
        n = len(pai1)
        ponto_corte = random.randint(0, n - 1)

        filho = pai1[:ponto_corte] + pai2[ponto_corte:]
    else:
        filho = pai1.copy()

    return filho


def mutacao_palin(
    individuo: list,
    valores_possiveis: list,
    taxa_mutacao: float = 0.1,
) -> list:
    """
    Realiza a mutação de um indivíduo do problema dos palíndromos.

    Args:
        `individuo` (`list`): lista representando um indivíduo do problema, onde cada elemento é uma letra.
        `valores_possiveis` (`list`): lista contendo os valores possíveis para o gene, que são as letras do alfabeto em minúsculas.
        `taxa_mutacao` (`float`): probabilidade de mutação de cada gene do indivíduo.

    Returns:
        `list`: Um indivíduo mutado, onde alguns genes podem ter sido alterados.

    Examples:
    ```python
        >>> individuo = ['a', 'b', 'c', 'b', 'a']
        >>> mutacao_palin(individuo, 0.1)
        ['a', 'b', 'd', 'b', 'a']
    ```

    """
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            individuo[i] = gene_palin(valores_possiveis)
            individuo[-i - 1] = individuo[i]

    return individuo    
