import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_plot(df):
    '''Generates line plot for raw data'''

    sns.set_theme(style='whitegrid')
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.lineplot(data=df, x='time', y='ADW1_BR1_Loadcell_Aktuel_Deger', ax=ax, label='ADW1_BR1_Loadcell_Aktuel_Deger')
    sns.lineplot(data=df, x='time', y='ADW1_BR1_Tartim_Yapiliyor', ax=ax, label='ADW1_BR1_Tartim_Yapiliyor')
    sns.lineplot(data=df, x='time', y='ADW1_Out_BR1_Kepce_Actuator_Tersle', ax=ax,
                 label='ADW1_Out_BR1_Kepce_Actuator_Tersle')
    ax.set_title('Raw Data')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')

    ax.xaxis.set_major_locator(plt.MaxNLocator(10))  # Adjust number of ticks as needed

    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    df = pd.read_csv('raw_data.csv')
    generate_plot(df)


if __name__ == '__main__':
    main()
