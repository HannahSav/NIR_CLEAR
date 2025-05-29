import os
import scipy
# from scipy.signal import hilbert
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
# import neurokit2 as nk
import csv

SUBJECT = 1
EXER_GROUP = 2

FLAG_SHOW = True
FLAG_WRITE_FILE = False

# скользящее среднее (moving average)
def smooth_emg(signal, window_size=50):
    window = np.ones(window_size) / window_size
    return np.apply_along_axis(lambda x: np.convolve(x, window, mode='same'), axis=0, arr=signal)

# def hilbert_smooth(signal):
#     return np.abs(hilbert(signal, axis=0))

# from scipy.signal import butter, filtfilt

# def lowpass_filter(emg, cutoff=10, fs=2000, order=4):
#     b, a = butter(order, cutoff / (0.5 * fs), btype='low')
#     return filtfilt(b, a, emg, axis=0)

# Получаем путь к текущему исполняемому файлу
script_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем относительный путь
relative_path = os.path.join(script_dir, 'NinaPro_data', f'S{SUBJECT}_A1_E{EXER_GROUP}.mat')

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

# Запрос выбора движения у пользователя
chosen = int(input("Введите stimulus движения, которое нужно отобразить: "))

# Фильтрация по выбранному движению
indices = np.where(stimulus == chosen)[0]

# Разбиение по repetition
segments = []
if len(indices) > 0:
    current_rep = repetition[indices[0]]
    start_idx = indices[0]

    for i in range(1, len(indices)):
        idx = indices[i]
        if repetition[idx] != current_rep:
            segments.append((start_idx, indices[i-1]+1))
            current_rep = repetition[idx]
            start_idx = idx
    segments.append((start_idx, indices[-1]+1))  # последний сегмент
else:
    print(f"Нет данных для stimulus = {chosen}")
    exit()

# Получаем min/max по эмг и glove для нормировки
emg_min = np.min(emg[indices])
emg_max = np.max(emg[indices])
glove_min = np.min(glove[indices])
glove_max = np.max(glove[indices])

# Построение графиков
for idx, (start, end) in enumerate(segments):
    t = np.arange(end - start) / fs
    emg_seg = emg[start:end]
    emg_smooth = smooth_emg(emg_seg, window_size=100)
    
    # ТАК СЕБЕ СГЛАЖИВАНИЯ
    # emg_hilbert = hilbert_smooth(emg_seg)
    # emg_low_filtred = lowpass_filter(emg_seg)
    # emg_nk = np.zeros_like(emg_seg)
    # for i in range(emg.shape[1]):
    #     emg_nk[:, i] = nk.signal_smooth(emg_seg[:, i], method="convolution", kernel="boxzen", size=100)

    glove_seg = glove[start:end]
    # print("GLOVE START MOVE:", list(map(float, glove_seg[0])))

    glove_array = [[0.0] + list(map(float, row)) for row in glove_seg[::2]]
    # print("GLOVE SEGMENT AS 2D ARRAY:", glove_array)

    if FLAG_WRITE_FILE:
        with open(r'C:\Users\GSavon\Desktop\Sirius\nir\NIR\new\glove_angles'+f"\glove_array_S{SUBJECT}_E{EXER_GROUP}_{chosen}.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(glove_array)

    if FLAG_SHOW:
        fig = plt.figure(figsize=(15, 10))  # увеличиваем высоту фигуры
        gs = gridspec.GridSpec(5, 1, height_ratios=[2, 0.15, 1, 1, 1], hspace=0.0)

        ax1 = fig.add_subplot(gs[0])
        spacer = fig.add_subplot(gs[1])  # невидимый отступ
        ax2 = fig.add_subplot(gs[2], sharex=ax1)
        ax3 = fig.add_subplot(gs[3], sharex=ax1)
        ax4 = fig.add_subplot(gs[4], sharex=ax1)
        spacer.axis('off')  # убираем оси у отступа

        # EMG
        # for i in range(emg_seg.shape[1]): #10
        for i in range(8):
            color = colors[i % 8]
            ax1.plot(t, emg_seg[:, i], label=f'EMG {i+1}', linestyle=':', color = color)
            ax1.plot(t, emg_smooth[:, i], color = color)
            # ax1.plot(t, emg_nk[:, i], color=color, linestyle='--')
        ax1.set_ylabel('ЭМГ')
        ax1.set_ylim(emg_min, emg_max)
        ax1.legend(loc='upper right', fontsize=8)
        # ax1.set_xticks([])  # убираем подписи времени

        # Glove 1-8
        for i in range(8):
            color = colors[i % 8]
            ax2.plot(t, glove_seg[:, i], label=f'Glove {i+1}', color=color, linestyle='-')
        ax2.set_ylabel('G1–8')
        ax2.set_ylim(glove_min, glove_max)
        ax2.legend(loc='upper right', ncol=4, fontsize=8)
        # ax2.set_xticks([])

        # Glove 9–16
        for i in range(8, 16):
            color = colors[i % 8]
            ax3.plot(t, glove_seg[:, i], label=f'Glove {i+1}', color=color, linestyle='--')
        ax3.set_ylabel('G9–16')
        ax3.set_ylim(glove_min, glove_max)
        ax3.legend(loc='upper right', ncol=4, fontsize=8)
        # ax3.set_xticks([])

        # Glove 17–22
        for i in range(16, 22):
            color = colors[i % 8]
            ax4.plot(t, glove_seg[:, i], label=f'Glove {i+1}', color=color, linestyle=':')
        ax4.set_ylabel('G17–22')
        ax4.set_xlabel('Время (с)')
        ax4.set_ylim(glove_min, glove_max)
        ax4.legend(loc='upper right', ncol=4, fontsize=8)

        rep_val = repetition[start]
        fig.suptitle(f'Subject {subject}, Exercise {exercise}, Stimulus: {chosen}, Repetition: {rep_val}', fontsize=12)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()