import random


def gene_senha(letras_possiveis: list[str]) -> str:
    """
    Sorteia uma letra.

    Args:
        `letras_possiveis` (`list[str]`): Lista de letras possíveis de serem sorteadas.

    Returns:
        `str`: Uma letra sorteada aleatoriamente da lista de letras possíveis.

    Examples:
    ```python
        >>> letras_possiveis = ['a', 'b', 'c', 'd']
        >>> gene_senha(letras_possiveis)
        'b'
    ```
    """
    letra = random.choice(letras_possiveis)
    return letra


def cria_candidato_senha_var_len(
    caracteres_possiveis: list[str],
    min_len: int = 1,
    max_len: int = 30,
) -> list[str]:
    """
    Cria um candidato para o problema da senha com tamanho variável.

    Args:
        `caracteres_possiveis` (`list[str]`): Lista de caracteres possíveis de serem sorteados.
        `min_len` (`int`): Tamanho mínimo da senha de cada indivíduo.
        `max_len` (`int`): Tamanho máximo da senha de cada indivíduo.

    Returns:
        `list[str]`: Uma lista representando um candidato (senha) com tamanho variável.

    Examples:
    ```python
        >>> caracteres_possiveis = ['a', 'b', 'c', 'd']
        >>> cria_candidato_senha_var_len(caracteres_possiveis, 3, 5)
        ['a', 'b', 'c']
    ```
    """
    tamanho_senha = random.randint(min_len, max_len)
    candidato = []
    for _ in range(tamanho_senha):
        candidato.append(gene_senha(caracteres_possiveis))
    return candidato


def populacao_senha_var_len(
    tamanho_populacao: int,
    caracteres_possiveis: list[str],
    min_len: int = 1,
    max_len: int = 30,
) -> list[list[str]]:
    """
    Cria população inicial no problema da senha com tamanho variável.

    Args:
        `tamanho_populacao` (`int`): Tamanho da população a ser criada.
        `caracteres_possiveis` (`list[str]`): Lista de caracteres possíveis de serem sorteados.
        `min_len` (`int`): Tamanho mínimo da senha de cada indivíduo.
        `max_len` (`int`): Tamanho máximo da senha de cada indivíduo.

    Returns:
        `list[list[str]]`: Uma lista de listas, onde cada sublista representa um candidato (senha) com tamanho variável.

    Examples:
    ```python
        >>> tamanho_populacao = 5
        >>> caracteres_possiveis = ['a', 'b', 'c', 'd']
        >>> populacao_senha_var_len(tamanho_populacao, caracteres_possiveis, 3, 5)
        [['a', 'b', 'c'], ['d', 'a', 'b'], ['c', 'd'], ['b', 'c', 'a'], ['a']]
    ```
    """
    populacao = []
    for _ in range(tamanho_populacao):
        populacao.append(
            cria_candidato_senha_var_len(caracteres_possiveis, min_len, max_len)
        )
    return populacao


def funcao_objetivo_senha_var_len(
    candidato: list[str],
    senha_verdadeira: list[str],
    penalty_per_length_diff: int,
) -> int:
    """
    Computa a funcao objetivo de um candidato no problema da senha com tamanho variável. Quanto menor o valor, melhor o candidato.

    Args:
        `candidato` (`list[str]`): Candidato (senha) a ser avaliado.
        `senha_verdadeira` (`list[str]`): A senha que você está tentando descobrir.
        `penalty_per_length_diff` (`int`): Penalidade por cada unidade de diferença de tamanho entre o candidato e a senha verdadeira.

    Returns:
        `int`: Um valor inteiro representando a "distância" do candidato para a senha verdadeira. Quanto menor, melhor o candidato.

    Examples:
    ```python
        >>> candidato = ['a', 'b', 'c']
        >>> senha_verdadeira = ['a', 'b', 'd']
        >>> penalty_per_length_diff = 2
        >>> funcao_objetivo_senha_var_len(candidato, senha_verdadeira, penalty_per_length_diff)
        1
    ```
    """
    distancia_chars = 0
    len_candidato = len(candidato)
    len_verdadeira = len(senha_verdadeira)

    for i in range(min(len_candidato, len_verdadeira)):
        num_letra_candidato = ord(candidato[i])
        num_letra_senha = ord(senha_verdadeira[i])
        distancia_chars += abs(num_letra_candidato - num_letra_senha)

    diferenca_tamanho = abs(len_candidato - len_verdadeira)
    penalidade_tamanho = diferenca_tamanho * penalty_per_length_diff

    return distancia_chars + penalidade_tamanho


def funcao_objetivo_pop_senha_var_len(
    populacao: list[list[str]],
    senha_verdadeira: list[str],
    penalty_per_length_diff: int,
) -> list[int]:
    """
    Computa a funcao objetivo de uma populacao no problema da senha com tamanho variável.

    Args:
        `populacao` (`list[list[str]]`): Lista de candidatos (senhas) a serem avaliados.
        `senha_verdadeira` (`list[str]`): A senha que você está tentando descobrir.
        `penalty_per_length_diff` (`int`): Penalidade por cada unidade de diferença de tamanho entre o candidato e a senha verdadeira.

    Returns:
        `list[int]`: Uma lista de valores inteiros representando a "distância" de cada candidato para a senha verdadeira. Quanto menor, melhor o candidato.

    Examples:
    ```python
        >>> populacao = [['a', 'b', 'c'], ['d', 'a', 'b'], ['c', 'd']]
        >>> senha_verdadeira = ['a', 'b', 'd']
        >>> penalty_per_length_diff = 2
        >>> funcao_objetivo_pop_senha_var_len(populacao, senha_verdadeira, penalty_per_length_diff)
        [1, 3, 4]
    ```
    """
    fitness = []
    for individuo in populacao:
        fitness.append(
            funcao_objetivo_senha_var_len(
                individuo, senha_verdadeira, penalty_per_length_diff
            )
        )
    return fitness


def cruzamento_uniforme_var_len(
    pai: list[str],
    mae: list[str],
    chance_de_cruzamento: float,
    caracteres_possiveis: list[str],
    max_len: int = 30,
) -> tuple[list[str], list[str]]:
    """
    Realiza cruzamento uniforme para pais de tamanhos possivelmente diferentes. Os filhos podem ter tamanhos diferentes dos pais e entre si.

    Args:
        `pai` (`list[str]`): Lista representando o pai.
        `mae` (`list[str]`): Lista representando a mãe.
        `chance_de_cruzamento` (`float`): Probabilidade de ocorrer o cruzamento.
        `caracteres_possiveis` (`list[str]`): Lista de caracteres possíveis para os filhos.
        `max_len` (`int`): Tamanho máximo dos filhos.
    Returns:
        `tuple[list[str], list[str]]`: Dupla contendo as listas dos filhos resultantes do cruzamento.

    Examples:
    ```python
        >>> pai = ['a', 'b', 'c']
        >>> mae = ['d', 'e']
        >>> chance_de_cruzamento = 0.5
        >>> caracteres_possiveis = ['a', 'b', 'c', 'd', 'e']
        >>> cruzamento_uniforme_var_len(pai, mae, chance_de_cruzamento, caracteres_possiveis)
        (['a', 'e', 'c'], ['d', 'b'])
    ```
    """
    filho1_final, filho2_final = list(pai), list(mae)

    if random.random() < chance_de_cruzamento:
        filho1_genes = []
        filho2_genes = []
        len_pai = len(pai)
        len_mae = len(mae)
        max_loop_len = max(len_pai, len_mae)

        for i in range(max_loop_len):
            gene_pai = pai[i] if i < len_pai else None
            gene_mae = mae[i] if i < len_mae else None

            if gene_pai is not None and gene_mae is not None:
                if random.choice([True, False]):
                    filho1_genes.append(gene_pai)
                else:
                    filho1_genes.append(gene_mae)
            elif gene_pai is not None:
                if random.choice([True, False]):
                    filho1_genes.append(gene_pai)
            elif gene_mae is not None:
                if random.choice([True, False]):
                    filho1_genes.append(gene_mae)

            if gene_pai is not None and gene_mae is not None:
                if random.choice([True, False]):
                    filho2_genes.append(gene_pai)
                else:
                    filho2_genes.append(gene_mae)
            elif gene_pai is not None:
                if random.choice([True, False]):
                    filho2_genes.append(gene_pai)
            elif gene_mae is not None:
                if random.choice([True, False]):
                    filho2_genes.append(gene_mae)

        filho1_final = (
            filho1_genes if filho1_genes else [random.choice(caracteres_possiveis)]
        )
        if len(filho1_final) > max_len:
            filho1_final = filho1_final[:max_len]

        filho2_final = (
            filho2_genes if filho2_genes else [random.choice(caracteres_possiveis)]
        )
        if len(filho2_final) > max_len:
            filho2_final = filho2_final[:max_len]

        return filho1_final, filho2_final
    else:
        return filho1_final, filho2_final


def mutacao_simples_var_len(
    populacao: list[list[str]],
    chance_de_mutacao: float,
    valores_possiveis: list[str],
) -> None:
    """
    Realiza mutação simples em indivíduos de tamanho variável.

    Args:
        `populacao` (`list[list[str]]`): Lista de indivíduos (candidatos) a serem mutados.
        `chance_de_mutacao` (`float`): Probabilidade de um gene ser mutado.
        `valores_possiveis` (`list[str]`): Lista de valores possíveis para os genes.

    Returns:
        `None`: A função modifica a população diretamente, não retorna nada.

    Examples:
    ```python
        >>> populacao = [['a', 'b', 'c'], ['d', 'e']]
        >>> chance_de_mutacao = 0.1
        >>> valores_possiveis = ['a', 'b', 'c', 'd', 'e']
        >>> mutacao_simples_var_len(populacao, chance_de_mutacao, valores_possiveis)
    ```
    """
    for individuo in populacao:
        if not individuo:
            continue
        if random.random() < chance_de_mutacao:
            gene_idx = random.randint(0, len(individuo) - 1)
            valor_gene_atual = individuo[gene_idx]
            valores_sorteio = [
                val for val in valores_possiveis if val != valor_gene_atual
            ]
            if valores_sorteio:
                individuo[gene_idx] = random.choice(valores_sorteio)


def mutacao_salto_var_len(
    populacao: list[list[str]],
    chance_de_mutacao: float,
    valores_possiveis_lista: list[str],
) -> None:
    """
    Realiza mutação de salto em indivíduos de tamanho variável.

    Args:
        `populacao` (`list[list[str]]`): Lista de indivíduos (candidatos) a serem mutados.
        `chance_de_mutacao` (`float`): Probabilidade de um gene ser mutado.
        `valores_possiveis_lista` (`list[str]`): Lista de valores possíveis para os genes.

    Returns:
        `None`: A função modifica a população diretamente, não retorna nada.

    Examples:
    ```python
        >>> populacao = [['a', 'b', 'c'], ['d', 'e']]
        >>> chance_de_mutacao = 0.1
        >>> valores_possiveis_lista = ['a', 'b', 'c', 'd', 'e']
        >>> mutacao_salto_var_len(populacao, chance_de_mutacao, valores_possiveis_lista)
        >>> populacao
        [['a', 'b', 'd'], ['d', 'e']]
    ```
    """
    for individuo in populacao:
        if not individuo:
            continue
        if random.random() < chance_de_mutacao:
            gene_idx = random.randint(0, len(individuo) - 1)
            valor_gene_atual = individuo[gene_idx]
            try:
                indice_letra = valores_possiveis_lista.index(valor_gene_atual)
                indice_letra += random.choice([1, -1])
                indice_letra %= len(valores_possiveis_lista)  # Wrap around
                individuo[gene_idx] = valores_possiveis_lista[indice_letra]
            except ValueError:
                if valores_possiveis_lista:
                    individuo[gene_idx] = random.choice(valores_possiveis_lista)


def selecao_torneio_min(
    populacao: list[list[str]],
    fitness: list[int],
    tamanho_torneio: int,
) -> list[list[str]]:
    """
    Faz a seleção de uma população usando torneio.

    Args:
        `populacao` (`list`): Lista de indivíduos da população.
        `fitness` (`list`): Lista de valores de fitness correspondentes aos indivíduos.
        `tamanho_torneio` (`int`): Número de indivíduos a serem sorteados para cada torneio.

    Returns:
        `list`: Lista de indivíduos selecionados após o torneio.

    Examples:
    ```python
        >>> populacao = [['a', 'b'], ['c', 'd'], ['e', 'f']]
        >>> fitness = [2, 1, 3]
        >>> tamanho_torneio = 2
        >>> selecao_torneio_min(populacao, fitness, tamanho_torneio)
        [['c', 'd'], ['a', 'b']]
    ```
    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        min_fitness = min(fitness_sorteados)
        indice_min_fitness = fitness_sorteados.index(min_fitness)
        individuo_selecionado = sorteados[indice_min_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados


def mutacao_altera_tamanho(
    populacao: list[list[str]],
    chance_mutacao_tamanho: float,
    caracteres_possiveis: list[str],
    min_len: int = 1,
    max_len: int = 30,
) -> None:
    """
    Muda o tamanho de um indivíduo adicionando ou removendo um gene.

    Args:
        `populacao` (`list[list[str]]`): Lista de indivíduos (candidatos) a serem mutados.
        `chance_mutacao_tamanho` (`float`): Probabilidade de um indivíduo ter seu tamanho alterado.
        `caracteres_possiveis` (`list[str]`): Lista de caracteres possíveis para os genes.
        `min_len` (`int`): Tamanho mínimo permitido para cada indivíduo.
        `max_len` (`int`): Tamanho máximo permitido para cada indivíduo.

    Returns:
        `None`: A função modifica a população diretamente, não retorna nada.

    Examples:
    ```python
        >>> populacao = [['a', 'b'], ['c', 'd']]
        >>> chance_mutacao_tamanho = 0.1
        >>> caracteres_possiveis = ['a', 'b', 'c', 'd', 'e']
        >>> mutacao_altera_tamanho(populacao, chance_mutacao_tamanho, caracteres_possiveis, 1, 5)
        >>> populacao
        [['a', 'b', 'e'], ['c', 'd']]
    ```
    """
    for i in range(len(populacao)):
        individuo = populacao[i]
        if random.random() < chance_mutacao_tamanho:
            individuo_modificado = list(individuo)

            if not individuo_modificado and min_len > 0:
                num_genes_iniciais = random.randint(min_len, min(min_len + 2, max_len))
                individuo_modificado = [
                    random.choice(caracteres_possiveis)
                    for _ in range(num_genes_iniciais)
                ]
                populacao[i] = individuo_modificado
                continue

            acao = random.choice(["adicionar", "remover"])

            if acao == "adicionar" and len(individuo_modificado) < max_len:
                ponto_insercao = random.randint(0, len(individuo_modificado))
                novo_char = random.choice(caracteres_possiveis)
                individuo_modificado.insert(ponto_insercao, novo_char)
            elif acao == "remover" and len(individuo_modificado) > min_len:
                ponto_remocao = random.randint(0, len(individuo_modificado) - 1)
                individuo_modificado.pop(ponto_remocao)
                if not individuo_modificado and min_len > 0:
                    individuo_modificado.append(random.choice(caracteres_possiveis))

            populacao[i] = individuo_modificado
