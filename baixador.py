import requests

vinculo_str_l = ['provento-membros-inativos',
                 'provento-servidores-inativos',
                 'remuneracao-membros-ativos',
                 'remuneracao-servidores-ativos',
                 'valores-percebidos-pensionistas',
                 'valores-percebidos-colaboradores',
]

def baixador(mes, ano):
    formato = 'ods'
    f_list = []

    for i, vinculo in enumerate(vinculo_str_l):
        url = "http://www.transparencia.mpf.mp.br/conteudo/contracheque/" + vinculo + "/" + ano + "/" + vinculo + "_" + ano + "_" + mes + "." + formato
        r = requests.get(url)
        f_list.append(open('tmp/' + vinculo + '_' + ano + '_' + mes + '.'+ formato, 'wb'))
        f_list[i].write(r.content)

if __name__ == '__main__':
    baixador('Janeiro', '2020')
    
