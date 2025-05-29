import os
import math
# Добавляем путь к DLL
os.add_dll_directory("C:/Opensim 4.5/bin")
import opensim as osim
from opensim import Millard2012EquilibriumMuscle
import matplotlib.pyplot as plt
import time
import csv

muscles_to_keep = {
    'ECRL',  # extensor carpi radialis longus
    'ECRB',  # extensor carpi radialis brevis
    'ECU',   # extensor carpi ulnaris
    'FCR',   # flexor carpi radialis
    'FCU',   # flexor carpi ulnaris
    'PL',    # palmaris longus
    'EDCL', 'EDCR', 'EDCM', 'EDCI'  # extensor digitorum components
    # 'brachioradialis' — если есть в модели
}

length_data = {name: [] for name in muscles_to_keep}

#Углы перчатки:
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


# with open(r"C:\Users\GSavon\Desktop\Sirius\nir\NIR\new\glove_angles\glove_array_S1_E3_9.csv", "r") as f:
with open(r".\EMG_from_NINA_PRO\glove_angles\glove_array_S1_E1_1.csv", "r") as f:
    reader = csv.reader(f)
    row = next(reader)
    glove_test_angles = [list(map(float, row)) for row in reader]

# Путь к модели
model_path = r'C:\Users\GSavon\Documents\OpenSim 4.5\Code\Python\ARMS_Wrist_Hand_Model_4.3\Hand_Wrist_Model_for_development.osim'
# model_path = r'C:\Users\GSavon\Documents\OpenSim 4.5\Code\Python\ARMS_Wrist_Hand_Model_4.3\Hand_Wrist_Model_wo_muscles.osim'
# model_path = r'C:\Users\GSavon\Documents\OpenSim 4.5\Code\Python\just_try\MOBL_ARMS_fixed_41.osim'
model = osim.Model(model_path)

# muscles = model.getMuscles()
# print(f"Количество мышц в модели: {muscles.getSize()}")
# for i in range(muscles.getSize()):
#     muscle = muscles.get(i)
#     print(f"{i}: {muscle.getName()}")

# print("$"*100)

# Включаем визуализатор до инициализации
model.setUseVisualizer(True)

# Только после этого инициализируем систему
state = model.initSystem()

# Получение всех координат
coords = model.getCoordinateSet()
# print("Изначальные углы суставов:")
for i in range(coords.getSize()):
    coord = coords.get(i)
    name = coord.getName()
    value = coord.getValue(state)
    # print(f"{i}: {name} = {value:.4f} рад")

flag = False
for glove_test_angles_line in glove_test_angles[:1000:5]:
    for key, val in glove_angles.items():
        if val !=  '':
            # Установка нового значения для одного из суставов
            coord_name_to_modify = val
            new_angle_deg = glove_test_angles_line[key]
            # if key == 2:
            #         print(key, val, new_angle_deg)
                    # N:glove -> OpenSim
                    # 2 mp_flixion 120-90 -> 30-0
                    # 3 ip_flexion: 111 -> 20-30
                    # 4 cmc_abduction 130 -> -10-0
                    # 5 2mcp_flexion: 130 -> 50
                    # 6 2pm_flexion 100-175 -> 70
                    # 7 2md_flexion 78-105(62) -> 10-20
                    # 8 3mcp_flexion 107-130 ->
                    # 9 3pm_flexion 76-170 (118-68) ->
                    # 10 3md_flexion 73-57 ->
                    # 12 4mcp_flexion 128-160 (111-130) ->
                    # 13 4pm_flexion 79-140 ()
                    # 14 4md_flexion 55-38 ->
                    # 
                    # 21: 147 -> 17 
                    # 
            if val in ['deviation']:
                # new_angle_deg = 90 - new_angle_deg
                new_angle_deg = 120 - new_angle_deg
                # 130
            elif val in ['flexion']:
                # 150
                new_angle_deg = new_angle_deg - 180
            elif val in ['cmc_flexion']: #???????????????????
                # 150 -> 5
                new_angle_deg = new_angle_deg - 180 
                # new_angle_deg = 90 - new_angle_deg
                # new_angle_deg = new_angle_deg - 90
            elif val in ['cmc_abduction']:
                # 130 -> 
                # new_angle_deg = new_angle_deg - 90
                new_angle_deg = 180 - new_angle_deg
            else:
                # new_angle_deg = new_angle_deg + 180
                # new_angle_deg = 90 - new_angle_deg
                # new_angle_deg = new_angle_deg - 90
                new_angle_deg = new_angle_deg - 80
            new_angle_rad = math.radians(new_angle_deg)

            if coords.contains(coord_name_to_modify):
                coord = coords.get(coord_name_to_modify)
                coord.setLocked(state, False)  # если вдруг заблокировано
                name = coord.getName()
                min_angle = coord.getRangeMin()
                max_angle = coord.getRangeMax()
                # print(f"{idx}: {name} — диапазон: от {math.degrees(min_angle):.1f}° до {math.degrees(max_angle):.1f}°")
                # coord.setRangeMin(min(new_angle_rad - 1.0, math.radians(min_angle)))  # можно уточнить допустимый диапазон
                coord.setRangeMin(min(0.0, math.radians(min_angle)))  # можно уточнить допустимый диапазон
                # coord.setRangeMax(max(new_angle_rad + 1.0, math.radians(max_angle)))
                coord.setRangeMax(max(2.0, math.radians(max_angle)))
                # print(f"\nУгол '{coord_name_to_modify}' установлен в {new_angle_deg}°.")
                coord.setValue(state, new_angle_rad)
                
            else:
                ...
                # print(f"\nСустав '{coord_name_to_modify}' не найден.")
    #         glove_test_angles_line[key] = new_angle_deg
    # print(glove_test_angles_line)
    # break

    # Пересчитываем состояние
    model.realizePosition(state)

    # Показываем в визуализаторе
    model.getVisualizer().show(state)
    if not flag:
        # time.sleep(5)
        flag = True
    else:
        time.sleep(0.0001)

    muscles = model.getMuscles()

    for i in range(muscles.getSize()):
        # muscle = muscles.get(i)
        # name = muscle.getName()
        
        raw_muscle = muscles.get(i)
        name = raw_muscle.getName()

        # Попытка привести к Millard2012EquilibriumMuscle
        muscle = Millard2012EquilibriumMuscle.safeDownCast(raw_muscle)
        # print(dir(muscle))  
        # time.sleep(50)

        if name in muscles_to_keep:

            # print(f"Muscle: {name}")

            # activation = muscle.getActivation(state)
            length = muscle.getLength(state)
            # velocity = muscle.getLengtheningSpeed(state)
            # force = muscle.getForce(state)
            # active_force = muscle.getActiveForce(state)
            # passive_force = muscle.getPassiveForce(state)
            # fiber_length_norm = muscle.getNormalizedFiberLength(state)
            # fiber_velocity_norm = muscle.getNormalizedFiberVelocity(state)
            # tendon_length = muscle.getTendonLength(state)
            # pennation_angle = muscle.getPennationAngle(state)

            # print(f"  Activation: {activation}")
            # print(f"  Length: {length}")
            # print(f"{round(length, 5):.5f}", end='\t')

            # print(f"  Velocity: {velocity}")
            # print(f"  Force: {force}")
            # print(f"  Active Force: {active_force}")
            # print(f"  Passive Force: {passive_force}")

            # print(f"  Normalized Fiber Length: {fiber_length_norm}")
            # print(f"  Normalized Fiber Velocity: {fiber_velocity_norm}")
            # print(f"  Tendon Length: {tendon_length}")
            # print(f"  Pennation Angle: {pennation_angle}")

                        # # Получить нормированную длину волокна
                        # norm_fiber_length = muscle.getNormalizedFiberLength(state)

                        # # Получить активный множитель силы по длине
                        # multiplier = muscle.calcActiveForceLengthMultiplier(state)

                        # # Получить активацию (0–1)
                        # activation = muscle.getActivation(state)

                        # # Получить максимальную изометрическую силу
                        # f_max = muscle.getMaxIsometricForce()

                        # # Расчёт активной силы
                        # active_force = activation * multiplier * f_max
                        # length_data[name].append(active_force)

            
            # active_force = muscle.getActiveForce(state)
            # passive_force = muscle.getPassiveFiberForceAlongTendon(state)
            # if passive_force > -10:
            #     length_data[name].append(passive_force)
            length_data[name].append(length)

    # print()

time_points = [i * 0.01 for i in range(len(glove_test_angles[:1000:5]))]
for name, values in length_data.items():
    if (len(values) > 0):
        plt.plot(time_points, values, label=name)

plt.xlabel("Time")
plt.ylabel("Muscle Length")
plt.title("Muscle Length from Time")
plt.legend()
plt.grid(True)
plt.show()