from package.categoria import Categoria

# --- 1. TESTES DE SUCESSO ---

def test_deve_criar_categoria_com_sucesso():
    categoria = Categoria("Azul", "Estudos")
    assert categoria.cor == "Azul", f"Esperado 'Azul', mas veio '{categoria.cor}'"
    assert categoria.tipo == "Estudos", f"Esperado 'Estudos', mas veio '{categoria.tipo}'"


def test_deve_limpar_espacos_em_branco_nas_pontas():
    categoria = Categoria("  Verde  ", "  Trabalho  ")
    assert categoria.cor == "Verde", "Não limpou os espaços da cor"
    assert categoria.tipo == "Trabalho", "Não limpou os espaços do tipo"


# --- 2. TESTES DE FALHA (Validação de Erros) ---

def test_deve_lancar_erro_se_a_cor_nao_for_string():
    try:
        Categoria(123, "Estudos")
        assert False, "Deveria ter lançado TypeError para cor numérica, mas passou direto."
    except TypeError:
        pass # Erro esperado aconteceu! Teste passou.


def test_deve_lancar_erro_se_o_tipo_nao_for_string():
    try:
        Categoria("Azul", True)
        assert False, "Deveria ter lançado TypeError para tipo booleano, mas passou direto."
    except TypeError:
        pass


def test_deve_lancar_erro_se_a_cor_estiver_vazia():
    try:
        Categoria("   ", "Estudos")
        assert False, "Deveria ter lançado TypeError para cor vazia, mas passou direto."
    except TypeError:
        pass


def test_deve_lancar_erro_se_o_tipo_estiver_vazio():
    try:
        Categoria("Azul", "")
        assert False, "Deveria ter lançado TypeError para tipo vazio, mas passou direto."
    except TypeError:
        pass


# --- EXECUTOR DOS TESTES ---

if __name__ == "__main__":
    print("Iniciando os testes da classe Categoria...\n")
    
    # Lista com todas as funções de teste
    lista_de_testes = [
        test_deve_criar_categoria_com_sucesso,
        test_deve_limpar_espacos_em_branco_nas_pontas,
        test_deve_lancar_erro_se_a_cor_nao_for_string,
        test_deve_lancar_erro_se_o_tipo_nao_for_string,
        test_deve_lancar_erro_se_a_cor_estiver_vazia,
        test_deve_lancar_erro_se_o_tipo_estiver_vazio
    ]
    
    sucessos = 0
    
    for teste in lista_de_testes:
        try:
            teste()
            print(f"✅ {teste.__name__}")
            sucessos += 1
        except AssertionError as erro:
            print(f"❌ {teste.__name__} FALHOU!")
            print(f"   Detalhe do erro: {erro}\n")
            
    print(f"\nResultado: {sucessos}/{len(lista_de_testes)} testes passaram com sucesso!")

