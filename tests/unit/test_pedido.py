import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido


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



# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método



# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método
