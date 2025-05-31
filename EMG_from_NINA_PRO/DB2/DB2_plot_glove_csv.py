import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_glove_from_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    time = [i / 2000 for i in range(len(df))]  # также 2 кГц для синхронизации

    plt.figure(figsize=(15, 6))
    for i in range(df.shape[1]):
        plt.plot(time, df[i], label=f'Glove {i+1}')
    plt.xlabel('Время (с)')
    plt.ylabel('Углы (ед.)')
    plt.title(f'Glove данные из {os.path.basename(file_path)}')
    plt.legend(loc='upper right', ncol=4)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Задай путь к файлу, который хочешь отобразить
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'cutted_data' ,'glove_segments', 'glove_s1_e1_stim2_rep1.csv')
    plot_glove_from_csv(file_path)
