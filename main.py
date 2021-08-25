import math
import numpy as np

# {{ sieve tray }}
# {{  Get the tray spacing from the user  }}

# ایجاد لیست قطر و فاصله بین سینی ها  اولی ها قطر برجن دومی ها فاصله بین سینی ها
tray_spacing_TowerDiameter_list = [[np.arange(0, 1, 0.5), 0.5], [np.arange(1, 3, 0.5), 0.6],
                                   [np.arange(3, 4, 0.5), 0.75], [np.arange(4, 8, 0.5), 0.9]]

#   انتخاب فاصله سینی اولیه
tray_spacing = tray_spacing_TowerDiameter_list[0][1]  # input("enter tray spacing (If you press enter,
# the default value is 0.5)= ")


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
R = 8.314

#
# {{ mole average in liquid & vapor }}
MolAvg_liquid = 100 / ((Mfl / MolWt_1) + ((100 - Mfl) / MolWt_2))
MolAvg_gas = Mfv / 100 * MolWt_1 + (100 - Mfv) / 100 * MolWt_2
Volumetric_flow_rate_L = FlowRateLiquid * MolAvg_liquid / liquid_density
Gas_density = Pressure * MolAvg_gas / (R * (Temperature + 273)) * 100  # kg/m^3
print('Gas_density', Gas_density, 'MolAvg_gas', MolAvg_gas)
Volumetric_flow_rate_G = FlowRateVapor * MolAvg_gas / Gas_density  # m^3/s

# {{ commons }}

# انتخاب قطر سوراخ های سینی
Do_list = [4.5, 6.0, 9.0, 12.0, 15.0, 18]  # 3.0 was deleted
Do = 4.5

# انتخاب جنس برج برای طراحی و شماره دهی  0:استیل و 1:کربن
material_design = input('\n \nPlease select the material you want to design: Stainless steel or Carbon steel ('
                        'preferably '
                        'Stainless steel).= ')
if material_design == 'Stainless steel':
    material_design_id = 0
elif material_design == 'Carbon steel':
    material_design_id = 1
    Do = 9

# جدول قطرسوراخ و نسبت ضخامت به قطر سوراخ(L/Do) برای دو جنس 0:استیل و 1:کربن
Do_Stainless_Carbon_list = {4.5: [0.43], 6.0: [0.32], 9.0: [0.22, 0.5], 12.0: [0.16, 0.38],
                            15.0: [0.17, 0.3], 18.0: [0.11, 0.25]}

# فاصله مرکز سوراخ تا سوراخ روی سینی: P'  و L  ضخامت سینی
P_prim = math.ceil(2.5 * Do)  # common Distance to center (2.5-5)Do  [mm]
L = math.ceil(Do * Do_Stainless_Carbon_list[Do][material_design_id])  # common thickness  [mm]

#  محاسبهAo/Aa برای محاسبه CF
division_AoToAa = 0.907 * (Do ** 2 / P_prim ** 2)

#  {{ محاسبه CF }}
# ابتدا L'/G'(density_g/density_l)^0.5 که نامش را division_for_CF میگذاریم، را  محاسبه میکنیم
division_for_CF = ((Volumetric_flow_rate_L * liquid_density) / (Volumetric_flow_rate_G * Gas_density)) * (
        Gas_density / liquid_density) ** 0.5
if 0.01 <= division_for_CF <= 0.1:
    division_for_CF = 0.1

# f division_AoToAa >= 0.1:
# lif division_AoToAa < 0.1:

