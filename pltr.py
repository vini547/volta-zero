import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import time
import argparse
def pltr(value, index, func, ylabel, xlabel, opcao,freq,meses=[]):

    r"""



      /\\\\\\\\\\\\\    /\\\          /\\\\\\\\\\\\\\\    /\\\\\\\\\             
      \/\\\/////////\\\ \/\\\         \///////\\\/////   /\\\///////\\\          
       \/\\\       \/\\\ \/\\\               \/\\\       \/\\\     \/\\\         
        \/\\\\\\\\\\\\\/  \/\\\               \/\\\       \/\\\\\\\\\\\/         
         \/\\\/////////    \/\\\               \/\\\       \/\\\//////\\\        
          \/\\\             \/\\\               \/\\\       \/\\\    \//\\\      
           \/\\\             \/\\\____________   \/\\\       \/\\\     \//\\\    
            \/\\\             \/\\\\\\\\\\\\\\\   \/\\\       \/\\\      \//\\\  
             \///              \///////////////    \///        \///        \///  
                                                                                 
    
    ============================================================================
    ||                               PLTR                                     ||
    ============================================================================

    Monitora diretório e plota gráficos no instante em que csvs são alterados.
    Uma vez detectado o csv, este é processado para gerar as séries de dados
    que serão plotadas. Pode-se customizar os dados através de qualquer função
    de agragação ou uma lsita delas.

    -----------------------------------------------------------------------------
    |                                                                           |
    |  Parametros:                                                              |
    |    value  - feature a ser agregada pela função.                           |
    |    index  - features a serem usadas como index da pivot table.            |  
    |    func   - funcao de agragação.                                          | 
    |    ylabel - título do eixo y.                                             |
    |    xlabel - título do eixo y.                                             |                                     
    |    opcao  - modo de representação dos valores agregados                   |
    |    freq   - frequência de verificação.                                    |
    |                                                                           |    
    -----------------------------------------------------------------------------

    -----------------------------------------------------------------------------
    |                                                                           |
    |  Returna:                                                                 |
    |    Retorna um pandas dataframe com os dados processados e plota o gráfico |
    |    configurado.                                                           |
    |                                                                           |
    -----------------------------------------------------------------------------
    """    
    month_map = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
        'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
        'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'}
    folder_path = './input'
    time_threshold = time.time() - freq  # Configura o tempo de verificação.

    # Checa se qualquer arquivo na pasta foi modificado nos últimos 10s.
    updated_files = []
    modification_times = []
    # Checa se foram passados argumentos para o parametro meses.

    if meses:
        for mes in meses:
            file_path1='./input/SINASC_RO_2019_'+mes+'.csv'
            parts = file_path1.split('_')  # Splitting by underscore
            print(f'Processing file: SINASC_RO_2019_'+mes+'.csv')
            df = pd.read_csv(file_path1)   
            
            if len(parts) >= 4:
                year = parts[2]  # Extract year (e.g., "2019")
                month_abbr = parts[3].replace('.csv', '')  # Extract month abbreviation (e.g., "JAN")
                month_num = month_map.get(month_abbr.upper(), '00')

                # Create a folder in the format "YYYY-MM"
                folder_name = f'{year}-{month_num}'
                save_folder = os.path.join('./plots', folder_name)
                os.makedirs(save_folder, 
                            exist_ok=True)
                
                # Pivot Table
                if opcao == 'default':
                    pivot = pd.pivot_table(df, 
                                values=value, 
                                index=index,
                                aggfunc=func)
                    pivot.plot(figsize=[15, 5])
                    plt.xticks(ticks=range(len(pivot.index)), labels=pivot.index, rotation=45)
                elif opcao == 'rankeado':
                    pivot = pd.pivot_table(df, 
                                        values=value, 
                                        index=index,
                                        aggfunc=func).sort_values(value)
                    pivot.plot(figsize=[15, 5])
                    plt.xticks(ticks=range(len(pivot.index)), labels=pivot.index, rotation=45)

                elif opcao == 'unstack':
                    pivot = pd.pivot_table(df, 
                                        values=value, 
                                        index=index,
                                        aggfunc=func).unstack()
                    pivot.plot(figsize=[15, 5])
                    plt.xticks(ticks=range(len(pivot.index)), labels=pivot.index, rotation=45)

                plt.ylabel(ylabel)
                plt.xlabel(xlabel)                

                plot_filename = f'{func}-{value}-{index}-{year}-{month_num}-{opcao}.png'
                plot_filepath = os.path.join(save_folder, plot_filename)
                plt.savefig(plot_filepath)
                print(f'Plot saved to: {plot_filepath}')
                plt.show()
                plt.close()

    else: # Caso não fornecidos argumentos para parametro meses

        # Constroi lista com tempos de última modificação dos arquivos
        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(folder_path, file)
                modification_times.append(os.path.getmtime(file_path))
                
        # Verifica se há tempos dentro da janela de 10s.
        if file_path:            
            if any(mod_time > time_threshold for mod_time in modification_times):
                updated_files.append(file_path)  
                print(f'Updated file(s) found: {file_path}')
        else:
            print('file_path not built')
        df = pd.DataFrame()
        
        if updated_files:       
            
            for file_path in updated_files:
                print(f'Processing updated file(s): {file_path}')
                df = pd.read_csv(file_path)
                base_name = os.path.basename(file_path)
                parts = base_name.split('_')  # Splitting by underscore

                if len(parts) >= 4:
                    year = parts[2]  # Extract year (e.g., "2019")
                    month_abbr = parts[3].replace('.csv', '')  # Extract month abbreviation (e.g., "JAN")
                    month_num = month_map.get(month_abbr.upper(), '00')

                    # Create a folder in the format "YYYY-MM"
                    folder_name = f'{year}-{month_num}'
                    save_folder = os.path.join('.\plots', folder_name)
                    os.makedirs(save_folder, 
                                exist_ok=True)

                    # Pivot Table
                    if opcao == 'default':
                        pivot = pd.pivot_table(df, 
                                    values=value, 
                                    index=index,
                                    aggfunc=func)
                        pivot.plot(figsize=[15, 5])
                        plt.xticks(ticks=range(len(pivot.index)), labels=pivot.index, rotation=45)
                    elif opcao == 'rankeado':
                        pivot = pd.pivot_table(df, 
                                            values=value, 
                                            index=index,
                                            aggfunc=func).sort_values(value)
                        pivot.plot(figsize=[15, 5])
                        plt.xticks(ticks=range(len(pivot.index)), labels=pivot.index, rotation=45)

                    elif opcao == 'unstack':
                        pivot = pd.pivot_table(df, 
                                            values=value, 
                                            index=index,
                                            aggfunc=func).unstack()
                    pivot.plot(figsize=[15, 5])
                    plt.xticks(ticks=range(len(pivot.index)), labels=pivot.index, rotation=45)

                    plt.ylabel(ylabel)
                    plt.xlabel(xlabel)
                    

                    plot_filename = f'{func}-{value}-{index}-{year}-{month_num}-{opcao}.png'
                    plot_filepath = os.path.join(save_folder, plot_filename)
                    plt.savefig(plot_filepath)
                    print(f'Plot saved to: {save_folder}')
                    plt.show()
                    plt.close()
                else:
                    print(f'Filename does not match the expected pattern: {file_path}')
        else:
            print(f'No file updated in the last 10s.')    
    return df


if __name__ == '__main__':
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Process CSV files and generate plots.')
    parser.add_argument('meses', nargs='*', help='List of months to process (e.g., MAR ABR MAI)')
    parser.add_argument('--value', required=True, help='Feature to be aggregated.')
    parser.add_argument('--index', required=True, help='Features to be used as index in pivot table.')
    parser.add_argument('--func', required=True, help='Aggregation function.')
    parser.add_argument('--ylabel', required=True, help='Y-axis label.')
    parser.add_argument('--xlabel', required=True, help='X-axis label.')
    parser.add_argument('--opcao', default='default', help='Mode of representation of aggregated values.')
    parser.add_argument('--freq', type=int, default=10, help='Frequency of folder check.')

    args = parser.parse_args()

    # Call the pltr function with arguments
    pltr(args.value, args.index, args.func, args.ylabel, args.xlabel, args.opcao, args.freq, args.meses)
