# BÁO CÁO CÁC THAM SỐ VÀ PHƯƠNG PHÁP THUẬT TOÁN DI TRUYỀN (GA) TRONG BÀI TOÁN FJSP

Báo cáo này tổng hợp toàn bộ các tham số cấu hình, phương pháp mã hóa, lai ghép, đột biến và các yếu tố động được sử dụng trong chương trình lập lịch sản xuất linh hoạt (Flexible Job Shop Scheduling Problem - FJSP).

---

## 1. Thông số Cấu hình Thuật toán (GA Parameters)
Các tham số điều khiển quá trình tiến hóa được định nghĩa trong lớp `GA` (tại file `GA.py` và `main.py`):

| Tham số | Ký hiệu | Giá trị | Ý nghĩa |
| :--- | :--- |:--------| :--- |
| **Population Size** | `Pop_size` | 200     | Số lượng cá thể trong quần thể mỗi thế hệ. |
| **Max Iterations** | `Max_Itertions` | 200     | Số vòng lặp tối đa để thuật toán hội tụ. |
| **Crossover Probability** | `Pc` | 0.8     | Xác suất (80%) thực hiện lai ghép giữa hai cá thể. |
| **Mutation Probability** | `Pm` | 0.5     | Xác suất (50%) thực hiện đột biến trên một cá thể. |
| **Crossover Threshold** | `Pv` | 0.5     | Ngưỡng chọn loại lai ghép (Máy hoặc Thứ tự công đoạn). |
| **Mutation Threshold** | `Pw` | 0.95    | Ngưỡng chọn loại đột biến (Ưu tiên đột biến Máy - 95%). |

---

## 2. Mã hóa Nhiễm sắc thể (Encoding)
Chương trình sử dụng cấu trúc **Nhiễm sắc thể kép (Double-layer Chromosome)**:
- **Lớp MS (Machine Selection):** Độ dài $O_{num}$ (115 gene), mỗi gene lưu chỉ số máy được chọn cho một công đoạn cụ thể.
- **Lớp OS (Operation Sequence):** Độ dài $O_{num}$ (115 gene), lưu thứ tự ưu tiên của các công việc (mỗi công việc xuất hiện $n$ lần tương ứng $n$ công đoạn).

---

## 3. Các Phương pháp Kỹ thuật Chi tiết

### A. Chiến lược Khởi tạo (Initialization)
Quần thể ban đầu được tạo ra từ 3 nguồn để cân bằng giữa chất lượng và tính đa dạng:
1. **Global Selection (60%):** Chọn máy có tổng tải trọng (processing time) nhỏ nhất trên toàn hệ thống.
2. **Local Selection (20%):** Chọn máy dựa trên tải trọng nhỏ nhất tính riêng cho từng Job.
3. **Random Selection (20%):** Chọn máy ngẫu nhiên trong danh sách máy khả thi.

### B. Phương pháp Lai ghép (Crossover)
Dựa vào tham số `Pv`, thuật toán chọn một trong hai cách:
- **Machine Selection Crossover:** Hoán đổi ngẫu nhiên các lựa chọn máy giữa hai cha mẹ.
- **Operation Sequence Crossover:** Sử dụng cơ chế lai ghép bảo toàn thứ tự công việc (tương tự **POX**), đảm bảo con lai không vi phạm điều kiện logic về thứ tự công đoạn.

### C. Phương pháp Đột biến (Mutation)
Dựa vào tham số `Pw`, thuật toán chọn:
- **Machine Mutation (95%):** Chọn ngẫu nhiên một công đoạn và thay đổi máy gia công sang máy có thời gian hoàn thành sớm nhất (Greedy).
- **Operation Mutation (5%):** Chọn một nhóm nhỏ các Job (2-4 Job) và thực hiện hoán vị (Permutation) để tìm ra thứ tự tốt nhất (nhằm tránh bùng nổ tổ hợp).

### D. Phương pháp Chọn lọc (Selection)
- Sử dụng chiến lược **Cạnh tranh (Competition)**: Con lai được tạo ra sẽ so sánh độ thích nghi (`Fitness`) với chính cha mẹ của nó và các biến thể đột biến. Chỉ cá thể có giá trị `Fitness` nhỏ nhất được giữ lại cho thế hệ sau.

---

## 4. Các Yếu tố Động và Giải mã (Dynamic & Decoding)
- **Sự kiện Máy hỏng (Machine Breakdowns):** Có 5 sự kiện hỏng máy được mô phỏng. Thời gian máy hỏng được "đóng băng" trong biểu đồ Gantt (ký hiệu X màu đen).
- **Thời gian đến (Arrival Time):** Các công việc đến theo các đợt ($t_1, t_2,... t_n$).
- **Chiến lược Giải mã (Decoding):** Sử dụng **Active Scheduling** với cơ chế chèn (Insertion). Thuật toán tìm kiếm các "khoảng trống" (time windows) giữa các công đoạn đã xếp lịch hoặc sau khi sửa máy để chèn công đoạn mới vào, giúp giảm tối đa thời gian trống.

---

## 5. Hàm mục tiêu (Objective)
- **Hàm mục tiêu tối ưu** cho bài toán với hai mục tiêu được sử dụng là $Fitness = \alpha\times C_{max} + \beta \times Tardiness$
### Trong đó:
- **Makespan ($C_{max}$):** Tổng thời gian từ khi bắt đầu cho đến khi công việc cuối cùng kết thúc.
- **Tardiness :** Tổng thời gian từ khi bắt đầu cho đến khi công việc cuối cùng kết thúc.
- 