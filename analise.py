import json
import conn
import plotly.express as px
import plotly.graph_objects as go
"""
O resultado da query traz o total de vendas de produtos para a Araújo e o total
de devoluções que a Araújo faz. A função inserirTotalCompras junta os resultados das
vendas e das devoluções de cada loja
"""
def inserirTotalCompras(row, _vendas):
    id_unidade = int(row['ID'])
    devolucao = _vendas.loc[(id_unidade == _vendas['ID'].astype(int)) & (_vendas['tipoOperacao'] == 'F')]
    if len(devolucao) == 0:
        row['DEVOLUCAO'] = 0
    else:
        row['DEVOLUCAO'] = devolucao['totalOperacao'].values[0]
    
    vendidos = _vendas.loc[(id_unidade == _vendas['ID'].astype(int)) & (_vendas['tipoOperacao'] == 'C')]
    
    if len(vendidos) == 0:
        row['VENDIDOS'] = 0
    else:
        row['VENDIDOS'] = vendidos['totalOperacao'].values[0]
    return row

vendas = conn.buscarProdutos('20230101', '20240101')
order_valor_maior = vendas.sort_values(by=['totalPrecoEvento'], ascending=False)
dezp_monetario = order_valor_maior.iloc[0:10]

order_qtd_maior = vendas.sort_values(by=['qtdEvento'], ascending=False)
dezp_qtd = order_qtd_maior.iloc[0:10]

order_valor_menor = vendas.sort_values(by=['totalPrecoEvento'], ascending=True)
dezm_monetario = order_valor_menor.iloc[0:10]

fig = px.histogram(dezp_monetario, x='nomeProduto', y='totalPrecoEvento')
fig.write_html('tmp.html', auto_open=True)

# fig2 = px.histogram(dezp_qtd, x='nomeProduto', y='qtdEvento')
# fig2.write_html('tmp.html', auto_open=True)


# unidades = conn.callCadastros()

# unidades = unidades.apply(inserirTotalCompras, _vendas = total_lojas, axis=1)
# unidades['TOTAL'] = unidades['VENDIDOS'] - unidades['DEVOLUCAO']
# unidades = unidades.sort_values(by=['FANTASIA'])

# dez_primeiros = unidades.sort_values(by=['TOTAL'], ascending=False)
# primeiro = dez_primeiros.iloc[0:10]
# print(dez_primeiros)
# fig = px.histogram(primeiro, x='FANTASIA', y='TOTAL')

# fig = go.Figure(
#     data=[go.Bar(y=[2, 1, 3])],
#     layout_title_text="A Figure Displayed with fig.show()"
# )

#fig.write_html('tmp.html', auto_open=True)
# fig.show()

# df = px.data.tips()
# fig = px.histogram(df, x='total_bill')
# fig.show()
