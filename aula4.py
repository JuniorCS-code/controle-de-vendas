import pandas as pd
import streamlit as st
import plotly.express as px

# Passo 1: criar a tela do sistema

# O símbolo # antes do texto faz o Streamlit exibir o título em tamanho grande. Use ## para título médio e ### para título pequeno.
st.write('# Sistema de Vendas') 

# O pd.read_csv lê esse arquivo e o transforma em uma tabela que o Python consegue manipular
tabela = pd.read_csv('vendas.csv')

# Passo 2: criando o formulário de cadastro

# Cria o título do formulário na sidebar.
st.sidebar.write("## Cadastrar Venda")

# Campo de data com calendário interativo. O usuário clica e escolhe a data. 
# O resultado fica salvo na variável data.
data = st.sidebar.date_input('Data')

# Cria uma lista suspensa (dropdown) com opções fixas para o usuário escolher. 
# O selectbox é perfeito quando há um conjunto limitado de opções.
vendedor = st.sidebar.selectbox('Vendedor', ['', 'Ana', 'Bruno', 'Carla'])

# Outro dropdown, agora para o produto vendido. Funciona igual ao de vendedor.
produto = st.sidebar.selectbox('Produto', ['', 'Notebook', 'Celular', 'Fone'])

# Campo numérico. O step=1 faz o número aumentar e diminuir de 1 em 1
# quando o usuário clica nas setas laterais.
quantidade = st.sidebar.number_input('Quantidade', step=1)

# Campo numérico para o valor da venda. Aceita decimais, como 3500.50.
valor = st.sidebar.number_input('Valor')
# valor_formatado = f"R$ {valor:2f}".replace(",", "v").replace(".", ",").replace("v", ".")

# Cria o botão de cadastro. Quando clicado, a variável botao recebe o valor True. 
# Quando não foi clicado, recebe False.
botao = st.sidebar.button('Cadastrar Venda')

# Passo 3: Salvar a venda na base de dados

# SE o botão foi clicado (botao = True), execute as linhas abaixo.
if botao:

    # Os colchetes criam uma lista — uma "caixinha" que guarda vários valores em sequência. 
    # Aqui estamos guardando em nova_venda todos os dados que o usuário preencheu no formulário.
    nova_venda = [data, vendedor, produto, quantidade, valor]

    # Adiciona a nova venda na próxima linha disponível da tabela. O len(tabela) retorna o número 
    # de linhas existentes, que é o índice da posição onde a nova linha deve entrar.
    tabela.loc[len(tabela)] = nova_venda

    # Salva toda a tabela atualizada de volta no arquivo vendas.csv. 
    # O index=False evita que o Pandas adicione uma coluna extra de numeração no início de cada linha.
    tabela.to_csv('vendas.csv', index=False)

    # Exibe uma caixa verde de sucesso na tela, confirmando ao usuário que a venda foi salva com sucesso.
    st.success('Venda Cadastrada')

# Passo 4: Mostrando a base de dados na tabela

# Cria um subtítulo na página. No Streamlit, o número de # define o tamanho do título.
st.write('## Vendas Cadastradas')

# Exibe a variável tabela como uma tabela interativa na tela do sistema.
# Com o st.dataframe, o usuário pode:
# • Clicar nos cabeçalhos das colunas para ordenar os dados
# • Rolar horizontalmente para ver todas as colunas
# • Visualizar todas as vendas registradas no arquivo de forma clara e organizada
st.dataframe(tabela)

# Passo 5: Criar o Dashboard

# Cria o subtítulo da seção.
st.write('## Dashboard')

# Calculando e exibindo o faturamento total:
# tabela['valor'] — Seleciona apenas a coluna "valor" da tabela. 
# É como clicar numa coluna específica no Excel para trabalhar só com ela.
# .sum() — Soma todos os números dessa coluna. 
# Se a coluna tiver 1000, 2000 e 3500, o resultado será 6500.
soma = tabela['Valor'].sum()

# f'R${soma}' — Isso é um f-string (string formatada). O f antes das aspas permite colocar 
# variáveis dentro do texto usando {}. O Python substitui {soma} pelo valor da variável automaticamente. 
# Exemplo: 'R$6500.0'.
# st.metric — Cria um card visual destacado com um título acima e um valor grande abaixo. 
# É perfeito para indicadores importantes como faturamento total, número de vendas, média por venda, etc.

st.metric('Faturamento Total', f'R${soma}')

# Passo 6: Gráfico de Vendas

# Agora vamos adicionar os gráficos ao dashboard. Vamos criar dois gráficos diferentes usando o 
# Plotly Express (o apelido px que importamos no Passo 1).
# Gráfico de Barras — Vendas por Vendedor:

# Entendendo os parâmetros do px.bar:
# tabela → os dados que vamos usar para montar o gráfico
# x='vendedor' → o eixo horizontal mostra os nomes dos vendedores
# y='valor' → o eixo vertical mostra os valores das vendas
# color='produto' → cada produto recebe uma cor diferente nas barras, 
# criando um gráfico empilhado por produto
grafico = px.bar(tabela, x= 'Vendedor', y= 'Valor', color = 'Produto')

# Exibe o gráfico interativo na tela do sistema
st.plotly_chart(grafico)

# Gráfico de Pizza — Participação por Produto:
# Entendendo os parâmetros do px.pie:
# names='produto' → define os "pedaços" da pizza — um pedaço para cada produto
# values='valor' → define o tamanho de cada pedaço conforme o faturamento do produto
grafico2 = px.pie(tabela, names='Produto', values='Valor')

# Exibe o gráfico interativo na tela do sistema
st.plotly_chart(grafico2)

# Dica: Os gráficos do Plotly são interativos! Passe o mouse sobre barras ou fatias para ver os valores 
# exatos. Clique na legenda para mostrar ou esconder produtos específicos.


