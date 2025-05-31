import os
import scipy.io
import numpy as np
import pandas as pd

def process_and_save_segments(mat_file_path, emg_out_dir, glove_out_dir):
    data = scipy.io.loadmat(mat_file_path)

    emg = data['emg'][:, :8]  # только первые 8 ЭМГ каналов
    glove = data['glove']
    restimulus = data['restimulus'].flatten()
    repetition = data['repetition'].flatten()
    subject_number = int(data['subject'][0])
    exercise_number = int(data['exercise'][0])

    valid_indices = np.where((restimulus > 0) & (repetition > 0))[0]
    segments = {}
    for i in valid_indices:
        key = (restimulus[i], repetition[i])
        if key not in segments:
            segments[key] = []
        segments[key].append(i)

    for (stim, rep), indices in segments.items():
        segment_emg = emg[indices, :]
        segment_glove = glove[indices, :]

        base_name = f"s{subject_number}_e{exercise_number}_stim{int(stim)}_rep{int(rep)}.csv"
        emg_filename = os.path.join(emg_out_dir, f"emg_{base_name}")
        glove_filename = os.path.join(glove_out_dir, f"glove_{base_name}")

        pd.DataFrame(segment_emg).to_csv(emg_filename, index=False, header=False)
        pd.DataFrame(segment_glove).to_csv(glove_filename, index=False, header=False)

    print(f"Обработано {len(segments)} сегментов из {os.path.basename(mat_file_path)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Путь к файлу и папки
    mat_file = os.path.join(script_dir, 'raw_data', 'S1_E1_A1.mat')
    emg_dir = os.path.join(script_dir, 'cutted_data', 'emg_segments')
    glove_dir = os.path.join(script_dir, 'cutted_data', 'glove_segments')
    os.makedirs(emg_dir, exist_ok=True)
    os.makedirs(glove_dir, exist_ok=True)

    # Запуск
    process_and_save_segments(mat_file, emg_dir, glove_dir)
