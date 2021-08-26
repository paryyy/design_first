import math
import numpy as np

# {{ sieve tray }}

# {{ Condition of liquid flow  page 176 liquid flow number 2,3 and page 3 notebook }}


# {{ Give from user }}
FlowRateVapor = 0.1  # float(input("please enter Vapor Flow Rate(Kmol/s)= "))
FlowRateLiquid = 0.25  # float(input("please enter Liquid Flow Rate (Kmol/s)= "))
Temperature = 95  # C # float(input("please enter Temperature (C)= "))
Pressure = 1  # atm # float(input("please enter Pressure (atm)= "))
Mfv = 18  # float(input("please enter mole fraction in vapor= "))
Mfl = 15  # float(input("please enter mass fraction in liquid= "))
viscosity = 1.25 * 10 ** -5  # float(input("please enter viscosity of gas= (Kg/m.s)"))
MolWt_1 = 32  # 1=Methanol float(input("please enter MolWt_1 = "))
MolWt_2 = 18  # 2=water float(input("please enter MolWt_2 = "))
liquid_density = 961  # float(input("please enter liquid density = "))
surface_tension = 0.04  # float(input("please enter Surface tension of the liquid mixture [N/m] = "))
R = 8.314

# {{ mole average in liquid & vapor }}
MolAvg_liquid = 100 / ((Mfl / MolWt_1) + ((100 - Mfl) / MolWt_2))
MolAvg_gas = Mfv / 100 * MolWt_1 + (100 - Mfv) / 100 * MolWt_2
Volumetric_flow_rate_L = FlowRateLiquid * MolAvg_liquid / liquid_density
Gas_density = Pressure * MolAvg_gas / (R * (Temperature + 273)) * 100  # kg/m^3
Volumetric_flow_rate_G = FlowRateVapor * MolAvg_gas / Gas_density  # m^3/s

# {{  Get the tray spacing and Tower Diameter from user  }}
# جدول قطر و فاصله بین سینی ها  اولی ها قطر برجن دومی ها فاصله بین سینی ها
# show user table
tray_spacing_TowerDiameter_list = [[1, 0.5], [np.arange(1, 3, 0.5), 0.6],
                                   [np.arange(3, 4, 0.5), 0.75], [np.arange(4, 8, 0.5), 0.9]]
# Give from user:
TowerDiameter = 1  # float(input("please enter TowerDiameter [m] (1 [m] is good for first Choice)= "))
#   انتخاب فاصله سینی اولیه
tray_spacing = 0.5  # input("enter tray spacing [m] (0.5 [m] is good for first Choice) ")

# انتخاب جنس برج برای طراحی و شماره دهی  0:استیل و 1:کربن
material_design = input('\n \nPlease select the material you want to design: Stainless steel or Carbon steel ('
                        'preferably '
                        'Stainless steel).= ')
if material_design == 'Stainless steel':
    material_design_id = 0
elif material_design == 'Carbon steel':
    material_design_id = 1
    Do = 9

# show user table
if material_design == 'Stainless steel':
    # Show this for user
    Do_list = [4.5, 6.0, 9.0, 12.0, 15.0, 18]
elif material_design == 'Carbon steel':
    Do_list = [9.0, 12.0, 15.0, 18]
# انتخاب قطر سوراخ های سینی
# Give from user:
Do = 4.5  # input("enter Hole Diameter [mm] (4.5 [mm] is good for first Choice or 9[mm] for stainless steel) ")

# جدول قطرسوراخ و نسبت ضخامت به قطر سوراخ(L/Do) برای دو جنس 0:استیل و 1:کربن
Do_Stainless_Carbon_list = {4.5: [0.43], 6.0: [0.32], 9.0: [0.22, 0.5], 12.0: [0.16, 0.38],
                            15.0: [0.17, 0.3], 18.0: [0.11, 0.25]}

# فاصله مرکز سوراخ تا سوراخ روی سینی: P'  و L  ضخامت سینی
# Give from User distance between hole center
Times_dis_hol = 2.5  # input('How many times the distance between the holes in the tray than the Tower diameter
# range Multiply is (2.5-5) and '
# 'common choice is 2.5 ')
P_prim = math.ceil(Times_dis_hol * Do)
L = math.ceil(Do * Do_Stainless_Carbon_list[Do][material_design_id])  # [mm]

#  محاسبهAo/Aa برای محاسبه CF
division_AoToAa = 0.907 * (Do ** 2 / P_prim ** 2)
print('division_AoToAa = ', division_AoToAa)

#  {{ Calculation CF }}
# ابتدا L'/G'(density_g/density_l)^0.5 که نامش را division_for_CF میگذاریم، را  محاسبه میکنیم
division_for_CF = ((Volumetric_flow_rate_L * liquid_density) / (Volumetric_flow_rate_G * Gas_density)) * (
        Gas_density / liquid_density) ** 0.5
if 0.01 <= division_for_CF <= 0.1:
    division_for_CF = 0.1
# Calculation alfa and beta for CF
alfa = 0.0744 * tray_spacing + 0.01173
beta = 0.0304 * tray_spacing + 0.015
if division_AoToAa <= 0.1:  # question for >=
    alfa = alfa * ((5 * division_AoToAa) + 0.5)
    beta = beta * ((5 * division_AoToAa) + 0.5)
#  Calc CF
CF = (alfa * (math.log((1 / division_for_CF), 10)) + beta) * (surface_tension / 0.020) ** 0.2
# print('CF= ', CF)


# {{ Calc VF }}
VF = CF * ((liquid_density - Gas_density) / Gas_density) ** 0.5

# {{ Calc VL }}
# Give from user

Times_Vn_VF = 0.8  # input('How many times your velocity than the flooding speed? (it is better to be 0.8 times but
# 0.75 times better if your input flow fluctuates a lot)')
Vn = Times_Vn_VF * VF  # [m/s]    question:نمایش داده شده VL  گفت این سرعت گازه اما با

# سطح مقطع کل برج منهای یک ناودان
An = Volumetric_flow_rate_G / Vn  # [m^2]
# print('An= ', An)


#  Give from user Weir length relative to diameter 0.6 0.65 0.7 0.75 0.8
# is common for first Choice 0.7(Tower Diameter)
Times_W_T = 0.7  # float(input('How many times your Weir length than the diameter ? (it is better to be 0.7 times'))
#  table   6.1 (4)
#  نسبت طول بند به قطر برج  و ارتباطش با درصد سطح اشغال شده توسط ناودان اینجا به دادن جواب نسبت بسنده کردم
WToAreaUsedByOneDownSpout_list = {0.6: 5.257, 0.65: 6.899, 0.7: 8.808, 0.75: 11.255, 0.8: 14.145}
WToAreaUsedByOneDownSpout = WToAreaUsedByOneDownSpout_list[Times_W_T]

