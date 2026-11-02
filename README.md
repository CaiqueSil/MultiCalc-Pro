# 🧮 MultiCalc Pro — Calculadora & Conversores (Python + Tkinter)
> **Desafio Alura**: Aplicação de calculadora refatorada com operações matemáticas avançadas, interface gráfica moderna em Tkinter, conversores de volume e comprimento e **painel lateral direito de histórico isolado por funcionalidade**.

---

## 🌟 Principais Recursos

### 1. 🧮 Calculadora Completa & Científica
- **Operações Básicas**: Adição (`+`), Subtração (`-`), Multiplicação (`×`), Divisão (`÷` com proteção contra divisão por zero).
- **Porcentagem (`%`)**:
  - Cálculo percentual direto (ex: `25%` = `0,25`).
  - Cálculo contextual (ex: `200 + 10%` = `220`).
- **Exponenciação (`x²` e `xʸ`)**:
  - Elevação rápida ao quadrado.
  - Potências arbitrárias ($a^b$) com suporte a bases negativas e expoentes fracionários.
- **Radiciação (`√x` e `ⁿ√x`)**:
  - Raiz quadrada imediata.
  - Raiz com índice configurável ($\sqrt[n]{x}$).
  - Validação para raízes de números negativos nos reais.
- **Frações na Calculadora**:
  - Inverso fracionário (`¹/x`).
  - Conversão instantânea de números decimais para fração simplificada (`a/b ↔ dec`).
- **Avaliador de Expressões Seguro**: Utiliza a Árvore Sintática Abstrata (`ast`) do Python, permitindo parênteses e prioridade de operadores com máxima segurança (sem `eval` inseguro).
- **Suporte ao Teclado Físico**: Use `0-9`, `+`, `-`, `*`, `/`, `%`, `^`, `Enter`, `Backspace`, `Esc` e parênteses diretamente pelo teclado!

### 2. 🍰 Calculadora de Frações Dedicada
- Entrada visual de frações com **Numerador** e **Denominador**.
- Operações de **Soma**, **Subtração**, **Multiplicação**, **Divisão** e **Simplificação**.
- Exibição de:
  - **Fração Irredutível** (ex: `17/12`).
  - **Forma Mista** (ex: `1 e 5/12`).
  - **Valor Decimal** aproximado (ex: `~1,4167`).
- **Conversor Rápido Decimal ⇄ Fração**: Digite qualquer número com vírgula/ponto e obtenha a fração exata simplificada.

### 3. 📏 Conversor de Comprimento
Suporte completo às **11 unidades solicitadas**:
- `mm` (Milímetro)
- `cm` (Centímetro)
- `dm` (Decímetro)
- `m` (Metro — base padrão)
- `dam` (Decâmetro)
- `hm` (Hectômetro)
- `km` (Quilômetro)
- `polegadas` (Polegadas — *in*)
- `pés` (Pés — *ft*)
- `jardas` (Jardas — *yd*)
- `milhas` (Milhas — *mi*)
- **Diferencial**: Conversão instantânea ao digitar, botão de inversão rápida (`⇄`), botão de cópia (`📋`) e **tabela simultânea** exibindo a equivalência em todas as 11 unidades ao mesmo tempo!

### 4. 🧊 Conversor de Volume
Suporte às unidades solicitadas:
- `cm³` (Centímetro cúbico)
- `L` (Litro)
- `m³` (Metro cúbico)
- *(Com suporte complementar a `mL`, `dm³` e `mm³`)*
- Visualização de equivalência simultânea e dicas didáticas ($1\text{ m}^3 = 1.000\text{ L} = 1.000.000\text{ cm}^3$).

### 5. 🕒 Painel Lateral Direito — Histórico Isolado por Funcionalidade
- **Histórico Separado**: Cada tela possui seu próprio histórico de cálculos independente:
  - **Calculadora**: Histórico de contas aritméticas, potências, raízes, porcentagens e conversões de frações.
  - **Frações**: Histórico de operações fracionárias ($A/B \pm C/D$), simplificações e conversões.
  - **Comprimento**: Histórico de distâncias convertidas (ex: `5 km ➔ 5.000 m`).
  - **Volume**: Histórico de volumes convertidos (ex: `2,5 m³ ➔ 2.500 L`).
- **Cards Interativos**:
  - Exibe horário, expressão e resultado em destaque.
  - **Clique no card**: Copia o valor para a área de transferência com aviso visual e o restaura no visor/campo da tela ativa.
- **Limpeza Isolada**: O botão `🗑️ Limpar` apaga apenas os cálculos da funcionalidade ativa, preservando os demais.
- **Botão Ocultar/Exibir**: Botão para recolher ou expandir a barra lateral de histórico conforme a preferência de tela do usuário.

---

## 🎨 Design e Usabilidade
- **Acolhedor e Moderno**: Paleta de cores *Warm Slate*, tipografia limpa, bordas suaves e efeitos táteis de *hover*.
- **100% Responsivo**: Layout construído com pesos proporcionais (`weight`) e alinhamento flexível que se ajusta a qualquer tamanho de tela e redimensionamento.
- **Português do Brasil (PT-BR)**: Todos os textos, explicações, mensagens de erro e convenções numéricas (vírgula decimal) em português.
- **Duas Barras Laterais Inteligentes**: 
  - Lateral Esquerda: Menu de navegação rápido entre módulos.
  - Lateral Direita: Histórico dinâmico e contextual.

---

## 📂 Estrutura do Projeto

```text
Calculadora_Python/
│
├── main.py              # Ponto de entrada (GUI Tkinter ou CLI alternativa)
├── app.py               # Janela principal, sidebar de navegação e integração do histórico
├── theme.py             # Paleta de cores, tipografia e estilos visuais
├── math_operations.py   # Lógica matemática pura (+, -, *, /, %, potências, raízes, frações)
├── converters.py        # Fatores e funções de conversão de Comprimento e Volume
├── history_manager.py   # Gerenciador central de histórico isolado por funcionalidade
├── history_panel.py     # Barra lateral direita com cards de histórico interativos
├── calc_view.py         # Tela da Calculadora padrão e avançada
├── fractions_view.py    # Tela dedicada para operações com Frações
├── length_view.py       # Tela do Conversor de Comprimento (11 unidades)
├── volume_view.py       # Tela do Conversor de Volume (cm³, L, m³)
├── test_math.py         # Testes unitários das operações matemáticas e conversores
├── test_gui.py          # Testes de integração da interface gráfica e histórico
└── README.md            # Documentação completa
```

---

## 🚀 Como Executar

### 1. Iniciar a Interface Gráfica (Tkinter)
Execute no terminal:
```bash
python main.py
```
*(ou clique duas vezes em `main.py` no explorador de arquivos)*

### 2. Iniciar no Modo Linha de Comando (CLI Refatorado)
Caso prefira rodar no terminal sem interface gráfica:
```bash
python main.py --cli
```

### 3. Executar os Testes Automatizados
```bash
python test_math.py
python test_gui.py
```
