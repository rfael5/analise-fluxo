import json
import conn
import plotly.express as px
import plotly.graph_objects as go

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


def mostrarDezMaisVendidos():
    vendas = conn.buscarProdutos('20230101', '20240101')
    order_valor_maior = vendas.sort_values(by=['totalPrecoEvento'], ascending=False)
    dezp_monetario = order_valor_maior.iloc[0:10]

    order_qtd_maior = vendas.sort_values(by=['qtdEvento'], ascending=False)
    dezp_qtd = order_qtd_maior.iloc[0:10]

    order_valor_menor = vendas.sort_values(by=['totalPrecoEvento'], ascending=True)
    dezm_monetario = order_valor_menor.iloc[0:10]
    
    print(dezp_monetario[['nomeProduto', 'totalPrecoEvento']])
    
    fig = px.bar(dezp_monetario, x='nomeProduto', y='totalPrecoEvento')
    fig.write_html('tmp.html', auto_open=True)
    

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

btn_obter_data = Button(secondFrame, text="Dez mais vendidos", bg='#C0C0C0', font=("Arial", 16), command=mostrarDezMaisVendidos)
btn_obter_data.grid(row=1, column=0, padx=(80, 0), pady=10)

btn_obter_data = Button(secondFrame, text="Dez menos vendidos", bg='#C0C0C0', font=("Arial", 16))
btn_obter_data.grid(row=1, column=1, padx=(80, 0), pady=10)

btn_obter_data = Button(secondFrame, text="Pareto mais vendidos", bg='#C0C0C0', font=("Arial", 16))
btn_obter_data.grid(row=1, column=2, padx=(80, 0), pady=10)

root.mainloop()  

