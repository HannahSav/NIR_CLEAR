import os
import pandas as pd
import matplotlib.pyplot as plt
import json

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
    # Путь к текущему скрипту
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Путь к config.json (в той же папке)
    config_path = os.path.join(script_dir, 'config.json')

    # Читаем конфигурацию
    with open(config_path, 'r') as f:
        config = json.load(f)

    subject = config["subject"]
    exercise = config["exercise"]
    stimulus = config["stimulus"]
    repetition = config["repetition"]

    # Задай путь к файлу, который хочешь отобразить
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'cutted_data' ,'glove_segments', f'glove_s{subject}_e{exercise}_stim{stimulus}_rep{repetition}.csv')
    plot_glove_from_csv(file_path)
