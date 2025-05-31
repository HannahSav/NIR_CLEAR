import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_emg_from_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    time = [i / 2000 for i in range(len(df))]  # 2 кГц частота

    plt.figure(figsize=(15, 6))
    for i in range(df.shape[1]):
        plt.plot(time, df[i], label=f'EMG {i+1}')
    plt.xlabel('Время (с)')
    plt.ylabel('Амплитуда ЭМГ')
    plt.title(f'EMG данные из {os.path.basename(file_path)}')
    plt.legend(loc='upper right', ncol=4)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'cutted_data','emg_segments', 'emg_s1_e1_stim1_rep1.csv')
    plot_emg_from_csv(file_path)
