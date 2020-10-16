import pandas as pd

from downloader import downloader, vinculo_str_d

df_header = ['matricula',
             'nome',
             'cargo',
             'lotacao',
             'remuneracao-do-cargo-efetivo',
             'outras-verbas-remuneratorias-legais-ou-judiciais',
             'funcao-de-confianca-ou-cargo-em-comissao',
             'gratificacao-natalina',
             'ferias',
             'abono-de-permanencia',
             'outras-remuneracoes-temporarias',
             'verbas-indenizatorias',
             'total-de-rendimentos-brutos',
             'contribuicao-previdenciaria',
             'imposto-de-renda',
             'retencao-por-teto-constitucional',
             'total-de-descontos',
             'rendimento-liquido-total',
]

# Transforma lista de tabelas do excel em dataframes com informações normalizadas
def cleanser(table_list, table_format):
    df_struct = []
    excel_engine = {'.ods':'odf','.xls':None}
    
    for i,filename in enumerate(table_list):
        df = pd.read_excel('tmp/'+filename,
                           header=None,
                           engine=excel_engine[table_format])
        cleansed_df = individual_cleanser(df)
        cleansed_df.to_excel('tmp/cleansed_'+filename+'.xls')
        df_struct.append((vinculo_str_d[filename.split('_')[0]],
                          cleansed_df))

    return df_struct

# Realiza limpeza de dados em dataframes poluidos
def individual_cleanser(df):
    mat_idx = (df[0] == 'Matrícula').idxmax()
    tot_idx = (df[0] == 'TOTAL GERAL').idxmax()

    trash_header = df.loc[mat_idx:mat_idx+2, :]
    col_to_drop = []
    header = []
    for col in trash_header:
        nan_array = trash_header[col].isnull().values
        if nan_array.sum() == 3:
            col_to_drop.append(col)
        elif nan_array[2] == False:
            header.append(trash_header.loc[mat_idx+2, col])
        elif nan_array[1] == False:
            header.append(trash_header.loc[mat_idx+1, col])
        else:
            header.append(trash_header.loc[mat_idx, col])
            
    df.drop(col_to_drop, inplace=True, axis=1)    
    df = df.loc[mat_idx+3:tot_idx-1]
    df.columns = df_header
    df.index = list(range(len(df)))

    # Conversão de tipo
    df.loc[:, df_header[0]] = df[df_header[0]].astype(int)
    for col in df_header[4:]:
        df.loc[:, col] = df[col].replace('R$0,00 ','0.0')
        df.loc[:, col] = df[col].replace('0,00 ','0.0')
        df.loc[:, col] = df[col].astype(float)

    return df
