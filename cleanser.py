import pandas as pd

from downloader import downloader

df_header = ['Matrícula',
             'Nome',
             'Cargo',
             'Lotação',
             'Remuneração do Cargo Efetivo',
             'Outras Verbas Remuneratórias Legais ou Judiciais',
             'Função de Confiança ou Cargo em Comissão',
             'Gratificação Natalina',
             'Férias',
             'Abono de Permanência',
             'Outras Remunerações Temporárias',
             'Verbas Indenizatórias',
             'Total de Rendimentos Brutos',
             'Contribuição Previdenciária',
             'Imposto de Renda',
             'Retenção por Teto Constitucional',
             'Total de Descontos',
             'Rendimento Líquido Total',
]

# Transforma lista de tabelas do excel em dataframes com informações normalizadas
def cleanser(table_list, table_format):
    df_struct = []
    excel_engine = {'.ods':'odf','.xlsx':None}
    
    for i,filename in enumerate(table_list):
        df = pd.read_excel('tmp/'+filename+table_format,
                           header=None,
                           engine=excel_engine[table_format])
        cleansed_df = individual_cleanser(df)
        print(i, filename.split('_')[0])
        df_struct.append((filename.split('_')[0], cleansed_df))

    return df_struct

# Realiza limpeza de dados em dataframes poluidos
def individual_cleanser(df):
    # Extração de dados
    col_to_drop = [1,3,4,5,6,8,9,10,15]
    df.drop(col_to_drop, inplace=True, axis=1)
    df = df[10:-5]
    df.columns = df_header
    df.index = list(range(len(df)))

    # Conversão de tipo
    df.loc[:, df_header[0]] = df[df_header[0]].astype(int)
    for col in df_header[4:]:
        df.loc[:, col] = df[col].replace('R$0,00 ','0.0')
        df.loc[:, col] = df[col].astype(float)

    return df


if __name__ == '__main__':
    file_list = downloader('Janeiro', '2020')
    df_struct = cleanser(*file_list)
    for i,struct in enumerate(df_struct):
        print(struct[0])
        print(struct[1].info())
        struct[1].to_excel('test'+str(i)+'.xlsx')
