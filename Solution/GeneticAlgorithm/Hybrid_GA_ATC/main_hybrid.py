import random
import matplotlib.pyplot as plt
import numpy as np
import os

from DataSet.Instance import *
from Solution.DispatchingRules.Dispatching_Simulator import ATCSimulator
from Solution.GeneticAlgorithm.Initialization.Decode import Decode
from Solution.GeneticAlgorithm.Initialization.Encode import Encode
from Solution.GeneticAlgorithm.Initialization.GA import GA


def Gantt_Hybrid(Machines, title='Gantt Chart'):
    M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite', 'navy', 'sandybrown', 'moccasin']

    plt.figure(figsize=(12, 6))
    for i in range(len(Machines)):
        Machine = Machines[i]
        Start_time, End_time = Machine.O_start, Machine.O_end
        for i_1 in range(len(End_time)):
            task_info = Machine.assigned_task[i_1][0]
            if task_info == 'Break':
                task_color, task_label, hatch_style, text_color = 'black', 'X', '//', 'white'
            else:
                task_color = M[(task_info - 1) % len(M)]
                task_label, hatch_style, text_color = str(task_info), '', 'black'

            plt.barh(i, width=End_time[i_1] - Start_time[i_1], height=0.8, left=Start_time[i_1],
                     color=task_color, edgecolor='black', hatch=hatch_style)
            plt.text(x=Start_time[i_1] + (End_time[i_1] - Start_time[i_1]) / 2 - 0.2, y=i - 0.1,
                     s=task_label, color=text_color, fontweight='bold')

    plt.yticks(np.arange(len(Machines)), np.arange(1, len(Machines) + 1))
    plt.title(title)
    plt.ylabel('Machines')
    plt.xlabel('Time (min)')
    plt.tight_layout()

    # Lưu ảnh vào thư mục Hybrid_GA_ATC
    save_path = os.path.join(os.path.dirname(__file__), '', 'Gantt_Hybrid.png')
    plt.savefig(save_path)
    plt.close()


def atc_to_chromosome(sim_machines, J_dict, J_total, O_total, P_time):
    ms_gene, os_tasks = np.zeros(O_total, dtype=int), []

    def get_ms_index(job_id, op_idx):
        idx = 0
        for j_id in range(1, job_id): idx += J_dict[j_id]
        return idx + op_idx

    for m_idx, m_data in enumerate(sim_machines):
        for start, end, task_id in m_data['history']:
            if task_id != 'Break': os_tasks.append((start, task_id))

    os_tasks.sort(key=lambda x: x[0])
    os_gene = np.array([t[1] - 1 for t in os_tasks])

    counter_ms = {i: 0 for i in range(1, J_total + 1)}
    for start, job_id in os_tasks:
        for m_idx, m_data in enumerate(sim_machines):
            for s, e, t_id in m_data['history']:
                if s == start and t_id == job_id:
                    ms_idx = get_ms_index(job_id, counter_ms[job_id])
                    valid_machines = [k for k, time in enumerate(P_time[job_id - 1][counter_ms[job_id]]) if
                                      time != 9999]
                    ms_gene[ms_idx] = valid_machines.index(m_idx) if m_idx in valid_machines else 0
                    counter_ms[job_id] += 1
                    break
    return np.hstack((ms_gene, os_gene))


if __name__ == '__main__':
    # Tự động tạo thư mục nếu chưa có
    os.makedirs(os.path.join(os.path.dirname(__file__), ''), exist_ok=True)

    print("--- BƯỚC 1: CHẠY ATC TẠO ELITE SEED  ---")
    sim = ATCSimulator(J, Processing_time, M_num, Arrival_Time, Due_Dates, Breakdowns, k_parameter=2.0)
    cmax_atc, tardy_atc = sim.run()
    fitness_atc = (0.7 * cmax_atc) + (0.3 * tardy_atc)
    print(f"ATC Baseline -> Fitness: {fitness_atc:.2f} | Cmax: {cmax_atc} | Tardiness: {tardy_atc}\n")

    atc_chromosome = atc_to_chromosome(sim.machines, J, J_num, O_num, Processing_time)

    print("--- BƯỚC 2: TIẾN HÓA GA VỚI HYBRID SEED ---")
    g = GA()
    e = Encode(Processing_time, g.Pop_size, J, J_num, M_num)
    C = np.vstack((e.Global_initial(), e.Random_initial(), e.Local_initial()))
    C[0] = np.copy(atc_chromosome)  # Cấy NST được tạo ra sử dụng ATC

    Optimal_fit, Optimal_CHS, Best_fit = 9999, None, []

    for i in range(g.Max_Itertions):
        Fit = g.fitness(C, J, Processing_time, M_num, O_num, Arrival_Time, Breakdowns, Due_Dates)
        best_fitness = min(Fit)

        if best_fitness < Optimal_fit:
            Optimal_fit = best_fitness
            Optimal_CHS = np.copy(C[Fit.index(min(Fit))])
            Best_fit.append(Optimal_fit)
            d = Decode(J, Processing_time, M_num, Arrival_Time, Breakdowns, Due_Dates)
            cmax, tardiness = d.decode(Optimal_CHS, O_num)
            print(f'Thế hệ {i}! Best fitness: {best_fitness:.2f} | Cmax: {cmax} | Tardiness: {tardiness}')
            Gantt_Hybrid(d.Machines,
                         title=f"Hybrid Result | Fitness: {best_fitness:.2f} (Cmax: {cmax}, T: {tardiness})")
        else:
            Best_fit.append(Optimal_fit)

        for j in range(len(C)):
            Cafter = [np.copy(C[j])]
            if random.random() < g.Pc:
                N_i = random.choice(np.arange(len(C)))
                Cross = g.machine_cross(np.copy(C[j]), np.copy(C[N_i]), O_num) if random.random() < g.Pv \
                    else g.operation_cross(np.copy(C[j]), np.copy(C[N_i]), O_num, J_num)
                Cafter.extend([Cross[0], Cross[1]])

            if random.random() < g.Pm:
                Variance = g.machine_variation(np.copy(C[j]), Processing_time, O_num, J) if random.random() < g.Pw \
                    else g.operation_variation(np.copy(C[j]), O_num, J_num, J, Processing_time, M_num, Arrival_Time,
                                               Breakdowns, Due_Dates)
                Cafter.append(Variance)

            if Cafter:
                Fit_after = g.fitness(Cafter, J, Processing_time, M_num, O_num, Arrival_Time, Breakdowns, Due_Dates)
                C[j] = np.copy(Cafter[Fit_after.index(min(Fit_after))])

    plt.figure(figsize=(10, 5))
    plt.plot(np.linspace(0, g.Max_Itertions, g.Max_Itertions), Best_fit, '-b', linewidth=2,
             label='Hybrid GA Best Fitness')
    plt.axhline(y=fitness_atc, color='r', linestyle='--', label=f'ATC Baseline ({fitness_atc:.2f})')
    plt.title('Giá trị hàm thích nghi qua các thế hệ dùng GA + ATC')
    plt.ylabel('Giá trị hàm thích nghi (Fitness)')
    plt.xlabel('Thế hệ (Iteration)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.savefig(os.path.join(os.path.dirname(__file__), '', 'Result_Hybrid.png'), dpi=300)
    plt.show()