import pandas as pd
import numpy as np
import math

def convert_csv_to_mot(csv_path, output_path, coord_map, frequency):
    """
    Преобразует CSV с углами перчатки в .mot файл для OpenSim, выполняя нужное преобразование углов.

    :param csv_path: путь к исходному CSV без заголовков
    :param output_path: путь к выходному .mot файлу
    :param coord_map: словарь {индекс_колонки: имя_сустава}
    :param frequency: частота (Гц)
    """
    df = pd.read_csv(csv_path, header=None)
    num_frames = df.shape[0]
    time_step = 1.0 / frequency
    df['time'] = np.arange(0, num_frames * time_step, time_step)

    # Новая таблица для результирующих данных
    new_data = {'time': df['time']}

    for col_idx, coord_name in coord_map.items():
        if coord_name == '':
            continue  # пропускаем неиспользуемые каналы

        raw_deg = df[col_idx]

        # Преобразование углов (по твоим правилам)
        if coord_name == 'deviation':
            # transformed = 120 - raw_deg
            transformed = 0
        elif coord_name == 'flexion':
            # transformed = raw_deg - 180
            transformed = 0
        elif coord_name == 'cmc_flexion':
            transformed = raw_deg - 180
        elif coord_name == 'cmc_abduction':
            transformed = 180 - raw_deg
        else:
            transformed = raw_deg - 80

        new_data[coord_name] = transformed

    result_df = pd.DataFrame(new_data)

    # Заполнение недостающих колонок фиктивными значениями (если требуется)
    all_coords = ['time'] + [c for c in coord_map.values() if c != '']
    for col in all_coords:
        if col not in result_df.columns:
            result_df[col] = 0.0

    # Обеспечим правильный порядок колонок
    result_df = result_df[all_coords]

    header = [
        "Coordinates",
        f"version=1",
        f"nRows={result_df.shape[0]}",
        f"nColumns={result_df.shape[1]}",
        "inDegrees=yes",
        "endheader"
    ]

    with open(output_path, 'w') as f:
        for line in header:
            f.write(line + '\n')
        result_df.to_csv(f, sep='\t', index=False, float_format='%.6f')

    print(f"Файл сохранён: {output_path}")


if __name__ == "__main__":
    glove_angles = {
    # большой палец
    1: 'cmc_flexion',
    2: 'mp_flexion',
    3: 'ip_flexion',
    4: 'cmc_abduction',
    # указательный
    5: '2mcp_flexion',
    6: '2pm_flexion',
    7: '2md_flexion',
    # средний
    8: '3mcp_flexion',
    9: '3pm_flexion',
    10: '3md_flexion',
    11: '', # разница между '2mcp_abduction' и '3mcp_abduction'
    # безымянный
    # '4mcp_abduction'
    12: '4mcp_flexion',
    13: '4pm_flexion',
    14: '4md_flexion',
    15: '', # разница между '3mcp_abduction' и '4mcp_abduction'
    # мизинец
    16: '5mcp_flexion',
    17: '5pm_flexion',
    18: '5md_flexion',
    19: '', # разница между '4mcp_abduction' и '5mcp_abduction'
    20: '', # скорее всего '4cmc_flexion'
    # запястье
    21: 'flexion', # radians
    22: 'deviation' # radians
    }
    convert_csv_to_mot(r"C:\Users\GSavon\Desktop\Sirius\nir\NIR\new\glove_angles\glove_array_S1_E1_1.csv", 
                       r"C:\Users\GSavon\Desktop\Sirius\nir\NIR\new\NINAPRO\mot_data\try1.mot", glove_angles, 100)
