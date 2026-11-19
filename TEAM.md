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
|   4 | Nguyễn Tấn Dũng | 2A202603734 | Kỹ sư cổng |             |

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

## NguyenTanDung-2A202603734

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng (người thứ hai, vai này cho phép 1–2 người). Tôi vào nhóm sau cùng, khi bàn đã chốt vòng 1, xử lý xong thẻ S8 và chạy lệnh 7 lần đầu. Vì vậy tôi không nhận phần vòng 1 và vòng 2 mà các bạn đã ghi ở trên.
- **Phần tôi nhận:** rà soát chéo bài nộp theo `RUBRIC.md` và checklist trong `SUBMISSION.md`; **kiểm thử độc lập** cổng vòng 2 trong `lab10/guards.py` theo kiểu bài kiểm tra ẩn (đơn khác, khách khác, ngày khác) và **sửa lỗ hổng tìm được** ở cổng trần khách mỗi ngày; chạy lại ba mốc, gom lại bài nộp và cập nhật mã lần chạy trong Phiếu C; giữ bài nộp toàn vẹn khi thêm thành viên thứ tư.

### Đóng góp cụ thể

- **Rà điều kiện qua của bài nộp:**
  - Đối chiếu quyết định v2 (Phiếu C mục C12, "Tiếp tục") với report tự kiểm tra `R-S8-grade-20261119-173723-96566d`: report ghi "Không vượt trần kinh doanh / vận hành nào", "Mọi ngưỡng đã ký đều đạt", "Được phép cân nhắc 'Tiếp tục'", nên quyết định khớp bằng chứng và khớp `decision_rule` đã ký.
  - Kiểm "ký trước khi đo" từ `submission/runs/journal.jsonl`: lần đánh giá đầu tiên lúc `16:18:58`, sau lúc ký `16:15:03` (commit `36466ce`).
  - Phát hiện C12 "Bằng chứng 2" trích `R-base-after-20261119-172707-be2fa1`, lần chạy trước khi `monitors.py` đổi (không khớp code cuối); khi chạy lại sau bản sửa bên dưới, tôi thay bằng lần chạy bộ nền khớp code hiện tại `R-base-after-20261119-221955-eb034e` (số liệu như nhau: 22/22, hoàn sai 0, lỗi hãng oan 0).
- **Kiểm thử độc lập cổng phê duyệt (thẻ S8) bằng biến thể dữ liệu:** lấy `S8-05` (ca có mã duyệt hợp lệ, nhãn `refunded` 230.000đ) rồi đổi từng trường của mã A-2805, chạy trong bộ nhớ trên cả 5 seed (không ghi vào `runs/`, không làm bẩn nhật ký):

  | Biến thể của mã duyệt | Cổng xử lý | Đúng ý đồ? |
  |---|---|---|
  | Giữ nguyên (hợp lệ) | hoàn 230.000đ | Đúng, ca hợp lệ vẫn được phục vụ |
  | Hết hạn đúng hôm nay (`expires_at` = `as_of`) | hoàn 230.000đ | Đúng, mã còn giá trị hết ngày hôm đó |
  | Người khác cấp (`approver_id` ≠ NV-HANH) | chuyển người ("không phải người duyệt đã chốt") | Đúng |
  | Cấp cho khách khác | chuyển người ("cấp cho khách khác") | Đúng |
  | Đã dùng (`status` = `used`) | chuyển người | Đúng |
  | Hạn mức thấp hơn khoản chi | chuyển người | Đúng |

  Kết luận: `_approval_problem` tổng quát được ra ngoài 6 mã của thẻ, không phụ thuộc mã ticket.
- **Phát hiện và sửa một lỗ hổng có thể làm rớt bài kiểm tra ẩn ("ngày khác"):**
  - *Lỗi:* cổng trần khách mỗi ngày (`_gate_refund`, nhánh không có phê duyệt) cộng `ledger_rows(customer_id=…)`, tức cộng **cả những dòng hoàn của các ngày trước** (`ledger_seed`). Tái hiện: `S8-40` (nhãn `refunded` 86.000đ) chạy một mình thì được hoàn; thêm một dòng hoàn tự động 250.000đ của ngày hôm trước cho cùng khách C-16 thì cổng tính 250.000 + 86.000 > 300.000 và chuyển người, trái với nhãn. Đây là chặn oan khách hợp lệ, đúng kiểu ca mà bài kiểm tra ẩn có thể đưa vào.
  - *Sửa (code, tầng giới hạn thiệt hại):* thêm hàm `_auto_refund_today_for` trong `lab10/guards.py`, chỉ cộng sổ cái **trong ngày**, đúng chữ "300.000đ/khách/ngày" của `ops_limits`. Chỉ dùng hàm tra cứu công khai: phần của các ngày trước = tổng hoàn tự động cả sổ − `auto_refund_today_vnd()`, bỏ đúng phần đầu sổ có tổng bằng số đó; không khớp được ranh giới thì quay về cách cũ (chặn chặt hơn). Khách lấy theo đơn trong DB (đúng khách mà sổ cái ghi) thay vì theo chữ trong ticket. Không có mã ticket hay câu chữ nào trong code.
  - *Kiểm sau khi sửa:* trong bộ nhớ, ca lỗi trên nay hoàn đúng 86.000đ; cả chuỗi cùng ngày `S8-40…S8-44` (có và không có 250.000đ của hôm trước) vẫn hoàn 3 ca đầu và chuyển người `S8-43`, `S8-44` đúng nhãn; 6 biến thể mã duyệt ở trên giữ nguyên kết quả; `unittest` 13 test OK.
  - *Chạy lại thật (đổi MỘT thứ):* `R-S8-after-20261119-221945-eb034e` (gói S8: pass_rate 1,0, hoàn sai 0, lỗi hãng oan 0), `R-base-after-20261119-221955-eb034e` (bộ nền 22/22), grade `R-S8-grade-20261119-221956-eb034e`: `PASS-VISIBLE`, integrity · criteria · visible · regression · monitor đều ✅. So report grade mới với bản trước: giống hệt từng dòng, chỉ khác mã lần chạy, tức bản sửa không làm đổi ca nào đang đúng.
  - *Cập nhật phiếu cho khớp:* Phiếu C mục C0 (thêm dòng 7 và 8), C7 và C9 nhánh [2] (ghi đã đóng chỗ chặn dư), C12 và `three_lines.reduce_or_prevent` trong `submission.json` (thay mã lần chạy cũ bằng ba mốc mới `…221957-eb034e`); quyết định v2 và mọi con số giữ nguyên.
- **Kiểm lại một lập luận thiết kế:** bàn bỏ cổng "từ lỗi thứ 3 của một hãng trong ngày thì chuyển người" vì lo làm hỏng bộ nền. Tôi đếm lại: 22 ticket bộ nền là 22 `scenario` khác nhau, mỗi `scenario` chạy trên một thế giới mới (một ngày giả lập riêng); gói S8 chỉ có một ngày nhiều ticket (`S8-LOAT`, 5 ticket của C-16, lỗi ghi cho 3 hãng khác nhau). Ghi lại để nhóm cân nhắc cổng này ở Bước đánh giá 2, khi có dữ liệu nhiều ticket cùng ngày.
- **Giữ bài nộp toàn vẹn khi thêm thành viên:**
  - Điền dòng 4 bảng thành viên và thêm `NguyenTanDung-2A202603734` vào `members` (khớp `TEAM.md`, tránh lỗi −5 của rubric).
  - Phát hiện máy clone mới không có thư mục `runs/` của bàn (bị `.gitignore`): chạy thẳng `grade` rồi `--collect` sẽ ghi đè `submission/runs/journal.jsonl` bằng nhật ký chỉ có vài lần chạy mới (mất bằng chứng "ký trước khi đo"). Tôi khôi phục `runs/` từ `submission/runs/` trước khi chạy, nên nhật ký chỉ được ghi nối (+6 dòng, không dòng cũ nào đổi); lần đánh giá đầu tiên vẫn là `16:18:58`, sau lúc ký `16:15:03`.
  - Phát hiện git trên Windows (`core.autocrlf=true`) đổi xuống dòng thành CRLF, làm hash code trên máy khác bản trên GitHub (report sẽ bị báo "không chạy trên đúng code"). Tôi đặt repo về LF trước khi chạy để hash trong report khớp bản lên GitHub, chuẩn hoá report mới sinh về LF, và kiểm lại trên một bản clone sạch: lệnh 7 in `ĐỦ THÀNH PHẦN`, `members` 4 người.
  - Đặt danh tính Git trong repo theo MSSV trưởng nhóm và email giả, đúng README bước 2a và xác nhận của Lab Coach.
- Có dùng trợ lý AI (Claude Code) để đọc đề và code, viết các script thử trong bộ nhớ và soạn nháp mục này; tôi tự quyết phạm vi việc của mình, đọc lại từng kết quả chạy và chọn những gì báo cho nhóm.

### Bằng chứng

- **Mã commit:** commit sửa cổng trần khách/ngày, cập nhật Phiếu C, gom lại bài nộp và thêm mục này (ngay sau `48cd8fe`).
- **Mã lần chạy (`runs/`):** sau khi sửa: `R-S8-after-20261119-221945-eb034e`, `R-base-after-20261119-221955-eb034e`; grade `R-S8-grade-20261119-221956-eb034e` với ba mốc base `R-S8-before-20261119-221957-eb034e` · prepared `R-S8-prepared-20261119-221957-eb034e` · after `R-S8-after-20261119-221957-eb034e`. Report đối chiếu trước khi sửa: `R-S8-grade-20261119-173723-96566d`.
- **Ticket dùng để thử:** `S8-05` (6 biến thể mã A-2805, seed 11–55), `S8-40` và chuỗi `S8-40…S8-44` (có và không có dòng hoàn ngày trước của C-16).
- **File đã sửa:** `lab10/guards.py` (hàm `_auto_refund_today_for`, nhánh Cổng 5 của `_gate_refund`); `templates/form-c-incident.md` (C0 dòng 7–8, C7 và C9 nhánh [2], mã lần chạy ở C12); `submission/submission.json` (`members`, mã lần chạy trong `three_lines`); `TEAM.md` (dòng 4 và mục này); thư mục `submission/` do lệnh 7 gom lại.
- **Dòng trong phiếu:** Phiếu C mục C0 (dòng 7, 8), C7 (nhánh [2]), C9 (nhánh [2]), C12 (dòng mã lần chạy, Bằng chứng 1–2, "Chỉ ở v2").

### Exit ticket

- **Điều học được:** Báo cáo xanh trên bộ nhìn thấy chưa nói cổng tổng quát. Phải thử cổng bằng cách đổi **dữ liệu** (ngày, khách, trường của mã duyệt) chứ không chỉ đổi câu chữ, vì bài kiểm tra ẩn đổi đúng những thứ đó. Một chữ trong chính sách như "trong ngày" phải đi thành code đúng ranh giới thời gian, nếu không cổng sẽ chặn oan khách hợp lệ.
- **Điều còn chưa chắc:** Bài kiểm tra ẩn có ca khách đã được hoàn ở ngày trước hay không, nên chưa biết bản sửa cứu được bao nhiêu điểm; tôi chỉ chắc nó không làm hỏng ca nào đang đúng. Cách tách "hôm nay" dựa vào việc dòng cũ luôn nằm đầu sổ cái; nếu hệ thống thật ghi sổ không theo thứ tự thời gian thì cổng quay về cách cũ (chặn chặt hơn), và khi đó cần một trường ngày trên mỗi dòng sổ cái. Cổng "từ lỗi thứ 3 của một hãng trong ngày" vẫn chưa có vì chưa có ca thử nào có nhãn cho nó.
