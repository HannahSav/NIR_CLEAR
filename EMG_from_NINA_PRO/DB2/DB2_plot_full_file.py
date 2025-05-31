import os
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

def plot_emg_and_glove(emg, glove, restimulus, repetition, subject, exercise, time):
    # ЭМГ
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
    for i in range(8):  # первые 8 электродов
        ax1.plot(time, emg[:, i], label=f'EMG {i+1}')
    ax1.set_ylabel('Амплитуда ЭМГ')
    ax1.set_title(f'Субъект {subject}, Упражнение {exercise}')
    ax1.legend(loc='upper right', ncol=4)
    
    ax2.plot(time, restimulus, label='restimulus', linewidth=1)
    ax2.plot(time, repetition, label='repetition', linewidth=1)
    ax2.set_ylabel('Метки')
    ax2.set_xlabel('Время (с)')
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

    # Перчатка
    fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
    for i in range(glove.shape[1]):
        if i != 24:
            ax3.plot(time, glove[:, i], label=f'Glove {i+1}')
    ax3.set_ylabel('Сигнал перчатки')
    ax3.set_title(f'Субъект {subject}, Упражнение {exercise}')
    ax3.legend(loc='upper right', ncol=4)

    ax4.plot(time, restimulus, label='restimulus', linewidth=1)
    ax4.plot(time, repetition, label='repetition', linewidth=1)
    ax4.set_ylabel('Метки')
    ax4.set_xlabel('Время (с)')
    ax4.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Получаем абсолютный путь к папке, где лежит этот скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Добавляем путь к файлу внутри папки raw_data
    file_path = os.path.join(script_dir, 'raw_data', 'S1_E1_A1.mat')
    data = scipy.io.loadmat(file_path)

    # Извлечение переменных
    emg = data['emg']
    glove = data['glove']
    restimulus = data['restimulus'].flatten()
    repetition = data['repetition'].flatten()
    subject_number = int(data['subject'][0])
    exercise_number = int(data['exercise'][0])
    print(subject_number, exercise_number)

    # Временная шкала
    fs_emg = 2000  # Частота дискретизации ЭМГ
    time = np.arange(len(emg)) / fs_emg

    # Построение графиков
    plot_emg_and_glove(emg, glove, restimulus, repetition, subject_number, exercise_number, time)
