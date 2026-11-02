"""
Módulo da Interface da Calculadora
Implementa a tela da calculadora com suporte a adição, subtração, multiplicação,
divisão, porcentagem, exponenciação, radiciação, conversão e inversão de frações.
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

import theme as th
import math_operations as mo
from converters import formatar_numero


class CalculadoraView(tk.Frame):
    """
    Tela responsiva da Calculadora moderna e completa.
    """
    def __init__(
        self,
        parent,
        navegar_para_fracoes: Callable = None,
        on_calculo_realizado: Optional[Callable[[str, str, str], None]] = None
    ):
        super().__init__(parent, bg=th.BG_MAIN)
        self.navegar_para_fracoes = navegar_para_fracoes
        self.on_calculo_realizado = on_calculo_realizado
        
        self.expressao_str = ""
        self.entrada_atual = "0"
        self.resultado_anterior = None
        self.novo_numero = True
        self.modo_fracao = False
        
        self._construir_interface()
        self._configurar_responsividade()

    def _construir_interface(self):
        # Container centralizado em formato de cartão acolhedor
        self.card = tk.Frame(
            self,
            bg=th.BG_CARD,
            bd=1,
            relief="solid",
            highlightthickness=1,
            highlightbackground=th.BORDER_COLOR,
            padx=20,
            pady=20
        )
        self.card.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Cabeçalho da Calculadora
        header_frame = tk.Frame(self.card, bg=th.BG_CARD)
        header_frame.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 10))

        lbl_titulo = tk.Label(
            header_frame,
            text="Calculadora Completa",
            font=th.FONT_TITLE,
            fg=th.BTN_NUM_TEXT,
            bg=th.BG_CARD
        )
        lbl_titulo.pack(side="left")

        lbl_subtitulo = tk.Label(
            header_frame,
            text="Aritmética, Porcentagem, Potências, Raízes e Frações",
            font=th.FONT_SUBTITLE,
            fg=th.SIDEBAR_MUTED,
            bg=th.BG_CARD
        )
        lbl_subtitulo.pack(side="left", padx=(10, 0), pady=(4, 0))

        # Visor acolhedor da Calculadora
        self.display_frame = tk.Frame(
            self.card,
            bg="#F1F5F9",
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#CBD5E1",
            padx=15,
            pady=12
        )
        self.display_frame.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 16))

        # Linha superior do visor: Expressão em andamento
        self.lbl_expressao = tk.Label(
            self.display_frame,
            text="",
            font=th.FONT_CALC_EXPR,
            fg="#64748B",
            bg="#F1F5F9",
            anchor="e"
        )
        self.lbl_expressao.pack(fill="x")

        # Linha inferior do visor: Entrada principal ou resultado
        self.lbl_display = tk.Label(
            self.display_frame,
            text="0",
            font=th.FONT_CALC_DISPLAY,
            fg="#0F172A",
            bg="#F1F5F9",
            anchor="e"
        )
        self.lbl_display.pack(fill="x")

        # Linha auxiliar do visor (para feedback de frações / mensagens amigáveis)
        self.lbl_info = tk.Label(
            self.display_frame,
            text="Dica: Use os botões da tela ou o teclado físico.",
            font=(th.FONT_FAMILY, 9),
            fg="#94A3B8",
            bg="#F1F5F9",
            anchor="e"
        )
        self.lbl_info.pack(fill="x", pady=(2, 0))

        # Layout dos Botões
        # Linha 2 a 7: Grid de botões
        # Definição dos botões: (texto, row, col, tipo, comando, colspan)
        botoes = [
            # Linha 1 de Funções
            ("C", 2, 0, "clear", self.limpar_tudo, 1),
            ("CE", 2, 1, "clear", self.limpar_entrada, 1),
            ("⌫", 2, 2, "clear", self.apagar_ultimo, 1),
            ("(", 2, 3, "op", lambda: self.inserir_simbolo("("), 1),
            (")", 2, 4, "op", lambda: self.inserir_simbolo(")"), 1),

            # Linha 2 de Funções Científicas e Frações
            ("x²", 3, 0, "special", self.calcular_quadrado, 1),
            ("xʸ", 3, 1, "special", lambda: self.inserir_operador("^"), 1),
            ("√x", 3, 2, "special", self.calcular_raiz_quadrada, 1),
            ("¹/x", 3, 3, "special", self.calcular_inverso, 1),
            ("a/b", 3, 4, "special", self.converter_para_fracao, 1),

            # Linha 3
            ("%", 4, 0, "special", self.calcular_porcentagem_acao, 1),
            ("7", 4, 1, "num", lambda: self.inserir_digito("7"), 1),
            ("8", 4, 2, "num", lambda: self.inserir_digito("8"), 1),
            ("9", 4, 3, "num", lambda: self.inserir_digito("9"), 1),
            ("÷", 4, 4, "op", lambda: self.inserir_operador("÷"), 1),

            # Linha 4
            ("ⁿ√x", 5, 0, "special", self.iniciar_raiz_enesima, 1),
            ("4", 5, 1, "num", lambda: self.inserir_digito("4"), 1),
            ("5", 5, 2, "num", lambda: self.inserir_digito("5"), 1),
            ("6", 5, 3, "num", lambda: self.inserir_digito("6"), 1),
            ("×", 5, 4, "op", lambda: self.inserir_operador("×"), 1),

            # Linha 5
            ("±", 6, 0, "num", self.inverter_sinal, 1),
            ("1", 6, 1, "num", lambda: self.inserir_digito("1"), 1),
            ("2", 6, 2, "num", lambda: self.inserir_digito("2"), 1),
            ("3", 6, 3, "num", lambda: self.inserir_digito("3"), 1),
            ("-", 6, 4, "op", lambda: self.inserir_operador("-"), 1),

            # Linha 6
            ("0", 7, 0, "num", lambda: self.inserir_digito("0"), 1),
            (",", 7, 1, "num", self.inserir_virgula, 1),
            ("+", 7, 2, "op", lambda: self.inserir_operador("+"), 1),
            ("=", 7, 3, "equal", self.calcular_resultado, 2),
        ]

        self.botoes_ref = {}
        for texto, r, c, tipo, cmd, cspan in botoes:
            btn = self._criar_botao(self.card, texto, tipo, cmd)
            btn.grid(row=r, column=c, columnspan=cspan, sticky="nsew", padx=4, pady=4)
            self.botoes_ref[texto] = btn

    def _configurar_responsividade(self):
        # Responsividade do container principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Responsividade do cartão
        self.card.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="calc_col")
        # Linha 0 (header) e 1 (display) não expandem tanto quanto os botões
        self.card.grid_rowconfigure(0, weight=0)
        self.card.grid_rowconfigure(1, weight=1)
        # Linhas dos botões (2 a 7) expandem igualmente
        for r in range(2, 8):
            self.card.grid_rowconfigure(r, weight=2, uniform="calc_row")

    def _criar_botao(self, parent, texto: str, tipo: str, comando: Callable) -> tk.Button:
        if tipo == "num":
            bg, bg_hover, fg = th.BTN_NUM_BG, th.BTN_NUM_HOVER, th.BTN_NUM_TEXT
        elif tipo == "op":
            bg, bg_hover, fg = th.BTN_OP_BG, th.BTN_OP_HOVER, th.BTN_OP_TEXT
        elif tipo == "special":
            bg, bg_hover, fg = th.BTN_SPECIAL_BG, th.BTN_SPECIAL_HOVER, th.BTN_SPECIAL_TEXT
        elif tipo == "clear":
            bg, bg_hover, fg = th.BTN_CLEAR_BG, th.BTN_CLEAR_HOVER, th.BTN_CLEAR_TEXT
        elif tipo == "equal":
            bg, bg_hover, fg = th.PRIMARY, th.PRIMARY_HOVER, th.PRIMARY_TEXT
        else:
            bg, bg_hover, fg = th.BTN_NUM_BG, th.BTN_NUM_HOVER, th.BTN_NUM_TEXT

        btn = tk.Button(
            parent,
            text=texto,
            font=th.FONT_BTN_CALC,
            bg=bg,
            fg=fg,
            activebackground=bg_hover,
            activeforeground=fg,
            bd=1,
            relief="flat",
            highlightthickness=1,
            highlightbackground=th.BORDER_COLOR,
            cursor="hand2",
            command=comando
        )

        # Efeito de hover acolhedor
        btn.bind("<Enter>", lambda e: btn.config(bg=bg_hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # ========================================================================
    # LÓGICA E AÇÕES DA CALCULADORA
    # ========================================================================

    def _atualizar_display(self):
        # Exibe texto no visor principal
        self.lbl_display.config(text=self.entrada_atual)
        self.lbl_expressao.config(text=self.expressao_str)

    def inserir_digito(self, digito: str):
        if self.novo_numero or self.entrada_atual == "0" or "Erro" in self.entrada_atual:
            self.entrada_atual = digito
            self.novo_numero = False
        else:
            if len(self.entrada_atual) < 18:
                self.entrada_atual += digito
        self.modo_fracao = False
        self.lbl_info.config(text="")
        self._atualizar_display()

    def inserir_virgula(self):
        if self.novo_numero or "Erro" in self.entrada_atual:
            self.entrada_atual = "0,"
            self.novo_numero = False
        elif "," not in self.entrada_atual:
            self.entrada_atual += ","
        self._atualizar_display()

    def inserir_operador(self, operador: str):
        if "Erro" in self.entrada_atual:
            self.limpar_tudo()
            return
        
        # Converte vírgula para número utilizável
        val = self.entrada_atual.replace(",", ".")
        
        # Adiciona à expressão
        if self.expressao_str and self.expressao_str.endswith((" + ", " - ", " × ", " ÷ ", " ^ ")):
            if self.novo_numero:
                # Troca apenas o último operador se o usuário clicar em outro
                self.expressao_str = self.expressao_str[:-3] + f" {operador} "
                self._atualizar_display()
                return

        self.expressao_str += f"{self.entrada_atual} {operador} "
        self.novo_numero = True
        self.lbl_info.config(text="")
        self._atualizar_display()

    def inserir_simbolo(self, simbolo: str):
        if simbolo == "(":
            self.expressao_str += " ( "
            self.novo_numero = True
        elif simbolo == ")":
            self.expressao_str += f"{self.entrada_atual} ) "
            self.novo_numero = True
        self._atualizar_display()

    def apagar_ultimo(self):
        if self.novo_numero or "Erro" in self.entrada_atual:
            return
        if len(self.entrada_atual) > 1:
            self.entrada_atual = self.entrada_atual[:-1]
        else:
            self.entrada_atual = "0"
            self.novo_numero = True
        self._atualizar_display()

    def limpar_entrada(self):
        self.entrada_atual = "0"
        self.novo_numero = True
        self._atualizar_display()

    def limpar_tudo(self):
        self.expressao_str = ""
        self.entrada_atual = "0"
        self.novo_numero = True
        self.resultado_anterior = None
        self.lbl_info.config(text="Calculadora pronta.")
        self._atualizar_display()

    def inverter_sinal(self):
        if self.entrada_atual == "0" or "Erro" in self.entrada_atual:
            return
        if self.entrada_atual.startswith("-"):
            self.entrada_atual = self.entrada_atual[1:]
        else:
            self.entrada_atual = "-" + self.entrada_atual
        self._atualizar_display()

    def calcular_resultado(self):
        if "Erro" in self.entrada_atual:
            self.limpar_tudo()
            return

        expressao_completa = self.expressao_str + self.entrada_atual
        if not expressao_completa.strip():
            return

        resultado = mo.avaliar_expressao_segura(expressao_completa)
        if isinstance(resultado, str) and "Erro" in resultado:
            self.lbl_info.config(text=resultado)
            self.entrada_atual = resultado
            self.expressao_str = ""
            self.novo_numero = True
        else:
            self.lbl_expressao.config(text=f"{expressao_completa} =")
            self.resultado_anterior = resultado
            self.entrada_atual = formatar_numero(resultado)
            self.expressao_str = ""
            self.novo_numero = True
            
            # Mostra dica de conversão em fração
            frac, frac_str = mo.decimal_para_fracao(resultado)
            if frac.denominator != 1:
                self.lbl_info.config(text=f"Equivalente em fração simplificada: {frac_str}")
            else:
                self.lbl_info.config(text="Cálculo concluído com sucesso!")

            # Registra no histórico da Calculadora
            if self.on_calculo_realizado:
                detalhe = f"Fração: {frac_str}" if frac.denominator != 1 else ""
                self.on_calculo_realizado(expressao_completa, self.entrada_atual, detalhe)
        
        self.lbl_display.config(text=self.entrada_atual)

    # Operações de Porcentagem, Potência, Raiz e Fração
    def calcular_porcentagem_acao(self):
        """
        Calcula porcentagem de acordo com o contexto:
        Se houver uma expressão como '200 + 10 %', calcula 10% de 200.
        Se isolado, calcula número / 100.
        """
        try:
            val_atual = float(self.entrada_atual.replace(",", "."))
            if self.expressao_str:
                # Pega a base anterior
                partes = self.expressao_str.strip().split()
                if partes:
                    try:
                        base = float(partes[0].replace(",", "."))
                        op = partes[1] if len(partes) > 1 else "+"
                        
                        if op in ("+", "-"):
                            # Ex: 200 + 10% -> 10% de 200 = 20
                            pct = mo.calcular_porcentagem(base, val_atual, "taxa")
                            self.entrada_atual = formatar_numero(pct)
                            expr_info = f"{val_atual}% de {formatar_numero(base)}"
                            self.lbl_info.config(text=f"{expr_info} = {self.entrada_atual}")
                            if self.on_calculo_realizado:
                                self.on_calculo_realizado(expr_info, self.entrada_atual, "")
                            self._atualizar_display()
                            return
                    except Exception:
                        pass
            
            # Isolado: converte para porcentagem decimal (ex: 25 -> 0,25)
            res = val_atual / 100.0
            self.entrada_atual = formatar_numero(res)
            self.lbl_info.config(text=f"{val_atual}% = {self.entrada_atual}")
            if self.on_calculo_realizado:
                self.on_calculo_realizado(f"{val_atual}%", self.entrada_atual, "")
            self.novo_numero = True
            self._atualizar_display()
        except ValueError:
            self.lbl_info.config(text="Erro: Valor inválido para porcentagem!")

    def calcular_quadrado(self):
        """Eleva o número atual ao quadrado (x²)."""
        try:
            val = float(self.entrada_atual.replace(",", "."))
            res = mo.exponenciacao(val, 2)
            if isinstance(res, str):
                self.entrada_atual = res
            else:
                expr = f"({formatar_numero(val)})²"
                res_fmt = formatar_numero(res)
                self.lbl_info.config(text=f"{expr} = {res_fmt}")
                self.entrada_atual = res_fmt
                self.novo_numero = True
                if self.on_calculo_realizado:
                    self.on_calculo_realizado(expr, res_fmt, "")
            self._atualizar_display()
        except Exception:
            self.lbl_info.config(text="Erro ao calcular quadrado.")

    def calcular_raiz_quadrada(self):
        """Calcula a raiz quadrada (√x)."""
        try:
            val = float(self.entrada_atual.replace(",", "."))
            res = mo.radiciacao(val, 2)
            if isinstance(res, str):
                self.lbl_info.config(text=res)
                self.entrada_atual = res
            else:
                expr = f"√({formatar_numero(val)})"
                res_fmt = formatar_numero(res)
                self.lbl_info.config(text=f"{expr} = {res_fmt}")
                self.entrada_atual = res_fmt
                self.novo_numero = True
                if self.on_calculo_realizado:
                    self.on_calculo_realizado(expr, res_fmt, "")
            self._atualizar_display()
        except Exception:
            self.lbl_info.config(text="Erro ao calcular raiz quadrada.")

    def iniciar_raiz_enesima(self):
        """Prepara o operador de raiz n-ésima."""
        # Se expressao for A ⁿ√ B -> A^(1/B)
        self.inserir_operador("^(1/")
        self.lbl_info.config(text="Digite o índice da raiz e feche o parêntese ')'")

    def calcular_inverso(self):
        """Calcula a fração inversa 1/x."""
        try:
            val = float(self.entrada_atual.replace(",", "."))
            if val == 0:
                self.lbl_info.config(text="Erro: Divisão por zero!")
                self.entrada_atual = "Erro: Divisão por zero!"
            else:
                res = 1.0 / val
                expr = f"1 / ({formatar_numero(val)})"
                res_fmt = formatar_numero(res)
                self.lbl_info.config(text=f"{expr} = {res_fmt}")
                self.entrada_atual = res_fmt
                self.novo_numero = True
                if self.on_calculo_realizado:
                    self.on_calculo_realizado(expr, res_fmt, "")
            self._atualizar_display()
        except Exception:
            self.lbl_info.config(text="Erro ao calcular inverso fracionário.")

    def converter_para_fracao(self):
        """
        Converte o número no visor em fração simplificada ou vice-versa.
        """
        try:
            if "/" in self.entrada_atual:
                # Converte fração para decimal
                partes = self.entrada_atual.split("/")
                num, den = float(partes[0]), float(partes[1])
                res = num / den
                res_fmt = formatar_numero(res)
                expr = f"Fração {partes[0]}/{partes[1]}"
                self.entrada_atual = res_fmt
                self.lbl_info.config(text=f"{expr} em decimal: {res_fmt}")
                if self.on_calculo_realizado:
                    self.on_calculo_realizado(expr, res_fmt, "Conversão Fração ➔ Decimal")
            else:
                val = float(self.entrada_atual.replace(",", "."))
                frac, frac_str = mo.decimal_para_fracao(val)
                expr = f"Decimal {formatar_numero(val)}"
                self.entrada_atual = frac_str
                self.lbl_info.config(text=f"Fração irredutível: {frac_str} (MDC aplicado)")
                if self.on_calculo_realizado:
                    self.on_calculo_realizado(expr, frac_str, "Conversão Decimal ➔ Fração")
            self.novo_numero = True
            self._atualizar_display()
        except Exception:
            self.lbl_info.config(text="Erro ao converter fração.")

    def carregar_do_historico(self, item):
        """
        Carrega o resultado de um item do histórico diretamente no visor da calculadora.
        """
        val_limpo = item.resultado.lstrip("=").strip()
        self.entrada_atual = val_limpo
        self.expressao_str = ""
        self.novo_numero = True
        self.lbl_info.config(text=f"Carregado do histórico: {item.expressao} = {item.resultado}")
        self._atualizar_display()

    def processar_tecla(self, evento):
        """Lida com teclas físicas digitadas pelo usuário."""
        char = evento.char
        keysym = evento.keysym

        if char in "0123456789":
            self.inserir_digito(char)
        elif char in (",", "."):
            self.inserir_virgula()
        elif char == "+":
            self.inserir_operador("+")
        elif char == "-":
            self.inserir_operador("-")
        elif char == "*":
            self.inserir_operador("×")
        elif char == "/":
            self.inserir_operador("÷")
        elif char == "^":
            self.inserir_operador("^")
        elif char == "%":
            self.calcular_porcentagem_acao()
        elif char in ("(", ")"):
            self.inserir_simbolo(char)
        elif keysym in ("Return", "KP_Enter") or char == "=":
            self.calcular_resultado()
        elif keysym == "BackSpace":
            self.apagar_ultimo()
        elif keysym == "Escape":
            self.limpar_tudo()
