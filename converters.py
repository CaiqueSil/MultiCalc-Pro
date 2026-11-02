"""
Módulo de Conversores de Unidades
Suporta conversões precisas de Volume e Comprimento, com textos e siglas em PT-BR.
"""

from typing import Dict, List, Tuple


# ============================================================================
# CONVERSOR DE COMPRIMENTO
# Unidades solicitadas: mm, cm, dm, m, dam, hm, km, polegadas, pés, jardas, milhas
# Base de conversão: Metro (m)
# ============================================================================

UNIDADES_COMPRIMENTO: Dict[str, Tuple[str, float]] = {
    "mm": ("Milímetro (mm)", 0.001),
    "cm": ("Centímetro (cm)", 0.01),
    "dm": ("Decímetro (dm)", 0.1),
    "m": ("Metro (m)", 1.0),
    "dam": ("Decâmetro (dam)", 10.0),
    "hm": ("Hectômetro (hm)", 100.0),
    "km": ("Quilômetro (km)", 1000.0),
    "polegadas": ("Polegadas (in)", 0.0254),
    "pés": ("Pés (ft)", 0.3048),
    "jardas": ("Jardas (yd)", 0.9144),
    "milhas": ("Milhas (mi)", 1609.344),
}


def converter_comprimento(valor: float, unidade_origem: str, unidade_destino: str) -> float:
    """
    Converte um valor entre duas unidades de comprimento.
    """
    if unidade_origem not in UNIDADES_COMPRIMENTO:
        raise ValueError(f"Unidade de origem '{unidade_origem}' não é suportada.")
    if unidade_destino not in UNIDADES_COMPRIMENTO:
        raise ValueError(f"Unidade de destino '{unidade_destino}' não é suportada.")
    
    # Converte de origem para metros
    fator_origem = UNIDADES_COMPRIMENTO[unidade_origem][1]
    valor_em_metros = valor * fator_origem
    
    # Converte de metros para destino
    fator_destino = UNIDADES_COMPRIMENTO[unidade_destino][1]
    return valor_em_metros / fator_destino


def converter_comprimento_para_todas(valor: float, unidade_origem: str) -> List[Tuple[str, str, float]]:
    """
    Gera uma lista com o valor convertido para todas as unidades de comprimento disponíveis.
    Retorna lista de (chave, nome_formatado, valor_convertido).
    """
    resultado = []
    for chave, (nome, _) in UNIDADES_COMPRIMENTO.items():
        val = converter_comprimento(valor, unidade_origem, chave)
        resultado.append((chave, nome, val))
    return resultado


# ============================================================================
# CONVERSOR DE VOLUME
# Unidades solicitadas: cm³, L, m³ (com suporte adicional a mL, dm³, mm³)
# Base de conversão: Litro (L)
# 1 L = 1000 cm³
# 1 m³ = 1000 L = 1.000.000 cm³
# ============================================================================

UNIDADES_VOLUME: Dict[str, Tuple[str, float]] = {
    "cm³": ("Centímetro cúbico (cm³)", 0.001),
    "L": ("Litro (L)", 1.0),
    "m³": ("Metro cúbico (m³)", 1000.0),
    "mL": ("Mililitro (mL)", 0.001),
    "dm³": ("Decímetro cúbico (dm³)", 1.0),
    "mm³": ("Milímetro cúbico (mm³)", 0.000001),
}


def converter_volume(valor: float, unidade_origem: str, unidade_destino: str) -> float:
    """
    Converte um valor entre duas unidades de volume.
    """
    if unidade_origem not in UNIDADES_VOLUME:
        raise ValueError(f"Unidade de origem '{unidade_origem}' não é suportada.")
    if unidade_destino not in UNIDADES_VOLUME:
        raise ValueError(f"Unidade de destino '{unidade_destino}' não é suportada.")
    
    # Converte de origem para Litros
    fator_origem = UNIDADES_VOLUME[unidade_origem][1]
    valor_em_litros = valor * fator_origem
    
    # Converte de Litros para destino
    fator_destino = UNIDADES_VOLUME[unidade_destino][1]
    return valor_em_litros / fator_destino


def converter_volume_para_todas(valor: float, unidade_origem: str) -> List[Tuple[str, str, float]]:
    """
    Gera uma lista com o valor convertido para todas as unidades de volume disponíveis.
    Retorna lista de (chave, nome_formatado, valor_convertido).
    """
    resultado = []
    for chave, (nome, _) in UNIDADES_VOLUME.items():
        val = converter_volume(valor, unidade_origem, chave)
        resultado.append((chave, nome, val))
    return resultado


def formatar_numero(valor: float, precisao_maxima: int = 8) -> str:
    """
    Formata um número em notação decimal amigável em PT-BR (com vírgula decimal)
    evitando caudas longas de zeros e usando notação científica apenas para
    números extremamente pequenos ou imensos.
    """
    if abs(valor) < 1e-6 and valor != 0:
        texto = f"{valor:.6e}"
        return texto.replace(".", ",")
    
    # Formatação com arredondamento inteligente
    texto = f"{valor:.{precisao_maxima}f}".rstrip("0").rstrip(".")
    if not texto or texto == "-0":
        texto = "0"
    return texto.replace(".", ",")
