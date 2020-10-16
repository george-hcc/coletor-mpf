import requests

vinculo_str_d = {'provento-membros-inativos':"Membro Inativo",
                 'provento-servidores-inativos':"Servidor Inativo",
                 'remuneracao-membros-ativos':"Membro Ativo",
                 'remuneracao-servidores-ativos':"Servidor Ativo",
                 'valores-percebidos-pensionistas':"Pensionista",
                 'valores-percebidos-colaboradores':"Colaborador",
}

month_list = ['Janeiro',
              'Fevereiro',
              'Março',
              'Abril',
              'Maio',
              'Junho',
              'Julho',
              'Agosto',
              'Setembro',
              'Outubro',
              'Novembro',
              'Dezembro',
]

'''
Função para baixar lista com 6 planilhas do site do Ministério Público Federal
a partir do mês e do ano. Retorna lista de arquivos localizados na pasta tmp
e o formato (ods ou xlsx).
'''
def downloader(month, year):
    table_format = '.ods'
    if year < 2019:
        table_format = '.xls'
    if year == 2019 and month < 5:
        table_format = '.xls'
           
    table_list = []
    for vinculo in vinculo_str_d:
        url = ("http://www.transparencia.mpf.mp.br/conteudo/contracheque/"
               + vinculo + "/"
               + str(year) + "/"
               + vinculo + "_"
               + str(year) + "_"
               + month_list[month]
               + table_format)
        filename = (vinculo + '_'
                    + str(year) + '_'
                    + month_list[month]
                    + table_format)
        r = requests.get(url)
        f = open('tmp/' + filename, 'wb')
        f.write(r.content)
        f.close()
        table_list.append(filename)

    return table_list, table_format

if __name__ == '__main__':
    downloader('Janeiro', '2020')
