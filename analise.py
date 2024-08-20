import json
from tkinter import filedialog
import conn
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timezone
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox

import pandas as pd

"""
O resultado da query traz o total de vendas de produtos para a Araújo e o total
de devoluções que a Araújo faz. A função inserirTotalCompras junta os resultados das
vendas e das devoluções de cada loja
"""


#Mostra os 10 produtos mais vendidos por quantidade.
def mostraMaisVendidosQtd():
    dataInicio = dtInicio.get()
    dtInicioFormatada = formatarData(dataInicio)
    dataFim = dtFim.get()
    dtFimFormatada = formatarData(dataFim)
    
    vendas = conn.buscarProdutos(dtInicioFormatada, dtFimFormatada)
    if len(vendas) == 0:
        messagebox.showinfo("", "Sem encomendas registradas nesse período")
    else:
        order_qtd_maior = vendas.sort_values(by=['qtdEvento'], ascending=False)
        dezp_qtd = order_qtd_maior.iloc[0:10]
        print(dezp_qtd)
    fig = px.histogram(dezp_qtd, x='nomeProduto', y='qtdEvento')
    fig.update_layout(barmode = 'relative')
    fig.write_html('tmp.html', auto_open=True)

def formatarData(data):
    data_objeto = datetime.strptime(data, '%d/%m/%Y')
    data_formatada = data_objeto.strftime('%Y%m%d')
    return data_formatada

#Mostra os 10 produtos mais vendidos de acordo com o valor das vendas
def mostrarDezMaisVendidos():
    dataInicio = dtInicio.get()
    dtInicioFormatada = formatarData(dataInicio)
    dataFim = dtFim.get()
    dtFimFormatada = formatarData(dataFim)

    vendas = conn.buscarProdutos(dtInicioFormatada, dtFimFormatada)
    if len(vendas) == 0:
        messagebox.showinfo("", "Sem encomendas registradas nesse período.")
    else:
        order_valor_maior = vendas.sort_values(by=['totalValorVendas'], ascending=False)
        dezp_monetario = order_valor_maior.iloc[0:10]
        print(dezp_monetario)
    fig = px.histogram(dezp_monetario, x='nomeProduto', y='totalValorVendas')
    fig.update_layout(barmode = 'relative')
    fig.write_html('tmp.html', auto_open=True)


#Calcula a porcentagem de cada produto dentro do total de vendas e insere em uma coluna
#no dataframe.
def calcularPorcentagem(row, total):
    porcentagem = (row['totalValorVendas'] * 100) / total
    return round(porcentagem,2)
    
#Identifica os produtos que são responsáveis por 80% da arrecadação do buffet,
#baseando-se no princípio de pareto, que diz que 80% dos resultados vem de 20%
#das ações. No caso deste projeto, mais ou menos 20% dos produtos seriam responsáveis
#por 80% dos lucros.
def gerarListaCompleta():
    dataInicio = dtInicio.get()
    dtInicioFormatada = formatarData(dataInicio)
    dataFim = dtFim.get()
    dtFimFormatada = formatarData(dataFim)
    
    vendas = conn.buscarProdutos(dtInicioFormatada, dtFimFormatada)
    total_vendas = vendas['totalValorVendas'].sum()
 
    vendas['porcentagem'] = vendas.apply(calcularPorcentagem, total=total_vendas, axis=1)
    ordenados = vendas.sort_values(by=['totalValorVendas'], ascending=False)
    print(total_vendas)
    criarPlanilhaExcel(ordenados)

#Função para criar uma planilha Excel com os produtos que estão nos 20% mais vendidos, 
#ordenando do maior valor ao menor. As colunas incluem o nome do produto, as unidades
#vendidas, o valor total, e a porcentagem correspondente de cada produto.
def criarPlanilhaExcel(dataframe):
    """
    Abre uma janela para o usuário salvar um arquivo Excel com os produtos
    ordenados do mais vendido ao menos vendido.
    
    """
    # Abrir uma janela para o usuário salvar o arquivo
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Arquivos Excel", "*.xlsx")],
                                                title="Salvar arquivo Excel",
                                                initialfile=f"pareto_produtos")
    
    if not file_path:
        print("Operação cancelada pelo usuário.")
        return
    
    if not file_path.endswith(".xlsx"):
        file_path += ".xlsx"
    
    dataframe.to_excel(file_path, index=False)
    
    print(f"Arquivo salvo em: {file_path}")


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

scrollbar = ttk.Scrollbar(mainFrame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e:canvas.configure(scrollregion=canvas.bbox("all")))

secondFrame = Frame(canvas)
canvas.create_window((0, 0), window=secondFrame, anchor="nw")

lbl_dtInicio = Label(secondFrame, text="De:", font=("Arial", 14))
lbl_dtInicio.grid(row=1, padx=(0, 190), column=0, sticky="e")

dtInicio = DateEntry(secondFrame, font=('Arial', 12), width=22, height=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
dtInicio.grid(row=2, column=0, padx=(150, 0), pady=5, sticky="e")

lbl_dtFim = Label(secondFrame, text="Até:", font=("Arial", 14))
lbl_dtFim.grid(row=1, column=1, padx=(50, 0), pady=5, sticky="w")

dtFim = DateEntry(secondFrame, font=('Arial', 12), width=22, height=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
dtFim.grid(row=2, column=1, padx=(50, 0), pady=5, sticky="w")

explicacao = Label(secondFrame, text="Qual gráfico você quer gerar?", font=("Arial", 14))
explicacao.grid(row=3, columnspan=2, padx=(150, 0), pady=10, sticky="nsew")

btn_dez_mais = Button(secondFrame, text="Dez mais vendidos por valor", bg='#C0C0C0', font=("Arial", 16), command=mostrarDezMaisVendidos)
btn_dez_mais.grid(row=4, column=0, padx=(80, 0), pady=10)

btn_dez_menos = Button(secondFrame, text="Dez mais vendidos por unidade", bg='#C0C0C0', font=("Arial", 16), command=mostraMaisVendidosQtd)
btn_dez_menos.grid(row=4, column=1, padx=(80, 0), pady=10)

btn_pareto = Button(secondFrame, text="Porcentagem de encomendas por ano", bg='#C0C0C0', font=("Arial", 16), command=gerarListaCompleta)
btn_pareto.grid(row=4, column=2, padx=(80, 0), pady=10)

root.mainloop()  

