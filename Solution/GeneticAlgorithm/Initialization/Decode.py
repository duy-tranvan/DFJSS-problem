import numpy as np
from Solution.GeneticAlgorithm.Initialization.Job import Job
from Solution.GeneticAlgorithm.Initialization.Machine import Machine_Time_window


class Decode:
    def __init__(self, J, Processing_time, M_num, Arrival_Time, Breakdowns=None, Due_Dates=None):
        """
        :param J: Từ điển lưu số lượng công đoạn của từng công việc
        :param Processing_time: Ma trận thời gian gia công của từng công việc
        :param M_num: Số lượng máy gia công
        :param Arrival_Time: Mảng lưu thời gian xuất hiện của công việc
        :param Breakdowns: Danh sách các sự kiện máy hỏng
        :param Due_Dates: Mảng lưu thời hạn hoàn thành của công việc
        """
        self.Processing_time = Processing_time
        self.M_num = M_num
        self.J = J
        self.Due_Dates = Due_Dates
        self.Machines = []  # Lưu trữ các đối tượng máy
        self.Scheduled = []  # Các công đoạn đã được lên lịch
        self.fitness = 0  # Độ thích nghi (fitness) tạm tính bằng Makespan
        self.Machine_State = np.zeros(M_num, dtype=int)  # Công việc nào đang được gia công trên máy
        self.Jobs = []  # Lưu trữ các đối tượng công việc

        for j in range(M_num):
            self.Machines.append(Machine_Time_window(j))

        # Đóng băng các khoảng thời gian máy hỏng trước khi bắt đầu giải mã
        if Breakdowns is not None:
            for bd in Breakdowns:
                m_idx = bd['machine']
                s_time = bd['start']
                dur = bd['duration']
                self.Machines[m_idx].O_start.append(s_time)
                self.Machines[m_idx].O_end.append(s_time + dur)
                self.Machines[m_idx].assigned_task.append(['Break', 0])
                self.Machines[m_idx].End_time = max(self.Machines[m_idx].End_time, s_time + dur)

        for k, v in J.items():
            self.Jobs.append(Job(k, v, Arrival_Time[k - 1]))

    def Order_Matrix(self, MS):
        JM = [];
        T = [];
        Ms_decompose = [];
        Site = 0
        for S_i in self.J.values():
            Ms_decompose.append(MS[Site:Site + S_i])
            Site += S_i
        for i in range(len(Ms_decompose)):
            JM_i = [];
            T_i = []
            for j in range(len(Ms_decompose[i])):
                O_j = self.Processing_time[i][j]
                M_ij = [];
                T_ij = []
                for Mac_num in range(len(O_j)):
                    if O_j[Mac_num] != 9999:
                        M_ij.append(Mac_num);
                        T_ij.append(O_j[Mac_num])
                JM_i.append(M_ij[Ms_decompose[i][j]])
                T_i.append(T_ij[Ms_decompose[i][j]])
            JM.append(JM_i);
            T.append(T_i)
        return JM, T

    def Earliest_Start(self, Job, O_num, Machine):
        P_t = self.Processing_time[Job][O_num][Machine]
        last_O_end = self.Jobs[Job].Last_Processing_end_time
        Selected_Machine = Machine
        M_window = self.Machines[Selected_Machine].Empty_time_window()
        M_Tstart = M_window[0];
        M_Tend = M_window[1];
        M_Tlen = M_window[2]
        Machine_end_time = self.Machines[Selected_Machine].End_time
        ealiest_start = max(last_O_end, Machine_end_time)
        if M_Tlen is not None:
            for le_i in range(len(M_Tlen)):
                if M_Tlen[le_i] >= P_t:
                    if M_Tstart[le_i] >= last_O_end:
                        ealiest_start = M_Tstart[le_i];
                        break
                    if M_Tstart[le_i] < last_O_end and M_Tend[le_i] - last_O_end >= P_t:
                        ealiest_start = last_O_end;
                        break
        return ealiest_start, Selected_Machine, P_t, O_num, last_O_end, ealiest_start + P_t

    def decode(self, CHS, Len_Chromo):
        """
        :param CHS: Gene của quần thể
        :param Len_Chromo: Điểm phân chia giữa MS và OS
        :return: Makespan và Tổng thời gian trễ hạn
        """
        MS = list(CHS[0:Len_Chromo]);
        OS = list(CHS[Len_Chromo:2 * Len_Chromo])
        Needed_Matrix = self.Order_Matrix(MS);
        JM = Needed_Matrix[0]
        for i in OS:
            Job_idx = i
            O_num = self.Jobs[Job_idx].Current_Processed()
            Machine = JM[Job_idx][O_num]
            Para = self.Earliest_Start(Job_idx, O_num, Machine)
            self.Jobs[Job_idx]._Input(Para[0], Para[5], Para[1])
            if Para[5] > self.fitness: self.fitness = Para[5]
            self.Machines[Machine]._Input(Job_idx, Para[0], Para[2], Para[3])

        # Tính tổng thời gian trễ hạn
        total_tardiness = 0
        if self.Due_Dates is not None:
            for i in range(len(self.Jobs)):
                tardiness = max(0, self.Jobs[i].Last_Processing_end_time - self.Due_Dates[i])
                total_tardiness += tardiness
        return self.fitness, total_tardiness