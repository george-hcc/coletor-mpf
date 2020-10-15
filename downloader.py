import requests

vinculo_str_l = ['provento-membros-inativos',
                 'provento-servidores-inativos',
                 'remuneracao-membros-ativos',
                 'remuneracao-servidores-ativos',
                 'valores-percebidos-pensionistas',
                 'valores-percebidos-colaboradores',
]

def downloader(month, year):
    table_format = '.ods'
    table_list = []

    for vinculo in vinculo_str_l:
        url = ("http://www.transparencia.mpf.mp.br/conteudo/contracheque/"
               + vinculo + "/"
               + year + "/"
               + vinculo + "_"
               + year + "_"
               + month + table_format)
        filename = (vinculo + '_'
                    + year + '_'
                    + month)
        r = requests.get(url)
        f = open('tmp/' + filename + table_format, 'wb')
        f.write(r.content)
        f.close()
        table_list.append(filename)

    return table_list, table_format

if __name__ == '__main__':
    downloader('Janeiro', '2020')
