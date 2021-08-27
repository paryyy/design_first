import math
import numpy as np
from sympy import Eq, Symbol, solve

Td= 5.382
Td = round(Td, 2)
T_tuple = math.modf(Td)
T_Dec = T_tuple[0] * 100
T_Dec = round(T_Dec)
while T_Dec % 5 != 0:
    T_Dec += 1
Td = T_tuple[1]+(T_Dec/100)
print(Td)


# print(round(sep_a[0],2))

Do_Stainless_Carbon_list = {4.5: [0.43], 6.0: [0.32], 9.0: [0.22, 0.5], 12.0: [0.16, 0.38],
                            15.0: [0.17, 0.3], 18.0: [0.11, 0.25]}
a= Do_Stainless_Carbon_list[9][1]
print(a)

Volumetric_flow_rate_L = 2
Td = 1
if Volumetric_flow_rate_L/Td >0:
    print('check ')
a= 10
Td = 2
while Td < a/2 :
    Td+=0.5
print(Td)