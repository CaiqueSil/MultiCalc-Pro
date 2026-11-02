"""
Módulo da Interface do Conversor de Comprimento
Suporta todas as 11 unidades solicitadas:
mm, cm, dm, m, dam, hm, km, polegadas, pés, jardas, milhas.
Possui conversão instantânea, inversão de unidades e tabela de equivalência completa.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

import theme as th
import converters as cv


class ComprimentoView(tk.Frame):
    """
    Tela responsiva do Conversor de Comprimento.
    """
    def __init__(self, parent, on_calculo_realizado: Optional[Callable[[str, str, str], None]] = None):
        super().__init__(parent, bg=th.BG_MAIN)
        self.on_calculo_realizado = on_calculo_realizado
        self._timer_historico = None
        self._construir_interface()
        self._configurar_responsividade()
        self.executar_conversao(salvar_historico=False)

    def _construir_interface(self):
        # Card principal com margem
        self.card = tk.Frame(
            self,
            bg=th.BG_CARD,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=th.BORDER_COLOR,
            padx=25,
            pady=20
        )
        self.card.grid(row=0, column=0, sticky="nsew", padx=25, pady=20)

        # Cabeçalho
        header = tk.Frame(self.card, bg=th.BG_CARD)
        header.pack(fill="x", pady=(0, 15))

        lbl_titulo = tk.Label(
            header,
            text="Conversor de Comprimento",
            font=th.FONT_TITLE,
            fg=th.BTN_NUM_TEXT,
            bg=th.BG_CARD
        )
        lbl_titulo.pack(anchor="w")

        lbl_sub = tk.Label(
            header,
            text="Converta instantaneamente entre unidades métricas e imperiais.",
            font=th.FONT_SUBTITLE,
            fg=th.SIDEBAR_MUTED,
            bg=th.BG_CARD
        )
        lbl_sub.pack(anchor="w", pady=(2, 0))

        # Painel de Controle de Conversão (Entrada / De / Inverter / Para)
        ctrl_frame = tk.Frame(self.card, bg="#F8FAFC", bd=1, relief="solid", highlightbackground="#E2E8F0", padx=15, pady=15)
        ctrl_frame.pack(fill="x", pady=(0, 15))

        # Linha de controles
        linha_ctrl = tk.Frame(ctrl_frame, bg="#F8FAFC")
        linha_ctrl.pack(fill="x")

        # Campo de Valor
        f_val = tk.Frame(linha_ctrl, bg="#F8FAFC")
        f_val.pack(side="left", padx=(0, 10))
        tk.Label(f_val, text="Valor a converter:", font=(th.FONT_FAMILY, 9, "bold"), fg="#475569", bg="#F8FAFC").pack(anchor="w")
        self.entry_valor = tk.Entry(f_val, font=(th.FONT_FAMILY, 12), width=12)
        self.entry_valor.insert(0, "1")
        self.entry_valor.pack(pady=4)
        self.entry_valor.bind("<KeyRelease>", lambda e: self._ao_digitar_valor())
        self.entry_valor.bind("<Return>", lambda e: self.executar_conversao(salvar_historico=True))

        # Unidade de Origem (De)
        f_de = tk.Frame(linha_ctrl, bg="#F8FAFC")
        f_de.pack(side="left", padx=10)
        tk.Label(f_de, text="De (origem):", font=(th.FONT_FAMILY, 9, "bold"), fg="#475569", bg="#F8FAFC").pack(anchor="w")
        
        opcoes_nomes = [f"{chave} - {nome}" for chave, (nome, _) in cv.UNIDADES_COMPRIMENTO.items()]
        self.chaves_unidades = list(cv.UNIDADES_COMPRIMENTO.keys())

        self.combo_de = ttk.Combobox(f_de, values=opcoes_nomes, state="readonly", width=18, font=th.FONT_BODY)
        self.combo_de.current(self.chaves_unidades.index("m"))  # Padrão: metro
        self.combo_de.pack(pady=4)
        self.combo_de.bind("<<ComboboxSelected>>", lambda e: self.executar_conversao(salvar_historico=True))

        # Botão Inverter
        btn_inverter = tk.Button(
            linha_ctrl,
            text="⇄ Inverter",
            font=(th.FONT_FAMILY, 10, "bold"),
            bg="#E2E8F0",
            fg="#1E293B",
            activebackground="#CBD5E1",
            bd=0,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.inverter_unidades
        )
        btn_inverter.pack(side="left", padx=10, pady=(15, 0))

        # Unidade de Destino (Para)
        f_para = tk.Frame(linha_ctrl, bg="#F8FAFC")
        f_para.pack(side="left", padx=10)
        tk.Label(f_para, text="Para (destino):", font=(th.FONT_FAMILY, 9, "bold"), fg="#475569", bg="#F8FAFC").pack(anchor="w")
        self.combo_para = ttk.Combobox(f_para, values=opcoes_nomes, state="readonly", width=18, font=th.FONT_BODY)
        self.combo_para.current(self.chaves_unidades.index("km"))  # Padrão: km
        self.combo_para.pack(pady=4)
        self.combo_para.bind("<<ComboboxSelected>>", lambda e: self.executar_conversao(salvar_historico=True))

        # Botão Copiar
        btn_copiar = tk.Button(
            linha_ctrl,
            text="📋 Copiar",
            font=(th.FONT_FAMILY, 9, "bold"),
            bg=th.PRIMARY,
            fg=th.PRIMARY_TEXT,
            activebackground=th.PRIMARY_HOVER,
            activeforeground=th.PRIMARY_TEXT,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.copiar_resultado
        )
        btn_copiar.pack(side="left", padx=10, pady=(15, 0))

        # Card de Destaque do Resultado
        self.result_card = tk.Frame(self.card, bg="#EEF2FF", bd=1, relief="solid", highlightbackground="#C7D2FE", padx=18, pady=12)
        self.result_card.pack(fill="x", pady=(0, 15))

        self.lbl_resultado_grande = tk.Label(
            self.result_card,
            text="1 m = 0,001 km",
            font=th.FONT_RESULT_LARGE,
            fg="#3730A3",
            bg="#EEF2FF"
        )
        self.lbl_resultado_grande.pack(anchor="w")

        self.lbl_detalhes_resultado = tk.Label(
            self.result_card,
            text="Fórmula: dividir o valor em metros por 1000",
            font=(th.FONT_FAMILY, 9),
            fg="#4338CA",
            bg="#EEF2FF"
        )
        self.lbl_detalhes_resultado.pack(anchor="w", pady=(2, 0))

        # Tabela de Todas as Equivalências Simultâneas
        lbl_tabela_tit = tk.Label(
            self.card,
            text="Equivalência Simultânea em Todas as Unidades de Comprimento:",
            font=th.FONT_BODY_BOLD,
            fg="#1E293B",
            bg=th.BG_CARD
        )
        lbl_tabela_tit.pack(anchor="w", pady=(5, 8))

        # Grid de cartões de equivalência
        self.grid_cards_frame = tk.Frame(self.card, bg=th.BG_CARD)
        self.grid_cards_frame.pack(fill="both", expand=True)

        self.cards_labels = {}
        colunas = 3
        for idx, chave in enumerate(self.chaves_unidades):
            nome_completo, _ = cv.UNIDADES_COMPRIMENTO[chave]
            r = idx // colunas
            c = idx % colunas

            card_item = tk.Frame(
                self.grid_cards_frame,
                bg="#F8FAFC",
                bd=1,
                relief="solid",
                highlightthickness=1,
                highlightbackground="#E2E8F0",
                padx=12,
                pady=8
            )
            card_item.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

            lbl_u_nome = tk.Label(
                card_item,
                text=nome_completo,
                font=(th.FONT_FAMILY, 9, "bold"),
                fg="#64748B",
                bg="#F8FAFC"
            )
            lbl_u_nome.pack(anchor="w")

            lbl_u_val = tk.Label(
                card_item,
                text="-",
                font=(th.FONT_FAMILY, 11, "bold"),
                fg="#0F172A",
                bg="#F8FAFC"
            )
            lbl_u_val.pack(anchor="w", pady=(2, 0))
            self.cards_labels[chave] = lbl_u_val

        for c in range(colunas):
            self.grid_cards_frame.grid_columnconfigure(c, weight=1)

    def _configurar_responsividade(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _obter_unidade_selecionada(self, combo: ttk.Combobox) -> str:
        idx = combo.current()
        if idx >= 0:
            return self.chaves_unidades[idx]
        return "m"

    def _ao_digitar_valor(self):
        # Atualiza a conversão visual imediatamente
        self.executar_conversao(salvar_historico=False)
        # Agenda registro no histórico após pausa na digitação (700ms)
        if self._timer_historico:
            self.after_cancel(self._timer_historico)
        self._timer_historico = self.after(700, lambda: self.executar_conversao(salvar_historico=True))

    def inverter_unidades(self):
        idx_de = self.combo_de.current()
        idx_para = self.combo_para.current()
        self.combo_de.current(idx_para)
        self.combo_para.current(idx_de)
        self.executar_conversao(salvar_historico=True)

    def executar_conversao(self, salvar_historico: bool = False):
        txt_val = self.entry_valor.get().strip().replace(",", ".")
        if not txt_val:
            return

        try:
            valor = float(txt_val)
        except ValueError:
            self.lbl_resultado_grande.config(text="Digite um número válido")
            return

        u_de = self._obter_unidade_selecionada(self.combo_de)
        u_para = self._obter_unidade_selecionada(self.combo_para)

        try:
            resultado = cv.converter_comprimento(valor, u_de, u_para)
            val_fmt = cv.formatar_numero(valor)
            res_fmt = cv.formatar_numero(resultado)
            
            self.resultado_atual_str = f"{res_fmt} {u_para}"
            self.lbl_resultado_grande.config(text=f"{val_fmt} {u_de} = {res_fmt} {u_para}")

            nome_de = cv.UNIDADES_COMPRIMENTO[u_de][0]
            nome_para = cv.UNIDADES_COMPRIMENTO[u_para][0]
            self.lbl_detalhes_resultado.config(text=f"Conversão de {nome_de} para {nome_para}")

            # Registra no histórico de Comprimento se solicitado
            if salvar_historico and self.on_calculo_realizado:
                expr = f"{val_fmt} {u_de} ➔ {u_para}"
                res_txt = f"{res_fmt} {u_para}"
                det = f"{nome_de} para {nome_para}"
                self.on_calculo_realizado(expr, res_txt, det)

            # Atualiza todos os cards da tabela
            todas = cv.converter_comprimento_para_todas(valor, u_de)
            for chave, _, val_conv in todas:
                if chave in self.cards_labels:
                    self.cards_labels[chave].config(text=f"{cv.formatar_numero(val_conv)} {chave}")
        except Exception as e:
            self.lbl_resultado_grande.config(text=f"Erro: {str(e)}")

    def copiar_resultado(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.lbl_resultado_grande.cget("text"))
            self.executar_conversao(salvar_historico=True)
            messagebox.showinfo("Copiado!", "Resultado copiado para a área de transferência com sucesso!")
        except Exception:
            pass

    def carregar_do_historico(self, item):
        """Carrega valor selecionado do histórico para o campo de entrada."""
        try:
            # Ex: item.expressao: '5 km ➔ m' ou item.resultado: '5000 m'
            partes = item.resultado.split()
            if partes:
                val = partes[0].replace(".", "").replace(",", ".")
                self.entry_valor.delete(0, "end")
                self.entry_valor.insert(0, partes[0])
                self.executar_conversao(salvar_historico=False)
        except Exception:
            pass
