import os
import scipy
import numpy as np
import matplotlib.pyplot as plt

# Получаем путь к текущему исполняемому файлу
script_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем относительный путь
relative_path = os.path.join(script_dir, 'NinaPro_data', 'S1_A1_E1.mat')

data = scipy.io.loadmat(relative_path)

print(data.keys())

print(data['__header__'])
#emg - emg по времени(10 шт)
#glove - углы по времени(22 шт)
#subject - чел
#excercise - жест
#repetition - ? (по времени) 0-10
#restimulus - ? (по времени) 0-12
#rerepetition - ? (по времени) 0-10?

emg = data['emg']
glove = data['glove']
repetition = data['repetition'].flatten()
restimulus = data['restimulus'].flatten()
rerepetition = data['rerepetition'].flatten()
subject = int(data['subject'][0][0])
exercise = int(data['exercise'][0][0])

fs = 2000  # Частота дискретизации
N = len(repetition)

# Глобальные границы для шкалы Y
emg_min, emg_max = np.min(emg), np.max(emg)
glove_min, glove_max = np.min(glove), np.max(glove)

# Разбиение по сменам repetition
segments = []
start_idx = 0
for i in range(1, N):
    if repetition[i] != repetition[i - 1]:
        segments.append((start_idx, i))
        start_idx = i
segments.append((start_idx, N))  # последний сегмент

# Построение графиков по сегментам
for idx, (start, end) in enumerate(segments):
    t = np.arange(end - start) / fs
    emg_segment = emg[start:end]
    glove_segment = glove[start:end]
    rep_val = repetition[start]
    restim_val = restimulus[start]
    rerep_val = rerepetition[start]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)

    for i in range(emg_segment.shape[1]):
        ax1.plot(t, emg_segment[:, i], label=f'EMG {i+1}')
    ax1.set_ylabel('ЭМГ')
    ax1.set_ylim(emg_min, emg_max)
    ax1.legend(loc='upper right')

    for i in range(glove_segment.shape[1]):
        ax2.plot(t, glove_segment[:, i], label=f'Glove {i+1}')
    ax2.set_ylabel('Перчатка')
    ax2.set_xlabel('Время (с)')
    ax2.set_ylim(glove_min, glove_max)
    ax2.legend(loc='upper right', ncol=4)

    fig.suptitle(f'Субъект {subject}, Упражнение {exercise}, '
                 f'Repetition: {rep_val}, Restimulus: {restim_val}, Rerepetition: {rerep_val}', fontsize=14)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()