# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): QNH
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-QNH-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S8

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Lê Thanh Hà | 2A202603901 | Kỹ sư cổng | ✓ |
|   2 | Lã Quốc Nghị | 2A202603947 | Vận hành và pháp lý |             |
|   3 | Nguyễn Văn Quốc | 2A202603864 | Sản phẩm và kinh doanh |             |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## LeThanhHa-2A202603901

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng, đồng thời trưởng nhóm. Cả bàn làm trên máy của trưởng nhóm nên mọi commit mang cùng danh tính `2A202603901`; phần việc dưới đây tính theo vai, không theo máy gõ lệnh.
- **Vòng 1:** câu 2.1 (Phiếu B mục B1, mã lần chạy ở B0), câu 2.2 (B2, bảng soát lỗi `T-002@55`), câu 2.6 (B7.1, cổng trong `lab10/guards.py`), câu 2.7 (B7.2) và 2.8 (B7.3, ba ticket hiểm), chốt cổng vòng 1 bằng `lab10.checkpoint` (B8); PIC các dòng 1 và 4 của checklist (B5). Với vai trưởng nhóm: ký tiêu chí bằng `lab10.criteria sign` và đẩy ngay.
- **Vòng 2 (thẻ S8):** câu 3.0 (C1, chạy `grade` trước khi sửa), 3.1 (C2, dò trace và bảng soát lỗi), 3.4 (C6 và C9, fault tree), 3.5 (sửa `lab10/guards.py`, C7 phần code), 3.6 (C8 và `lab10/monitors.py`), chạy ba mốc, lệnh 7 (`check_submission --collect`) và rà bài nộp.

### Đóng góp cụ thể

- **Vòng 1:**
  - Chạy mốc base của bộ nền (`R-base-before-20261119-161858-b45eeb`): hoàn sai 20.000đ và 1 lỗi hãng oan; dò `T-002@55` và điền bảng soát lỗi: model lấy số ngày khách khai (5) đè số theo tracking (2).
  - Viết ba cổng trong `guards.py` từ dữ kiện DB và chính sách, không có mã ticket trong code: `_gate_refund` (số hoàn khớp quyền lợi tính từ DB, kiểm sổ cái và phê duyệt), `_gate_carrier_fault` (chỉ ghi lỗi hãng khi DB xác nhận, đúng kiện và đúng số ngày), `pre_guard` (ghim chính sách theo ngày hiệu lực thay vì cờ `index_active`). Không viết cổng "tối đa 2 lỗi mỗi hãng mỗi ngày" vì bộ nền có 4 lỗi hợp lệ cùng hãng VNX trong một ngày; cổng đó sẽ làm hỏng ca đang đúng.
  - Tách tác dụng từng lớp bằng ba lần chạy mỗi lần đổi một thứ: chỉ cổng code (`…162207-2d2862`), thêm cổng pháp lý (`…162207-a3a0ab`), thêm cổng kinh doanh và vận hành (`…162207-5f6460`); viết ba ticket hiểm bằng `--adhoc` (số ngày khách khai, lệnh cài trong ticket, số điện thoại trong ghi chú).
  - Chốt cổng vòng 1 (hash `46822947`) và chạy mốc prepared (`R-base-prepared-20261119-163940-9e91bf`).
- **Vòng 2, thẻ S8:**
  - Chạy `grade` trước khi sửa (mốc prepared `R-S8-prepared-20261119-171557-9e91bf`); dò `S8-02`, `S8-03`, `S8-04` (mã duyệt hết hạn, thiếu hạn mức, cấp cho đơn khác) và `S8-43@11` (hoàn rải cho khách C-16, tổng 498.000đ so với trần 300.000đ).
  - Sửa `guards.py`: hàm `_approval_problem` (kiểm trạng thái, hạn dùng, đơn, khách, ticket, người cấp, hạn mức), cổng hạn mức tự động, cổng trần khách mỗi ngày đọc từ `ops_limits`. Lần chạy đầu chưa đỡ thêm vì lệnh ghi không mang `customer_id`; lần sau lấy từ `ctx.ticket` thì S8-43 và S8-44 được chuyển người (`R-S8-after-20261119-171844-11cc8d`).
  - Thêm chỉ số theo dõi trong `monitors.py`: `invalid_approval_rate`, `customer_daily_auto_refund_max_vnd`, và hai chỉ số bắt lỗi chìm ngoài thẻ `claim_over_db_rate`, `claim_db_mismatch_rate` (bằng chứng `T-002@55`, `T-001@55`, `T-015@55`, `T-021@55`, `T-022@55`).
  - Kết quả bộ S8: hoàn sai 6.845.000đ → 0, lỗi hãng oan 35 → 0, pass_rate 0,8654 → 1,0; bộ nền vẫn 22/22. Lệnh 7 in `ĐỦ THÀNH PHẦN`.
- Có dùng trợ lý AI (Claude Code) trong gần như toàn bộ các việc trên: đọc đề và gom luật, soạn code cổng và chỉ số, chạy lệnh và soạn nháp các phiếu A, B, C. Tôi chọn các phương án (lý do pre-mortem, quyết định v1 và v2, ngày xét lại, PIC) và tự commit, push; các con số trong phiếu lấy từ report của `lab10`.

### Bằng chứng

- **Mã commit:** `f026576` (CP1), `36466ce` (ký tiêu chí), `07c51df` (Phiếu A), `9b94892` (chốt cổng vòng 1 và quyết định v1), `4c76fc2` (nhận thẻ S8), `08aea20` (CP4: cổng và chỉ số cho S8, Phiếu C), `089952a` (bài nộp).
- **Mã lần chạy (`runs/`):** vòng 1: `R-base-before-20261119-161858-b45eeb`, `R-base-after-20261119-162207-2d2862`, `R-base-after-20261119-162207-a3a0ab`, `R-base-after-20261119-162207-5f6460`, `R-base-prepared-20261119-163940-9e91bf`. Vòng 2: `R-S8-before-20261119-171557-9e91bf` (base), `R-S8-prepared-20261119-171557-9e91bf` (prepared), `R-S8-after-20261119-173724-96566d` (after), grade `R-S8-grade-20261119-173723-96566d`.
- **Dòng trong phiếu:** Phiếu B mục B0, B2, B7.1, B7.2, B7.3, B8; Phiếu C mục C0, C1, C2, C6, C7 (cột chỗ sửa), C8 (kể cả mục bonus), C9.

### Exit ticket

- **Điều học được:** Cổng phải dựa vào nguồn sự thật (DB, chính sách theo ngày hiệu lực, sổ cái), không dựa vào chữ khách hay một mã "có sẵn". Và số 100% pass chưa chắc là hết lỗi: `claim_over_db_rate` vẫn 0,0455 sau khi có cổng, tức lỗi gốc còn đó, cổng chỉ che.
- **Điều còn chưa chắc:** Cổng trần khách mỗi ngày dùng sổ cái không phân ngày nên có thể chặn dư, và khách dùng nhiều tài khoản vẫn lọt. Bàn chưa chạy được bài kiểm tra ẩn (đơn, khách, cách viết mới) nên chưa biết các cổng có tổng quát hay chỉ vừa với bộ nhìn thấy.

## NguyenVanQuoc-2A202603864

### Phần việc phụ trách

- **Vai trong bàn:** Sản phẩm và kinh doanh.
- **Vòng 1:** Câu 1.1 (Phiếu A mục A1), câu 1.6 (Phiếu A mục A4 và `config/acceptance_criteria.json`), cùng bàn câu 1.5 (A3) và rà soát ký A5; câu 2.3 (Phiếu B mục B3), cùng bàn câu 2.5 (B6 · lăng kính kinh doanh); câu 2.9 (Phiếu B mục B7.4 và `config/operating_gates.json` mục `business`); tham gia chốt quyết định v1 (Phiếu B mục B8).
- **Vòng 2 (tiếp tục khi nhận thẻ sự cố):** Câu 3.2 (Phiếu C mục C5), câu 3.5 (`config/operating_gates.json` mục `business`, Phiếu C mục C7), và quyết định v2 + 3 dòng bắt buộc (Phiếu C mục C12).

### Đóng góp cụ thể

- **Vòng 1:**
  - Viết mục tiêu cấp hệ thống của trợ lý hoàn tiền (câu 1.1) và hoàn thiện Bản tiêu chí chấp nhận (câu 1.6): ngưỡng `required` (`pass_rate_min: 0.97`, `pass_k_min: 0.95`, các ngưỡng an toàn `= 0`), `nice_to_have` (`escalation_rate_max: 0.28`), `business_ops` (`cost_per_ticket_vnd_max: 7000`, `roi_min: 0.4`, `queue_stuck_max: 0`), `stop_condition`, `decision_rule` 4 quyết định và 2 câu ranh giới đầu ra.
  - Lập bản đồ dữ liệu (nguồn sự thật vs bản sao) và phân tích ví dụ drift khi đổi chính sách `REFUND-v4` từ `2026-12-01` (Phiếu B mục B3); đóng góp lăng kính kinh doanh trong pre-mortem (mục B6).
  - Thiết lập cổng kinh doanh trong `config/operating_gates.json` (`daily_refund_cap_vnd: 1500000`, `cost_budget_per_ticket_vnd: 1000`, `pilot_scope: all/100%`, `roi_min: 0.4`) kèm lý do từ `data/world.json` (`ops_limits`, `ops_facts`), và cùng bàn chốt quyết định v1 (`Tiếp tục`) tại mục B8.
- **Vòng 2:** *(Chờ nhận thẻ sự cố `Sx` để hoàn thành câu 3.2, cập nhật `business` nếu cần ở câu 3.5 và chốt v2 ở C12).*

### Bằng chứng

- **Mã commit Vòng 1:** `f026576` (CP1), `36466ce` (ký tiêu chí `config/acceptance_criteria.lock`), `07c51df` (Phiếu A), `9b94892` (chốt cổng vòng 1, quyết định v1).
- **Mã lần chạy (`runs/`):** `R-base-before-20261119-161858-b45eeb` (base), `R-base-after-20261119-162207-2d2862` (after vòng 1), `R-base-prepared-20261119-163940-9e91bf` (prepared cho v1).
- **Dòng trong phiếu:** `templates/form-a-criteria.md` (A1 câu 1.1, A4 câu 1.6), `templates/form-b-evaluation-gates.md` (B3, B6, B7.4, B8).

### Exit ticket

- **Điều học được:** Phải viết và khóa Bản tiêu chí (`acceptance_criteria.json`, `decision_rule`) **trước** khi xem kết quả chạy thử, đồng thời gắn chặt các ngưỡng kinh doanh (`daily_refund_cap_vnd`, `cost_per_ticket_vnd_max`, `roi_min`) với dữ liệu vận hành thực tế (`ops_facts`, `ops_limits`) và chi phí nhân sự trực duyệt.
- **Điều còn chưa chắc:** Khi nhận thẻ sự cố `Sx` ở Vòng 2 (hoặc khi `REFUND-v4` có hiệu lực từ `2026-12-01`), ngưỡng `escalation_rate_max` (`0.28`) và phạm vi `pilot_scope` 100% ở cả 2 depot có còn giữ được chi phí mỗi ticket ≤ 7.000đ và `queue_stuck_max = 0` hay sẽ cần thu hẹp phạm vi.

## LaQuocNghi-2A202603947

### Phần việc phụ trách

Vai **Vận hành và pháp lý**.

- Câu 2.4: Phiếu B mục B4 (HAZOP vòng 1, ba dòng ngoài kỹ thuật: người duyệt, ngân sách, dữ liệu gửi bên thứ ba) và mục B5 (checklist 9 nhóm, PIC các dòng 3, 5, 7, 8).
- Câu 2.10: `config/operating_gates.json` mục `operations` và `legal`; Phiếu B mục B7.5 (Runbook phần 1–3) và B7.6 (Giờ cao điểm).
- Câu 3.7: Phiếu C mục C11 (cập nhật checklist, Runbook phần 4–5).
- `submission/submission.json`.

### Đóng góp cụ thể

- Duyệt bản nháp Runbook 1–3 và Giờ cao điểm, đối chiếu từng con số với `config/operating_gates.json` và `data/world.json`:
  - Khớp: PIC `NV-TUNG`, người duyệt `NV-HANH`, 2 người trực, 12 ca/giờ, chờ tối đa 45 phút, trần ngày 1.500.000đ và mức báo 80%, phạm vi `all`, hai trường không gửi hãng (`customer_note`, `recipient_contact`).
  - Tính lại giờ cao điểm: 66 ticket/giờ, khoảng 18 ca chuyển người; tới đều thì ca cuối chờ khoảng 30 phút, dồn một lúc thì khoảng 80 phút; người thứ 3 đưa chi phí lên khoảng 7.240đ/ticket ở ngày 22 ticket.
  - Phát hiện `operations.stop_conditions` (bản vòng 1) mới có 3 câu, thiếu hai điều kiện dừng mà Runbook 3 và `stop_condition` đã ký có. Ở vòng 2 đã bổ sung câu 4 (hoàn sai từ 1đ thì NV-TUNG tắt `issue_refund`) và câu 5 (lộ dữ liệu cá nhân thì tắt `notify_carrier`); giữ nguyên thứ tự câu 1–3 để chỗ B7.6 trỏ "mục 3" vẫn đúng. Chỉ đổi câu chữ, không đổi con số nào tham gia tính report; bản chụp vòng 1 không đụng tới.
  - Chỗ còn hở, chuyển sang vòng 2: người trực thứ hai chưa có tên, `NV-HANH` vừa duyệt vừa đứng tên; checklist dòng 5 (tải gấp ba, lỗi 429) còn Chưa, cần vào risk register C10.
- Viết Runbook 5 (Phiếu C mục C11): ba kịch bản tuần đầu (tải gấp 3, LLM lỗi quá 15 phút, người duyệt không tin trợ lý), số khớp config; đã kiểm `lab10/guards.py` chặn hoàn trùng khi sổ cái đã có khoản hoàn (khớp kịch bản 2).
- Điền `submission/submission.json`: `team`, `members`, `decision_v1`. Phần `incident`, `decision_v2`, `three_lines` điền sau khi có thẻ và C12.
- Có dùng trợ lý AI (Claude Code) để rà repo, đối chiếu con số giữa phiếu và config, và soạn nháp Runbook 5; mọi con số đã tự kiểm lại với `data/world.json` và report.

### Bằng chứng

- Commit chốt vòng 1 `9b94892` (mục `operations`, `legal`, B4, B5, B7.5, B7.6); commit ký tiêu chí `36466ce`.
- Lần chạy: `R-base-after-20261119-162207-5f6460` (số sau khi thêm cổng `operations`), `R-base-prepared-20261119-163940-9e91bf` (mốc prepared).
- Phiếu B: B4, B5 dòng 3/5/7/8, B7.5, B7.6. Phiếu C: C11 Runbook 5.
- `config/operating_gates.json` → `operations.stop_conditions` câu 4–5 (vòng 2).

### Exit ticket

- Học được: một con số trong config (số người trực, thời gian chờ tối đa) phải đi kèm một hành động có tên người làm trong runbook, nếu không nó chỉ là con số trên giấy.
- Chưa chắc: công suất 6 ca/giờ mỗi người và tỉ lệ chuyển người khoảng 0,24 lấy từ dữ liệu giả; giờ cao điểm thật có thể dồn cục hơn giả định "tới đều", khi đó 2 người trực có thể không đủ.
