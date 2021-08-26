import math
import numpy as np

c = math.log(10, 10)

a = np.arange(1, 3, 0.5)
c = np.arange(1, 3, 0.5)
b = [[np.arange(1, 3, 0.5), 2], [[1.4, 8.5], 3]]

f=(b[0][0])
print(f[1])


tray_spacing_TowerDiameter_list = [[1, 0.5], [np.arange(1, 3, 0.5), 0.6],
                                   [np.arange(3, 4, 0.5), 0.75], [np.arange(4, 8, 0.5), 0.9]]
TowerDiameter_list = tray_spacing_TowerDiameter_list[0][0]
print(TowerDiameter_list)


Times_W_T = 0.7  # float(input('How many times your Weir length than the diameter ? (it is better to be 0.7 times'))
#  table   6.1 (4)
#  نسبت طول بند به قطر برج  و ارتباطش با درصد سطح اشغال شده توسط ناودان اینجا به دادن جواب نسبت بسنده کردم
WToAreaUsedByOneDownSpout_list = {0.6: 5.257, 0.65: 6.899, 0.7: 8.808, 0.75: 11.255, 0.8: 14.145}
A=WToAreaUsedByOneDownSpout_list[Times_W_T]
print(A)