import random
import numpy as np


def massa() -> np.ndarray:
    """
    Gera uma massa aleatória para 3 elementos, totalizando entre 10 e 90 kg. A distribuição é feita de forma que cada elemento tenha uma massa entre 5 e 30 kg. A somas das massas é arredondada para duas casas decimais. A distribuição é feita usando a função Dirichlet para garantir que as massas somem 85 kg, e depois adiciona 5 kg a cada elemento.

    Args:
        `None`: Não recebe argumentos.

    Returns:
        `np.ndarray`: Um array de 3 elementos com massas aleatórias entre 5 e 35 kg, totalizando 90 kg.
    """
    parts = np.random.dirichlet([1, 1, 1]) * 85
    return np.round(parts + 5, 2)


def criar_individuo(elementos: tuple) -> tuple:
    """
    Cria um indivíduo aleatório com 3 elementos distintos e suas respectivas massas.

    Args:
        `elementos` (`tuple`): Uma tupla contendo os elementos disponíveis.

    Returns:
        `tuple`: Uma tupla contendo os elementos escolhidos e suas massas correspondentes.
    """
    elems = tuple(random.sample(elementos, 3))
    masses = massa()
    return elems, masses


def populacao_inicial(elementos: tuple, size: int = 200) -> list:
    """
    Gera uma população inicial de indivíduos aleatórios.

    Args:
        `elementos` (`tuple`): Uma tupla contendo os elementos disponíveis.
        `size` (`int`, opcional): O tamanho da população a ser gerada. Padrão é 200.

    Returns:
        `list`: Uma lista de indivíduos, onde cada indivíduo é uma tupla contendo os elementos e suas massas.
    """
    return [criar_individuo(elementos) for _ in range(size)]


def fitness(indiv: tuple, preco: dict) -> float:
    """
    Calcula o fitness de um indivíduo com base nos preços dos elementos e suas massas.

    Args:
        `indiv` (`tuple`): Um indivíduo, que é uma tupla contendo os elementos e suas massas.
        `preco` (`dict`): Um dicionário onde as chaves são os elementos e os valores são os preços por kg.

    Returns:
        `float`: O valor total do indivíduo, calculado como a soma dos preços dos elementos multiplicados por suas respectivas massas.
    """
    elems, masses = indiv
    kg = masses / 1000
    return sum(preco[e] * m for e, m in zip(elems, kg))


def torneio(pop: list, k: int = 3, fitness=fitness) -> tuple:
    """
    Realiza um torneio entre k indivíduos da população e retorna o melhor segundo a função de fitness.

    Args:
        `pop` (`list`): A população de indivíduos.
        `k` (`int`, opcional): Número de indivíduos no torneio. Padrão é 3.
        `fitness` (opcional): Função de avaliação de fitness.

    Returns:
        `tuple`: O indivíduo vencedor do torneio.
    """
    cand = random.sample(pop, k)
    return max(cand, key=fitness)


def crossover(p1: tuple, p2: tuple) -> tuple:
    """
    Realiza o crossover entre dois indivíduos, trocando um elemento aleatório entre eles.

    Args:
        `p1` (`tuple`): O primeiro indivíduo, que é uma tupla contendo os elementos e suas massas.
        `p2` (`tuple`): O segundo indivíduo, que é uma tupla contendo os elementos e suas massas.

    Returns:
        `tuple`: Dois novos indivíduos resultantes do crossover, onde um elemento foi trocado entre eles.
    """
    elems1, m1 = list(p1[0]), p1[1].copy()
    elems2, m2 = list(p2[0]), p2[1].copy()

    idx = random.randrange(3)
    elems1[idx], elems2[idx] = elems2[idx], elems1[idx]

    if len(set(elems1)) < 3 or len(set(elems2)) < 3:
        return p1, p2

    return (tuple(elems1), m1), (tuple(elems2), m2)


def mutacao(
    indiv: tuple,
    elementos: tuple,
    p_elem: float = 0.2,
    p_mass: float = 0.4,
) -> tuple:
    """
    Realiza mutações em um indivíduo, alterando um elemento ou redistribuindo a massa entre os elementos.

    Args:
        `indiv` (`tuple`): O indivíduo a ser mutado, que é uma tupla contendo os elementos e suas massas.
        `elementos` (`tuple`): Uma tupla contendo os elementos disponíveis.
        `p_elem` (`float`, opcional): Probabilidade de alterar um elemento. Padrão é 0.2.
        `p_mass` (`float`, opcional): Probabilidade de redistribuir a massa entre os elementos. Padrão é 0.4.

    Returns:
        `tuple`: O indivíduo mutado, que é uma tupla contendo os elementos e suas massas.
    """
    elems, masses = list(indiv[0]), indiv[1].copy()

    if random.random() < p_elem:
        pos = random.randrange(3)
        new_elem = random.choice([e for e in elementos if e not in elems])
        elems[pos] = new_elem

    if random.random() < p_mass:
        donor, receiver = random.sample(range(3), 2)
        delta = min(10, masses[donor] - 5)
        delta *= random.random()
        masses[donor] -= delta
        masses[receiver] += delta

    return (tuple(elems), np.round(masses, 2))
