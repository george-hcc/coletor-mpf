#!/usr/bin/env python3

import argparse
import sys

from downloader import downloader
from cleanser import cleanser
from parser import parser

def main():
    month, year = filter_param()
    file_list, file_format = downloader(month, year)
    df_struct = cleanser(file_list, file_format)
    parser(month, year, file_list, df_struct)

def filter_param(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Coletor de informações do site do MPF através do portal da transparencia. Em funcionamento normal enviará JSON estruturado para a stdout.")
    parser.add_argument("-m", "--mes", required=True,
                        help="Mês ao qual se refere a coleta.",)
    parser.add_argument("-a", "--ano", required=True,
                        help="Ano ao qual se refere a coleta.")
    param = parser.parse_args(args)
    mes = int(param.mes)
    ano = int(param.ano)
    return mes, ano

if __name__ == '__main__':
    main()
