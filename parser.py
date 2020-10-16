import json
import time
import sys

from cleanser import df_header
from downloader import vinculo_str_d

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
                       'month':month,
                       'year':year,
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
    employee_dict = {'reg':reg,
                     'name':name,
                     'role':role,
                     'type':vinculo,
                     'workplace':workplace,
                     'active': activity_test(vinculo),
                     'income':None,
                     'discounts':None,
    }

    return employee_dict

def activity_test(vinculo):
    return (vinculo == "Membro Ativo"
            or vinculo == "Servidor Ativo"
            or vinculo == "Colaborador")
