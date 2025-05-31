import os
import math
import time
import csv

# Путь к DLL OpenSim
os.add_dll_directory("C:/Opensim 4.5/bin")

import opensim as osim

subject = 1
exercise = 1
stimulus = 1
repetition = 1

# Получаем путь к текущему скрипту
script_dir = os.path.dirname(os.path.abspath(__file__))

# Поднимаемся на один уровень выше
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))

# Строим путь к нужному CSV-файлу
csv_path = os.path.join(parent_dir, 'EMG_from_NINA_PRO', 'DB2','cutted_data', 'glove_segments', f'glove_s{subject}_e{exercise}_stim{stimulus}_rep{repetition}.csv')


with open(csv_path, "r") as f:
    reader = csv.reader(f)
    next(reader)  # пропуск заголовка
    glove_test_angles = [list(map(float, row)) for row in reader]

# === Карта индексов glove → суставы OpenSim ===
glove_angles = {
    1: 'cmc_flexion',
    2: 'mp_flexion',
    3: 'ip_flexion',
    4: 'cmc_abduction',
    5: '2mcp_flexion',
    6: '2pm_flexion',
    7: '2md_flexion',
    8: '3mcp_flexion',
    9: '3pm_flexion',
    10: '3md_flexion',
    11: '',
    12: '4mcp_flexion',
    13: '4pm_flexion',
    14: '4md_flexion',
    15: '',
    16: '5mcp_flexion',
    17: '5pm_flexion',
    18: '5md_flexion',
    19: '',
    20: '',
    21: 'flexion',
    22: 'deviation'
}

# === Загрузка модели ===
model_path = os.path.abspath(os.path.join(script_dir, 'model', 'Hand_Wrist_Model_for_development.osim'))
model = osim.Model(model_path)
model.setUseVisualizer(True)
state = model.initSystem()

coords = model.getCoordinateSet()

# === Проигрывание движения ===
for glove_test_angles_line in glove_test_angles[:1000:5]:
    for key, val in glove_angles.items():
        # print(key)
        if val == '':
            continue
        angle_deg = glove_test_angles_line[key - 1]

        # # Преобразование углов в соответствии с биомеханикой
        # if val == 'deviation':
        #     angle_deg = 120 - angle_deg
        # elif val == 'flexion':
        #     angle_deg = angle_deg - 180
        # elif val == 'cmc_flexion':
        #     angle_deg = angle_deg - 180
        # elif val == 'cmc_abduction':
        #     angle_deg = 180 - angle_deg
        # else:
        #     angle_deg = angle_deg - 80

        angle_rad = math.radians(angle_deg)

        if coords.contains(val):
            coord = coords.get(val)
            coord.setLocked(state, False)
            coord.setValue(state, angle_rad)

    model.realizePosition(state)
    model.getVisualizer().show(state)
    time.sleep(0.01)  # скорость анимации (можно изменить)
