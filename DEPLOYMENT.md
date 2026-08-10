# Thông Tin Deploy — Checkpoint 5

> Bằng chứng deploy thật cho CP5. Không ghi giá trị secret vào repository.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Lương Quốc Khánh |
| Mã học viên | 2A202601713 |
| Repo | https://github.com/QuocKhanhLuong/K3-Day12-Cloud-Services-And-Deployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | https://day12-agent-production-4b26.up.railway.app |
| Platform | Railway |
| Ngày deploy | 2026-08-10 |

## Biến Môi Trường Đã Set Trên Cloud

Chỉ liệt kê tên biến và nguồn, không ghi giá trị secret:

| Biến | Đã set | Nguồn / Ghi chú |
|------|--------|------------------|
| `PORT` | ✅ | Railway cấp lúc runtime |
| `AGENT_API_KEY` | ✅ | Railway Variables, không lưu trong repo |
| `REDIS_URL` | ✅ | Reference tới `${{day12-redis.REDIS_URL}}` |
| `RATE_LIMIT_PER_MINUTE` | ✅ | Railway Variables, giá trị cấu hình 10 |
| `MONTHLY_BUDGET_USD` | ✅ | Railway Variables, giá trị cấu hình 10.0 |
| `LOG_LEVEL` | ✅ | Railway Variables, INFO |

## Lệnh Kiểm Tra

```bash
BASE_URL="https://day12-agent-production-4b26.up.railway.app"

# 1. Liveness — mong đợi 200
curl -i "$BASE_URL/health"

# 2. Readiness — mong đợi 200 và redis=true
curl -i "$BASE_URL/ready"

# 3. Không có API key — mong đợi 401
curl -i -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'

# 4. Có API key — mong đợi 200
# DEPLOY_API_KEY được export ở local shell, không commit vào repo.
curl -i -X POST "$BASE_URL/ask" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $DEPLOY_API_KEY" \
  -H "X-User-Id: cp5-test" \
  -d '{"question":"Deploy là gì?"}'
```

## Kết Quả Chạy Thật

Kết quả kiểm tra ngày 2026-08-10:

```text
GET /health
HTTP/2 200
{"status":"ok","service":"day12-agent","version":"1.0.0"}

GET /ready
HTTP/2 200
{"status":"ready","redis":true}

POST /ask (không có X-API-Key)
HTTP/2 401
{"detail":"invalid or missing API key"}

POST /ask (có X-API-Key hợp lệ)
HTTP/2 200
{"answer":"Câu hỏi hay. Deploy là gì thường được giải quyết bằng cách chuẩn hóa môi trường chạy: cùng một image chạy giống nhau ở laptop và trên cloud.","user_id":"cp5-test","history_length":0,"cost_usd":2.145e-05,"tokens":{"in":3,"out":35}}
```

## Ghi Chú Lỗi Deploy Đã Gặp

- Deployment đầu tiên build thành công nhưng health check thất bại do Start Command chưa shell-expand biến `PORT` đúng cách. Đã đổi `railway.toml` sang chạy qua `sh -c` và đọc `${PORT:-8000}`.
- Sau đó `/ready` trả 500 vì cấu hình Redis chưa đúng và còn thiếu `AGENT_API_KEY`. Đã sửa `REDIS_URL` thành reference `${{day12-redis.REDIS_URL}}`, thêm `AGENT_API_KEY` trong Railway Variables và redeploy.
- Sau khi sửa, `/health` và `/ready` đều trả 200; `/ask` trả 401 khi thiếu key và 200 khi dùng key hợp lệ.

## Ảnh Chụp Màn Hình

Lưu bằng chứng vào thư mục `screenshots/`:

- `screenshots/dashboard.png` — Railway dashboard hiển thị `day12-agent` và `day12-redis` Online/Active.
- `screenshots/health.png` — kết quả gọi `/health` trả 200.

## Local Fallback

Không sử dụng local fallback cho bài nộp chính vì service đã deploy thành công trên Railway. Giữ `LOCAL_FALLBACK=false` khi chạy CP5.
