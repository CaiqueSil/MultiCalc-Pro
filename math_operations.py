"""
Módulo de Operações Matemáticas
Contém as funções matemáticas puras com validações, tratamento de erros
e suporte a números reais, frações e avaliador seguro de expressões.
"""

import ast
import math
import operator
from fractions import Fraction
from typing import Tuple, Union


# Operadores seguros permitidos no avaliador de expressões
OPERADORES_SEGUROS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def somar(a: float, b: float) -> float:
    """Retorna a soma de dois números."""
    return a + b


def subtrair(a: float, b: float) -> float:
    """Retorna a diferença entre dois números."""
    return a - b


def multiplicar(a: float, b: float) -> float:
    """Retorna o produto de dois números."""
    return a * b


def dividir(a: float, b: float) -> Union[float, str]:
    """
    Retorna a divisão do primeiro número pelo segundo.
    Previne o erro matemático fatal de divisão por zero.
    """
    if b == 0:
        return "Erro: Não é possível dividir por zero!"
    return a / b


def calcular_porcentagem(valor: float, taxa: float, tipo: str = "taxa") -> float:
    """
    Cálculos de porcentagem:
    - 'taxa': calcula taxa% de um valor (ex: 15% de 200 = 30)
    - 'valor_sobre_total': quanto o valor representa percentualmente do total (ex: 50 de 200 = 25%)
    - 'adicionar_taxa': valor + taxa% (ex: 100 + 10% = 110)
    - 'descontar_taxa': valor - taxa% (ex: 100 - 10% = 90)
    """
    if tipo == "taxa":
        return (valor * taxa) / 100.0
    elif tipo == "valor_sobre_total":
        if taxa == 0:
            raise ValueError("O total não pode ser zero para calcular proporção percentual!")
        return (valor / taxa) * 100.0
    elif tipo == "adicionar_taxa":
        return valor + (valor * (taxa / 100.0))
    elif tipo == "descontar_taxa":
        return valor - (valor * (taxa / 100.0))
    else:
        return (valor * taxa) / 100.0


def exponenciacao(base: float, expoente: float) -> Union[float, str]:
    """
    Calcula base elevada ao expoente (base^expoente).
    Trata casos de números negativos com expoente fracionário e overflow.
    """
    try:
        if base == 0 and expoente < 0:
            return "Erro: Não é possível dividir por zero!"
        
        # Base negativa com expoente fracionário
        if base < 0 and not expoente.is_integer():
            frac = Fraction(str(expoente)).limit_denominator(1000)
            if frac.denominator % 2 == 1:
                res = math.pow(abs(base), expoente)
                return -res if frac.numerator % 2 != 0 else res
            return "Erro: Raiz par de número negativo não pertence aos reais!"
            
        return math.pow(base, expoente)
    except OverflowError:
        return "Erro: Valor muito grande (Estouro numérico)!"
    except Exception as e:
        return f"Erro no cálculo: {str(e)}"


def radiciacao(radicando: float, indice: float = 2.0) -> Union[float, str]:
    """
    Calcula a raiz de índice 'indice' do radicando.
    Por padrão calcula a raiz quadrada (indice = 2).
    """
    if indice == 0:
        return "Erro: O índice da raiz não pode ser zero!"
    
    if radicando == 0:
        return 0.0

    if radicando < 0:
        if indice.is_integer() and int(indice) % 2 != 0:
            return -math.pow(abs(radicando), 1.0 / indice)
        return "Erro: Raiz par de número negativo não pertence aos reais!"
    
    try:
        return math.pow(radicando, 1.0 / indice)
    except OverflowError:
        return "Erro: Valor muito grande (Estouro numérico)!"
    except Exception as e:
        return f"Erro no cálculo: {str(e)}"


def calcular_fracao(
    num1: int, den1: int,
    operacao: str,
    num2: int = 1, den2: int = 1
) -> Union[Tuple[Fraction, str, float], str]:
    """
    Realiza cálculos com frações exatas usando Fraction.
    Retorna uma tupla (fracao_resultante, representacao_mista, valor_decimal)
    ou mensagem de erro em caso de denomidador zero.
    """
    if den1 == 0 or den2 == 0:
        return "Erro: O denominador de uma fração não pode ser zero!"
    
    try:
        f1 = Fraction(num1, den1)
        f2 = Fraction(num2, den2)
        
        if operacao in ("somar", "+"):
            resultado = f1 + f2
        elif operacao in ("subtrair", "-"):
            resultado = f1 - f2
        elif operacao in ("multiplicar", "*", "×"):
            resultado = f1 * f2
        elif operacao in ("dividir", "/", "÷"):
            if f2 == 0:
                return "Erro: Não é possível dividir por uma fração nula!"
            resultado = f1 / f2
        elif operacao == "simplificar":
            resultado = f1
        else:
            return "Erro: Operação inválida!"
        
        # Representação mista se imprópria (ex: 7/4 = 1 e 3/4)
        misto = ""
        if abs(resultado.numerator) >= abs(resultado.denominator) and resultado.denominator != 1:
            inteiro = resultado.numerator // resultado.denominator
            resto = abs(resultado.numerator % resultado.denominator)
            if resto != 0:
                misto = f"{inteiro} e {resto}/{resultado.denominator}"
        
        return (resultado, misto, float(resultado))
    except Exception as e:
        return f"Erro ao processar fração: {str(e)}"


def decimal_para_fracao(decimal_val: float) -> Tuple[Fraction, str]:
    """
    Converte um valor decimal em sua representação fracionária irredutível.
    """
    f = Fraction(str(decimal_val)).limit_denominator(1000000)
    return f, f"{f.numerator}/{f.denominator}"


def _avaliar_ast_node(node: ast.AST) -> float:
    """Avaliador recursivo seguro para nós da AST."""
    if isinstance(node, ast.Expression):
        return _avaliar_ast_node(node.body)
    elif isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Constante não numérica não permitida.")
    elif isinstance(node, ast.BinOp):
        op_tipo = type(node.op)
        if op_tipo not in OPERADORES_SEGUROS:
            raise ValueError(f"Operador não permitido: {op_tipo}")
        left = _avaliar_ast_node(node.left)
        right = _avaliar_ast_node(node.right)
        
        if op_tipo == ast.Div:
            if right == 0:
                raise ZeroDivisionError("Divisão por zero!")
            return left / right
        elif op_tipo == ast.Pow:
            return float(exponenciacao(left, right))
        return float(OPERADORES_SEGUROS[op_tipo](left, right))
    elif isinstance(node, ast.UnaryOp):
        op_tipo = type(node.op)
        if op_tipo not in OPERADORES_SEGUROS:
            raise ValueError(f"Operador unário não permitido: {op_tipo}")
        operand = _avaliar_ast_node(node.operand)
        return float(OPERADORES_SEGUROS[op_tipo](operand))
    else:
        raise ValueError(f"Expressão inválida ou não suportada: {type(node).__name__}")


def avaliar_expressao_segura(expressao: str) -> Union[float, str]:
    """
    Avalia com segurança matemática uma expressão textual.
    Suporta: +, -, *, /, ^ (potência), % (módulo ou percentual), parênteses.
    Substitui símbolos comuns como '×' por '*', '÷' por '/', '^' por '**'.
    """
    try:
        # Higienização da expressão
        limpa = (
            expressao.replace("×", "*")
            .replace("÷", "/")
            .replace("^", "**")
            .replace(",", ".")
            .strip()
        )
        
        if not limpa:
            return 0.0

        tree = ast.parse(limpa, mode="eval")
        resultado = _avaliar_ast_node(tree)
        return resultado
    except ZeroDivisionError:
        return "Erro: Não é possível dividir por zero!"
    except OverflowError:
        return "Erro: Valor muito grande (Estouro)!"
    except Exception as e:
        return f"Erro de sintaxe na expressão!"
