# Phiếu Phản Ánh — K3 Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: điền nội dung ngay dưới mỗi câu hỏi.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Lương Quốc Khánh  Mã học viên: 2A202601713

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Khi deploy Railway, tôi từng quên khai báo `AGENT_API_KEY`. Việc để biến này bắt buộc giúp lỗi lộ ra ngay khi phần cấu hình được dùng, thay vì service âm thầm chạy với một key mặc định như `changeme`. Nếu dùng key mặc định, endpoint có thể bị đưa lên internet với credential dễ đoán và tôi có thể không phát hiện ra cho tới khi có request trái phép.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Log thực tế tôi thu được:
>
> ```json
> {"event":"ask_completed","level":"info","timestamp":"2026-08-10T03:34:24.952578+00:00","user_id":"exercise-log","tokens_in":4,"tokens_out":36,"cost_usd":2.22e-05}
> ```
>
> Từ log JSON này tôi có thể lọc/nhóm theo `event`, `user_id`, thời gian để điều tra request cụ thể; đồng thời có thể tổng hợp `tokens_in`, `tokens_out`, `cost_usd` để theo dõi usage và chi phí. Một câu `print("đã trả lời xong")` không có cấu trúc nên gần như không làm được hai việc đó tự động.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | 312 MB |
| Multi-stage | 296 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Kết quả thực tế của tôi là single-stage 312 MB và multi-stage 296 MB, giảm 16 MB. Phần chênh lệch chủ yếu là các file/phần dư chỉ cần trong quá trình cài dependency ở build stage nhưng không cần mang sang runtime image. Mức giảm không quá lớn vì project dùng `python:3.11-slim` và không có toolchain build nặng.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Tôi thêm một comment vào `app/main.py` rồi build lại. Docker vẫn dùng cache cho `COPY requirements.txt`, `RUN pip install` và `COPY --from=builder /install /usr/local`. Từ `COPY app/ app/` trở đi cache bị invalid nên `COPY utils/ utils/` và `RUN adduser ...` cũng chạy lại. Nếu đặt `COPY . .` trước `RUN pip install`, chỉ cần sửa một file source là layer copy thay đổi và kéo theo `pip install` chạy lại, làm build chậm hơn dù `requirements.txt` không đổi.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Nếu service Python có lỗ hổng cho phép thực thi lệnh và container đang chạy root, kẻ tấn công trước hết có quyền root bên trong container. Nếu deployment còn cấu hình nguy hiểm như mount thư mục host, cấp capability mạnh, chạy privileged hoặc có lỗ hổng container runtime, quyền root đó làm hậu quả nghiêm trọng hơn và có thể mở đường tác động tới host. `USER appuser` cắt chuỗi này ngay sau bước chiếm quyền trong ứng dụng: process bị compromise chỉ có quyền của user không đặc quyền trong container. Nó không bảo đảm tuyệt đối an toàn nhưng giảm đáng kể blast radius.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> Với fixed window reset ở giây 00, người dùng có thể gửi tối đa 20 request trong khoảng 2 giây: gửi 10 request ngay trước khi hết phút, ví dụ ở 12:00:59.x, rồi khi counter reset ở 12:01:00 gửi tiếp 10 request. Sliding window 60 giây tránh burst qua ranh giới này vì 10 request trước vẫn còn nằm trong cửa sổ tính khi 10 request sau tới.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> Rate limit kiểm soát tần suất request trong một khoảng thời gian ngắn, còn cost guard kiểm soát ngân sách tích lũy. Ví dụ một user chỉ gửi 2 request/phút nên rate limit cho qua, nhưng nếu ngân sách tháng gần cạn và request tiếp theo làm vượt budget thì cost guard phải chặn. Ngược lại, một user có thể gửi 11 request rất rẻ trong vài giây khi ngân sách vẫn còn nhiều: cost guard chưa cần chặn nhưng rate limit phải chặn request vượt ngưỡng 10/phút.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> Nếu endpoint dùng chung vừa làm liveness vừa kiểm tra Redis, khi Redis mất kết nối thì cả 3 container vẫn còn process Python sống nhưng probe đều trả lỗi. Platform có thể đánh dấu cả 3 instance unhealthy và lần lượt restart chúng. Sau khi restart, Redis vẫn chưa phục hồi nên probe tiếp tục fail, tạo vòng restart và làm mất capacity của cả cụm dù bản thân app không chết. Tách `/health` và `/ready` tránh việc này: `/health` vẫn báo process sống, còn `/ready` báo instance tạm thời chưa sẵn sàng nhận traffic cho tới khi Redis trở lại.

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> Khi chạy 3 replica và gọi nhiều lần với cùng user, tôi quan sát `history_length` tăng 0, 2, 4, 6, 8. Mỗi request thêm một message user và một message assistant, còn lịch sử nằm trong Redis dùng chung nên request vào replica nào cũng thấy cùng state. Nếu lưu bằng dict Python trong từng process thì mỗi replica có lịch sử riêng; do load balancing, giá trị có thể nhảy kiểu 0, 0, 0, 2, 2, 4 tùy request rơi vào instance nào, thay vì tăng đều toàn cục.

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> Lần deploy Railway đầu tiên của tôi build và deploy đều thành công nhưng bước `Network > Healthcheck` báo `Healthcheck failure`. Vì `/health` chạy tốt ở local và lỗi chỉ xuất hiện ở network stage, tôi kiểm tra lại command khởi động trong `railway.toml` và thấy dùng trực tiếp `$PORT` trong Docker start command. Tôi sửa thành chạy qua shell: `sh -c 'exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}'` để biến `PORT` được expand đúng. Sau khi redeploy, service chuyển sang `ACTIVE`, `/health` trả 200 và public deployment hoạt động bình thường.
