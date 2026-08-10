# Thông Tin Deploy — Checkpoint 5

> File này được chuẩn bị sẵn cho CP5. Sau khi deploy thật, thay trạng thái local
> bằng Public URL và dán output thực tế. Không ghi giá trị secret vào repository.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Chưa cập nhật |
| Mã học viên | Chưa cập nhật |
| Repo | https://github.com/QuocKhanhLuong/K3-Day12-Cloud-Services-And-Deployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | Chưa deploy cloud; local fallback dùng `http://localhost:8000` |
| Platform | Render dự kiến; hiện kiểm tra bằng Docker Compose local fallback |
| Ngày chuẩn bị | 2026-08-10 |

## Biến Môi Trường

Chỉ liệt kê tên biến và nguồn, không ghi giá trị secret:

| Biến | Trạng thái | Nguồn |
|------|------------|-------|
| `PORT` | ✅ | platform/container configuration |
| `AGENT_API_KEY` | ✅ | `.env` local hoặc secret trên dashboard cloud |
| `REDIS_URL` | ✅ | Redis service trong Compose; khi deploy đổi sang Redis add-on |
| `RATE_LIMIT_PER_MINUTE` | ✅ | environment, mặc định 10 |
| `MONTHLY_BUDGET_USD` | ✅ | environment, mặc định 10.0 |
| `LOG_LEVEL` | ✅ | environment, mặc định INFO |

## Lệnh Kiểm Tra Local

```bash
set -a
source .env
set +a

docker compose up -d --build

curl -i http://localhost:8000/health
curl -i http://localhost:8000/ready

# Không có API key -> mong đợi 401
curl -i -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'

# Có API key -> mong đợi 200
curl -i -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $AGENT_API_KEY" \
  -H "X-User-Id: sv-test" \
  -d '{"question":"Deploy là gì?"}'
```

## Kết Quả Chạy Thật

Chưa ghi output tại thời điểm chuẩn bị code. Cập nhật mục này bằng output thật
sau khi chạy local hoặc deploy cloud.

## Ảnh Chụp Màn Hình

Sau khi test, lưu bằng chứng vào `screenshots/`, tối thiểu:

- `screenshots/dashboard.png` — dashboard cloud hoặc Docker Desktop/terminal local fallback.
- `screenshots/health.png` — kết quả gọi `/health`.

## Local Fallback

Nếu chưa deploy được cloud, đặt `LOCAL_FALLBACK=true` trong `.env`, chạy stack
Docker Compose và chụp bằng chứng vào `screenshots/`. Khi đã có cloud URL, đổi
`LOCAL_FALLBACK=false`, cập nhật Public URL ở trên và chạy lại `test_cp5.py`.
