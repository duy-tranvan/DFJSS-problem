class Machine_Time_window:
    def __init__(self, Machine_index):
        """
        :param Machine_index: Số thứ tự máy gia công
        """
        self.Machine_index = Machine_index
        self.assigned_task = []  # Ghi lại các nhiệm vụ được phân công cho máy, bao gồm số thứ tự công việc và số thứ tự công đoạn
        self.O_start = []  # Ghi lại thời gian bắt đầu của các công đoạn nhiệm vụ
        self.O_end = []  # Ghi lại thời gian kết thúc của các công đoạn nhiệm vụ
        self.End_time = 0

        # [DFJSS] Thêm biến trạng thái để phục vụ lập lịch động
        self.Status = "FREE"  # Trạng thái máy: FREE (Rảnh), BUSY (Đang chạy), BROKEN (Đang hỏng)
        self.Current_running_job = None  # Công việc nào đang chiếm dụng máy lúc này

    # Những khung thời gian nào của máy đang trống, ở đây chỉ xem xét các khung thời gian đóng bên trong, tương tự như việc xếp chồng liên tiếp từng hàng của biểu đồ Gantt
    def Empty_time_window(self):
        """
        :return: Thời gian bắt đầu, kết thúc và độ dài của khoảng thời gian trống
        """
        time_window_start = []
        time_window_end = []
        len_time_window = []
        if self.O_end is None:
            pass
        elif len(self.O_end) == 1:
            if self.O_start[0] != 0:
                time_window_start = [0]
                time_window_end = [self.O_start[0]]
        elif len(self.O_end) > 1:
            if self.O_start[0] != 0:
                time_window_start.append(0)
                time_window_end.append(self.O_start[0])
            time_window_start.extend(self.O_end[
                                         :-1])  # Bởi vì điểm kết thúc của khung thời gian đang sử dụng chính là điểm bắt đầu của khung thời gian trống
            time_window_end.extend(self.O_start[1:])
        if time_window_end is not None:
            len_time_window = [time_window_end[i] - time_window_start[i] for i in range(len(time_window_end))]
        return time_window_start, time_window_end, len_time_window

    # Máy được đưa vào chu kỳ gia công mới
    def _Input(self, Job, M_Ealiest, P_t, O_num):
        if self.O_end != []:
            # Nếu thời gian bắt đầu sớm nhất của máy hiện tại lớn hơn thời gian được ghi lại, thì lần lượt xếp các nhiệm vụ về phía sau, nếu không thì chèn nhiệm vụ vào giữa bản ghi các nhiệm vụ đã phân công
            if self.O_start[-1] > M_Ealiest:
                for i in range(len(self.O_end)):
                    if self.O_start[i] >= M_Ealiest:
                        self.assigned_task.insert(i, [Job + 1, O_num + 1])
                        break
            else:
                self.assigned_task.append([Job + 1, O_num + 1])
        else:
            self.assigned_task.append([Job + 1, O_num + 1])
        self.O_start.append(M_Ealiest)
        self.O_start.sort()
        self.O_end.append(M_Ealiest + P_t)
        self.O_end.sort()
        self.End_time = self.O_end[-1]