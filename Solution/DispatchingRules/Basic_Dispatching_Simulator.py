import matplotlib.pyplot as plt
import numpy as np

# Nhập dữ liệu từ file Instance
from DataSet.Instance import *


class BasicDispatchingSimulator:
    def __init__(self, J, Processing_time, M_num, Arrival_Time, Due_Dates, Breakdowns=None, rule='SPT'):
        """
        :param rule: Các luật hỗ trợ: 'FIFO', 'SPT', 'EDD', 'MOR', 'MWKR'
        """
        self.J = J
        self.Processing_time = Processing_time
        self.M_num = M_num
        self.Arrival_Time = Arrival_Time
        self.Due_Dates = Due_Dates
        self.Breakdowns = Breakdowns if Breakdowns else []
        self.rule = rule

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
            for b in m_breakdowns:
                self.machines[i]['history'].append((b['start'], b['start'] + b['duration'], 'Break'))

    def run(self):
        t = 0
        while not all(j['is_done'] for j in self.jobs):
            # 1. Tìm máy rảnh
            idle_machines = []
            for m in self.machines:
                is_broken = any(b['start'] <= t < b['start'] + b['duration'] for b in m['breakdowns'])
                if t >= m['free_time'] and not is_broken:
                    idle_machines.append(m)

            # 2. Tìm Job sẵn sàng
            ready_jobs = [j for j in self.jobs if not j['is_done'] and j['ready_time'] <= t]

            # 3. Phân bổ công việc dựa trên Luật
            assigned_this_round = True
            while assigned_this_round and idle_machines and ready_jobs:
                assigned_this_round = False
                assignments = []

                # Lấy tất cả các cặp (Máy, Công việc) hợp lệ
                for m in idle_machines:
                    for j in ready_jobs:
                        op_idx = j['current_op']
                        p_t = self.Processing_time[j['id'] - 1][op_idx][m['id']]

                        if p_t != 9999:
                            finish_t = t + p_t
                            overlap = any(
                                b['start'] < finish_t and (b['start'] + b['duration']) > t for b in m['breakdowns'])

                            if not overlap:
                                # Tính MOR (Số công đoạn còn lại)
                                rem_ops = j['total_ops'] - j['current_op']

                                # Tính MWKR (Ước lượng tổng thời gian các công đoạn còn lại bằng giá trị trung bình)
                                rem_work = 0
                                for op in range(j['current_op'], j['total_ops']):
                                    valid_times = [p for p in self.Processing_time[j['id'] - 1][op] if p != 9999]
                                    if valid_times:
                                        rem_work += sum(valid_times) / len(valid_times)

                                assignments.append({
                                    'job': j, 'machine': m, 'p_t': p_t,
                                    'rem_ops': rem_ops,
                                    'rem_work': rem_work
                                })

                if assignments:
                    # Logic sắp xếp dựa trên các Dispatching Rules
                    if self.rule == 'FIFO':
                        assignments.sort(key=lambda x: (x['job']['ready_time'], x['p_t']))
                    elif self.rule == 'SPT':
                        assignments.sort(key=lambda x: x['p_t'])
                    elif self.rule == 'EDD':
                        assignments.sort(key=lambda x: (x['job']['due_date'], x['p_t']))
                    elif self.rule == 'MOR':
                        # Dấu âm (-) trước x['rem_ops'] để ưu tiên giá trị MAX, tiêu chí phụ là SPT
                        assignments.sort(key=lambda x: (-x['rem_ops'], x['p_t']))
                    elif self.rule == 'MWKR':
                        # Dấu âm (-) trước x['rem_work'] để ưu tiên giá trị MAX, tiêu chí phụ là SPT
                        assignments.sort(key=lambda x: (-x['rem_work'], x['p_t']))

                    best = assignments[0]

                    # Cập nhật trạng thái
                    best['machine']['history'].append((t, t + best['p_t'], best['job']['id']))
                    best['machine']['free_time'] = t + best['p_t']
                    best['job']['current_op'] += 1

                    if best['job']['current_op'] >= best['job']['total_ops']:
                        best['job']['is_done'] = True
                        best['job']['finish_time'] = t + best['p_t']
                    else:
                        best['job']['ready_time'] = t + best['p_t']

                    idle_machines.remove(best['machine'])
                    ready_jobs.remove(best['job'])
                    assigned_this_round = True

                    # 4. Bước thời gian
            next_events = [j['ready_time'] for j in self.jobs if not j['is_done'] and j['ready_time'] > t]
            next_events += [m['free_time'] for m in self.machines if m['free_time'] > t]
            for m in self.machines:
                for b in m['breakdowns']:
                    if b['start'] > t: next_events.append(b['start'])
                    if b['start'] + b['duration'] > t: next_events.append(b['start'] + b['duration'])

            t = min(next_events) if next_events else t + 1

        cmax = max(j['finish_time'] for j in self.jobs)
        tardiness = sum(max(0, j['finish_time'] - j['due_date']) for j in self.jobs)
        return cmax, tardiness


if __name__ == '__main__':
    alpha = 0.7
    beta = 0.3

    rules = ['FIFO', 'SPT', 'EDD', 'MOR', 'MWKR']

    print(f"{'Dispatching Rules':<15} | {'FITNESS':<10} | {'CMAX':<8} | {'TARDINESS'}")
    print("-" * 50)

    for rule in rules:
        sim = BasicDispatchingSimulator(J, Processing_time, M_num, Arrival_Time, Due_Dates, Breakdowns, rule=rule)
        cmax_res, tardy_res = sim.run()
        fitness_value = (alpha * cmax_res) + (beta * tardy_res)

        print(f"{rule:<15} | {fitness_value:<10.2f} | {cmax_res:<8} | {tardy_res}")

    print("-" * 50)