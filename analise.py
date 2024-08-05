import json
import conn

"""
O resultado da query traz o total de vendas de produtos para a Araújo e o total
de devoluções que a Araújo faz. A função unirFluxoUnidades junta os resultados das
vendas e das devoluções de cada loja
"""
def unirFluxoUnidades(row, copia_lista):
    resultadosJson = copia_lista.to_json(orient='records')
    dadosDesserializados = json.loads(resultadosJson)
    row['totalVenda'] = 0
    row['totalCompra'] = 0
    for unidade in dadosDesserializados:
        print(row)
        if int(row['ID']) == int(unidade['ID']) and row['tipoOperacao'] == 'C':
            #unidade['totalVenda'] = row['totalOperacao']
            row['totalVenda'] = unidade['totalOperacao']
        elif int(row['ID']) == int(unidade['ID']) and row['tipoOperacao'] == 'F':
            #unidade['totalCompra'] = row['totalOperacao']
            row['totalCompra'] = unidade['totalOperacao']
        print(row)

total_lojas = conn.buscarTotalLojas('20240501', '20240701')
copia_lista = total_lojas

total_lojas = total_lojas.apply(unirFluxoUnidades, copia_lista=copia_lista, axis=1)

#print(total_lojas)