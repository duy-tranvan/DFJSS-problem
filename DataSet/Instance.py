"""
Processing_time: Ma trận thời gian gia công của từng công đoạn trên các máy tương ứng
J: Từ điển lưu số lượng công đoạn của từng công việc
M_num: Số lượng máy gia công (Mở rộng lên 20)
O_num: Tổng số công đoạn gia công
J_num: Số lượng công việc (Mở rộng lên 15)
Arrival_Time: Thời điểm các công việc đến xưởng (Sự kiện động)
Breakdowns: Sự kiện máy hỏng đột xuất
Due_Dates: Ngày hạn định hoàn thành cho từng Job
"""

import random

# LOẠI 1: Quy trình gồm 5 công đoạn (Tương thích 20 máy)
CKS_Type1 = [
    [10, 9, 15, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 12, 9999, 9999, 9999, 18, 9999, 9999, 9999, 9999, 9999],
    [9999, 9999, 14, 16, 12, 9999, 9999, 9999, 9999, 9999, 9999, 11, 9999, 9999, 9999, 9999, 15, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999, 15, 25, 21, 9999, 9999, 9999, 9999, 9999, 14, 17, 9999, 9999, 9999, 9999, 9999, 20],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9, 13, 15, 24, 9999, 9999, 9999, 9999, 10, 9999, 12, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 10, 15, 9999, 9999, 9999, 12, 9999, 18, 14]
]

# LOẠI 2: Quy trình gồm 8 công đoạn (Tương thích 20 máy)
CKS_Type2 = [
    [12, 9, 10, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 11, 9999, 9999, 9999, 13, 9999, 9999, 9999, 9999],
    [9999, 9999, 9999, 16, 14, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 15, 9999, 9999, 9999, 9999, 12, 9999, 9999],
    [9999, 9999, 9999, 9999, 15, 18, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 14, 9999, 9999, 9999, 9999, 19, 9999],
    [9999, 9999, 9999, 9999, 9999, 27, 22, 19, 9999, 9999, 9999, 9999, 9999, 9999, 20, 9999, 9999, 9999, 9999, 15],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 21, 17, 16, 9999, 9999, 9999, 9999, 9999, 18, 9999, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 19, 14, 9999, 9999, 9999, 9999, 9999, 15, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 17, 13, 12, 9999, 9999, 9999, 9999, 11, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 18, 9999, 15, 14, 9999, 9999, 9999, 16, 12]
]

# LOẠI 3: Quy trình phức tạp gồm 10 công đoạn (Tương thích 20 máy)
CKS_Type3 = [
    [8, 12, 9999, 9999, 9999, 15, 9999, 9999, 9999, 9999, 9999, 9999, 10, 9999, 9999, 9999, 14, 9999, 9999, 9999],
    [9999, 9999, 11, 14, 9999, 9999, 9999, 12, 9999, 9999, 9999, 9999, 9999, 15, 9999, 9999, 9999, 18, 9999, 9999],
    [9999, 9999, 9999, 9999, 13, 10, 9999, 9999, 18, 9999, 9999, 9999, 9999, 9999, 12, 9999, 9999, 9999, 16, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 16, 15, 9999, 11, 9999, 9999, 9999, 9999, 9999, 14, 9999, 9999, 9999, 13],
    [9999, 15, 9999, 9999, 9999, 9999, 9999, 9999, 14, 12, 17, 9999, 9999, 9999, 9999, 9999, 10, 9999, 9999, 9999],
    [9999, 9999, 10, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 14, 15, 9999, 9999, 9999, 9999, 9999, 11, 14, 9999],
    [9999, 9999, 9999, 12, 16, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 13, 18, 9999, 9999, 9999, 9999, 9999, 15],
    [9999, 9999, 9999, 9999, 9999, 14, 11, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 15, 12, 9999, 9999, 9999, 9999],
    [12, 9999, 9999, 9999, 9999, 9999, 9999, 10, 15, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 14, 9999, 9999, 18],
    [9999, 10, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 14, 11, 9999, 9999, 9999, 16, 9999, 9999, 13, 15, 9999]
]

# ==========================================
# CÁC KỊCH BẢN THỰC NGHIỆM (SCENARIOS)
# ==========================================
# Thay đổi giá trị SCENARIO (1 -> 9) để chạy các bộ dữ liệu khác nhau
SCENARIO = 8

# =========================================================================
# NHÓM 1: ĐÁNH GIÁ CƠ SỞ VÀ KHẢ NĂNG MỞ RỘNG QUY MÔ (KỊCH BẢN 1–3)
# =========================================================================
if SCENARIO == 1:
    # ---------------------------------------------------------
    # KỊCH BẢN 1: QUY MÔ NHỎ & TĨNH (BASELINE)
    # Mục đích: Chạy nhanh, kiểm tra tính đúng đắn của biểu đồ Gantt,
    # không có yếu tố nhiễu (máy hỏng hay thời gian đến khác nhau).
    # ---------------------------------------------------------
    Processing_time = [CKS_Type1] * 2 + [CKS_Type2] * 2 + [CKS_Type3] * 2
    M_num = 20
    J_num = 6
    J = {i: (5 if i <= 2 else (8 if i <= 4 else 10)) for i in range(1, J_num + 1)}
    O_num = sum(J.values())  # Tổng 46 công đoạn

    # Yếu tố động: Không có
    Arrival_Time = [0] * J_num
    Breakdowns = []
    Due_Dates = [100, 110, 150, 160, 200, 210]

elif SCENARIO == 2:
    # ---------------------------------------------------------
    # KỊCH BẢN 2: QUY MÔ TRUNG BÌNH & ĐỘNG MẠNH (HIGH DYNAMIC)
    # Mục đích: Kiểm tra khả năng "chèn" (Insertion Decoding) của
    # Thuật toán khi máy hỏng liên tục và Job đến xưởng rải rác.
    # ---------------------------------------------------------
    Processing_time = [CKS_Type1] * 4 + [CKS_Type2] * 3 + [CKS_Type3] * 3
    M_num = 20
    J_num = 10
    J = {i: (5 if i <= 4 else (8 if i <= 7 else 10)) for i in range(1, J_num + 1)}
    O_num = sum(J.values())  # Tổng 74 công đoạn

    Arrival_Time = [0, 0, 10, 15, 30, 30, 45, 50, 60, 60]
    Breakdowns = [
        {'machine': 2, 'start': 10, 'duration': 40},
        {'machine': 10, 'start': 35, 'duration': 25},
        {'machine': 11, 'start': 60, 'duration': 30},
        {'machine': 14, 'start': 85, 'duration': 20}
    ]
    Due_Dates = [80, 90, 120, 130, 160, 170, 200, 220, 250, 260]

elif SCENARIO == 3:
    # ---------------------------------------------------------
    # KỊCH BẢN 3: QUY MÔ LỚN & PHỨC TẠP (BẢN GỐC)
    # Mục đích: Stress-test thuật toán GA, kiểm tra khả năng hội tụ
    # trong một không gian tìm kiếm cực kỳ lớn (115 công đoạn).
    # ---------------------------------------------------------
    Processing_time = [CKS_Type1] * 5 + [CKS_Type2] * 5 + [CKS_Type3] * 5
    M_num = 20
    J_num = 15
    J = {i: (5 if i <= 5 else (8 if i <= 10 else 10)) for i in range(1, J_num + 1)}
    O_num = sum(J.values())  # Tổng 115 công đoạn

    Arrival_Time = [0, 0, 0, 0, 0, 25, 25, 25, 50, 50, 50, 50, 80, 80, 80]
    Breakdowns = [
        {'machine': 1, 'start': 20, 'duration': 30},
        {'machine': 7, 'start': 40, 'duration': 25},
        {'machine': 14, 'start': 60, 'duration': 20},
        {'machine': 4, 'start': 90, 'duration': 15},
        {'machine': 17, 'start': 110, 'duration': 40}
    ]
    Due_Dates = [100, 110, 120, 130, 140, 160, 180, 200, 220, 250, 280, 300, 320, 350, 380]

# =========================================================================
# NHÓM 2: ĐÁNH GIÁ KHẢ NĂNG PHẢN ỨNG TRƯỚC RỦI RO ĐẶC THÙ (KỊCH BẢN 4–6)
# =========================================================================
elif SCENARIO == 4:
    # ---------------------------------------------------------
    # KỊCH BẢN 4: THẮT NÚT CỔ CHAI (BOTTLENECK)
    # Đặc điểm: Máy 1 và Máy 2 cực chậm (thời gian x2, x3)
    # nhưng lại tham gia vào hầu hết các công đoạn.
    # ---------------------------------------------------------
    J_num = 10
    M_num = 20
    # Sửa đổi thời gian gia công để tạo nút thắt cổ chai tại máy index 0, 1
    CKS_BOTTLE = []
    for row in CKS_Type2:
        new_row = [p * 3 if i < 2 and p != 9999 else p for i, p in enumerate(row)]
        CKS_BOTTLE.append(new_row)

    Processing_time = [CKS_BOTTLE] * J_num
    J = {i: 8 for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0] * J_num
    Breakdowns = []
    # Due dates thoải mái để tập trung xem GA né máy bottleneck như thế nào
    Due_Dates = [500] * J_num

elif SCENARIO == 5:
    # ---------------------------------------------------------
    # KỊCH BẢN 5: ĐƠN HÀNG KHẨN CẤP (URGENT ORDERS)
    # Đặc điểm: 12 Job đến dồn dập, Due Dates cực ngắn.
    # Mục tiêu: Xem thuật toán hi sinh Cmax để cứu Tardiness như thế nào.
    # ---------------------------------------------------------
    J_num = 2
    M_num = 20
    Processing_time = [CKS_Type1] * 4 + [CKS_Type2] * 4 + [CKS_Type3] * 4
    J = {i: (5 if i <= 4 else (8 if i <= 8 else 10)) for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    Breakdowns = [{'machine': 5, 'start': 50, 'duration': 30}]

    # Hạn định cực ngắn (chỉ vừa đủ thời gian chạy máy tối thiểu)
    Due_Dates = [60, 70, 80, 100, 110, 120, 140, 150, 170, 190, 210, 230]

elif SCENARIO == 6:
    # ---------------------------------------------------------
    # KỊCH BẢN 6: XƯỞNG SẢN XUẤT "HỖN LOẠN" (CHAOS)
    # Đặc điểm: Máy hỏng liên tục ở khắp nơi.
    # ---------------------------------------------------------
    J_num = 8
    M_num = 20
    Processing_time = [CKS_Type2] * 4 + [CKS_Type3] * 4
    J = {i: (8 if i <= 4 else 10) for i in range(1, J_num + 1)}
    O_num = sum(J.values())

    Arrival_Time = [0, 20, 40, 60, 0, 20, 40, 60]
    # 8 sự cố máy hỏng trên các máy chủ chốt
    Breakdowns = [
        {'machine': 0, 'start': 10, 'duration': 20},
        {'machine': 2, 'start': 30, 'duration': 15},
        {'machine': 4, 'start': 50, 'duration': 25},
        {'machine': 8, 'start': 70, 'duration': 20},
        {'machine': 12, 'start': 10, 'duration': 40},
        {'machine': 15, 'start': 90, 'duration': 30},
        {'machine': 18, 'start': 40, 'duration': 20},
        {'machine': 19, 'start': 120, 'duration': 25}
    ]
    Due_Dates = [300] * J_num

# =========================================================================
# NHÓM 3: ĐÁNH GIÁ GIỚI HẠN CHỊU TẢI VÀ ĐỘ BỀN BỈ QUY MÔ CÔNG NGHIỆP (KỊCH BẢN 7–9)
# =========================================================================
elif SCENARIO == 7:
    # ---------------------------------------------------------
    # KỊCH BẢN 7: QUY MÔ CÔNG NGHIỆP TĨNH (100 JOBS BASELINE)
    # Đặc điểm: Số lượng công việc rất lớn (100 Jobs), các Job phân
    # phối ngẫu nhiên theo tỷ lệ Type1:Type2:Type3 = 4:4:2.
    # Mục đích: Đánh giá hiệu năng tính toán và khả năng tối ưu toàn cục
    # của GA/Hybrid trong môi trường tĩnh quy mô lớn (Tất cả Job đến ở t=0).
    # ---------------------------------------------------------
    random.seed(101)
    J_num = 100
    M_num = 20
    Job_types = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2], k=J_num)
    Processing_time, J = [], {}
    for i, t in enumerate(Job_types):
        if t == 1: Processing_time.append(CKS_Type1); J[i+1] = 5
        elif t == 2: Processing_time.append(CKS_Type2); J[i+1] = 8
        else: Processing_time.append(CKS_Type3); J[i+1] = 10
    O_num = sum(J.values())

    Arrival_Time = [0] * J_num # Tất cả công việc đều có mặt từ đầu
    Breakdowns = []
    Due_Dates = [J[i+1] * random.randint(30, 60) for i in range(J_num)]

elif SCENARIO == 8:
    # ---------------------------------------------------------
    # KỊCH BẢN 8
    # Đặc điểm: 120 Jobs xuất hiện rải rác từ t=0 đến t=3000. Đi kèm
    # với 15 sự cố hỏng máy ngẫu nhiên kéo dài (từ 50-150 đơn vị thời gian).
    # Tỷ lệ loại Job phân bổ đồng đều hơn (3:4:3).
    # Mục đích: Thử thách thuật toán tái lập lịch động (Dynamic Scheduling)
    # và chiến lược chèn vị trí trống trong một chuỗi sự kiện dày đặc.
    # ---------------------------------------------------------
    random.seed(102)
    J_num = 120
    M_num = 20
    Job_types = random.choices([1, 2, 3], weights=[0.3, 0.4, 0.3], k=J_num)
    Processing_time, J = [], {}
    for i, t in enumerate(Job_types):
        if t == 1: Processing_time.append(CKS_Type1); J[i+1] = 5
        elif t == 2: Processing_time.append(CKS_Type2); J[i+1] = 8
        else: Processing_time.append(CKS_Type3); J[i+1] = 10
    O_num = sum(J.values())

    Arrival_Time = sorted([random.randint(0, 3000) for _ in range(J_num)])
    Due_Dates = [Arrival_Time[i] + J[i+1] * random.randint(40, 80) for i in range(J_num)]
    Breakdowns = [
        {'machine': random.randint(0, M_num - 1),
         'start': random.randint(500, 4000),
         'duration': random.randint(50, 150)} for _ in range(15)
    ]

elif SCENARIO == 9:
    # ---------------------------------------------------------
    # KỊCH BẢN 9
    # Đặc điểm: Quy mô stress-test cao nhất với 150 Jobs (Xấp xỉ hơn 1000 công đoạn).
    # Thời gian Job đến kéo dài tới t=5000; Tỷ lệ Job phức tạp rất cao (50% Type2, 30% Type3).
    # Đồng thời xưởng chịu 25 đợt hỏng máy có thể kéo dài lên tới 300 đơn vị thời gian.
    # Mục đích: Đánh giá giới hạn chịu tải, tốc độ hội tụ và độ ổn định bền vững
    # (Robustness) của mô hình lai (Hybrid) trong điều kiện vận hành khắc nghiệt nhất.
    # ---------------------------------------------------------
    random.seed(103)
    J_num = 150
    M_num = 20
    Job_types = random.choices([1, 2, 3], weights=[0.2, 0.5, 0.3], k=J_num)
    Processing_time, J = [], {}
    for i, t in enumerate(Job_types):
        if t == 1: Processing_time.append(CKS_Type1); J[i+1] = 5
        elif t == 2: Processing_time.append(CKS_Type2); J[i+1] = 8
        else: Processing_time.append(CKS_Type3); J[i+1] = 10
    O_num = sum(J.values())

    Arrival_Time = sorted([random.randint(0, 5000) for _ in range(J_num)])
    Due_Dates = [Arrival_Time[i] + J[i+1] * random.randint(30, 100) for i in range(J_num)]
    Breakdowns = [
        {'machine': random.randint(0, M_num - 1),
         'start': random.randint(1000, 6000),
         'duration': random.randint(100, 300)} for _ in range(25)
    ]