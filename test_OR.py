import numpy as np
from itertools import combinations


def or_test(lista):
    sum_list = []
    # skapar A + B + C
    for i in lista:
        sum_list.append(i)

    print("A + B + C: ", sum_list)
    val_sum = sum(sum_list)

    # Beräknar A * B * C
    val_prod = 0
    if len(sum_list) > 2:
        val_prod = np.prod(sum_list)

    print("A * B * C: ", val_prod)

    # Skapar -AB -AC -BC
    negatives = list(combinations(lista, 2))

    for index in range(len(negatives)):
        negatives[index] = np.prod(negatives[index]) * -1
    print("AB +  AC: ", negatives)

    # Beräknar (A + B + C) - (AB + AC + BC) + (A * B * C)
    total = val_sum + negatives[0] + val_prod
    # print(total)