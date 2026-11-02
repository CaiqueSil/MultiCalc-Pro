"""
Módulo da Interface da Calculadora de Frações
Permite operações aritméticas completas entre frações com numerador e denominador,
exibição irredutível, representação mista e conversão decimal <-> fração.
"""

from fractions import Fraction
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

import theme as th
import math_operations as mo
from converters import formatar_numero


class FracoesView(tk.Frame):
    """
    Tela dedicada para cálculo e simplificação de frações.
    """
    def __init__(self, parent, on_calculo_realizado: Optional[Callable[[str, str, str], None]] = None):
        super().__init__(parent, bg=th.BG_MAIN)
        self.on_calculo_realizado = on_calculo_realizado
        self._construir_interface()
        self._configurar_responsividade()

    def _construir_interface(self):
        # Card principal
        self.card = tk.Frame(
            self,
            bg=th.BG_CARD,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=th.BORDER_COLOR,
            padx=30,
            pady=25
        )
        self.card.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Cabeçalho
        header = tk.Frame(self.card, bg=th.BG_CARD)
        header.pack(fill="x", pady=(0, 20))

        lbl_titulo = tk.Label(
            header,
            text="Calculadora de Frações",
            font=th.FONT_TITLE,
            fg=th.BTN_NUM_TEXT,
            bg=th.BG_CARD
        )
        lbl_titulo.pack(anchor="w")

        lbl_sub = tk.Label(
            header,
            text="Operações exatas, simplificação irredutível, números mistos e conversão.",
            font=th.FONT_SUBTITLE,
            fg=th.SIDEBAR_MUTED,
            bg=th.BG_CARD
        )
        lbl_sub.pack(anchor="w", pady=(2, 0))

        # Seção 1: Operações entre duas frações
        frame_ops = tk.LabelFrame(
            self.card,
            text=" Operações com Frações ",
            font=th.FONT_BODY_BOLD,
            fg="#1E293B",
            bg=th.BG_CARD,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )
        frame_ops.pack(fill="x", pady=(0, 20))

        # Linha de entrada visual de frações
        calc_row = tk.Frame(frame_ops, bg=th.BG_CARD)
        calc_row.pack(pady=10)

        # Fração 1
        f1_box = tk.Frame(calc_row, bg=th.BG_CARD)
        f1_box.pack(side="left", padx=10)

        tk.Label(f1_box, text="Fração 1", font=(th.FONT_FAMILY, 9, "bold"), fg="#64748B", bg=th.BG_CARD).pack()
        self.entry_num1 = tk.Entry(f1_box, font=(th.FONT_FAMILY, 14, "bold"), width=6, justify="center")
        self.entry_num1.pack(pady=2)
        self.entry_num1.insert(0, "3")

        sep1 = tk.Frame(f1_box, height=2, bg="#334155")
        sep1.pack(fill="x", pady=2)

        self.entry_den1 = tk.Entry(f1_box, font=(th.FONT_FAMILY, 14, "bold"), width=6, justify="center")
        self.entry_den1.pack(pady=2)
        self.entry_den1.insert(0, "4")

        # Operador Seletor
        op_box = tk.Frame(calc_row, bg=th.BG_CARD)
        op_box.pack(side="left", padx=15)

        tk.Label(op_box, text="Operação", font=(th.FONT_FAMILY, 9, "bold"), fg="#64748B", bg=th.BG_CARD).pack()
        self.var_op = tk.StringVar(value="+")
        self.combo_op = ttk.Combobox(
            op_box,
            textvariable=self.var_op,
            values=["+ (Adição)", "- (Subtração)", "× (Multiplicação)", "÷ (Divisão)", "Simplificar (apenas Fração 1)"],
            state="readonly",
            width=20,
            font=th.FONT_BODY
        )
        self.combo_op.current(0)
        self.combo_op.pack(pady=12)

        # Fração 2
        f2_box = tk.Frame(calc_row, bg=th.BG_CARD)
        f2_box.pack(side="left", padx=10)

        tk.Label(f2_box, text="Fração 2", font=(th.FONT_FAMILY, 9, "bold"), fg="#64748B", bg=th.BG_CARD).pack()
        self.entry_num2 = tk.Entry(f2_box, font=(th.FONT_FAMILY, 14, "bold"), width=6, justify="center")
        self.entry_num2.pack(pady=2)
        self.entry_num2.insert(0, "2")

        sep2 = tk.Frame(f2_box, height=2, bg="#334155")
        sep2.pack(fill="x", pady=2)

        self.entry_den2 = tk.Entry(f2_box, font=(th.FONT_FAMILY, 14, "bold"), width=6, justify="center")
        self.entry_den2.pack(pady=2)
        self.entry_den2.insert(0, "3")

        # Botão Calcular Fração
        btn_calc = tk.Button(
            calc_row,
            text="Calcular ➔",
            font=(th.FONT_FAMILY, 11, "bold"),
            bg=th.PRIMARY,
            fg=th.PRIMARY_TEXT,
            activebackground=th.PRIMARY_HOVER,
            activeforeground=th.PRIMARY_TEXT,
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.calcular_operacao
        )
        btn_calc.pack(side="left", padx=(20, 10))

        # Card de Resultados da Fração
        self.res_card = tk.Frame(
            frame_ops,
            bg="#F8FAFC",
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground="#E2E8F0",
            padx=20,
            pady=15
        )
        self.res_card.pack(fill="x", pady=(15, 5))

        self.lbl_res_equacao = tk.Label(
            self.res_card,
            text="Resultado: 3/4 + 2/3 = 17/12",
            font=(th.FONT_FAMILY, 14, "bold"),
            fg=th.PRIMARY,
            bg="#F8FAFC"
        )
        self.lbl_res_equacao.pack(anchor="w")

        self.lbl_res_detalhes = tk.Label(
            self.res_card,
            text="Fração Irredutível: 17/12  |  Forma Mista: 1 e 5/12  |  Valor Decimal: ~1,4167",
            font=th.FONT_BODY,
            fg="#334155",
            bg="#F8FAFC"
        )
        self.lbl_res_detalhes.pack(anchor="w", pady=(6, 0))

        # Seção 2: Conversor Rápido Decimal <-> Fração
        frame_conv = tk.LabelFrame(
            self.card,
            text=" Conversor Decimal ⇄ Fração ",
            font=th.FONT_BODY_BOLD,
            fg="#1E293B",
            bg=th.BG_CARD,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )
        frame_conv.pack(fill="x", pady=(10, 0))

        conv_row = tk.Frame(frame_conv, bg=th.BG_CARD)
        conv_row.pack(fill="x", pady=5)

        tk.Label(conv_row, text="Digite um número decimal:", font=th.FONT_BODY, bg=th.BG_CARD).pack(side="left", padx=(0, 10))
        self.entry_dec = tk.Entry(conv_row, font=th.FONT_BODY, width=15)
        self.entry_dec.pack(side="left", padx=(0, 10))
        self.entry_dec.insert(0, "0.625")

        btn_dec_to_frac = tk.Button(
            conv_row,
            text="Converter para Fração",
            font=(th.FONT_FAMILY, 9, "bold"),
            bg="#0D9488",
            fg="#FFFFFF",
            activebackground="#0F766E",
            activeforeground="#FFFFFF",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.converter_decimal
        )
        btn_dec_to_frac.pack(side="left", padx=5)

        self.lbl_dec_resultado = tk.Label(
            conv_row,
            text="➜  Fração correspondente: 5/8",
            font=(th.FONT_FAMILY, 11, "bold"),
            fg="#0F766E",
            bg=th.BG_CARD
        )
        self.lbl_dec_resultado.pack(side="left", padx=15)

    def _configurar_responsividade(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def calcular_operacao(self):
        try:
            n1 = int(self.entry_num1.get().strip())
            d1 = int(self.entry_den1.get().strip())
            if d1 == 0:
                messagebox.showerror("Erro de Denominador", "O denominador da Fração 1 não pode ser zero!")
                return
        except ValueError:
            messagebox.showerror("Entrada Inválida", "Digite números inteiros válidos na Fração 1.")
            return

        op_selecionada = self.combo_op.get()
        if "Simplificar" in op_selecionada:
            res = mo.calcular_fracao(n1, d1, "simplificar")
            if isinstance(res, str):
                messagebox.showerror("Erro", res)
                return
            frac, misto, dec = res
            self.lbl_res_equacao.config(text=f"Simplificação de {n1}/{d1} = {frac.numerator}/{frac.denominator}")
            misto_txt = f"  |  Forma Mista: {misto}" if misto else ""
            self.lbl_res_detalhes.config(
                text=f"Fração Irredutível: {frac.numerator}/{frac.denominator}{misto_txt}  |  Decimal: {formatar_numero(dec)}"
            )
            if self.on_calculo_realizado:
                detalhe = f"Decimal: {formatar_numero(dec)}" + (f" | Misto: {misto}" if misto else "")
                self.on_calculo_realizado(f"Simplificar {n1}/{d1}", f"{frac.numerator}/{frac.denominator}", detalhe)
            return

        try:
            n2 = int(self.entry_num2.get().strip())
            d2 = int(self.entry_den2.get().strip())
            if d2 == 0:
                messagebox.showerror("Erro de Denominador", "O denominador da Fração 2 não pode ser zero!")
                return
        except ValueError:
            messagebox.showerror("Entrada Inválida", "Digite números inteiros válidos na Fração 2.")
            return

        if "+" in op_selecionada:
            op_cod = "+"
            op_simbolo = "+"
        elif "-" in op_selecionada:
            op_cod = "-"
            op_simbolo = "-"
        elif "×" in op_selecionada:
            op_cod = "*"
            op_simbolo = "×"
        elif "÷" in op_selecionada:
            op_cod = "/"
            op_simbolo = "÷"
        else:
            op_cod = "+"
            op_simbolo = "+"

        resultado = mo.calcular_fracao(n1, d1, op_cod, n2, d2)
        if isinstance(resultado, str):
            messagebox.showerror("Erro no Cálculo", resultado)
            return

        frac, misto, dec = resultado
        eq_txt = f"Resultado: ({n1}/{d1}) {op_simbolo} ({n2}/{d2}) = {frac.numerator}/{frac.denominator}"
        self.lbl_res_equacao.config(text=eq_txt)
        misto_txt = f"  |  Forma Mista: {misto}" if misto else ""
        self.lbl_res_detalhes.config(
            text=f"Fração Irredutível: {frac.numerator}/{frac.denominator}{misto_txt}  |  Decimal: {formatar_numero(dec)}"
        )
        if self.on_calculo_realizado:
            detalhe = f"Decimal: {formatar_numero(dec)}" + (f" | Misto: {misto}" if misto else "")
            self.on_calculo_realizado(f"({n1}/{d1}) {op_simbolo} ({n2}/{d2})", f"{frac.numerator}/{frac.denominator}", detalhe)

    def converter_decimal(self):
        txt = self.entry_dec.get().strip().replace(",", ".")
        try:
            val = float(txt)
            frac, frac_str = mo.decimal_para_fracao(val)
            self.lbl_dec_resultado.config(text=f"➜  Fração correspondente: {frac_str}")
            if self.on_calculo_realizado:
                self.on_calculo_realizado(f"Decimal {txt}", frac_str, "Conversão Decimal ➔ Fração")
        except ValueError:
            messagebox.showerror("Valor Inválido", "Por favor, digite um número decimal válido (ex: 0.75 ou 1.5).")

    def carregar_do_historico(self, item):
        """Carrega uma fração ou decimal selecionado do histórico."""
        val = item.resultado.lstrip("=").strip()
        if "/" in val:
            try:
                partes = val.split("/")
                self.entry_num1.delete(0, "end")
                self.entry_num1.insert(0, partes[0].strip())
                self.entry_den1.delete(0, "end")
                self.entry_den1.insert(0, partes[1].strip())
            except Exception:
                pass
        else:
            self.entry_dec.delete(0, "end")
            self.entry_dec.insert(0, val)
