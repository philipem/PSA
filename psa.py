import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations



probs = {
    "314_VA": 3.5*10**-4,
    "314_VB": 3.5*10**-4,
    "314_VC": 2.1*10**-4,

    "323_PA_OS": 40.1*10**-6,
    "323_PA_US": 9.4*10**-4,
    "323_PB_OS": 40.1*10**-6,
    "323_PB_US": 9.4*10**-4,
    "323_TA_UF": 2.5*10**-5,
    "323_TB_UF": 2.5*10**-5,
    "323_VA_UÖ": 7.8*10**-5,
    "323_VB_UÖ": 7.8*10**-5,
    "323_VC_SL": 4.0*10**-4,
    "323_VD_SL": 4.0*10**-4,

    "327_PA_OS": 40.1*10**-6,
    "327_PA_US": 2.4*10**-3,
    "327_PB_OS": 40.1*10**-6,
    "327_PB_US": 2.4*10**-3,
    "327_TA_UF": 8.7*10**-4,
    "327_VA_UÖ": 1.1*10**-4,
    "327_VB_UÖ": 6.7*10**-4,
    "327_VC_SL": 1.3*10**-4,

    "631_IS": 3.2*10**-6,
    "641_IS": 7.1*10**-6,
    "642_IS": 7.1*10**-6,

    "721_UK": 2.0*10**-6 ,
    "722_UK": 2.0*10**-6 ,
    "751_IK": 58.0*10**-5
}

probs_proj = {

    "V1_IT": 1.0 * 10 ** -4,
    "V2_IT": 1.0 * 10 ** -4,
    "V3_IT": 1.0 * 10 ** -4,
    "V4_FS": 8.0 * 10 ** -4,
    "V5_FS": 8.0 * 10 ** -4,
    "SUMP_IT": 3 * 10 ** -7,
    "LPP_USTA": 3.0 * 10 ** -3,
    "LPP_USTR": 3.0 * 10 ** -6,
    "LPP_DS": 1.3 * 10 ** -5,
    "HPP_USTA": 2.3 * 10 ** -3,
    "HPP_USTR": 3.0 * 10 ** -6,
    "HPP_DS": 1.5 * 10 ** -5,

    "V6_FS": 8.0 * 10 ** -4,
    "V7_FS": 8.0 * 10 ** -4,
    "V8_UÖ": 8.0 * 10 ** -4,
    "V9_UÖ": 8.0 * 10 ** -4,
    "TANK_TOM": 2.0 * 10 ** -7,
    "CSP_USTA": 3.0 * 10 ** -3,
    "CSP_USTR": 3.0 * 10 ** -6,
    "CSP_DS": 1.3 * 10 ** -5,
    "HE_IT": 3 * 10 ** -7,
    "SPRINKLER_FS": 3.0 * 10 ** -4,

}


def plot_bars(probs, tot):
    """
    Plot function which returns each probability of components as a bar chart normalized over the total number of
    parts in the entire system.

    :param probs:

        A dictionary of all the probabilities in the entire system.

    :param tot:

        The number of parts in the system.

    :return:

        A barchart of all probabilities.
    """

    plt.figure(1)

    factor = 1 / tot

    for i in probs.keys():
        probs[i] = probs[i] * factor

    plt.bar(list(probs.keys()), probs.values(), color='g')
    plt.xticks(list(probs.keys()), probs.keys(), rotation='vertical')

def AND(lista):
    """
       This method returns the value for a logical AND gate given the different parts connected to it.

       :param lista:

           Takes an input list of single float values for every part of the component system.

       :return:

           The probability for this gate to fail.
       """

    sum_list = []
    for i in lista:
        sum_list.append(i)

    # Beräknar A * B * C
    val_prod = np.prod(sum_list)
    # print(val_prod)

    return val_prod


def OR(lista):
    """
    This method returns the value for a logical OR gate given the different parts connected to it.

    :param lista:

        Takes an input list of single float values for every part of the component system.

    :return:

        The probability for this gate to fail.
    """

    sum_list = []
    # skapar A + B + C
    for i in lista:
        sum_list.append(i)

    # print("A + B + C: ", sum_list)
    val_sum = sum(sum_list)

    # Beräknar A * B * C
    val_prod = 0
    if len(sum_list) > 2:
        val_prod = np.prod(sum_list)

    # print("A * B * C: ", val_prod)

    # Skapar -AB -AC -BC
    negatives = list(combinations(lista, 2))

    for index in range(len(negatives)):
        negatives[index] = np.prod(negatives[index]) * -1
    # print("AB +  AC: ", negatives)

    # Beräknar (A + B + C) - (AB + AC + BC) + (A * B * C)
    total = val_sum + negatives[0] + val_prod
    # print(total)
    return total


def lab():
    """
    This function calculates the probabilites of three different components of a nuclear cooling system.
    The system consists of the following components:

        - Low pressure
        - High pressure
        - Pressure lowering

    :return:

    Each calculation returns the probability that the component fails.
    """

    # Low pressure.
    sexton = OR([probs['323_VD_SL'], probs['323_TB_UF']])
    elva = OR([probs['323_VC_SL'], probs['323_TA_UF']])
    sex = OR([probs['323_PB_US'], probs['323_PB_OS'], probs['641_IS'], probs['722_UK'], sexton])
    fyra = OR([probs['323_PA_US'], probs['323_PA_OS'], probs['641_IS'], probs['722_UK'], elva])
    tva = OR([probs['323_VB_UÖ'], sex])
    ett = OR([probs['323_VA_UÖ'], fyra])
    fin_low = AND([ett, tva])

    print("This is low pressure: {}".format(fin_low))

    # High pressure.
    tio = OR([probs['327_VC_SL'], probs['327_TA_UF']])
    sex = OR([probs['721_UK'], tio])
    otta = OR([probs['327_PB_US'], probs['327_PB_OS'], probs['642_IS']])
    sju = OR([probs['327_PA_US'], probs['327_PA_OS'], probs['641_IS']])
    fem = AND([sju, otta])
    fyra = OR([fem, sex])
    tva = OR([probs['327_VB_UÖ'], probs['631_IS'], fyra])
    fin_high = OR([probs['327_VA_UÖ'], tva])

    print("This is high pressure: {}".format(fin_high))

    # Pressure lowering.
    tva = OR([probs['631_IS'], probs['314_VC']])
    tre = OR([probs['314_VA'], probs['751_IK']])
    fyra = OR([probs['314_VB'], probs['751_IK']])
    ett = AND([tre, fyra])
    fin_down = AND([ett, tva])

    print("This is high pressure: {}".format(fin_down))

    # plot_bars(probs, 30)
    # plt.show()


def proj():
    """
        This function calculates the probabilites of three different components of a nuclear cooling system.
        The system consists of the following components:

            - Containment cooling.
            - Pressure injection.

        :return:

            Each calculation returns the probability that the component fails.

        TODO:

            Fråga om antalet sannolikheter? Behöver alla som finns i listan kopplade till en vill komponent vara med?

        """

    # behov = input('Har du behov? Skriv då in behovet!')
    # hr = input('Är du i behov av antal timmar? Skriv då in antal timmar!')

    # Containment.
    V9_ej_vatten = OR([probs_proj['V8_UÖ'], probs_proj['SUMP_IT']])
    V9_fail = OR([probs_proj['V9_UÖ'], V9_ej_vatten])
    V6_fail =  OR([probs_proj['V6_FS'], probs_proj['TANK_TOM']])
    CSP_ej_vatten = AND([V6_fail, V9_fail])
    HE_ej_vatten = OR([probs_proj['CSP_USTA'], probs_proj['CSP_USTR'], probs_proj['CSP_DS'], CSP_ej_vatten])
    V7_ej_vatten = OR([probs_proj['CSP_USTA'], HE_ej_vatten])
    SPRINKLER_ej_vatten = OR([probs_proj['V7_FS'], V7_ej_vatten])
    TOP_cont = OR([probs_proj['SPRINKLER_FS'], SPRINKLER_ej_vatten])

    print('This is containment fail prob {}'.format(TOP_cont))

    # Pressure injection.
    PP_ej_vatten = AND([V6_fail, V9_fail])
    V4_ej_vatten = OR([probs_proj['LPP_USTA'], probs_proj['LPP_USTR'], probs_proj['LPP_DS'], PP_ej_vatten])
    V5_ej_vatten = OR([probs_proj['HPP_USTA'], probs_proj['HPP_USTR'], probs_proj['HPP_DS'], PP_ej_vatten])
    V2_ej_vatten = OR([probs_proj['V4_FS'], V4_ej_vatten])
    V2_fail = OR([probs_proj['V2_IT'], V2_ej_vatten])
    V3_ej_vatten = OR([probs_proj['V5_FS'], V5_ej_vatten])
    V3_fail = OR([probs_proj['V3_IT'], V3_ej_vatten])
    V1_ej_vatten = AND([V2_fail, V3_fail])
    TOP_inj = OR([probs_proj['V1_IT'], V1_ej_vatten])

    print('This is pressure fail prob {}'.format(TOP_inj))


proj()
