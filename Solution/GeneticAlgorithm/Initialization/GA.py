import itertools
import random

import numpy as np

from Solution.GeneticAlgorithm.Initialization.Decode import Decode
from DataSet.Instance import *


class GA():
    def __init__(self):
        self.Pop_size = 200  # Số lượng cá thể trong quần thể
        self.Pc = 0.8  # Xác suất lai ghép
        self.Pm = 0.8  # Xác suất đột biến
        self.Pv = 0.5  # Ngưỡng xác suất để chọn phương pháp lai ghép
        self.Pw = 0.95  # Ngưỡng xác suất để chọn phương pháp đột biến
        self.Max_Itertions = 200  # Số lần lặp tối đa
        # Trọng số ưu tiên (alpha: Makespan, beta: Tardiness)
        self.alpha = 0.7
        self.beta = 0.3

    # Hàm thích nghi đa mục tiêu
    def fitness(self, CHS, J, Processing_time, M_num, Len, Arrival_Time, Breakdowns, Due_Dates):
        Fit = []
        for i in range(len(CHS)):
            d = Decode(J, Processing_time, M_num, Arrival_Time, Breakdowns, Due_Dates)
            Cmax, Tardiness = d.decode(CHS[i], Len)
            # Hàm mục tiêu tổng hợp (Weighted Sum)
            Fit.append((self.alpha * Cmax) + (self.beta * Tardiness))
        return Fit

    # Lai ghép phần máy móc
    def machine_cross(self, CHS1, CHS2, T0):
        """
        :param CHS1: Gene phần chọn máy 1
        :param CHS2: Gene phần chọn máy 2
        :param T0: Tổng số công đoạn
        :return: Gene phần chọn máy sau khi lai ghép
        """
        T_r = [j for j in range(T0)]; r = random.randint(1, 10); random.shuffle(T_r); R = T_r[0:r]
        OS_1 = CHS1[O_num:2 * T0]; OS_2 = CHS2[O_num:2 * T0]
        MS_1 = CHS2[0:T0]; MS_2 = CHS1[0:T0]
        for i in R:
            K, K_2 = MS_1[i], MS_2[i]; MS_1[i], MS_2[i] = K_2, K
        return np.hstack((MS_1, OS_1)), np.hstack((MS_2, OS_2))

    # Lai ghép phần công đoạn
    def operation_cross(self, CHS1, CHS2, T0, J_num):
        """
        :param CHS1: Gene phần chọn công đoạn 1
        :param CHS2: Gene phần chọn công đoạn 2
        :param T0: Tổng số công đoạn
        :param J_num: Tổng số công việc
        :return: Gene phần chọn công đoạn sau khi lai ghép
        """
        OS_1 = CHS1[T0:2 * T0]; OS_2 = CHS2[T0:2 * T0]
        MS_1 = CHS1[0:T0]; MS_2 = CHS2[0:T0]
        Job_list = [i for i in range(J_num)]; random.shuffle(Job_list)
        r = random.randint(1, J_num - 1); Set1 = Job_list[0:r]; new_os = list(np.zeros(T0, dtype=int))
        for k, v in enumerate(OS_1):
            if v in Set1: new_os[k] = v + 1
        for i in OS_2:
            if i not in Set1: site = new_os.index(0); new_os[site] = i + 1
        new_os = np.array([j - 1 for j in new_os])
        return np.hstack((MS_1, new_os)), np.hstack((MS_2, new_os))

    # Đột biến phần máy móc
    def machine_variation(self, CHS, O, T0, J):
        """
        :param CHS: Gene phần chọn máy
        :param O: Ma trận thời gian gia công
        :param T0: Tổng số công đoạn
        :param J: Thông tin gia công của từng công việc
        :return: Gene phần chọn máy sau khi đột biến
        """
        Tr = [i for i in range(T0)]; MS = CHS[0:T0]; OS = CHS[T0:2 * T0]
        r = random.randint(1, T0 - 1); random.shuffle(Tr); T_r = Tr[0:r]
        for num in T_r:
            K = []; site = 0
            for k, v in J.items(): K.append([j for j in range(site, site + v)]); site += v
            for i in range(len(K)):
                if num in K[i]: O_i = i; O_j = K[i].index(num); break
            Machine_using = O[O_i][O_j]; Machine_time = [j for j in Machine_using if j != 9999]
            MS[num] = Machine_time.index(min(Machine_time))
        return np.hstack((MS, OS))

    # Đột biến phần công đoạn
    def operation_variation(self, CHS, T0, J_num, J, O, M_num, Arrival_Time, Breakdowns, Due_Dates):
        """
        :param CHS: Gene phần chọn công đoạn
        :param T0: Tổng số công đoạn
        :param J_num: Tổng số công việc
        :param J: Thông tin gia công của từng công việc
        :param O: Ma trận thời gian gia công
        :param M_num: Tổng số máy
        :return: Gene phần chọn công đoạn sau khi đột biến
        """
        MS = CHS[0:T0]; OS = list(CHS[T0:2 * T0])
        r = random.randint(2, min(4, J_num - 1)); Tr = [i for i in range(J_num)]; random.shuffle(Tr); Tr = Tr[0:r]
        site = [OS.index(Tr[i]) for i in range(r)]; A = list(itertools.permutations(Tr, r)); A_CHS = []
        for i in range(len(A)):
            for j in range(len(A[i])): OS[site[j]] = A[i][j]
            A_CHS.append(np.hstack((MS, OS)))
        Fit = []
        for i in range(len(A_CHS)):
            d = Decode(J, O, M_num, Arrival_Time, Breakdowns, Due_Dates)
            Cmax, Tardiness = d.decode(A_CHS[i], T0)
            Fit.append((self.alpha * Cmax) + (self.beta * Tardiness))
        return A_CHS[Fit.index(min(Fit))]