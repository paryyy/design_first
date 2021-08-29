import math
import numpy as np
from sympy.abc import x
from sympy import Eq, solve

# {{ sieve tray }}
# {{ Condition of liquid flow  page 176 liquid flow number 2,3 and page 3 notebook }}
# {{ Give from user }}
FlowRateVapor = 0.1  # float(input("please enter Vapor Flow Rate(Kmol/s)= "))
FlowRateLiquid = 0.25  # float(input("please enter Liquid Flow Rate (Kmol/s)= "))
Temperature = 95  # C # float(input("please enter Temperature (C)= "))
Pressure = 1  # atm # float(input("please enter Pressure (atm)= "))
Mfv = 18  # float(input("please enter mole fraction in vapor= "))
Mfl = 15  # float(input("please enter mass fraction in liquid= "))
viscosity = 1.25 * 10 ** -5  # float(input("please enter viscosity of gas if you don't have it you can use viscosity of
# water = (Kg/m.s)"))
MolWt_1 = 32  # 1=Methanol float(input("please enter MolWt_1 = "))
MolWt_2 = 18  # 2=water float(input("please enter MolWt_2 = "))
liquid_density = 961  # float(input("please enter liquid density = "))
surface_tension = 0.04  # float(input("please enter Surface tension of the liquid mixture [N/m] = "))
R = 8.314
g = 9.807  # [m^2/s]
gc = 1
# {{ mole average in liquid & vapor }}
MolAvg_liquid = 100 / ((Mfl / MolWt_1) + ((100 - Mfl) / MolWt_2))
MolAvg_gas = Mfv / 100 * MolWt_1 + (100 - Mfv) / 100 * MolWt_2
Volumetric_flow_rate_L = round(FlowRateLiquid * MolAvg_liquid / liquid_density, 3)
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

# انتخاب قطر سوراخ های سینی
# Give from user:
Do = 4.5  # input("enter Hole Diameter [mm] (4.5 [mm] is good for first Choice or 9[mm] for stainless steel) ")
#  Give from user Weir length relative to diameter 0.6 0.65 0.7 0.75 0.8
# is common for first Choice 0.7(Tower Diameter)
times_w_t = 0.7  # float(input('How many times your Weir length than the diameter ? (it is better to be 0.7 times'))
#  table   6.1 (4)

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
# جدول قطرسوراخ و نسبت ضخامت به قطر سوراخ(L/Do) برای دو جنس 0:استیل و 1:کربن 6.2(2)
Do_Stainless_Carbon_list = {4.5: [0.43], 6.0: [0.32], 9.0: [0.22, 0.5], 12.0: [0.16, 0.38],
                            15.0: [0.17, 0.3], 18.0: [0.11, 0.25]}
# فاصله مرکز سوراخ تا سوراخ روی سینی: P'  و L  ضخامت سینی
# Give from User distance between hole center
Times_dis_hol = 2.5  # input('How many times the distance between the holes in the tray than the Tower diameter
# range Multiply is (2.5-5) and '
# 'common choice is 2.5 ')
Times_vn_vf = 0.8  # input('How many times your velocity than the flooding speed? (it is better to be 0.8 times but
# 0.75 times better if your input flow fluctuates a lot)')

P_prim = math.ceil(Times_dis_hol * Do)
L = math.ceil(Do * Do_Stainless_Carbon_list[Do][material_design_id])  # [mm]
division_L_to_do = Do_Stainless_Carbon_list[Do][material_design_id]


# تابعی برای منطقی و رند کردن شعاع ها
def _round_diameter(td):
    td = round(td, 2)
    t_tuple = math.modf(td)
    t_dec = t_tuple[0] * 100
    t_dec = round(t_dec)
    while t_dec % 5 != 0:
        t_dec += 1
    td = t_tuple[1] + (t_dec / 100)
    return td


division_AoToAa = round(0.907 * (Do ** 2 / P_prim ** 2), 4)


# print('division_AoToAa = ', division_AoToAa)


def _calc_vf_():
    #  {{ Calculation CF }}
    # ابتدا L'/G'(density_g/density_l)^0.5 که نامش را division_for_CF میگذاریم، را  محاسبه میکنیم
    division_for_cf = ((Volumetric_flow_rate_L * liquid_density) / (Volumetric_flow_rate_G * Gas_density)) * (
            Gas_density / liquid_density) ** 0.5
    if 0.01 <= division_for_cf <= 0.1:
        division_for_cf = 0.1
    # Calculation alfa and beta for CF
    alfa = 0.0744 * tray_spacing + 0.01173
    beta = 0.0304 * tray_spacing + 0.015
    if division_AoToAa <= 0.1:  # question for >=
        alfa = alfa * ((5 * division_AoToAa) + 0.5)
        beta = beta * ((5 * division_AoToAa) + 0.5)
    #  Calc CF
    cf = (alfa * (math.log((1 / division_for_cf), 10)) + beta) * (surface_tension / 0.020) ** 0.2
    # print('CF= ', CF)
    # {{ Calc VF }}
    vf = cf * ((liquid_density - Gas_density) / Gas_density) ** 0.5
    return vf


# ایجاد تابع برای شعاع محیط اتمسفریک
# محاسبهAo/Aa برای محاسبه CF برای محیط اتمسفریک
def _atmospheric_diam_tower_():
    vf = _calc_vf_()
    # {{ Calc VL }}
    # Give from user
    vn = Times_vn_vf * vf  # [m/s]    question:نمایش داده شده VL  گفت این سرعت گازه اما با
    # سطح مقطع کل برج منهای یک ناودان
    an = Volumetric_flow_rate_G / vn  # [m^2]
    # print('An= ', An)

    #  Give from user Weir length relative to diameter 0.6 0.65 0.7 0.75 0.8
    # is common for first Choice 0.7(Tower Diameter)
    times_w_t = 0.7  # float(input('How many times your Weir length than the diameter ? (it is better to be 0.7 times'))
    #  table   6.1 (4)
    #  نسبت طول بند به قطر برج  و ارتباطش با درصد سطح اشغال شده توسط ناودان اینجا به دادن جواب نسبت بسنده کردم
    division_ad_to_at_in_w_to_t_dic = {0.6: 5.257, 0.65: 6.899, 0.7: 8.808, 0.75: 11.255, 0.8: 14.145}
    w_to_area_used_by_one_downspout = division_ad_to_at_in_w_to_t_dic[times_w_t]
    # print('WToAreaUsedByOneDownSpout= ', WToAreaUsedByOneDownSpout)

    # solve At as x
    # At = An + (division_ad_to_at_in_w_to_t_dic[times_w_t]/100) * At
    eq_solve_at = Eq(an + (division_ad_to_at_in_w_to_t_dic[times_w_t] / 100) * x, x)
    at = solve(eq_solve_at)  # [m^2]
    # print('At= ', At)

    # value of Tower Diameter(Td) as x
    eq_solve_td = Eq((math.pi * x ** 2) / 4, at[0])
    td = solve(eq_solve_td)
    td = td[1]

    # print(Td)
    # برای رند کردن به عدد منطقی مانند 1.25 . 1.30 و.. ضرایبی از پنج
    # اول اعشارشو کندم به ضریبی از 5 تبدیل کردم و بعد دوباره اعشارو به عدد اضافه کردم

    td = _round_diameter(td)
    return [td, times_w_t, w_to_area_used_by_one_downspout, an]


# چک کردن q/T  در برج اتمسفریک
def _check_diameter_(td_atm):
    while Volumetric_flow_rate_L / td_atm > 0.015:
        td_atm += 0.05
    return td_atm


Times_W_T = _atmospheric_diam_tower_()[1]
WToAreaUsedByOneDownSpout = _atmospheric_diam_tower_()[2]


# محاسبه مساحت ها با شعاع جدید
def _calc_areas_(td):
    at = round(math.pi * td ** 2 / 4, 3)
    # محاسبه طول بند W  با قطر جدید
    w = round(Times_W_T * td, 3)  # [m]
    # محاسبه سطح مقطع ناودان
    ad = round(WToAreaUsedByOneDownSpout / 100 * at, 3)  # [m^2]
    # print(Ad)
    # مساحت سطح فعال
    aa = round(at - 2 * ad - 0.2 * (at - 2 * ad), 2)
    # print('Ad', Ad)
    return [at, ad, aa, w]


def _calcs_atmospheric_():
    # شعاع برج اتمسفریک
    td_atmospheric, an = _atmospheric_diam_tower_()[0], round(_atmospheric_diam_tower_()[3], 4)
    # محاسبه مجدد مساحت ها با شعاع جدید
    at, ad, aa, w = _calc_areas_(td_atmospheric)
    # چک کردن شرط q/T<0.015
    td_atmospheric = _check_diameter_(td_atmospheric)
    return [td_atmospheric, at, ad, aa, w, an]


def _calcs_under_pressure_():
    t_d = Volumetric_flow_rate_L / Times_W_T * 0.032
    t_d = _round_diameter(t_d)
    while t_d <= Volumetric_flow_rate_L / Times_W_T * 0.032:
        t_d += 0.05
    at, ad, aa, w = _calc_areas_(t_d)
    an = round(at - ad, 4)
    vn = Volumetric_flow_rate_G / an
    vf = _calc_vf_()
    while vn >= Times_vn_vf * vf:
        t_d += 0.25
        at, ad, aa, w = _calc_areas_(t_d)
        an = at - ad
        vn = Volumetric_flow_rate_G / an
    return [t_d, at, ad, aa, w, an]


# {{ محاسبات مربوط به برج اتمسفریک , خلا }}
if Pressure == 1:
    Td = _calcs_atmospheric_()[0]
    Td_check = Td
    W = _calcs_atmospheric_()[4]
    Aa = _calcs_atmospheric_()[3]
    An = _calcs_atmospheric_()[5]
    # print('An= ', An)
    # print('Aa= ', Aa)
    # print(Td_atmospheric)
# {{ محاسبات مربوط به برج تحت فشار }}
if Pressure > 1:
    Td = _calcs_under_pressure_()[0]
    Td_check = Td
    W = _calcs_under_pressure_()[4]
    Aa = _calcs_under_pressure_()[3]
    An = _calcs_under_pressure_()[5]
    # print('An= ', An)
    # print('Td_under_pressure= ', Td_under_pressure)


# {{ مسئله هیدرودینامیک }}
def _h1_():
    # hh1 همون h1 هست
    hh1 = round((1 / 1.839 * Volumetric_flow_rate_L / W) ** (2 / 3), 3)  # [m]
    # print(hh1)
    if times_w_t < 0.7:
        # solve w as x
        eq_solve_w = Eq((Td / W) ** 2 - ((((Td / W) ** 2) - 1) ** 0.5 + (2 * h1 / Td * (Td / W))) ** 2, x ** 2)
        y = solve(eq_solve_w)  # [m^2]
        hh1 = round((hh1 * (1 / y[1]) ** (2 / 3)), 3)  # [m]
        return hh1


# ارتفاع مایع روی بند خروجی از سینی
h1 = _h1_()

# ارتفاع بند: weir height
if Pressure == 1:
    hw = 50  # float(input('enter weir height [mm] is common between (50 - 100) and better is 50 [mm]'))
if Pressure > 1:
    hw = 25  # float(input('enter weir height [mm] is common between (25 - 50) and better is 25 [mm]'))


def _calc_h_():
    # {{  افت فشار سینی  }}

    # {{  calc hD      افت فشار مایع روی سینی: hD     }}
    # calc Co
    co = round(1.09 / division_L_to_do ** 0.25, 3)  # [mm]
    # print('Co= ', Co)
    # calc Ao
    ao = round(division_AoToAa * Aa, 2)  # [m^2]
    # print(Ao)
    # calc Vo  سرعت گاز در هر سوراخ
    vo = round(Volumetric_flow_rate_G / ao, 1)  # [m/s]
    # print(Vo)
    # calc Re
    re = (Gas_density * vo * Do * 0.001) / viscosity
    # print(Re)
    # calc f
    # solve f as x that x = 1 / sqrt(f)
    eq_f = Eq((3.6 * math.log(re / 7, 10)) ** 2, 1 / x)
    f = solve(eq_f)
    f = round(f[0], 3)
    # print(f)
    # calc hD
    #  افت فشار مایع روی سینی: hD
    eq_hd = Eq(co * ((0.4 * (1.25 - (ao / An))) + (4 * f * division_L_to_do) + (1 - ao / An) ** 2), 2 * x * g *
               liquid_density / (vo ** 2 * Gas_density))
    solve_hd = solve(eq_hd)
    hd = round(solve_hd[0], 4)  # [متر مایع روی سینی]
    # print('hD= ', hD)

    # {{  calc hL   # افت اصطکاکی جریان گاز به خاطر مایع روی سینی  }}
    # calc Z
    z = (W + Td) / 2  # [m]
    # print(z)
    # calc Va
    va = round(Volumetric_flow_rate_G / Aa, 3)  # [m/s]
    # print(Va)
    # calc hL as x
    eq_hl = Eq((6.1 * 10 ** (-3)) + (0.725 * hw * 10 ** -3) - (0.238 * hw * 10 ** -3 * va * (Gas_density ** 0.5)) + (
            1.225 * Volumetric_flow_rate_L / z), x)
    solve_hl = solve(eq_hl)
    hl = round(solve_hl[0], 2)  # [m]
    # print(hL)

    # {{ hR افت فشار اضافی ناشی از کشش سطحی }}
    # calc hR
    hr = round(6 * surface_tension * gc / (liquid_density * Do * 10 ** -3 * g), 4)  # [m]

    # calc hG  افت فشار گاز در یک سینی
    hg = round(hd + hl + hr, 3)  # [m]
    # print(hG)
    # محاسبه افت فشار روی هر سینی
    delta_p = liquid_density * g * hg  # [pa]
    # print(delta_P)
    # 6.1 (5)   چک کردن افت فشار روی هر سینی
    if Pressure == 1 :
        while delta_p < 500 :
            Td -= 0.05



