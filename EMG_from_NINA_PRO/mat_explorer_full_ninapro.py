import os
import scipy
import numpy as np
import matplotlib.pyplot as plt

# Получаем путь к текущему исполняемому файлу
script_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем относительный путь
relative_path = os.path.join(script_dir, 'NinaPro_data', 'S1_A1_E2.mat')

data = scipy.io.loadmat(relative_path)

print(data.keys())

print(data['__header__'])
#emg - emg по времени(10 шт)
#glove - углы по времени(22 шт)
#subject - чел
#excercise - жест
#repetition - повторение (по времени) 0-10
#restimulus - жест (по времени) 0-12
#rerepetition - ? (по времени) 0-10?

# Извлечение переменных
emg = data['emg']         # N x 10
glove = data['glove']     # N x 22
subject = int(data['subject'][0])
exercise = int(data['exercise'][0])
restimulus = data['restimulus'].flatten()
repetition = data['repetition'].flatten()
rerepetition = data['rerepetition'].flatten()


print("EMG MEANINGS:")
for i in range(emg.shape[1]):
    print(f"emg{i+1} {min(emg[:, i])} - {max(emg[:, i])} ({np.mean(emg[:, i])})")

fs = 2000  # Частота дискретизации, Гц
time = np.arange(len(emg)) / fs  # Временная шкала в секундах

# Первый график: ЭМГ + разметка
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
for i in range(emg.shape[1]):
    ax1.plot(time, emg[:, i], label=f'EMG {i+1}')
ax1.set_ylabel('Амплитуда ЭМГ')
ax1.set_title(f'Субъект {subject}, Набор упражнений {exercise}')
ax1.legend(loc='upper right')

ax2.plot(time, restimulus, label='restimulus', linewidth=1)
ax2.plot(time, repetition, label='repetition', linewidth=1)
# ax2.plot(time, rerepetition, label='rerepetition', linewidth=1)
ax2.set_ylabel('Метка движения')
ax2.set_xlabel('Время (с)')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()

# Второй график: Glove + разметка
fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
for i in range(glove.shape[1]):
    ax3.plot(time, glove[:, i], label=f'Sensor {i+1}')
ax3.set_ylabel('Сигнал перчатки')
ax3.set_title(f'Субъект {subject}, Набор упражнений {exercise}')
ax3.legend(loc='upper right', ncol=4)

ax4.plot(time, restimulus, label='restimulus', linewidth=1)
ax4.plot(time, repetition, label='repetition', linewidth=1)
# ax4.plot(time, rerepetition, label='rerepetition', linewidth=1)
ax4.set_ylabel('Метка движения')
ax4.set_xlabel('Время (с)')
ax4.legend(loc='upper right')

plt.tight_layout()
plt.show()

