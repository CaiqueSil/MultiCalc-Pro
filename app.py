"""
Módulo Principal da Aplicação Tkinter
Gerencia a janela principal, barra lateral esquerda responsiva,
área de conteúdo, painel lateral direito de Histórico isolado por funcionalidade
e atalhos de teclado.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict

import theme as th
from calc_view import CalculadoraView
from fractions_view import FracoesView
from length_view import ComprimentoView
from volume_view import VolumeView
from history_manager import HistoryManager, ItemHistorico
from history_panel import HistoryPanel


class MultiCalcApp(tk.Tk):
    """
    Aplicação Desktop com barra lateral esquerda de navegação,
    painel central responsivo e barra lateral direita com histórico separado.
    """
    def __init__(self):
        super().__init__()

        self.title("Calculadora Inteligente & Conversores | Python")
        self.geometry("1180x700")
        self.minsize(980, 580)
        self.configure(bg=th.BG_MAIN)

        # Configura estilo do ttk para combinar com o tema
        self._configurar_estilos_ttk()

        # Gerenciador de histórico isolado por funcionalidade
        self.history_manager = HistoryManager()

        # Dicionários e controle de telas
        self.nav_botoes: Dict[str, tk.Button] = {}
        self.telas: Dict[str, tk.Frame] = {}
        self.tela_atual = None
        self.historico_visivel = True

        self._construir_layout_principal()
        self._inicializar_telas()
        self._configurar_atalhos_teclado()

        # Inicia com a Calculadora selecionada
        self.navegar_para("calculadora")

    def _configurar_estilos_ttk(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Estilo moderno para Comboboxes
        style.configure(
            "TCombobox",
            fieldbackground="#FFFFFF",
            background="#F1F5F9",
            foreground="#0F172A",
            bordercolor=th.BORDER_COLOR,
            lightcolor=th.BORDER_COLOR,
            darkcolor=th.BORDER_COLOR,
            arrowcolor="#475569",
            padding=5
        )

        # Estilo para Scrollbar do Histórico
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="#CBD5E1",
            troughcolor="#F8FAFC",
            bordercolor="#F8FAFC",
            arrowcolor="#64748B"
        )

    def _construir_layout_principal(self):
        # Grid da Janela:
        # Coluna 0: Barra Lateral Esquerda (Menu)
        # Coluna 1: Container de Conteúdo (Calculadora / Frações / Comprimento / Volume)
        # Coluna 2: Barra Lateral Direita (Histórico dos Cálculos)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=220)  # Menu esquerdo
        self.grid_columnconfigure(1, weight=1)               # Conteúdo central
        self.grid_columnconfigure(2, weight=0, minsize=290)  # Histórico direito

        # ====================================================================
        # BARRA LATERAL ESQUERDA (SIDEBAR DE NAVEGAÇÃO)
        # ====================================================================
        self.sidebar = tk.Frame(self, bg=th.BG_SIDEBAR, padx=14, pady=20)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Cabeçalho da Sidebar
        brand_frame = tk.Frame(self.sidebar, bg=th.BG_SIDEBAR)
        brand_frame.pack(fill="x", pady=(0, 20))

        lbl_logo = tk.Label(
            brand_frame,
            text="🧮 MultiCalc",
            font=(th.FONT_FAMILY, 15, "bold"),
            fg=th.SIDEBAR_TEXT,
            bg=th.BG_SIDEBAR
        )
        lbl_logo.pack(anchor="w")

        lbl_desc = tk.Label(
            brand_frame,
            text="Calculadora & Conversores",
            font=(th.FONT_FAMILY, 9),
            fg=th.SIDEBAR_MUTED,
            bg=th.BG_SIDEBAR
        )
        lbl_desc.pack(anchor="w", pady=(2, 0))

        # Divisor sutil
        sep = tk.Frame(self.sidebar, height=1, bg="#1E293B")
        sep.pack(fill="x", pady=(0, 15))

        # Rótulo da Seção de Menu
        tk.Label(
            self.sidebar,
            text="MÓDULOS PRINCIPAIS",
            font=(th.FONT_FAMILY, 8, "bold"),
            fg="#64748B",
            bg=th.BG_SIDEBAR
        ).pack(anchor="w", pady=(0, 10))

        # Botões de Navegação
        itens_menu = [
            ("calculadora", "🧮  Calculadora"),
            ("fracoes", "🍰  Cálculo de Frações"),
            ("comprimento", "📏  Conversor Comprimento"),
            ("volume", "🧊  Conversor Volume"),
        ]

        for id_tela, rotulo in itens_menu:
            btn = self._criar_botao_sidebar(id_tela, rotulo)
            btn.pack(fill="x", pady=4)
            self.nav_botoes[id_tela] = btn

        # Rodapé da Sidebar
        footer_frame = tk.Frame(self.sidebar, bg=th.BG_SIDEBAR)
        footer_frame.pack(side="bottom", fill="x", pady=(10, 0))

        # Botão para alternar visibilidade do histórico
        self.btn_toggle_hist = tk.Button(
            footer_frame,
            text="🕒 Alternar Painel Histórico",
            font=(th.FONT_FAMILY, 8, "bold"),
            bg="#1E293B",
            fg="#94A3B8",
            activebackground="#334155",
            activeforeground="#FFFFFF",
            bd=0,
            relief="flat",
            padx=8,
            pady=6,
            cursor="hand2",
            command=self.alternar_painel_historico
        )
        self.btn_toggle_hist.pack(fill="x", pady=(0, 10))

        tk.Label(
            footer_frame,
            text="Desafio Alura • Python 3",
            font=(th.FONT_FAMILY, 8),
            fg=th.SIDEBAR_MUTED,
            bg=th.BG_SIDEBAR
        ).pack(anchor="w")

        tk.Label(
            footer_frame,
            text="Interface Responsiva Tkinter",
            font=(th.FONT_FAMILY, 8),
            fg="#475569",
            bg=th.BG_SIDEBAR
        ).pack(anchor="w", pady=(2, 0))

        # ====================================================================
        # ÁREA DE CONTEÚDO PRINCIPAL (CENTRO)
        # ====================================================================
        self.container_conteudo = tk.Frame(self, bg=th.BG_MAIN)
        self.container_conteudo.grid(row=0, column=1, sticky="nsew")
        self.container_conteudo.grid_rowconfigure(0, weight=1)
        self.container_conteudo.grid_columnconfigure(0, weight=1)

        # ====================================================================
        # BARRA LATERAL DIREITA (HISTÓRICO SEPARADO POR FUNCIONALIDADE)
        # ====================================================================
        self.history_panel = HistoryPanel(
            self,
            history_manager=self.history_manager,
            on_item_selecionado=self._ao_selecionar_item_historico
        )
        self.history_panel.grid(row=0, column=2, sticky="nsew")
        self.history_panel.grid_propagate(False)

    def _criar_botao_sidebar(self, id_tela: str, texto: str) -> tk.Button:
        btn = tk.Button(
            self.sidebar,
            text=texto,
            font=th.FONT_BTN_SIDEBAR,
            anchor="w",
            padx=14,
            pady=10,
            bd=0,
            relief="flat",
            bg=th.BG_SIDEBAR,
            fg=th.SIDEBAR_TEXT,
            activebackground=th.SIDEBAR_HOVER,
            activeforeground=th.SIDEBAR_TEXT,
            cursor="hand2",
            command=lambda: self.navegar_para(id_tela)
        )

        btn.bind("<Enter>", lambda e: self._on_sidebar_hover(id_tela, True))
        btn.bind("<Leave>", lambda e: self._on_sidebar_hover(id_tela, False))
        return btn

    def _on_sidebar_hover(self, id_tela: str, hovering: bool):
        btn = self.nav_botoes[id_tela]
        if self.tela_atual == id_tela:
            return
        if hovering:
            btn.config(bg=th.SIDEBAR_HOVER)
        else:
            btn.config(bg=th.BG_SIDEBAR)

    def _inicializar_telas(self):
        # Instancia as 4 telas conectando cada uma ao seu histórico dedicado
        self.calc_view = CalculadoraView(
            self.container_conteudo,
            navegar_para_fracoes=lambda: self.navegar_para("fracoes"),
            on_calculo_realizado=lambda expr, res, det: self.history_manager.adicionar("calculadora", expr, res, det)
        )

        self.fracoes_view = FracoesView(
            self.container_conteudo,
            on_calculo_realizado=lambda expr, res, det: self.history_manager.adicionar("fracoes", expr, res, det)
        )

        self.comprimento_view = ComprimentoView(
            self.container_conteudo,
            on_calculo_realizado=lambda expr, res, det: self.history_manager.adicionar("comprimento", expr, res, det)
        )

        self.volume_view = VolumeView(
            self.container_conteudo,
            on_calculo_realizado=lambda expr, res, det: self.history_manager.adicionar("volume", expr, res, det)
        )

        self.telas["calculadora"] = self.calc_view
        self.telas["fracoes"] = self.fracoes_view
        self.telas["comprimento"] = self.comprimento_view
        self.telas["volume"] = self.volume_view

        for view in self.telas.values():
            view.grid(row=0, column=0, sticky="nsew")

    def navegar_para(self, id_tela: str):
        if id_tela not in self.telas:
            return

        self.tela_atual = id_tela

        # Atualiza botões da sidebar esquerda
        for chave, btn in self.nav_botoes.items():
            if chave == id_tela:
                btn.config(bg=th.PRIMARY, fg="#FFFFFF", font=(th.FONT_FAMILY, 11, "bold"))
            else:
                btn.config(bg=th.BG_SIDEBAR, fg=th.SIDEBAR_TEXT, font=th.FONT_BTN_SIDEBAR)

        # Atualiza a barra de histórico da direita para exibir a categoria selecionada
        self.history_panel.definir_categoria(id_tela)

        # Traz a tela selecionada para o topo
        self.telas[id_tela].tkraise()

    def alternar_painel_historico(self):
        """Alterna a visibilidade da barra lateral de histórico (mostrar/ocultar)."""
        if self.historico_visivel:
            self.history_panel.grid_remove()
            self.historico_visivel = False
            self.btn_toggle_hist.config(text="🕒 Mostrar Painel Histórico")
        else:
            self.history_panel.grid(row=0, column=2, sticky="nsew")
            self.historico_visivel = True
            self.btn_toggle_hist.config(text="🕒 Ocultar Painel Histórico")

    def _ao_selecionar_item_historico(self, item: ItemHistorico):
        """Ao clicar em um item do histórico, restaura na tela ativa se suportado."""
        tela_atual_widget = self.telas.get(self.tela_atual)
        if tela_atual_widget and hasattr(tela_atual_widget, "carregar_do_historico"):
            tela_atual_widget.carregar_do_historico(item)

    def _configurar_atalhos_teclado(self):
        self.bind("<Key>", self._tratar_tecla_global)

    def _tratar_tecla_global(self, evento):
        widget_foco = self.focus_get()
        if isinstance(widget_foco, tk.Entry):
            return
        
        if self.tela_atual == "calculadora":
            self.calc_view.processar_tecla(evento)


def iniciar_aplicacao():
    app = MultiCalcApp()
    app.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()
