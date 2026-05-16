import matplotlib.pyplot as plt
import numpy as np
import math

# Nhập dữ liệu từ file Instance
from DataSet.Instance import *


class ATCSimulator:
    def __init__(self, J, Processing_time, M_num, Arrival_Time, Due_Dates, Breakdowns=None, k_parameter=2.0):
        """
        :param k_parameter: Tham số k của luật ATC (thường từ 1.5 - 4.5)
        """
        self.J = J
        self.Processing_time = Processing_time
        self.M_num = M_num
        self.Arrival_Time = Arrival_Time
        self.Due_Dates = Due_Dates
        self.Breakdowns = Breakdowns if Breakdowns else []
        self.k = k_parameter

        # Khởi tạo trạng thái Công việc
        self.jobs = []
        for k_id, v in self.J.items():
            self.jobs.append({
                'id': k_id,
                'total_ops': v,
                'current_op': 0,
                'ready_time': self.Arrival_Time[k_id - 1],
                'due_date': self.Due_Dates[k_id - 1],
                'is_done': False,
                'finish_time': 0
            })

        # Khởi tạo trạng thái Máy
        self.machines = []
        for i in range(self.M_num):
            m_breakdowns = [b for b in self.Breakdowns if b['machine'] == i]
            self.machines.append({
                'id': i,
                'free_time': 0,
                'history': [],
                'breakdowns': m_breakdowns
            })
            # Ghi nhận máy hỏng vào history
            for b in m_breakdowns:
                self.machines[i]['history'].append((b['start'], b['start'] + b['duration'], 'Break'))

    def run(self):
        t = 0
        while not all(j['is_done'] for j in self.jobs):
            # 1. Tìm các máy rảnh và không hỏng tại t
            idle_machines = []
            for m in self.machines:
                is_broken = any(b['start'] <= t < b['start'] + b['duration'] for b in m['breakdowns'])
                if t >= m['free_time'] and not is_broken:
                    idle_machines.append(m)

            # 2. Tìm các Job đã sẵn sàng
            ready_jobs = [j for j in self.jobs if not j['is_done'] and j['ready_time'] <= t]

            # 3. Phân bổ theo luật ATC
            if idle_machines and ready_jobs:
                # Tính p_bar (thời gian gia công trung bình của các công việc đang chờ)
                all_possible_pt = []
                for j in ready_jobs:
                    op_idx = j['current_op']
                    p_row = self.Processing_time[j['id'] - 1][op_idx]
                    valid_pt = [p for p in p_row if p != 9999]
                    if valid_pt:
                        all_possible_pt.append(np.mean(valid_pt))

                p_bar = np.mean(all_possible_pt) if all_possible_pt else 1.0

                assignments = []
                for m in idle_machines:
                    for j in ready_jobs:
                        op_idx = j['current_op']
                        p_t = self.Processing_time[j['id'] - 1][op_idx][m['id']]

                        if p_t != 9999:
                            # Kiểm tra va chạm máy hỏng
                            finish_t = t + p_t
                            overlap = any(
                                b['start'] < finish_t and (b['start'] + b['duration']) > t for b in m['breakdowns'])

                            if not overlap:
                                # TÍNH TOÁN CHỈ SỐ ATC
                                slack = j['due_date'] - t - p_t
                                exp_term = math.exp(-max(0, slack) / (self.k * p_bar))
                                atc_index = (1.0 / p_t) * exp_term

                                assignments.append({
                                    'job': j, 'machine': m, 'p_t': p_t, 'index': atc_index
                                })

                if assignments:
                    # Chọn cặp có chỉ số ATC cao nhất
                    assignments.sort(key=lambda x: x['index'], reverse=True)
                    best = assignments[0]

                    # Cập nhật
                    best['machine']['history'].append((t, t + best['p_t'], best['job']['id']))
                    best['machine']['free_time'] = t + best['p_t']
                    best['job']['current_op'] += 1
                    if best['job']['current_op'] >= best['job']['total_ops']:
                        best['job']['is_done'] = True
                        best['job']['finish_time'] = t + best['p_t']
                    else:
                        best['job']['ready_time'] = t + best['p_t']

                    continue  # Kiểm tra lại máy rảnh ngay lập tức

            # 4. Tiến thời gian
            next_events = [j['ready_time'] for j in self.jobs if not j['is_done'] and j['ready_time'] > t]
            next_events += [m['free_time'] for m in self.machines if m['free_time'] > t]
            for m in self.machines:
                for b in m['breakdowns']:
                    if b['start'] > t: next_events.append(b['start'])
                    if b['start'] + b['duration'] > t: next_events.append(b['start'] + b['duration'])

            t = min(next_events) if next_events else t + 1

        # Tính toán kết quả
        cmax = max(j['finish_time'] for j in self.jobs)
        tardiness = sum(max(0, j['finish_time'] - j['due_date']) for j in self.jobs)
        return cmax, tardiness


def Draw_Gantt(machines, cmax, tardiness):
    colors = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
              'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
              'navajowhite', 'navy', 'sandybrown', 'moccasin']
    plt.figure(figsize=(12, 6))
    for m in machines:
        for start, end, task in m['history']:
            if task == 'Break':
                plt.barh(m['id'], width=end - start, left=start, color='black', hatch='//')
            else:
                plt.barh(m['id'], width=end - start, left=start, color=colors[(task - 1) % len(colors)],
                         edgecolor='black')
                plt.text(start + (end - start) / 2, m['id'], str(task), color='black', fontweight='bold', ha='center',
                         va='center', fontsize=8)

    plt.yticks(range(len(machines)), range(1, len(machines) + 1))
    plt.title(f'ATC Rule Gantt | Cmax: {cmax} | Total Tardiness: {tardiness}')
    plt.xlabel('Time (min)');
    plt.ylabel('Machine')
    plt.tight_layout();
    plt.show()


if __name__ == '__main__':
    sim = ATCSimulator(J, Processing_time, M_num, Arrival_Time, Due_Dates, Breakdowns, k_parameter=2.0)
    cmax_res, tardy_res = sim.run()
    # Tính toán hàm mục tiêu đa mục tiêu
    alpha = 0.7
    beta = 0.3
    fitness_value = (alpha * cmax_res) + (beta * tardy_res)
    print(f"KẾT QUẢ GIẢI THUẬT ATC (k=2.0)")
    print(f"-> Makespan (Cmax): {cmax_res}")
    print(f"-> Tổng thời gian trễ (Tardiness): {tardy_res}")
    print(f"-> Giá trị hàm mục tiêu (Fitness): {fitness_value:.2f}")
    Draw_Gantt(sim.machines, cmax_res, tardy_res)