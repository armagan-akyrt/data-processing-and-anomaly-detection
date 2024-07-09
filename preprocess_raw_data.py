import pandas as pd
import sys

INPUT_FILE = 'raw_data.csv'
OUTPUT_FILE = 'processed_data.csv'

def main():

    n = len(sys.argv)
    if n != 3:
        print('No arguments for input file provided. Assuming default value of raw_data.csv.\n'
              'Output file name: processed_data.csv')

    else:
        print(f'Input file provided: {sys.argv[1]}\n Output file name: {sys.argv[2]}')
        INPUT_FILE = sys.argv[1]
        OUTPUT_FILE = sys.argv[2]

    df = pd.read_csv(INPUT_FILE)

    processed_data = {
        'tartima_baslama_zamani': [],
        'tartim_degeri': [],
        'bosaltma_maks_degeri': [],
        'oran': []
    }

    values_arr = []
    is_weighed = False
    weight_value = None
    start_time = None
    for i in range(1, len(df)):

        if df['ADW1_BR1_Tartim_Yapiliyor'][i] == 500 and df['ADW1_BR1_Tartim_Yapiliyor'][i - 1] == 0:
            start_time = df['time'][i]
            is_weighed = True

        if df['ADW1_BR1_Tartim_Yapiliyor'][i] == 0 and df['ADW1_BR1_Tartim_Yapiliyor'][i - 1] == 500:
            weight_value = df['ADW1_BR1_Loadcell_Aktuel_Deger'][i]

        if df['ADW1_Out_BR1_Kepce_Actuator_Tersle'][i] == 250 and is_weighed:
            values_arr.append(df['ADW1_BR1_Loadcell_Aktuel_Deger'][i])

        if df['ADW1_Out_BR1_Kepce_Actuator_Tersle'][i] == 0 and df['ADW1_Out_BR1_Kepce_Actuator_Tersle'][
            i - 1] == 250 and is_weighed:
            if values_arr and weight_value is not None:
                processed_data['tartima_baslama_zamani'].append(start_time)
                processed_data['tartim_degeri'].append(weight_value)
                processed_data['bosaltma_maks_degeri'].append(max(values_arr))
                processed_data['oran'].append(max(values_arr) / weight_value)

            weight_value = None
            start_time = None
            is_weighed = False
            values_arr = []

    '''print(processed_data)'''
    print(len(processed_data['tartima_baslama_zamani']))
    print(len(processed_data['tartim_degeri']))
    print(len(processed_data['bosaltma_maks_degeri']))
    processed_df = pd.DataFrame(processed_data)

    # convert time to datetime to remedy UTF-UTF+3 encoding error
    processed_df['tartima_baslama_zamani'] = pd.to_datetime(processed_df['tartima_baslama_zamani'])

    processed_df.to_csv(OUTPUT_FILE, index=False)


if __name__ == '__main__':
    main()

