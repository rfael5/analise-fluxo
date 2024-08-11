import json
#import conn
# import plotly.express as px
# import plotly.graph_objects as go

from datetime import datetime, timezone
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
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

# vendas = conn.buscarProdutos('20230101', '20240101')
# order_valor_maior = vendas.sort_values(by=['totalPrecoEvento'], ascending=False)
# dezp_monetario = order_valor_maior.iloc[0:10]

# order_qtd_maior = vendas.sort_values(by=['qtdEvento'], ascending=False)
# dezp_qtd = order_qtd_maior.iloc[0:10]

# order_valor_menor = vendas.sort_values(by=['totalPrecoEvento'], ascending=True)
# dezm_monetario = order_valor_menor.iloc[0:10]

# fig = px.histogram(dezp_monetario, x='nomeProduto', y='totalPrecoEvento')
# fig.write_html('tmp.html', auto_open=True)

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

#Tkinter
root = Tk()
root.title("| Gerar pedidos de suprimento |")

root.geometry("1150x800")

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

page1 = Frame(notebook)
notebook.add(page1, text='| Relatório pedidos de suprimento |')

mainFrame = Frame(page1)
mainFrame.pack(fill=BOTH, expand=1)

canvas = Canvas(mainFrame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)
#canvas.grid(row=0, column=0, sticky=EW)

scrollbar = ttk.Scrollbar(mainFrame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
#scrollbar.grid(row=0, rowspan=10, column=1, sticky="ns")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e:canvas.configure(scrollregion=canvas.bbox("all")))

secondFrame = Frame(canvas)
canvas.create_window((0, 0), window=secondFrame, anchor="nw")


explicacao = Label(secondFrame, text="Qual gráfico você quer gerar?", font=("Arial", 14))
explicacao.grid(row=0, columnspan=2, padx=(150, 0), pady=10, sticky="nsew")

btn_obter_data = Button(secondFrame, text="Dez mais vendidos", bg='#C0C0C0', font=("Arial", 16))
btn_obter_data.grid(row=1, column=0, padx=(80, 0), pady=2)

btn_obter_data = Button(secondFrame, text="Dez menos vendidos", bg='#C0C0C0', font=("Arial", 16))
btn_obter_data.grid(row=1, column=0, padx=(80, 0), pady=2)

btn_obter_data = Button(secondFrame, text="Pareto mais vendidos", bg='#C0C0C0', font=("Arial", 16))
btn_obter_data.grid(row=1, column=0, padx=(80, 0), pady=2)

btn_obter_data = Button(secondFrame, text="Salgados mais vendidos", bg='#C0C0C0', font=("Arial", 16))
btn_obter_data.grid(row=1, column=0, padx=(80, 0), pady=2)

btn_obter_data = Button(secondFrame, text="Doces mais vendidos", bg='#C0C0C0', font=("Arial", 16))
btn_obter_data.grid(row=1, column=0, padx=(80, 0), pady=2)


# lbl_dtInicio = Label(secondFrame, text="De:", font=("Arial", 14))
# lbl_dtInicio.grid(row=1, padx=(0, 190), column=0, sticky="e")

# dtInicio = DateEntry(secondFrame, font=('Arial', 12), width=22, height=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
# dtInicio.grid(row=2, column=0, padx=(150, 0), pady=5, sticky="e")

# lbl_dtFim = Label(secondFrame, text="Até:", font=("Arial", 14))
# lbl_dtFim.grid(row=1, column=1, padx=(50, 0), pady=5, sticky="w")

# dtFim = DateEntry(secondFrame, font=('Arial', 12), width=22, height=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
# dtFim.grid(row=2, column=1, padx=(50, 0), pady=5, sticky="w")

# btn_obter_data = Button(secondFrame, text="Mostrar lista", bg='#C0C0C0', font=("Arial", 16))
# btn_obter_data.grid(row=3, column=0, columnspan=2, padx=(80, 0), pady=2, sticky='nsew')


root.mainloop()  