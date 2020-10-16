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
    if int(year) < 2018:
        table_format = '.xlsx'
    if int(year) == 2019 and month_list.index(month) < 5:
        table_format = '.xlsx'
           
    table_list = []
    for vinculo in vinculo_str_d:
        url = ("http://www.transparencia.mpf.mp.br/conteudo/contracheque/"
               + vinculo + "/"
               + year + "/"
               + vinculo + "_"
               + year + "_"
               + month + table_format)
        filename = (vinculo + '_'
                    + year + '_'
                    + month + table_format)
        r = requests.get(url)
        f = open('tmp/' + filename, 'wb')
        f.write(r.content)
        f.close()
        table_list.append(filename)

    return table_list, table_format

if __name__ == '__main__':
    downloader('Janeiro', '2020')
