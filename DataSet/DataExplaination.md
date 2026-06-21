# Dynamic Flexible Job-shop Scheduling Problem (DFJSS) - Data Explanation

Tài liệu này giải thích cấu trúc dữ liệu và các thành phần cốt lõi của bài toán **Lập lịch Shop linh hoạt có yếu tố động (DFJSS)** được triển khai trong dự án.

## 1. Tổng quan về bài toán DFJSS

Mô hình này giải quyết các thách thức trong môi trường sản xuất thực tế thông qua hai đặc điểm chính:
* **Tính linh hoạt (Flexible):** Mỗi công đoạn ($O_{ij}$) có thể được thực hiện trên nhiều máy khác nhau với thời gian gia công tương ứng. Điều này cho phép hệ thống tối ưu hóa việc phân bổ nguồn lực dựa trên tình trạng máy móc.
* **Tính động (Dynamic):** Hệ thống không cố định mà thay đổi theo thời gian thực nhờ việc tích hợp các sự kiện như công việc mới đến xưởng (Job Arrival) và các sự cố máy hỏng (Machine Breakdown).

## 1. Cấu trúc dữ liệu đầu vào 

### Thông số hệ thống và Quy trình gia công
* **`Processing_time`**: Ma trận lưu trữ thời gian gia công của từng công đoạn trên các máy tương ứng.
  * Nếu một máy không thể thực hiện công đoạn đó, giá trị được gán là **9999** (Biểu diễn giá trị 0 trong ma trận).

|            | Machine1 | Machine2 | Machine3 | Machine4 | Machine5 | Machine6 | Machine7 | Machine8 | Machine9 | Machine10 | Machine11 |
| :--------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :-------: | :-------: |
| Operation1 |    10    |    0    |    0    |    0    |    0    |    0    |    0    |    0    |    0    |     0     |     0     |
| Operation2 |    0    |    9    |    0    |    0    |    0    |    0    |    0    |    0    |    0    |     0     |     0     |
| Operation3 |    0    |    0    |    14    |    16    |    0    |    0    |    0    |    0    |    0    |     0     |     0     |
| Operation4 |    0    |    0    |    0    |    0    |    15    |    25    |    21    |    0    |    0    |     0     |     0     |
| Operation5 |    0    |    0    |    0    |    0    |    0    |    0    |    0    |    9    |    13    |    25    |    14    |

* **`J`**: Từ điển (`dict`) lưu trữ số lượng công đoạn cho từng công việc (Job). Ví dụ: `{1: 5, 2: 5}`.
* **`J_num`**: Tổng số lượng công việc (Jobs) trong hệ thống.
* **`M_num`**: Tổng số lượng máy gia công (ví dụ: 20 máy).
* **`O_num`**: Tổng số lượng tất cả các công đoạn cần thực hiện ($O_{total}$).


Ví dụ, nếu số lượng công đoạn của công việc cần làm là **5**, thông số đầu vào sẽ được biểu diễn như sau:

```python
Processing_time = [[10, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999],
                   [9999, 9, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999],
                   [9999, 9999, 14, 16, 9999, 9999, 9999, 9999, 9999, 9999, 9999],
                   [9999, 9999, 9999, 9999, 15, 25, 21, 9999, 9999, 9999, 9999],
                   [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9, 13, 25, 24]]
J = {1: 5, 2: 5, 3: 5, 4: 5, 5: 5}
J_num = 5
M_num = 11
O_num = 25
```

### Các thành phần động (Dynamic Elements)
* **`Arrival_Time`**: Danh sách thời điểm các công việc đến xưởng. Một công việc chỉ có thể bắt đầu gia công sau thời điểm "Arrival" của nó.
* **`Breakdowns`**: Danh sách các sự cố máy hỏng đột xuất. Mỗi sự cố bao gồm:
    * `machine`: Chỉ số máy bị hỏng.
    * `start`: Thời điểm bắt đầu xảy ra sự cố.
    * `duration`: Khoảng thời gian cần thiết để sửa chữa máy.
* **`Due_Dates`**: Ngày hạn định hoàn thành cho từng Job. Thông số này dùng để tính toán độ trễ (Tardiness) và đánh giá hiệu quả lập lịch.

## 3. Các kịch bản thực nghiệm (Experimental Scenarios)

Hệ thống cung cấp 12 kịch bản thực nghiệm  để kiểm chứng khả năng thích ứng của thuật toán trong các điều kiện khác nhau:


### Kịch bản 1-6: 
| Kịch bản | Đặc điểm | Mục tiêu kiểm thử |
| :--- | :--- | :--- |
| **Scenario 1** | Quy mô nhỏ & Tĩnh | Kiểm tra tính đúng đắn cơ bản và hiển thị biểu đồ Gantt. |
| **Scenario 2** | Quy mô trung bình & Động mạnh | Kiểm tra khả năng chèn lịch khi máy hỏng và Job đến rải rác. |
| **Scenario 3** | Quy mô lớn & Phức tạp | Kiểm tra khả năng xử lý bài toán khối lượng lớn (115 công đoạn). |
| **Scenario 4** | Thắt nút cổ chai (Bottleneck) | Đánh giá khả năng điều phối khi một số máy có tải trọng cực lớn. |
| **Scenario 5** | Đơn hàng khẩn cấp | Ưu tiên tối ưu hóa độ trễ (Tardiness) khi thời hạn (Due Date) rất ngắn. |
| **Scenario 6** | Xưởng hỗn loạn (Chaos) | Thử nghiệm trong môi trường cực đoan với nhiều máy hỏng liên tục. |