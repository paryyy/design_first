import math
import numpy as np

Do = 4.5

# جدول قطرسوراخ و نسبت ضخامت به قطر سوراخ(L/Do) برای دو جنس 0:استیل و 1:کربن
Do_Stainless_Carbon_list = {4.5: [0.43], 6.0: [0.32], 9.0: [0.22, 0.5], 12.0: [0.16, 0.38],
                            15.0: [0.17, 0.3], 18.0: [0.11, 0.25]}
material_design_id = 0

# فاصله مرکز سوراخ تا سوراخ روی سینی: P'  و L  ضخامت سینی
P_prim = math.ceil(2.5 * Do)  # common Distance to center (2.5-5)Do  [mm]
L = math.ceil(Do * Do_Stainless_Carbon_list[Do][material_design_id])  # common thickness  [mm]

# محاسبهAo/Aa
divi_Ao_Aa = 0.907 * (Do ** 2 / P_prim ** 2)

a = 0.02
# if 0.50 <= value <= 150 and round(value, 2) == value:
if 0.01 <= a <= 0.1:
    print('yess')

start = 1.0
stop = 3.0
step = 0.5
float_range_array = np.arange(1, 3, 0.5)
float_range_list = list(float_range_array)
print('float_range_list= ', float_range_list)


b = {1: np.arange(0, 3, 0.5)}
c = 0.5
if c in b[1]:
    print('i can check the range in dict yessss')

a_list = [[1, np.arange(0.1, 0.7, 0.1)], [2, 0.1]]
b_list = [[1, 0.5], [2, 0.1]]
print('b_list[0][1] = ', b_list[0][1])


tray_spacing_TowerDiameter_list = [[np.arange(0, 1, 0.5), 0.5], [np.arange(1, 3, 0.5), 0.6],
                                   [np.arange(3, 4, 0.5), 0.75], [np.arange(4, 8, 0.5), 0.9]]
tray_spacing = tray_spacing_TowerDiameter_list[0][1] # input("enter tray spacing (If you press enter, the default value is 0.5)= ")
print('tray_spacing', tray_spacing)

