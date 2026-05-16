import random
import os
import matplotlib.pyplot as plt
import numpy as np

from Solution.GeneticAlgorithm.Initialization.Decode import Decode
from Solution.GeneticAlgorithm.Initialization.Encode import Encode
from Solution.GeneticAlgorithm.Initialization.GA import GA
from DataSet.Instance import *


# Vẽ biểu đồ Gantt
def Gantt(Machines):
    M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite', 'navy', 'sandybrown', 'moccasin']

    plt.figure(figsize=(12, 6))
    for i in range(len(Machines)):
        Machine = Machines[i]
        Start_time = Machine.O_start
        End_time = Machine.O_end

        for i_1 in range(len(End_time)):
            task_info = Machine.assigned_task[i_1][0]

            if task_info == 'Break':
                task_color = 'black'
                task_label = 'X'
                hatch_style = '//'
                text_color = 'white'
            else:
                task_color = M[
                    (task_info - 1) % len(M)]  # % len(M) để tránh lỗi index out of range khi J_num lớn hơn số lượng màu
                task_label = str(task_info)
                hatch_style = ''
                text_color = 'black'

            plt.barh(i, width=End_time[i_1] - Start_time[i_1], height=0.8, left=Start_time[i_1],
                     color=task_color, edgecolor='black', hatch=hatch_style)
            plt.text(x=Start_time[i_1] + (End_time[i_1] - Start_time[i_1]) / 2 - 0.2, y=i - 0.1,
                     s=task_label, color=text_color, fontweight='bold')

    plt.yticks(np.arange(len(Machines)), np.arange(1, len(Machines) + 1))
    plt.title('Dynamic Scheduling Gantt Chart (with Breakdowns & Arrival Times)')
    plt.ylabel('Machines')
    plt.xlabel('Time(min)')
    plt.tight_layout()
    save_path = os.path.join(os.path.dirname(__file__), '', 'Gantt_GA.png')
    plt.savefig(save_path)
    plt.show()


if __name__ == '__main__':
    # Tự động tạo thư mục nếu chưa có
    os.makedirs(os.path.join(os.path.dirname(__file__), ''), exist_ok=True)
    Optimal_fit = 9999  # Độ thích nghi tốt nhất (khởi tạo)
    Optimal_CHS = 0  # Cá thể gene tương ứng với độ thích nghi tốt nhất (khởi tạo)
    best_fitness = 9999
    cmax = 0
    tardiness = 0
    g = GA()
    e = Encode(Processing_time, g.Pop_size, J, J_num, M_num)
    CHS1 = e.Global_initial()
    CHS2 = e.Random_initial()
    CHS3 = e.Local_initial()
    C = np.vstack((CHS1, CHS2, CHS3))
    Best_fit = []  # Ghi lại sự thay đổi của độ thích nghi trong quá trình lặp, thuận tiện cho việc vẽ đồ thị

    for i in range(g.Max_Itertions):
        print(f'Thế hệ thứ {i}! Best_fitness: {best_fitness:.2f} | Cmax: {cmax} | Tardiness: {tardiness}')

        # Tính toán fitness cho quần thể hiện tại
        Fit = g.fitness(C, J, Processing_time, M_num, O_num, Arrival_Time, Breakdowns, Due_Dates)
        Best = C[Fit.index(min(Fit))]
        best_fitness = min(Fit)

        if best_fitness < Optimal_fit:
            Optimal_fit = best_fitness
            Optimal_CHS = Best
            Best_fit.append(Optimal_fit)

            # Giải mã để lấy thông số thực tế in ra màn hình
            d = Decode(J, Processing_time, M_num, Arrival_Time, Breakdowns, Due_Dates)
            cmax, tardiness = d.decode(Optimal_CHS, O_num)

            print('--- New best_fitness found:', best_fitness)
            Gantt(d.Machines)
        else:
            Best_fit.append(Optimal_fit)

        # Quá trình tiến hóa: Lai ghép và Đột biến
        for j in range(len(C)):
            Cafter = [np.copy(C[j])]
            # Lai ghép
            if random.random() < g.Pc:
                N_i = random.choice(np.arange(len(C)))

                if random.random() < g.Pv:
                    Cross = g.machine_cross(np.copy(C[j]), np.copy(C[N_i]), O_num)
                else:
                    Cross = g.operation_cross(np.copy(C[j]), np.copy(C[N_i]), O_num, J_num)

                Cafter.append(Cross[0])
                Cafter.append(Cross[1])

            # Đột biến
            if random.random() < g.Pm:
                if random.random() < g.Pw:
                    Variance = g.machine_variation(np.copy(C[j]), Processing_time, O_num, J)
                else:
                    Variance = g.operation_variation(np.copy(C[j]), O_num, J_num, J, Processing_time, M_num,
                                                     Arrival_Time,
                                                     Breakdowns, Due_Dates)
                Cafter.append(Variance)

            # Chọn lọc cá thể tốt nhất sau biến dị đưa vào quần thể mới
            if Cafter != []:
                Fit_after = g.fitness(Cafter, J, Processing_time, M_num, O_num, Arrival_Time, Breakdowns, Due_Dates)
                C[j] = np.copy(Cafter[Fit_after.index(min(Fit_after))])

    # Vẽ đồ thị quá trình hội tụ
    x = np.linspace(0, g.Max_Itertions, g.Max_Itertions)
    plt.plot(x, Best_fit, '-k')
    plt.title('Giá trị hàm thích nghi qua các thế hệ dùng GA')
    plt.ylabel('Giá trị hàm thích nghi (Fitness)')
    plt.xlabel('Thế hệ (Iteration)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.savefig(os.path.join(os.path.dirname(__file__), '', 'Result_GA.png'), dpi=300)
    plt.show()