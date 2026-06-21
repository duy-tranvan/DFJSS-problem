import random
import os
import matplotlib.pyplot as plt
import numpy as np

from GeneticAlgorithm.Initialization.Decode import Decode
from GeneticAlgorithm.Initialization.Encode import Encode
from GeneticAlgorithm.Initialization.GA import GA
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
    plt.title('Dynamic Scheduling Gantt Chart (Event-Driven Rescheduling)')
    plt.ylabel('Machines')
    plt.xlabel('Time(min)')
    plt.tight_layout()
    plt.show()


# [DFJSS] Hàm mới: Trích xuất và sắp xếp các sự kiện theo thời gian thực tế
def extract_events(Arrival_Time, Breakdowns):
    events = []
    for idx, time in enumerate(Arrival_Time):
        events.append({'time': time, 'type': 'new_job', 'job_idx': idx})
    for bd in Breakdowns:
        events.append({'time': bd['start'], 'type': 'breakdown', 'machine': bd['machine'], 'duration': bd['duration']})

    # Sắp xếp hàng đợi sự kiện theo thời gian tăng dần
    events.sort(key=lambda x: x['time'])
    return events


if __name__ == '__main__':
    # Tự động tạo thư mục nếu chưa có
    os.makedirs(os.path.join(os.path.dirname(__file__), 'GA_Solution'), exist_ok=True)

    # [DFJSS] Lấy danh sách sự kiện từ Instance
    event_queue = extract_events(Arrival_Time, Breakdowns)

    current_time = 0
    active_jobs = []  # Các công việc đã sẵn sàng gia công tại thời điểm t

    g = GA()
    # [DFJSS] Giảm số lần lặp tối đa tại mỗi sự kiện để đáp ứng tốc độ thời gian thực của thuật toán động
    g.Max_Itertions = 50

    Optimal_fit = 9999  # Độ thích nghi tốt nhất (khởi tạo)
    Optimal_CHS = 0  # Cá thể gene tương ứng với độ thích nghi tốt nhất (khởi tạo)
    Final_Decode_Machine = None  # Lưu trạng thái máy móc cuối cùng

    print("=== BẮT ĐẦU CHẠY HỆ THỐNG LẬP LỊCH ĐỘNG (DFJSS) ===")

    # [DFJSS] Vòng lặp Mô phỏng Thời gian thực
    while event_queue:
        current_event = event_queue.pop(0)
        current_time = current_event['time']

        print(f"\n[{current_time} min] SỰ KIỆN MỚI: {current_event['type'].upper()}")

        if current_event['type'] == 'new_job':
            active_jobs.append(current_event['job_idx'])
            print(f" -> Job {current_event['job_idx'] + 1} đã đến xưởng.")
        elif current_event['type'] == 'breakdown':
            print(
                f" -> Máy {current_event['machine']} báo lỗi! Dự kiến sửa chữa trong {current_event['duration']} phút.")

        # [DFJSS] Nếu có nhiều sự kiện xảy ra cùng một thời điểm, gom lại xử lý một thể để tối ưu
        if event_queue and event_queue[0]['time'] == current_time:
            continue

        print(f"--- KÍCH HOẠT THUẬT TOÁN GA ĐỂ RESCHEDULING TẠI T = {current_time} ---")

        best_fitness = 9999
        Optimal_fit = 9999

        # Khởi tạo quần thể mới cho mỗi lần Rescheduling
        e = Encode(Processing_time, g.Pop_size, J, J_num, M_num)
        CHS1 = e.Global_initial()
        CHS2 = e.Random_initial()
        CHS3 = e.Local_initial()
        C = np.vstack((CHS1, CHS2, CHS3))

        for i in range(g.Max_Itertions):
            # Tính toán fitness cho quần thể hiện tại
            Fit = g.fitness(C, J, Processing_time, M_num, O_num, Arrival_Time, Breakdowns, Due_Dates)
            Best = C[Fit.index(min(Fit))]
            best_fitness = min(Fit)

            if best_fitness < Optimal_fit:
                Optimal_fit = best_fitness
                Optimal_CHS = Best

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
                                                         Arrival_Time, Breakdowns, Due_Dates)
                    Cafter.append(Variance)

                # Chọn lọc cá thể tốt nhất sau biến dị đưa vào quần thể mới
                if Cafter != []:
                    Fit_after = g.fitness(Cafter, J, Processing_time, M_num, O_num, Arrival_Time, Breakdowns, Due_Dates)
                    C[j] = np.copy(Cafter[Fit_after.index(min(Fit_after))])

        print(f" -> Cập nhật lịch trình thành công. Fitness dự kiến hiện tại: {best_fitness:.2f}")

    # [DFJSS] Giải mã phương án tối ưu cuối cùng sau khi xử lý hết mọi biến động
    print("\n=== HOÀN THÀNH MÔ PHỎNG, XUẤT LỊCH TRÌNH CUỐI CÙNG ===")
    d = Decode(J, Processing_time, M_num, Arrival_Time, Breakdowns, Due_Dates)
    cmax, tardiness = d.decode(Optimal_CHS, O_num)

    print(f"Kết quả tổng quát: Makespan (Cmax) = {cmax} | Tổng Trễ hạn = {tardiness}")
    Gantt(d.Machines)