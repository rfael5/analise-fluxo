import json
import conn

"""
O resultado da query traz o total de vendas de produtos para a Araújo e o total
de devoluções que a Araújo faz. A função unirFluxoUnidades junta os resultados das
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

total_lojas = conn.buscarTotalLojas('20240501', '20240701')
unidades = conn.callCadastros()

unidades = unidades.apply(inserirTotalCompras, _vendas = total_lojas, axis=1)
unidades['TOTAL'] = unidades['VENDIDOS'] - unidades['DEVOLUCAO']
unidades = unidades.sort_values(by=['FANTASIA'])

print(unidades)

#print(total_lojas)