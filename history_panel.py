"""
Módulo da Interface do Painel Lateral de Histórico
Exibe o histórico separado para cada funcionalidade (Calculadora, Frações, Comprimento, Volume)
com cards interativos, cópia rápida, limpeza e estado vazio acolhedor.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

import theme as th
from history_manager import HistoryManager, ItemHistorico


class HistoryPanel(tk.Frame):
    """
    Barra lateral direita responsiva para exibição do histórico de cálculos.
    """
    def __init__(
        self,
        parent,
        history_manager: HistoryManager,
        on_item_selecionado: Optional[Callable[[ItemHistorico], None]] = None,
        on_alternar_visibilidade: Optional[Callable[[], None]] = None
    ):
        super().__init__(parent, bg=th.BG_CARD, bd=0, highlightthickness=1, highlightbackground=th.BORDER_COLOR)
        
        self.history_manager = history_manager
        self.on_item_selecionado = on_item_selecionado
        self.on_alternar_visibilidade = on_alternar_visibilidade
        
        self.categoria_atual = "calculadora"
        self._construir_interface()

        # Registra atualização automática quando houver novo cálculo
        self.history_manager.registrar_ouvinte(self._ao_alterar_historico)

    def _construir_interface(self):
        # ====================================================================
        # CABEÇALHO DO PAINEL DE HISTÓRICO
        # ====================================================================
        self.header_frame = tk.Frame(self, bg=th.BG_CARD, padx=14, pady=14)
        self.header_frame.pack(fill="x")

        # Linha 1 do Header: Título + Botão de Limpar
        top_row = tk.Frame(self.header_frame, bg=th.BG_CARD)
        top_row.pack(fill="x")

        lbl_tit = tk.Label(
            top_row,
            text="🕒 Histórico",
            font=(th.FONT_FAMILY, 12, "bold"),
            fg=th.BTN_NUM_TEXT,
            bg=th.BG_CARD
        )
        lbl_tit.pack(side="left")

        # Botão Limpar Histórico
        self.btn_limpar = tk.Button(
            top_row,
            text="🗑️ Limpar",
            font=(th.FONT_FAMILY, 8, "bold"),
            bg="#FEF2F2",
            fg="#DC2626",
            activebackground="#FEE2E2",
            activeforeground="#B91C1C",
            bd=0,
            relief="flat",
            padx=8,
            pady=4,
            cursor="hand2",
            command=self._confirmar_limpar_categoria
        )
        self.btn_limpar.pack(side="right")

        # Linha 2 do Header: Badge indicando a funcionalidade ativa
        badge_row = tk.Frame(self.header_frame, bg=th.BG_CARD)
        badge_row.pack(fill="x", pady=(8, 0))

        self.lbl_badge = tk.Label(
            badge_row,
            text="Calculadora",
            font=(th.FONT_FAMILY, 8, "bold"),
            bg="#EEF2FF",
            fg="#4F46E5",
            padx=8,
            pady=3
        )
        self.lbl_badge.pack(side="left")

        self.lbl_contador = tk.Label(
            badge_row,
            text="0 registros",
            font=(th.FONT_FAMILY, 8),
            fg=th.SIDEBAR_MUTED,
            bg=th.BG_CARD
        )
        self.lbl_contador.pack(side="right")

        # Feedback visual rápido de ação (ex: "✓ Copiado!")
        self.lbl_toast = tk.Label(
            self.header_frame,
            text="",
            font=(th.FONT_FAMILY, 8, "bold"),
            fg="#059669",
            bg=th.BG_CARD
        )
        self.lbl_toast.pack(anchor="w", pady=(4, 0))

        # Divisor sutil
        sep = tk.Frame(self, height=1, bg=th.BORDER_COLOR)
        sep.pack(fill="x")

        # ====================================================================
        # ÁREA DE CONTEÚDO ROLÁVEL (CANVAS + SCROLLBAR)
        # ====================================================================
        self.scroll_container = tk.Frame(self, bg=th.BG_CARD)
        self.scroll_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self.scroll_container,
            bg=th.BG_CARD,
            bd=0,
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self.scroll_container,
            orient="vertical",
            command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame interno que segura os cards
        self.cards_frame = tk.Frame(self.canvas, bg=th.BG_CARD, padx=10, pady=10)
        self.window_id = self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")

        # Eventos para redimensionamento e rolagem
        self.cards_frame.bind("<Configure>", self._ao_configurar_cards_frame)
        self.canvas.bind("<Configure>", self._ao_configurar_canvas)
        self._configurar_rolagem_mouse(self.canvas)
        self._configurar_rolagem_mouse(self.cards_frame)

    def _configurar_rolagem_mouse(self, widget):
        widget.bind("<MouseWheel>", self._ao_rolar_mouse)

    def _ao_rolar_mouse(self, event):
        # Suporte a rolagem no Windows
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _ao_configurar_cards_frame(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _ao_configurar_canvas(self, event):
        # Ajusta a largura interna do frame para preencher o canvas
        self.canvas.itemconfig(self.window_id, width=event.width)

    def definir_categoria(self, categoria: str):
        """
        Altera a visualização para a categoria de funcionalidade indicada.
        """
        self.categoria_atual = categoria
        nome_cat = HistoryManager.NOMES_CATEGORIAS.get(categoria, categoria.capitalize())
        bg_cor, fg_cor = HistoryManager.CORES_CATEGORIAS.get(categoria, ("#F1F5F9", "#475569"))

        self.lbl_badge.config(text=nome_cat, bg=bg_cor, fg=fg_cor)
        self.recarregar_itens()

    def _ao_alterar_historico(self, categoria_modificada: str):
        # Atualiza a tela se a categoria modificada for a ativa ou se for 'todas'
        if categoria_modificada in (self.categoria_atual, "todas"):
            self.recarregar_itens()

    def recarregar_itens(self):
        """Reconstrói a lista de cards com base na categoria ativa."""
        # Limpa widgets anteriores
        for w in self.cards_frame.winfo_children():
            w.destroy()

        itens = self.history_manager.obter_historico(self.categoria_atual)
        qtd = len(itens)
        self.lbl_contador.config(text=f"{qtd} registro{'s' if qtd != 1 else ''}")

        if not itens:
            self._renderizar_estado_vazio()
            return

        for item in itens:
            self._criar_card_item(item)

    def _renderizar_estado_vazio(self):
        empty_box = tk.Frame(self.cards_frame, bg=th.BG_CARD, pady=40)
        empty_box.pack(fill="both", expand=True)

        lbl_icon = tk.Label(
            empty_box,
            text="📝",
            font=(th.FONT_FAMILY, 24),
            fg="#94A3B8",
            bg=th.BG_CARD
        )
        lbl_icon.pack(pady=(10, 6))

        lbl_msg = tk.Label(
            empty_box,
            text="Nenhum cálculo registrado",
            font=(th.FONT_FAMILY, 10, "bold"),
            fg="#64748B",
            bg=th.BG_CARD
        )
        lbl_msg.pack()

        nome_cat = HistoryManager.NOMES_CATEGORIAS.get(self.categoria_atual, "desta tela")
        lbl_sub = tk.Label(
            empty_box,
            text=f"Os cálculos de {nome_cat}\naparecerão aqui automaticamente.",
            font=(th.FONT_FAMILY, 9),
            fg="#94A3B8",
            bg=th.BG_CARD,
            justify="center"
        )
        lbl_sub.pack(pady=(4, 10))

    def _criar_card_item(self, item: ItemHistorico):
        card = tk.Frame(
            self.cards_frame,
            bg="#F8FAFC",
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground="#E2E8F0",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        card.pack(fill="x", pady=4)

        # Cabeçalho do Card: Horário
        head_row = tk.Frame(card, bg="#F8FAFC")
        head_row.pack(fill="x")

        lbl_hora = tk.Label(
            head_row,
            text=item.timestamp,
            font=(th.FONT_FAMILY, 8),
            fg="#94A3B8",
            bg="#F8FAFC"
        )
        lbl_hora.pack(side="right")

        lbl_dica = tk.Label(
            head_row,
            text="clique p/ copiar/usar",
            font=(th.FONT_FAMILY, 7),
            fg="#CBD5E1",
            bg="#F8FAFC"
        )
        lbl_dica.pack(side="left")

        # Linha da Expressão
        lbl_expr = tk.Label(
            card,
            text=item.expressao,
            font=(th.FONT_FAMILY, 9),
            fg="#475569",
            bg="#F8FAFC",
            anchor="w",
            wraplength=230,
            justify="left"
        )
        lbl_expr.pack(fill="x", pady=(2, 0))

        # Linha do Resultado
        lbl_res = tk.Label(
            card,
            text=f"= {item.resultado}",
            font=(th.FONT_FAMILY, 11, "bold"),
            fg="#0F172A",
            bg="#F8FAFC",
            anchor="w",
            wraplength=230,
            justify="left"
        )
        lbl_res.pack(fill="x", pady=(2, 0))

        # Detalhes opcionais
        if item.detalhes:
            lbl_det = tk.Label(
                card,
                text=item.detalhes,
                font=(th.FONT_FAMILY, 8),
                fg="#64748B",
                bg="#F8FAFC",
                anchor="w",
                wraplength=230,
                justify="left"
            )
            lbl_det.pack(fill="x", pady=(2, 0))

        # Efeitos de Hover e Clique em todos os elementos do card
        widgets = [card, head_row, lbl_hora, lbl_dica, lbl_expr, lbl_res]
        if item.detalhes:
            widgets.append(lbl_det)

        for w in widgets:
            w.bind("<Enter>", lambda e, c=card, w_list=widgets: self._on_card_hover(c, w_list, True))
            w.bind("<Leave>", lambda e, c=card, w_list=widgets: self._on_card_hover(c, w_list, False))
            w.bind("<Button-1>", lambda e, it=item: self._on_card_click(it))
            self._configurar_rolagem_mouse(w)

    def _on_card_hover(self, card, widgets, is_hovering):
        bg = "#F1F5F9" if is_hovering else "#F8FAFC"
        bd_color = "#CBD5E1" if is_hovering else "#E2E8F0"
        card.config(bg=bg, highlightbackground=bd_color)
        for w in widgets:
            try:
                w.config(bg=bg)
            except Exception:
                pass

    def _on_card_click(self, item: ItemHistorico):
        # Copia o resultado para a área de transferência
        try:
            self.clipboard_clear()
            self.clipboard_append(item.resultado)
            self._mostrar_toast("✓ Copiado para a área de transferência!")
        except Exception:
            pass

        # Dispara callback se configurado para restaurar na tela ativa
        if self.on_item_selecionado:
            self.on_item_selecionado(item)

    def _mostrar_toast(self, mensagem: str):
        self.lbl_toast.config(text=mensagem)
        self.after(2200, lambda: self.lbl_toast.config(text=""))

    def _confirmar_limpar_categoria(self):
        itens = self.history_manager.obter_historico(self.categoria_atual)
        if not itens:
            return

        nome_cat = HistoryManager.NOMES_CATEGORIAS.get(self.categoria_atual, self.categoria_atual)
        resposta = messagebox.askyesno(
            "Limpar Histórico",
            f"Deseja limpar todo o histórico de {nome_cat}?",
            parent=self
        )
        if resposta:
            self.history_manager.limpar_categoria(self.categoria_atual)
            self._mostrar_toast("Histórico limpo com sucesso!")
