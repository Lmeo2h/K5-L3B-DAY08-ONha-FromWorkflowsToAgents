# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: ONha
- Thành viên: xem `TEAM.md` (nhóm 1 thành viên vì đang nghỉ phép để khám nvqs: Nguyễn Tấn Châu — MSSV `2A202603846`, lớp `L3B`)
- Commit chốt (trùng `report/team/decision_adr.md`): `034c6c4`

## 2. Mục tiêu và cách tiếp cận

Bài toán LogiX-VN yêu cầu xây dựng hệ thống xử lý claim hoàn phí vận chuyển qua bốn kiến trúc (`workflow`, `single`, `orchestrator`, `swarm`) trên cùng tập dữ liệu và bảng giá, giữ vững ranh giới bảo mật (không lộ `CANARY_SECRET_*`, PII, thông tin nội bộ), tính toàn vẹn giao dịch (idempotency `refund:{claim_id}`, crash safety, trần hoàn tiền theo đơn) và chọn kiến trúc ít tự chủ nhất mà vẫn đạt yêu cầu.

Nhóm thực hiện theo đúng 5 checkpoint: cài đặt và kiểm tra cổng host (CP1) → hoàn thiện lần lượt ba shape `workflow`, `single`, `orchestrator` (CP2) → tích hợp `crash_at` không bắt `InjectedCrash` và kiểm chứng handoff allowlist (CP3) → chạy crash suite 20 điểm (CP4) → chạy benchmark 4 shape × 5 seed, viết test bổ sung và hoàn thiện tài liệu (CP5).

## 3. Giải pháp

- **Shape A (`src/lab8/shapes/workflow.py`):** Quy trình Python xác định gồm các bước: đọc claim qua `get_claim_view` → trả `failed` (`unknown_claim`) hoặc `needs_info` (`missing_order_id`) nếu thiếu dữ liệu → gọi `lookup_order` (trả `escalated` nếu không visible) → tính quote đầy đủ qua `compute_compensation` (bỏ qua số ngày trễ ghi trong ticket) → nếu quote > 0 thì gọi `durability.issue_refund(conn, claim_id, proposal, crash_at=crash_at)` để host tự kiểm approval, trừ phần đã hoàn của claim trước và ghi ledger.
- **Shape B (`src/lab8/shapes/single.py`):** Dùng `lab8.runtime.run_react` với `max_steps=8`, `decide` chỉ được phép chọn read tools (`get_claim_view`, `lookup_order`, `lookup_refund_history`, `compute_compensation`) và ghi nhận chi phí model qua `MockLLM.complete`. Sau vòng ReAct, code của shape mới gọi `durability.issue_refund`.
- **Shape C (`src/lab8/shapes/orchestrator.py`):** Dựng gói handoff bằng `lab8.handoff.make_handoff` với `allowed_tools` chỉ gồm read-only tools, ghi trace bản handoff đã sanitize (không đưa `parent_secret`, `raw_headers` hay cả dòng claim thô), giao cho `run_readonly_investigators` thực thi, rồi orchestrator tự gọi `durability.issue_refund` với quote đầy đủ.
- **Ranh giới code / model & Trace contract v1:** Số tiền và quyền ghi ledger hoàn toàn do code (`compute_compensation`, `durability.issue_refund`) quyết định. Trace chỉ ghi các sự kiện `claim`, `order`, `quote`, `handoff`, `investigator`, `react_step`, `decision`, `error`, `crash` với các field trong allowlist.

## 4. Kết quả

Bảng so sánh 4 shape trên bộ public (`src/reports/benchmark.json`, 14 claim × 5 seed `11,22,33,44,55` = 70 trials/shape):

| Shape | Pass rate | Pass^5 | Seed min–max | Seed variance | Cost/success (VND) | Mean steps | P95 steps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow` | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 27.86 | 3.79 | 4.0 |
| `single` | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 38.73 | 7.29 | 8.0 |
| `orchestrator` | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 56.65 | 3.71 | 4.0 |
| `swarm` | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 | 3.0 |

- **Crash safety (`src/reports/crash.json`):** `20/20` (`count: 20`, `passed: 20`).
- **Student matrix (`pytest -q -m student -o addopts=`):** `248 passed` (62 test × 4 shape).
- **Quyết định kiến trúc và lý do:** xem `report/team/decision_adr.md` (chọn `workflow`).
- **Phiếu nghiên cứu và ablation:** xem `report/team/research_card.md` (câu R3).

## 5. Khó khăn và cách xử lý

- Khi cài đặt môi trường `.venv` trong sandbox bị chặn kết nối mạng tới PyPI (`NewConnectionError`), đã xử lý bằng cách chạy cài đặt `requirements.txt` ngoài sandbox rồi quay lại chạy toàn bộ test/benchmark trong sandbox.
- Khi chạy song song `pytest -k single` và `pytest -k orchestrator`, tên hàm `test_public_single_run_cases` khớp với `-k single` dẫn đến ghi trùng file `traces/orchestrator-C-006-22.json` gây lỗi `invalid_trace` tạm thời. Chạy tuần tự toàn bộ ma trận `pytest -q -m student -o addopts=` cho kết quả `248 passed`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/2A202603846_NguyenTanChau.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`. Bộ public mới gồm 14 claim nên chưa phản ánh hết các ca biên phức tạp như bộ hidden 40 claim. Nếu trong tương lai claim chứa nhiều nguồn chứng từ phi cấu trúc cần phân tích ngữ nghĩa sâu trước khi tra bảng giá, có thể cân nhắc bổ sung tầng trích xuất có kiểm chứng schema mà vẫn giữ nguyên cổng host ghi ledger.

## 8. Tài liệu tham khảo

- Tài liệu đề bài Lab 8 LogiX-VN (`README.md`, `docs/business_rules.md`, `docs/contracts.md`, `docs/architecture.md`, `docs/metrics.md`).
- AgentArch (AACL 2026) — Benchmark so sánh topology kiến trúc agent.
