# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: 034c6c4
- Run id dẫn chứng: workflow-C-001-11 (src/reports/benchmark.json)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000-1.000 / 0.000000
- Cost per success (mô phỏng, VND): 27.86
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 / 0 (70/70 trials ok, 0 leak, 0 bypass)

## Vì sao shape này

Trên cùng bộ public (`data/public_claims.jsonl`, 14 claim × 5 seed `11,22,33,44,55` = 70 trials/shape) và cùng bảng giá `config/pricing.yaml`, ba shape nhóm viết (`workflow`, `single`, `orchestrator`) đều đạt pass rate `1.000`, pass^5 `1.000`, seed min-max `1.000-1.000` và variance `0.000000`, vượt qua `swarm` (`0.986`, pass^5 `0.929`, variance `0.000816`, fail T02 ở seed `55`). Theo nguyên tắc chọn kiến trúc **ít tự chủ nhất mà vẫn làm được việc**, `workflow` là lựa chọn tối ưu vì quy trình xử lý claim hoàn toàn xác định (đọc claim → kiểm tra `order_id` → tra cứu đơn và chính sách hiện hành → tính bồi thường bằng code `compute_compensation` → gọi cổng host `durability.issue_refund`), đạt chi phí mô phỏng thấp nhất (`27.86` VND/success, so với `38.73` ở `single`, `56.65` ở `orchestrator` và `49.57` ở `swarm`), không có biến động giữa các seed và không phụ thuộc vào quyết định chọn tool của model.

## Có đáng đổi lấy multi-agent không

Không đáng đổi lấy multi-agent cho bài toán xử lý claim có quy trình nghiệp vụ và công thức tính tiền xác định như LogiX-VN. Multi-agent (`orchestrator` và `swarm`) làm tăng chi phí mô phỏng lên gần gấp đôi (`56.65` và `49.57` VND/success so với `27.86` của `workflow`) và phát sinh thêm ranh giới truyền dữ liệu (cần handoff allowlist) hoặc rủi ro sai lệch khi model tin văn bản ticket (`swarm` fail T02 ở seed 55). Quyết định chỉ đảo lại sang `single` hoặc `orchestrator` nếu đề bài mở rộng thành tác vụ mở không có quy trình cố định (ví dụ cần tổng hợp nhiều nguồn dữ liệu tự do hoặc phân rã điều tra song song với điều kiện vẫn giữ nguyên cổng host ghi ledger).

## Trace và bằng chứng

Trace của nhóm (`lab8.trace.Trace`) chỉ ghi các sự kiện đã qua allowlist: `claim` (`claim_id`, `order_id`), `order` (output của `lookup_order`), `quote` (output của `compute_compensation`), `decision` (`status`, `reason`, `proposal_amount`), `error` và `crash` (`at`). Nhóm cố ý **không** ghi nguyên dòng `claims` hay `orders` từ SQLite để loại bỏ hoàn toàn `parent_secret`, `CANARY_SECRET_*`, `raw_headers`, số điện thoại, địa chỉ, tên hàng và ghi chú nội bộ. Nếu một trace nằm ngoài thư mục mà scanner quét được, đội security vẫn không thể chứng minh log đó sạch (grader áp dụng fail-closed với `missing_trace`, `stale_trace`, `invalid_trace`, `trace_run_id_mismatch`), nên mọi artifact debug cùng `run_id` đều phải nằm cùng thư mục trace để scanner kiểm tra đầy đủ.

## Giới hạn

MockLLM không phải model sản xuất. Latency để `unavailable`. Không sửa JSON cho đủ 0.75.
