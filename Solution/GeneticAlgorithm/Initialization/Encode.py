import random

import numpy as np


class Encode:
    def __init__(self, Matrix, Pop_size, J, J_num, M_num):
        """
        :param Matrix: Ma trận thời gian gia công của máy
        :param Pop_size: Số lượng cá thể trong quần thể
        :param J: Số lượng công đoạn tương ứng của mỗi công việc
        :param J_num: Số lượng công việc
        :param M_num: Số lượng máy
        """
        self.Matrix = Matrix
        self.J = J
        self.J_num = J_num
        self.M_num = M_num
        self.CHS = []
        self.GS_num = int(0.6 * Pop_size)  # Khởi tạo lựa chọn toàn cục
        self.LS_num = int(0.2 * Pop_size)  # Khởi tạo lựa chọn cục bộ
        self.RS_num = int(0.2 * Pop_size)  # Khởi tạo lựa chọn ngẫu nhiên
        self.Len_Chromo = 0
        for i in J.values():
            self.Len_Chromo += i

    # Tạo phần chuẩn bị công đoạn
    def OS_List(self):
        OS_list = []
        for k, v in self.J.items():
            OS_add = [k - 1 for j in range(v)]
            OS_list.extend(OS_add)
        return OS_list

    # Tạo ma trận khởi tạo
    def CHS_Matrix(self, C_num):
        return np.zeros([C_num, self.Len_Chromo], dtype=int)

    # Xác định vị trí của từng công đoạn của mỗi công việc
    def Site(self, Job, Operation):
        O_num = 0
        for i in range(len(self.J)):
            if i == Job:
                return O_num + Operation
            else:
                O_num = O_num + self.J[i + 1]
        return O_num

    # Khởi tạo toàn cục
    def Global_initial(self):
        MS = self.CHS_Matrix(self.GS_num)  # Tạo quần thể dựa trên GS_num
        OS_list = self.OS_List()
        OS = self.CHS_Matrix(self.GS_num)
        for i in range(self.GS_num):
            Machine_time = np.zeros(self.M_num, dtype=int)  # Bước 1: Tạo một mảng số nguyên, độ dài bằng số lượng máy và khởi tạo mỗi phần tử là 0
            random.shuffle(OS_list)  # Tạo phần sắp xếp công đoạn
            OS[i] = np.array(OS_list)  # Xáo trộn ngẫu nhiên rồi gán cho một hàng nào đó của OS (vì có một quần thể, thứ i tức là gán vào hàng thứ i của OS, từ đó tạo ra OS hoàn chỉnh)
            GJ_list = [i_1 for i_1 in range(self.J_num)]  # Tạo tập hợp công việc
            random.shuffle(GJ_list)  # Xáo trộn ngẫu nhiên tập hợp công việc, mục đích là để bước tiếp theo có thể rút ra ngẫu nhiên công việc đầu tiên
            for g in GJ_list:  # Chọn công việc đầu tiên (vì bước trước đã xáo trộn tập hợp công việc nên rút ra cái đầu tiên cũng là "ngẫu nhiên")
                h = self.Matrix[g]  # h là ma trận thời gian tương ứng với các công đoạn bao gồm trong công việc đầu tiên
                for j in range(len(h)):  # Bắt đầu từ công đoạn đầu tiên của công việc này
                    D = h[j]  # D là ma trận thời gian tương ứng với công đoạn đầu tiên của công việc đầu tiên
                    List_Machine_weizhi = []
                    for k in range(len(D)):  # Xác định máy có thể sử dụng cho công đoạn nằm ở vị trí thứ mấy
                        Useing_Machine = D[k]
                        if Useing_Machine != 9999:
                            List_Machine_weizhi.append(k)
                    Machine_Select = []
                    for Machine_add in List_Machine_weizhi:  # Cộng vị trí tương ứng của mảng thời gian máy với thời gian của máy có thể chọn cho công đoạn
                        Machine_Select.append(Machine_time[Machine_add] + D[Machine_add])
                    Min_time = min(Machine_Select)  # Chọn ra máy có thời gian nhỏ nhất
                    K = Machine_Select.index(Min_time)  # Vị trí xuất hiện thời gian nhỏ nhất lần đầu tiên, xác định tải trọng nhỏ nhất thuộc về máy nào, tức là máy thứ K trong số các máy có thể chọn cho công đoạn đó, không phải là Mk
                    I = List_Machine_weizhi[K]  # Máy thứ I trong tất cả các máy, tức là Mi
                    Machine_time[I] += Min_time  # Vị trí máy tương ứng cộng thêm thời gian nhỏ nhất
                    site = self.Site(g, j)  # Xác định vị trí của từng công đoạn của mỗi công việc
                    MS[i][site] = K  # Gán máy thứ K mà mỗi công đoạn đã chọn vào vị trí của từng công đoạn của mỗi công việc, tức là tạo ra nhiễm sắc thể MS
        CHS1 = np.hstack((MS, OS))  # Tích hợp MS và OS thành một ma trận
        return CHS1

    # Khởi tạo cục bộ
    def Local_initial(self):
        MS = self.CHS_Matrix(self.LS_num)  # Tạo kích thước quần thể lựa chọn cục bộ dựa trên LS_num
        OS_list = self.OS_List()
        OS = self.CHS_Matrix(self.LS_num)
        for i in range(self.LS_num):
            random.shuffle(OS_list)  # Tạo phần sắp xếp công đoạn
            OS[i] = np.array(OS_list)  # Xáo trộn ngẫu nhiên rồi gán cho một hàng nào đó của OS (vì có một quần thể, thứ i tức là gán vào hàng thứ i của OS, từ đó tạo ra OS hoàn chỉnh)
            GJ_List = [i_1 for i_1 in range(self.J_num)]  # Tạo tập hợp công việc
            for g in GJ_List:  # Chọn công việc đầu tiên (Lưu ý: Không cần xáo trộn ngẫu nhiên nữa)
                Machine_time = np.zeros(self.M_num,
                                        dtype=int)  # Thiết lập một mảng số nguyên và khởi tạo mỗi phần tử là 0, do khởi tạo cục bộ, sau khi tất cả các công đoạn của mỗi công việc kết thúc đều phải khởi tạo lại, nên khác với khởi tạo toàn cục, bước này nên đặt ở đây
                h = self.Matrix[g]  # h là ma trận thời gian tương ứng với các công đoạn bao gồm trong công việc đầu tiên
                for j in range(len(h)):  # Bắt đầu từ công đoạn đầu tiên của công việc được chọn
                    D = h[j]  # Ma trận thời gian gia công của máy tương ứng với công đoạn đầu tiên của công việc này
                    List_Machine_weizhi = []
                    for k in range(len(D)):  # Xác định máy có thể sử dụng cho công đoạn nằm ở vị trí thứ mấy
                        Useing_Machine = D[k]
                        if Useing_Machine != 9999:
                            List_Machine_weizhi.append(k)
                    Machine_Select = []
                    for Machine_add in List_Machine_weizhi:  # Cộng vị trí tương ứng của mảng thời gian máy với thời gian của máy có thể chọn cho công đoạn
                        Machine_Select.append(Machine_time[Machine_add] + D[Machine_add])
                    Min_time = min(Machine_Select)  # Chọn ra thời gian nhỏ nhất trong số các thời gian này
                    K = Machine_Select.index(Min_time)  # Vị trí xuất hiện thời gian nhỏ nhất lần đầu tiên, xác định tải trọng nhỏ nhất thuộc về máy nào, tức là máy thứ K trong số các máy có thể chọn cho công đoạn đó, không phải là Mk
                    I = List_Machine_weizhi[K]  # Máy thứ I trong tất cả các máy, tức là Mi
                    Machine_time[I] += Min_time
                    site = self.Site(g, j)  # Xác định vị trí của từng công đoạn của mỗi công việc
                    MS[i][site] = K  # Gán máy thứ K mà mỗi công đoạn đã chọn vào vị trí của từng công đoạn của mỗi công việc
        CHS1 = np.hstack((MS, OS))  # Tích hợp MS và OS thành một ma trận
        return CHS1

    # Khởi tạo ngẫu nhiên
    def Random_initial(self):
        MS = self.CHS_Matrix(self.RS_num)  # Tạo kích thước quần thể lựa chọn ngẫu nhiên dựa trên RS_num
        OS_list = self.OS_List()
        OS = self.CHS_Matrix(self.RS_num)
        for i in range(self.RS_num):
            random.shuffle(OS_list)
            OS[i] = np.array(OS_list)
            GJ_List = [i_1 for i_1 in range(self.J_num)]  # Tạo tập hợp công việc
            for g in GJ_List:  # Chọn công việc đầu tiên
                h = self.Matrix[g]
                for j in range(len(h)):  # Chọn công đoạn đầu tiên của công việc đầu tiên
                    D = h[j]  # Ma trận thời gian tương ứng với máy có thể gia công cho công đoạn đầu tiên của công việc này
                    List_Machine_weizhi = []
                    for k in range(len(D)):
                        Useing_Machine = D[k]
                        if Useing_Machine != 9999:
                            List_Machine_weizhi.append(k)
                    number = random.choice(List_Machine_weizhi)  # Chọn ngẫu nhiên một máy từ các mã số máy có thể chọn (mã số này chính là mã số máy)
                    K = List_Machine_weizhi.index(number)  # Tức là máy thứ K trong số các máy có thể chọn cho công đoạn đó, không phải là Mk
                    site = self.Site(g, j)  # Xác định vị trí của từng công đoạn của mỗi công việc
                    MS[i][site] = K  # Gán máy thứ K mà mỗi công đoạn đã chọn vào vị trí của từng công đoạn của mỗi công việc
        CHS1 = np.hstack((MS, OS))
        return CHS1