import numpy as np

def add_test(lista):
    sum_list = []
    for i in lista:
        sum_list.append(i)

     # Beräknar A * B * C
    val_prod = np.prod(sum_list)
    assert val_prod is int

