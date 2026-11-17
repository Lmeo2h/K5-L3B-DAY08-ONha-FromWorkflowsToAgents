# Báo cáo cá nhân — 2A202603846_NguyenTanChau

## 1. Thông tin thành viên

- Họ tên: Nguyễn Tấn Châu
- MSSV: 2A202603846
- Email: chau010804@gmail.com
- GitHub: Lmeo2h

## 2. Phần việc phụ trách

Là nhóm 1 thành viên (`ONha`, lớp `L3B`), mình phụ trách toàn bộ các phần của bài lab:
- Cài đặt môi trường `.venv`, kiểm tra cổng host và baseline CP1.
- Cài đặt cả 3 shape: `workflow`, `single`, `orchestrator` (CP2 & CP3).
- Kiểm thử crash suite 20 điểm (CP4), chạy benchmark 4 shape × 5 seed, viết test bổ sung và hoàn thiện báo cáo nhóm, ADR, research card (CP5).

## 3. Đóng góp cụ thể

- Triển khai `src/lab8/shapes/workflow.py`, `src/lab8/shapes/single.py`, `src/lab8/shapes/orchestrator.py` tuân thủ đầy đủ business rules, Trace contract v1, handoff allowlist và cơ chế `crash_at` không nuốt `InjectedCrash`.
- Thêm file test `src/tests/test_team_onha_shapes.py` kiểm chứng chống prompt injection từ ticket (`C-002`, seed `55`), không lộ secret trong trace và cơ chế truyền full quote cho host trừ phần đã hoàn trước đó (`C-014`).
- Lựa chọn kiến trúc `workflow` trong `report/team/decision_adr.md` dựa trên số liệu thực nghiệm (`pass_rate=1.000`, `cost_per_success=27.86 VND`, `variance=0.0`).

## 4. Bằng chứng

- Commit gốc làm việc: `034c6c4` (và commit hoàn thiện bài nộp).
- Test đã thêm: `src/tests/test_team_onha_shapes.py` (`test_ticket_injection_does_not_override_order_and_trace_is_clean`, `test_partial_prior_refund_passes_full_quote_to_host`).
- File bằng chứng: `src/reports/benchmark.json` (run id dẫn chứng `workflow-C-001-11`), `src/reports/crash.json` (`crash_safety = 20/20`).

## 5. Công cụ AI đã dùng

- Sử dụng trợ lý AI Antigravity để đọc hiểu contract, gợi ý cài đặt khung 3 shape, viết test kiểm tra invariant và rà soát số liệu báo cáo.
- Tự kiểm tra toàn bộ kết quả bằng cách chạy trực tiếp `python -m lab8.smoke`, `python -m pytest -q`, `python -m pytest -q -m student -o addopts=`, `python -m lab8.crash_test`, `python -m lab8.benchmark` và `python -m lab8.check_submission` trên môi trường `.venv` tại máy.

## 6. Tự đánh giá

Hoàn thành đầy đủ 5 checkpoint đúng quy chuẩn, cổng host và toàn bộ 248 test student xanh, crash safety đạt `20/20`, không vi phạm rule cấm sửa file thước đo hay lộ secret trong trace.
