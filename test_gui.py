"""
Teste de integração da GUI, fluxos do usuário e Histórico separado por funcionalidade.
"""

from app import MultiCalcApp


def testar_gui():
    app = MultiCalcApp()
    app.update_idletasks()

    # 1. Calculadora: 12 + 8 = 20
    calc = app.calc_view
    calc.limpar_tudo()
    calc.inserir_digito("1")
    calc.inserir_digito("2")
    calc.inserir_operador("+")
    calc.inserir_digito("8")
    calc.calcular_resultado()
    assert calc.lbl_display.cget("text") == "20", f"Esperado 20, obtido {calc.lbl_display.cget('text')}"
    print("[OK] Calculadora - Adição básica")

    # 2. Exponenciação: 2 ^ 3 = 8
    calc.limpar_tudo()
    calc.inserir_digito("2")
    calc.inserir_operador("^")
    calc.inserir_digito("3")
    calc.calcular_resultado()
    assert calc.lbl_display.cget("text") == "8", f"Esperado 8, obtido {calc.lbl_display.cget('text')}"
    print("[OK] Calculadora - Exponenciação")

    # 3. Radiciação: √144 = 12
    calc.limpar_tudo()
    calc.inserir_digito("1")
    calc.inserir_digito("4")
    calc.inserir_digito("4")
    calc.calcular_raiz_quadrada()
    assert calc.lbl_display.cget("text") == "12", f"Esperado 12, obtido {calc.lbl_display.cget('text')}"
    print("[OK] Calculadora - Raiz quadrada")

    # 4. Porcentagem: 200 + 10%
    calc.limpar_tudo()
    calc.inserir_digito("2")
    calc.inserir_digito("0")
    calc.inserir_digito("0")
    calc.inserir_operador("+")
    calc.inserir_digito("1")
    calc.inserir_digito("0")
    calc.calcular_porcentagem_acao()
    calc.calcular_resultado()
    assert calc.lbl_display.cget("text") == "220", f"Esperado 220, obtido {calc.lbl_display.cget('text')}"
    print("[OK] Calculadora - Porcentagem contextual")

    # 5. Fração: 0.75 -> 3/4
    calc.limpar_tudo()
    calc.inserir_digito("0")
    calc.inserir_virgula()
    calc.inserir_digito("7")
    calc.inserir_digito("5")
    calc.converter_para_fracao()
    assert calc.lbl_display.cget("text") == "3/4", f"Esperado 3/4, obtido {calc.lbl_display.cget('text')}"
    print("[OK] Calculadora - Conversão para fração")

    # 6. Tela de Frações dedicada: 3/4 + 2/3 = 17/12
    app.navegar_para("fracoes")
    app.update_idletasks()
    frac_view = app.fracoes_view
    frac_view.entry_num1.delete(0, "end")
    frac_view.entry_num1.insert(0, "3")
    frac_view.entry_den1.delete(0, "end")
    frac_view.entry_den1.insert(0, "4")
    frac_view.combo_op.current(0)  # +
    frac_view.entry_num2.delete(0, "end")
    frac_view.entry_num2.insert(0, "2")
    frac_view.entry_den2.delete(0, "end")
    frac_view.entry_den2.insert(0, "3")
    frac_view.calcular_operacao()
    assert "17/12" in frac_view.lbl_res_equacao.cget("text")
    print("[OK] Tela de Frações - Soma de frações")

    # 7. Conversor de Comprimento: 5 km = 5000 m
    app.navegar_para("comprimento")
    app.update_idletasks()
    comp = app.comprimento_view
    comp.entry_valor.delete(0, "end")
    comp.entry_valor.insert(0, "5")
    comp.combo_de.current(comp.chaves_unidades.index("km"))
    comp.combo_para.current(comp.chaves_unidades.index("m"))
    comp.executar_conversao(salvar_historico=True)
    assert "5000 m" in comp.lbl_resultado_grande.cget("text")
    print("[OK] Tela de Comprimento - 5 km para metros")

    # 8. Conversor de Volume: 2 m³ = 2000 L
    app.navegar_para("volume")
    app.update_idletasks()
    vol = app.volume_view
    vol.entry_valor.delete(0, "end")
    vol.entry_valor.insert(0, "2")
    vol.combo_de.current(vol.chaves_unidades.index("m³"))
    vol.combo_para.current(vol.chaves_unidades.index("L"))
    vol.executar_conversao(salvar_historico=True)
    assert "2000 L" in vol.lbl_resultado_grande.cget("text")
    print("[OK] Tela de Volume - 2 m³ para Litros")

    # ========================================================================
    # 9. TESTES DO HISTÓRICO SEPARADO POR FUNCIONALIDADE
    # ========================================================================
    hist_calc = app.history_manager.obter_historico("calculadora")
    hist_frac = app.history_manager.obter_historico("fracoes")
    hist_comp = app.history_manager.obter_historico("comprimento")
    hist_vol = app.history_manager.obter_historico("volume")

    assert len(hist_calc) > 0, "Histórico da calculadora não deve estar vazio"
    assert len(hist_frac) > 0, "Histórico de frações não deve estar vazio"
    assert len(hist_comp) > 0, "Histórico de comprimento não deve estar vazio"
    assert len(hist_vol) > 0, "Histórico de volume não deve estar vazio"

    # Verifica isolamento das categorias
    for item in hist_calc:
        assert item.categoria == "calculadora", f"Item inválido na calculadora: {item}"
    for item in hist_frac:
        assert item.categoria == "fracoes", f"Item inválido em frações: {item}"
    for item in hist_comp:
        assert item.categoria == "comprimento", f"Item inválido em comprimento: {item}"
    for item in hist_vol:
        assert item.categoria == "volume", f"Item inválido em volume: {item}"

    print(f"[OK] Histórico Isolado: Calc ({len(hist_calc)}), Frações ({len(hist_frac)}), Comp ({len(hist_comp)}), Vol ({len(hist_vol)})")

    # 10. Teste de navegação do HistoryPanel
    app.navegar_para("calculadora")
    app.update_idletasks()
    assert app.history_panel.categoria_atual == "calculadora"
    assert app.history_panel.lbl_badge.cget("text") == "Calculadora"

    app.navegar_para("comprimento")
    app.update_idletasks()
    assert app.history_panel.categoria_atual == "comprimento"
    assert app.history_panel.lbl_badge.cget("text") == "Conversor de Comprimento"

    # 11. Teste de limpeza isolada de uma categoria
    qtd_antes_frac = len(app.history_manager.obter_historico("fracoes"))
    app.history_manager.limpar_categoria("calculadora")
    assert len(app.history_manager.obter_historico("calculadora")) == 0, "Histórico de calculadora deveria estar limpo"
    assert len(app.history_manager.obter_historico("fracoes")) == qtd_antes_frac, "Histórico de frações não deveria ser afetado"
    print("[OK] Limpeza isolada de histórico por categoria aprovada")

    # 12. Teste de alternância (toggle) da visibilidade da barra de histórico
    assert app.historico_visivel is True
    app.alternar_painel_historico()
    assert app.historico_visivel is False
    app.alternar_painel_historico()
    assert app.historico_visivel is True
    print("[OK] Alternância de visibilidade do painel de histórico aprovada")

    app.destroy()
    print("\nTODOS OS TESTES DE GUI, INTEGRAÇÃO E HISTÓRICO FORAM APROVADOS COM SUCESSO!")


if __name__ == "__main__":
    testar_gui()
