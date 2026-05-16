class Job:
    def __init__(self, Job_index, Operation_num, Arrival_time=0):
        """
        :param Job_index: Số thứ tự công việc
        :param Operation_num: Số lượng công đoạn
        :param Arrival_time: Thời gian công việc đến xưởng (MỚI)
        """
        self.Job_index = Job_index
        self.Operation_num = Operation_num
        self.Arrival_time = Arrival_time
        self.Processed = []  # Ghi lại tiến độ gia công các công đoạn của công việc
        self.J_start = []  # Ghi lại thời gian bắt đầu các công đoạn của công việc
        self.J_end = []  # Ghi lại thời gian kết thúc các công đoạn của công việc
        self.J_machine = []  # Ghi lại máy móc được chọn cho các công đoạn của công việc
        self.Last_Processing_Machine = None  # Máy gia công công đoạn hiện tại của công việc

        # Note: Công việc không thể bắt đầu trước thời điểm nó xuất hiện
        self.Last_Processing_end_time = Arrival_time

        # [DFJSS] Các trạng thái phục vụ việc cắt lớp lịch trình động
        self.Status = "PENDING"  # PENDING (Chưa đến), WAITING (Đã đến, chờ xếp), IN_PROGRESS (Đang làm), COMPLETED (Xong)

    # Số lượng công đoạn đã được gia công của công việc
    def Current_Processed(self):
        return len(self.Processed)

    # [DFJSS] Kiểm tra xem toàn bộ các công đoạn đã hoàn thành chưa
    def Is_Completed(self):
        return len(self.Processed) == self.Operation_num

    # Bắt đầu gia công một công đoạn nào đó của công việc
    def _Input(self, W_Eailiest, End_time, Machine):
        """
        :param W_Eailiest: Thời gian bắt đầu công đoạn hiện tại của công việc
        :param End_time: Thời gian kết thúc công đoạn hiện tại của công việc
        :param Machine: Máy gia công được chọn cho công đoạn hiện tại của công việc
        :return:
        """
        self.Last_Processing_Machine = Machine
        self.Last_Processing_end_time = End_time
        self.Processed.append(1)
        self.J_start.append(W_Eailiest)
        self.J_end.append(End_time)
        self.J_machine.append(Machine)

        if self.Is_Completed():
            self.Status = "COMPLETED"
        else:
            self.Status = "IN_PROGRESS"