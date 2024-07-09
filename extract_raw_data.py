import pandas as pd
import sys
from dotenv import load_dotenv
import os
from influxdb import InfluxDBClient
import datetime
import pytz

QUERY_TIME_FACTOR = '24h'
OUTPUT_FILE_NAME = 'raw_data.csv'

def read_queries(query, client):
    df = client.query(query)
    return df

def main():

    n = len(sys.argv)
    if n != 3:
        print('No arguments for query length provided. Assuming default value of 24h.\n'
              'Output file name: raw_data.csv')
    else:
        print(f'Query length provided: {sys.argv[1]}')
        QUERY_TIME_FACTOR = sys.argv[1]
        OUTPUT_FILE_NAME = sys.argv[2]



    load_dotenv()

    pwd_client = os.getenv('PWD_CLIENT')
    uname_client = os.getenv('UNAME_CLIENT')
    db_client = os.getenv('DB_CLIENT')
    host_client = os.getenv('HOST_CLIENT')
    port_client = 8086

    print(f'pwd_client: {pwd_client}\n'
          f'uname_client: {uname_client}\n'
          f'db_client: {db_client}\n'
          f'host_client: {host_client}\n'
          f'port_client: {port_client}\n')

    client = InfluxDBClient(host=host_client, port=port_client, username=uname_client, password=pwd_client,
                            database=db_client)

    # Define queries
    actual_data = f'''SELECT "value"
                      FROM "variable_value_rp"."variable_value"
                      WHERE ("name" = 'ADW1_BR1_Loadcell_Aktuel_Deger') AND time > now() - {QUERY_TIME_FACTOR}
                      tz('Europe/Istanbul');
    '''
    is_weighing = f'''SELECT "value" * 500
                      FROM "variable_value_rp"."variable_value"
                      WHERE ("name" = 'ADW1_BR1_Tartim_Yapiliyor') AND time > now() - {QUERY_TIME_FACTOR}
                      tz('Europe/Istanbul');
    '''
    actuator_reversing = f'''SELECT "value" * 250
                             FROM "variable_value_rp"."variable_value"
                             WHERE ("name" = 'ADW1_Out_BR1_Kepce_Actuator_Tersle') AND time > now() - {QUERY_TIME_FACTOR}
                             tz('Europe/Istanbul');
    '''

    df_q1 = read_queries(actual_data, client)
    df_q2 = read_queries(is_weighing, client)
    df_q3 = read_queries(actuator_reversing, client)

    df_q1 = df_q1.raw['series']
    df_q2 = df_q2.raw['series']
    df_q3 = df_q3.raw['series']

    df_q1 = pd.DataFrame(df_q1[0]['values'], columns=df_q1[0]['columns'])
    df_q2 = pd.DataFrame(df_q2[0]['values'], columns=df_q2[0]['columns'])
    df_q3 = pd.DataFrame(df_q3[0]['values'], columns=df_q3[0]['columns'])

    df_q1.rename(columns={'time': 'time', 'value': 'ADW1_BR1_Loadcell_Aktuel_Deger'}, inplace=True)
    df_q2.rename(columns={'time': 'time', 'value': 'ADW1_BR1_Tartim_Yapiliyor'}, inplace=True)
    df_q3.rename(columns={'time': 'time', 'value': 'ADW1_Out_BR1_Kepce_Actuator_Tersle'}, inplace=True)

    # Convert 'time' column to datetime if not already
    df_q1['time'] = pd.to_datetime(df_q1['time'])
    df_q2['time'] = pd.to_datetime(df_q2['time'])
    df_q3['time'] = pd.to_datetime(df_q3['time'])

    # Convert to UTC+3
    utc_plus_3 = pytz.timezone('Etc/GMT-3')  # UTC+3 timezone
    df_q1['time'] = df_q1['time'].dt.tz_convert(utc_plus_3)
    df_q2['time'] = df_q2['time'].dt.tz_convert(utc_plus_3)
    df_q3['time'] = df_q3['time'].dt.tz_convert(utc_plus_3)

    # Merge dataframes on 'time' using outer join
    df = pd.merge(df_q1, df_q2, on='time', how='outer')
    df = pd.merge(df, df_q3, on='time', how='outer')

    # Sort by 'time'
    df.sort_values(by='time', inplace=True)

    # Initialize columns with the first non-NaN values
    first_values = {
        'ADW1_BR1_Loadcell_Aktuel_Deger': df['ADW1_BR1_Loadcell_Aktuel_Deger'].dropna().iloc[0] if not df['ADW1_BR1_Loadcell_Aktuel_Deger'].dropna().empty else 0,
        'ADW1_BR1_Tartim_Yapiliyor': df['ADW1_BR1_Tartim_Yapiliyor'].dropna().iloc[0] if not df['ADW1_BR1_Tartim_Yapiliyor'].dropna().empty else 0,
        'ADW1_Out_BR1_Kepce_Actuator_Tersle': df['ADW1_Out_BR1_Kepce_Actuator_Tersle'].dropna().iloc[0] if not df['ADW1_Out_BR1_Kepce_Actuator_Tersle'].dropna().empty else 0
    }

    df.loc[0, 'ADW1_BR1_Loadcell_Aktuel_Deger'] = first_values['ADW1_BR1_Loadcell_Aktuel_Deger']
    df.loc[0, 'ADW1_BR1_Tartim_Yapiliyor'] = first_values['ADW1_BR1_Tartim_Yapiliyor']
    df.loc[0, 'ADW1_Out_BR1_Kepce_Actuator_Tersle'] = first_values['ADW1_Out_BR1_Kepce_Actuator_Tersle']

    # Fill NaN values with the last valid observation (ffill) for each column separately
    df['ADW1_BR1_Loadcell_Aktuel_Deger'].ffill(inplace=True)
    df['ADW1_BR1_Tartim_Yapiliyor'].ffill(inplace=True)
    df['ADW1_Out_BR1_Kepce_Actuator_Tersle'].ffill(inplace=True)

    # Set 'time' column as index (ensure it's a DatetimeIndex)
    df.set_index('time', inplace=True)

    # Resample to 1-second intervals and fill NaN values with the last valid observation (ffill)
    df_resampled = df.resample('1s').ffill()

    # Reset index to have 'time' as a column
    df_resampled.reset_index(inplace=True)

    # Print or save the resulting dataframe
    print(df_resampled)

    # Save to CSV
    df_resampled.to_csv(OUTPUT_FILE_NAME, index=False)


if __name__ == '__main__':
    main()
