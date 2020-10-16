from downloader import downloader
from cleanser import cleanser
from parser import parser

def main():
    month = 'Janeiro'
    year = '2020'
    file_list, file_format = downloader(month, year)
    df_struct = cleanser(file_list, file_format)
    parser(month, year, file_list, df_struct)
    

if __name__ == '__main__':
    main()
