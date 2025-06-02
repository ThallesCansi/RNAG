import random


def funcao_objetivo_cb(candidato: list) -> int:
    """
    Computa a função objetivo no problema das caixas binárias.

    Args:
      `candidato` (`list`): lista contendo os valores de cada caixa.

    Returns:
      `int`: soma dos valores das caixas, que representa o valor total do candidato.

    Examples:

    ```python
        >>> candidato = [1, 0, 1, 1]
        >>> funcao_objetivo_cb(candidato)
        3
    ```
    """
    return sum(candidato)


def gene_cb() -> int:
    """
    Sorteia um valor para uma caixa no problema das caixas binárias.

    Args:
      Nenhum argumento é necessário.

    Returns:
      `int`: valor sorteado, que pode ser 0 ou 1.

    Examples:
    ```python
        >>> gene_cb()
        1
        >>> gene_cb()
        0
    ```
    """
    valores_possiveis = [0, 1]
    gene = random.choice(valores_possiveis)
    return gene


def cria_candidato_cb(n: int) -> list:
    """
    Cria uma lista com n valores zero ou um.

    Args:
      `n` (`int`): inteiro que representa o número de caixas.

    Returns:
      `list`: lista contendo n valores sorteados, que podem ser 0 ou 1.

    Examples:
    ```python
        >>> cria_candidato_cb(4)
        [1, 0, 1, 1]
        >>> cria_candidato_cb(3)
        [0, 1, 0]
    ```
    """
    candidato = []
    for _ in range(n):
        gene = gene_cb()
        candidato.append(gene)
    return candidato


def populacao_cb(tamanho: int, n: int) -> list:
    """
    Cria uma população para o problema das caixas binárias.

    Args:
      `tamanho` (`int`): tamanho da população
      `n` (`int`): inteiro que representa o número de caixas de cada indivíduo.

    Returns:
      `list`: lista contendo `tamanho` indivíduos, cada um com `n` valores sorteados.

    Examples:
    ```python
        >>> populacao_cb(3, 4)
        [[1, 0, 1, 1], [0, 1, 0, 0], [1, 1, 0, 1]]
        >>> populacao_cb(2, 5)
        [[0, 1, 1, 0, 1], [1, 0, 0, 1, 0]]
    """
    populacao = []
    for _ in range(tamanho):
        populacao.append(cria_candidato_cb(n))
    return populacao


def funcao_objetivo_pop_cb(populacao: list) -> list:
    """
    Computa a função objetivo para uma população no problema das caixas binárias.

    Args:
      `populacao` (`list`): lista contendo os individuos do problema

    Returns:
      `list`: lista contendo os valores computados da função objetivo para cada indivíduo.

    Examples:
    ```python
        >>> populacao = [[1, 0, 1, 1], [0, 1, 0, 0], [1, 1, 0, 1]]
        >>> funcao_objetivo_pop_cb(populacao)
        [3, 1, 3]
    ```
    """
    fitness = []
    for individuo in populacao:
        fitness.append(funcao_objetivo_cb(individuo))
    return fitness


def selecao_roleta_max(populacao: list, fitness: list) -> list:
    """
    Realiza seleção da população pela roleta.

    Args:
      `populacao` (`list`): lista contendo os individuos do problema
      `fitness` (`list`): lista contendo os valores computados da funcao objetivo

    Returns:
      `list`: lista contendo os indivíduos selecionados.

    Examples:
    ```python
        >>> populacao = [[1, 0, 1, 1], [0, 1, 0, 0], [1, 1, 0, 1]]
        >>> fitness = [3, 1, 3]
        >>> selecao_roleta_max(populacao, fitness)
        [[1, 0, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1]]
    ```
    """
    selecionados = random.choices(populacao, fitness, k=len(populacao))
    return selecionados


def cruzamento_ponto_simples(
    pai: list, mae: list, chance_de_cruzamento: float
) -> tuple:
    """
    Realiza cruzamento de ponto simples.

    Args:
      `pai` (`list`): lista contendo os valores do pai
      `mae` (`list`): lista contendo os valores da mãe
      `chance_de_cruzamento` (`float`): float entre 0 e 1 representando a chance de cruzamento

    Returns:
      `tuple`: tupla contendo os filhos gerados pelo cruzamento ou os pais se não ocorrer cruzamento.

    Examples:
    ```python
        >>> pai = [1, 0, 1, 1]
        >>> mae = [0, 1, 0, 0]
        >>> cruzamento_ponto_simples(pai, mae, 0.5)
        ([1, 0, 0, 0], [0, 1, 1, 1])
    ```
    """
    if random.random() < chance_de_cruzamento:
        corte = random.randint(1, len(mae) - 1)
        filho1 = pai[:corte] + mae[corte:]
        filho2 = mae[:corte] + pai[corte:]
        return filho1, filho2
    else:
        return pai, mae


def mutacao_simples_cb(populacao: list, chance_de_mutacao: float) -> None:
    """
    Realiza mutação simples no problema das caixas binárias

    Args:
      `populacao` (`list`): lista contendo os individuos do problema
      `chance_de_mutacao` (`float`): float entre 0 e 1 representando a chance de mutação

    Returns:
      `None`: a função modifica a população diretamente, não retorna nada.

    Examples:
    ```python
        >>> populacao = [[1, 0, 1, 1], [0, 1, 0, 0], [1, 1, 0, 1]]
        >>> mutacao_simples_cb(populacao, 0.1)
        >>> populacao
        [[1, 0, 1, 1], [0, 1, 0, 0], [1, 1, 0, 0]]
    ```
    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            individuo[gene] = 0 if individuo[gene] == 1 else 1
