import os
import scipy
from scipy.signal import hilbert
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import neurokit2 as nk

# скользящее среднее (moving average)
def smooth_emg(signal, window_size=50):
    window = np.ones(window_size) / window_size
    return np.apply_along_axis(lambda x: np.convolve(x, window, mode='same'), axis=0, arr=signal)

# Получаем путь к текущему исполняемому файлу
script_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем относительный путь
relative_path = os.path.join(script_dir, 'NinaPro_data', 'S1_A1_E1.mat')

data = scipy.io.loadmat(relative_path)

print(data.keys())

print(data['__header__'])

colors = plt.cm.tab10.colors[:8]
line_styles = ['-', '--', ':']

#emg - emg по времени(10 шт)
#glove - углы по времени(22 шт)
#subject - чел
#excercise - группа жестов
#repetition - повторение (по времени) 0-10
#restimulus - номер жеста группы (по времени) 0-12
#rerepetition - ? (по времени) 0-10?

emg = data['emg']
glove = data['glove']
stimulus = data['stimulus'].flatten()
repetition = data['repetition'].flatten()
restimulus = data['restimulus'].flatten()
rerepetition = data['rerepetition'].flatten()
subject = int(data['subject'][0][0])
exercise = int(data['exercise'][0][0])
fs = 2000  # частота дискретизации

# Получаем уникальные значения стимулов
unique_stimuli = np.unique(stimulus)
print(f"Доступные движения (stimulus): {unique_stimuli}")
# Запрос выбора движения
chosen = int(input("Введите stimulus для выделения изолиний (1–12): "))

# Находим отрезки, где stimulus == 0 между сегментами с выбранным stimulus
segments = []
zero = 0
in_segment = False

for i in range(1, len(stimulus)):
    if stimulus[i-1] == chosen and stimulus[i] == zero:
        start = i
        in_segment = True
    elif stimulus[i-1] == zero and stimulus[i] == chosen and in_segment:
        end = i
        segments.append((start, end))
        in_segment = False

if not segments:
    print(f"Нет изолиний для stimulus = {chosen}")
    exit()

# Нормировка
all_idx = np.hstack([np.arange(start, end) for start, end in segments])
emg_min, emg_max = np.min(emg[all_idx]), np.max(emg[all_idx])
glove_min, glove_max = np.min(glove[all_idx]), np.max(glove[all_idx])

# Цвета и стили
colors = plt.cm.tab10.colors[:8]
line_styles = ['-', '--', ':']

# Построение графиков
for idx, (start, end) in enumerate(segments):
    t = np.arange(end - start) / fs
    emg_seg = emg[start:end]
    glove_seg = glove[start:end]

    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(4, 1, height_ratios=[2.5, 1, 1, 1], hspace=0.05)

    ax1 = fig.add_subplot(gs[0])
    for i in range(emg_seg.shape[1]):
        ax1.plot(t, emg_seg[:, i], label=f'EMG {i+1}')
    ax1.set_ylabel('ЭМГ')
    ax1.set_ylim(emg_min, emg_max)
    ax1.legend(loc='upper right', fontsize=8)

    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    for i in range(8):
        ax2.plot(t, glove_seg[:, i], color=colors[i % 8], linestyle='-')
    ax2.set_ylabel('Glove 1-8')
    ax2.set_ylim(glove_min, glove_max)

    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    for i in range(8, 16):
        ax3.plot(t, glove_seg[:, i], color=colors[i % 8], linestyle='--')
    ax3.set_ylabel('Glove 9-16')
    ax3.set_ylim(glove_min, glove_max)

    ax4 = fig.add_subplot(gs[3], sharex=ax1)
    for i in range(16, 22):
        ax4.plot(t, glove_seg[:, i], color=colors[i % 8], linestyle=':')
    ax4.set_ylabel('Glove 17-22')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylim(glove_min, glove_max)

    fig.suptitle(f'Изолиния перед stimulus {chosen}, Segment {idx+1}', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
