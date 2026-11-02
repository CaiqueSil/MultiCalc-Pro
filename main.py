"""
Ponto de Entrada Principal da Aplicação
Calculadora e Conversores em Python (Tkinter + CLI Refatorada)
Desafio Alura
"""

import sys
import math_operations as mo
import converters as cv


def executar_modo_cli():
    """
    Versão refatorada e expandida do menu via linha de comando (CLI),
    incluindo todas as novas operações: porcentagem, exponenciação, radiciação,
    frações e conversores de volume e comprimento.
    """
    print("=" * 60)
    print("        BEM-VINDO À CALCULADORA & CONVERSORES PYTHON        ")
    print("=" * 60)

    while True:
        print("\nSelecione a funcionalidade desejada:")
        print("  1. Adição (+)")
        print("  2. Subtração (-)")
        print("  3. Multiplicação (*)")
        print("  4. Divisão (/)")
        print("  5. Porcentagem (%)")
        print("  6. Exponenciação (x^y)")
        print("  7. Radiciação (√x)")
        print("  8. Operações com Frações (a/b)")
        print("  9. Conversor de Comprimento (mm, cm, m, km, pol, pés, milhas...)")
        print(" 10. Conversor de Volume (cm³, L, m³...)")
        print(" 11. Sair do programa")

        opcao = input("\nDigite sua escolha (1 a 11): ").strip()

        if opcao == "11":
            print("\nObrigado por utilizar a Calculadora & Conversores! Encerrando...")
            break

        # Operações Aritméticas Básicas (1 a 4)
        if opcao in ("1", "2", "3", "4"):
            try:
                num1 = float(input("Digite o primeiro número: "))
                num2 = float(input("Digite o segundo número: "))
            except ValueError:
                print("Erro: Digite apenas números válidos!")
                continue

            if opcao == "1":
                res = mo.somar(num1, num2)
                print(f"\n>>> Resultado: {num1} + {num2} = {res}")
            elif opcao == "2":
                res = mo.subtrair(num1, num2)
                print(f"\n>>> Resultado: {num1} - {num2} = {res}")
            elif opcao == "3":
                res = mo.multiplicar(num1, num2)
                print(f"\n>>> Resultado: {num1} * {num2} = {res}")
            elif opcao == "4":
                res = mo.dividir(num1, num2)
                print(f"\n>>> Resultado: {res}")

        # 5. Porcentagem
        elif opcao == "5":
            print("\nTipos de cálculo de porcentagem:")
            print("  a. Calcular taxa% sobre um valor (ex: 15% de 200)")
            print("  b. Adicionar taxa% a um valor (ex: 100 + 10%)")
            print("  c. Descontar taxa% de um valor (ex: 100 - 10%)")
            print("  d. Proporção percentual (quanto X representa de Y)")
            sub_op = input("Escolha (a/b/c/d): ").strip().lower()

            try:
                if sub_op in ("a", "b", "c"):
                    val = float(input("Digite o valor base: "))
                    taxa = float(input("Digite a taxa percentual (%): "))
                    if sub_op == "a":
                        res = mo.calcular_porcentagem(val, taxa, "taxa")
                        print(f"\n>>> {taxa}% de {val} = {res}")
                    elif sub_op == "b":
                        res = mo.calcular_porcentagem(val, taxa, "adicionar_taxa")
                        print(f"\n>>> {val} + {taxa}% = {res}")
                    elif sub_op == "c":
                        res = mo.calcular_porcentagem(val, taxa, "descontar_taxa")
                        print(f"\n>>> {val} - {taxa}% = {res}")
                elif sub_op == "d":
                    val = float(input("Digite a parte (X): "))
                    total = float(input("Digite o total (Y): "))
                    res = mo.calcular_porcentagem(val, total, "valor_sobre_total")
                    print(f"\n>>> {val} representa {res:.2f}% de {total}")
                else:
                    print("Opção inválida.")
            except ValueError as e:
                print(f"Erro: {e}")

        # 6. Exponenciação
        elif opcao == "6":
            try:
                base = float(input("Digite a base: "))
                expoente = float(input("Digite o expoente: "))
                res = mo.exponenciacao(base, expoente)
                print(f"\n>>> Resultado: {base} ^ {expoente} = {res}")
            except ValueError:
                print("Erro: Digite apenas números válidos!")

        # 7. Radiciação
        elif opcao == "7":
            try:
                radicando = float(input("Digite o radicando (número sob a raiz): "))
                indice_str = input("Digite o índice da raiz (pressione Enter para raiz quadrada 2): ").strip()
                indice = float(indice_str) if indice_str else 2.0
                res = mo.radiciacao(radicando, indice)
                print(f"\n>>> Raiz de índice {indice} de {radicando} = {res}")
            except ValueError:
                print("Erro: Digite apenas números válidos!")

        # 8. Frações
        elif opcao == "8":
            try:
                print("\nOperação com Frações:")
                print("Digite a Fração 1:")
                n1 = int(input("  Numerador 1: "))
                d1 = int(input("  Denominador 1: "))
                op_f = input("Operação (+, -, *, / ou 's' para simplificar): ").strip()

                if op_f.lower() == "s":
                    res = mo.calcular_fracao(n1, d1, "simplificar")
                else:
                    print("Digite a Fração 2:")
                    n2 = int(input("  Numerador 2: "))
                    d2 = int(input("  Denominador 2: "))
                    res = mo.calcular_fracao(n1, d1, op_f, n2, d2)

                if isinstance(res, str):
                    print(f"\n>>> {res}")
                else:
                    frac, misto, dec = res
                    misto_info = f" | Forma Mista: {misto}" if misto else ""
                    print(f"\n>>> Fração Irredutível: {frac.numerator}/{frac.denominator}{misto_info} | Decimal: {dec}")
            except ValueError:
                print("Erro: Numeradores e denominadores devem ser inteiros!")

        # 9. Conversor de Comprimento
        elif opcao == "9":
            print("\nUnidades disponíveis:", ", ".join(cv.UNIDADES_COMPRIMENTO.keys()))
            try:
                val = float(input("Digite o valor a converter: "))
                u_origem = input("Unidade de origem: ").strip()
                u_destino = input("Unidade de destino: ").strip()
                res = cv.converter_comprimento(val, u_origem, u_destino)
                print(f"\n>>> {cv.formatar_numero(val)} {u_origem} = {cv.formatar_numero(res)} {u_destino}")
            except Exception as e:
                print(f"Erro na conversão: {e}")

        # 10. Conversor de Volume
        elif opcao == "10":
            print("\nUnidades disponíveis:", ", ".join(cv.UNIDADES_VOLUME.keys()))
            try:
                val = float(input("Digite o volume a converter: "))
                u_origem = input("Unidade de origem (ex: m³, L, cm³): ").strip()
                u_destino = input("Unidade de destino (ex: m³, L, cm³): ").strip()
                res = cv.converter_volume(val, u_origem, u_destino)
                print(f"\n>>> {cv.formatar_numero(val)} {u_origem} = {cv.formatar_numero(res)} {u_destino}")
            except Exception as e:
                print(f"Erro na conversão: {e}")

        else:
            print("Opção inválida! Escolha um número de 1 a 11.")

        repetir = input("\nDeseja realizar outra operação? (s/n): ").strip().lower()
        if repetir != "s":
            print("\nEncerrando a aplicação. Até logo!")
            break


def main():
    # Se o usuário passar flag --cli ou -c, roda o modo terminal
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--cli", "-c", "cli"):
        executar_modo_cli()
        return

    # Caso contrário, inicia a interface gráfica Tkinter moderna
    try:
        from app import iniciar_aplicacao
        iniciar_aplicacao()
    except Exception as e:
        print(f"Aviso: Não foi possível abrir a interface gráfica Tkinter ({e}).")
        print("Iniciando modo linha de comando (CLI) alternativo...\n")
        executar_modo_cli()


if __name__ == "__main__":
    main()
