import json
import time
import sys

from cleanser import df_header
from downloader import vinculo_str_d, month_list

def parser(month, year, file_list, df_struct):
    json_data = json_encoder(month, year, file_list, df_struct)
    print(json_data)

def json_encoder(month, year, file_list, employee_struct):
    # Criação de lista de dicionários (LofD) de funcionários
    employee_lofd = []
    for employee_tuple in employee_struct:
        vinculo = employee_tuple[0]
        df = employee_tuple[1]
        for employee in df.index:
            employee_lofd.append(gen_employee_dict(vinculo,
                                                   df.loc[employee]))
    # Removi o procinfo dessa estrutura pois não entendi como colocar o stdout na saída sem criar uma recursão
    crawling_result = {'aid':'MPF',
                       'month':month_list[month],
                       'year':str(year),
                       'crawler':{'id':None,
                                  'version':None,
                       },
                       'files':file_list,
                       'employees':employee_lofd,
                       'timestamp':time.ctime(),
    }
    return json.dumps(crawling_result, indent=4)
    
def gen_employee_dict(vinculo, df_slice):
    reg = int(df_slice[df_header[0]])
    name = str(df_slice[df_header[1]])
    role = str(df_slice[df_header[2]])
    workplace = str(df_slice[df_header[3]])
    income_dict = {key:float(df_slice[key]) for key in df_header[4:13]}
    discount_dict = {key:float(df_slice[key]) for key in df_header[13:17]}
    
    # Devido ao não entendimento da estrutura de rendimentos e dividendos dos
    # incomes, discounts, funds e perks, resolvi não implementar da forma
    # proposta por não saber como mapear as células das tabelas com as variáveis
    # das estruturas de dados propostas na API.
    employee_dict = {'reg':reg,
                     'name':name,
                     'role':role,
                     'type':vinculo,
                     'workplace':workplace,
                     'active': activity_test(vinculo),
                     'income':income_dict,
                     'discounts':discount_dict,
    }

    return employee_dict

def activity_test(vinculo):
    return (vinculo == "Membro Ativo"
            or vinculo == "Servidor Ativo"
            or vinculo == "Colaborador")
