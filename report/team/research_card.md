# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R3 |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | AgentArch, AACL 2026 (benchmark so sánh topology kiến trúc agent trên cùng tập tool và tác vụ) |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Hiệu năng và chi phí giữa các kiến trúc (single, workflow, orchestrator, swarm) chỉ so sánh công bằng khi cố định model, bộ tool, prompt và evaluator; kiến trúc phức tạp hơn không mặc nhiên vượt kiến trúc đơn giản hơn trên tác vụ tuần tự có cấu trúc. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Giới hạn trong môi trường benchmark mô phỏng LogiX-VN với MockLLM có seed cố định, 14 public claims và bảng giá `config/pricing.yaml` (không đo latency thật). |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Khi đổi topology từ `workflow` sang `single`, `orchestrator` và `swarm` trên cùng corpus/seed/tool/giá, pass rate không tăng (vẫn <= 1.000, riêng `swarm` giảm nhẹ do tin ticket ở seed 55), trong khi `cost_per_success_vnd` tăng từ ~28 VND lên ~39–57 VND. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Biến giữ cố định: MockLLM, read-only tools và host `durability.issue_refund`, seeds `[11, 22, 33, 44, 55]`, corpus `data/public_claims.jsonl` (14 claims), bảng giá `config/pricing.yaml`, evaluator `lab8.benchmark`. Biến duy nhất thay đổi: topology `shape` (`workflow` vs `single` vs `orchestrator` vs `swarm`). |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: chi phí tăng khi thêm vòng ReAct / handoff / peer call và `swarm` fail T02 ở seed 55 (`status resolved != denied`); đo bằng `pass_rate`, `pass_5`, `seed_variance`, `cost_per_success_vnd`, `mean_steps` trong `src/reports/benchmark.json`. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `src/reports/benchmark.json` (ví dụ `workflow-C-001-11`, `single-C-001-11`, `orchestrator-C-001-11`, `swarm-C-002-55`)
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: **Đúng với hypothesis.** `workflow` đạt `pass_rate = 1.000`, `pass_5 = 1.000`, `seed_variance = 0.000000`, `cost_per_success_vnd = 27.86`, `mean_steps = 3.79`; `single` đạt `1.000 / 1.000 / 0.000000 / 38.73 VND / 7.29 steps`; `orchestrator` đạt `1.000 / 1.000 / 0.000000 / 56.65 VND / 3.71 steps`; `swarm` đạt `0.986 / 0.929 / 0.000816 / 49.57 VND / 2.80 steps` (fail 1 trial T02 ở seed 55).
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
