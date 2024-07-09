import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
import pytz



def generate_plot(df):
    '''Generates line plot for processed data'''

    sns.set_theme(style='whitegrid')
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.lineplot(data=df, x='tartima_baslama_zamani', y='oran', ax=ax)
    ax.set_title('Processed Data')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')

    # Set x-axis major locator to show fewer ticks
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))  # Adjust the number of ticks as needed

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    df = pd.read_csv('processed_data.csv')
    # Limiting oran values for better visualization
    df['oran'] = df['oran'].clip(lower=0.25, upper=1.75)  # Adjust upper limit as needed
    generate_plot(df)


if __name__ == '__main__':
    main()
