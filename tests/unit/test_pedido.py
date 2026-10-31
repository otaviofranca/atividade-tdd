import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido, contar_frete_gratis


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================

def test_bug1_subtotal_considera_quantidade(pedido_pequeno):
    # 6,00 x 1 + 4,50 x 2 = 15,00 (o código soma só os preços: 10,50)
    assert pedido_pequeno.subtotal() == 15.0


def test_bug2_frete_gratis_com_subtotal_exatamente_50():
    # Valor-limite: R$ 50,00 inclusive tem frete grátis (o código usa ">")
    pedido = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert pedido.tem_frete_gratis() is True


def test_bug3_item_mais_barato_retorna_o_menor_preco(pedido_pequeno):
    # Pão de queijo (4,50) é mais barato que o Café (6,00)
    assert pedido_pequeno.item_mais_barato().nome == "Pão de queijo"


def test_bug4_desconto_e_subtraido_do_subtotal():
    # R$ 100,00 com 10% de desconto = 90,00 (o código soma: 110,00)
    pedido = Pedido("Carla", [Item("Combo", 100.0, 1)])
    assert pedido.total_com_desconto(10) == 90.0



# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função

def test_contar_frete_gratis_todos_com_frete_gratis(pedido_grande):
    # Ambos os pedidos têm subtotal >= 50: 73,00 e 50,00
    outro = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert contar_frete_gratis([pedido_grande, outro]) == 2


def test_contar_frete_gratis_nenhum_com_frete_gratis(pedido_pequeno):
    # 15,00 e 49,99: ambos abaixo de 50
    outro = Pedido("Carla", [Item("Lanche", 49.99, 1)])
    assert contar_frete_gratis([pedido_pequeno, outro]) == 0


def test_contar_frete_gratis_lista_mista(pedido_pequeno, pedido_grande):
    # 15,00 (não) + 73,00 (sim) + 50,00 (sim) = 2 pedidos com frete grátis
    limite = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert contar_frete_gratis([pedido_pequeno, pedido_grande, limite]) == 2


def test_contar_frete_gratis_lista_vazia():
    assert contar_frete_gratis([]) == 0



# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método

def test_situacao_cancelado_quando_mais_de_25_por_cento_indisponivel():
    # 4 unidades x 25,00 = 100,00 (frete grátis), mas 2 de 4 (50%) sem estoque
    pedido = Pedido("Carla", [Item("Combo", 25.0, 4)])
    assert pedido.situacao(2) == "Cancelado por falta de estoque"


def test_situacao_confirmado_com_frete_gratis(pedido_grande):
    # Tudo disponível e subtotal de 73,00 (>= 50)
    assert pedido_grande.situacao(0) == "Confirmado com frete grátis"


def test_situacao_confirmado_sem_frete_gratis(pedido_pequeno):
    # Tudo disponível e subtotal de 15,00 (< 50)
    assert pedido_pequeno.situacao(0) == "Confirmado"


def test_situacao_exatamente_25_por_cento_segue_para_a_regra_do_frete():
    # 1 de 4 unidades = exatamente 25%: não cancela, decide pelo frete
    com_frete = Pedido("Carla", [Item("Combo", 25.0, 4)])  # 100,00
    sem_frete = Pedido("Bruno", [Item("Suco", 5.0, 4)])  # 20,00
    assert com_frete.situacao(1) == "Confirmado com frete grátis"
    assert sem_frete.situacao(1) == "Confirmado"


def test_situacao_pouco_acima_de_25_por_cento_cancela():
    # 2 de 7 unidades = ~28,6%: acima do limite
    pedido = Pedido("Carla", [Item("Lanche", 10.0, 7)])
    assert pedido.situacao(2) == "Cancelado por falta de estoque"



# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método

def test_sugerir_frete_gratis_abaixo_de_50_aciona_o_servico(pedido_pequeno):
    # Subtotal 15,00 -> faltam 35,00 para o frete grátis
    sms_service = MagicMock()
    pedido_pequeno.sugerir_frete_gratis(sms_service)
    sms_service.enviar.assert_called_once_with("Bruno", 35.0)
