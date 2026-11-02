"""
Módulo de Gerenciamento de Histórico
Armazena e gerencia históricos independentes para cada funcionalidade:
- Calculadora
- Frações
- Comprimento
- Volume
"""

import datetime
from typing import Callable, Dict, List, Optional


class ItemHistorico:
    """
    Representa uma entrada individual no histórico de cálculos/conversões.
    """
    def __init__(self, categoria: str, expressao: str, resultado: str, detalhes: str = ""):
        self.categoria = categoria
        self.expressao = expressao
        self.resultado = resultado
        self.detalhes = detalhes
        self.timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    def __repr__(self):
        return f"<ItemHistorico [{self.categoria}] {self.expressao} = {self.resultado} ({self.timestamp})>"


class HistoryManager:
    """
    Gerenciador central com armazenamento isolado por categoria.
    """
    NOMES_CATEGORIAS = {
        "calculadora": "Calculadora",
        "fracoes": "Cálculo de Frações",
        "comprimento": "Conversor de Comprimento",
        "volume": "Conversor de Volume",
    }

    CORES_CATEGORIAS = {
        "calculadora": ("#EEF2FF", "#4F46E5"),   # (Fundo, Texto)
        "fracoes": ("#ECFDF5", "#059669"),
        "comprimento": ("#F5F3FF", "#7C3AED"),
        "volume": ("#EFF6FF", "#2563EB"),
    }

    def __init__(self):
        # Históricos isolados para cada funcionalidade
        self._historicos: Dict[str, List[ItemHistorico]] = {
            "calculadora": [],
            "fracoes": [],
            "comprimento": [],
            "volume": [],
        }
        self._ouvintes: List[Callable[[str], None]] = []

    def adicionar(self, categoria: str, expressao: str, resultado: str, detalhes: str = "") -> Optional[ItemHistorico]:
        """
        Adiciona uma nova entrada ao histórico da categoria informada.
        Evita duplicatas idênticas imediatas.
        """
        if categoria not in self._historicos:
            self._historicos[categoria] = []

        # Validação básica
        expressao = str(expressao).strip()
        resultado = str(resultado).strip()
        if not expressao or not resultado:
            return None

        # Previne inserção repetida do mesmo cálculo consecutivo
        if self._historicos[categoria]:
            ultimo = self._historicos[categoria][0]
            if ultimo.expressao == expressao and ultimo.resultado == resultado:
                return ultimo

        item = ItemHistorico(categoria, expressao, resultado, detalhes)
        # Mais recente no início
        self._historicos[categoria].insert(0, item)

        # Limite máximo de histórico por funcionalidade (50 registros)
        if len(self._historicos[categoria]) > 50:
            self._historicos[categoria].pop()

        self._notificar_ouvintes(categoria)
        return item

    def obter_historico(self, categoria: str) -> List[ItemHistorico]:
        """Retorna uma cópia da lista de itens da categoria informada."""
        return list(self._historicos.get(categoria, []))

    def limpar_categoria(self, categoria: str):
        """Limpa o histórico apenas da categoria informada."""
        if categoria in self._historicos:
            self._historicos[categoria].clear()
            self._notificar_ouvintes(categoria)

    def limpar_todos(self):
        """Limpa o histórico de todas as categorias."""
        for cat in self._historicos:
            self._historicos[cat].clear()
        self._notificar_ouvintes("todas")

    def registrar_ouvinte(self, callback: Callable[[str], None]):
        """Registra um callback a ser acionado quando houver alteração no histórico."""
        self._ouvintes.append(callback)

    def _notificar_ouvintes(self, categoria: str):
        for ouvinte in self._ouvintes:
            try:
                ouvinte(categoria)
            except Exception:
                pass
