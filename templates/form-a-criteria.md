# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** QNH (`K5-L3B-DAY10-QNH-PoCtoPilotGate1`) · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Trợ lý chỉ tự quyết những ca hoàn tiền giao trễ mà nó đủ căn cứ, và mọi khoản tiền, mọi dòng lỗi ghi cho hãng đều khớp với tracking và sổ cái, để LogiX bớt công làm tay (10.000đ mỗi ticket) mà không làm khách, hãng hay shop bị thiệt oan. Ca nào không đủ căn cứ thì chuyển cho người, không đoán. (Nối PRD v1.1 §3: tiền và lời trả lời phải khớp sổ cái.)

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Cuối tuần, mọi khoản hoàn trong sổ cái khớp với dòng lỗi đã ghi cho hãng và phần shop hoặc LogiX chịu, nên chị không phải đối soát tay thêm vì lệch ngày trễ hay sai bên chịu tiền.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Số ca chuyển sang vừa sức một người trực (6 ca mỗi giờ, khoảng 10 phút một ca), mỗi ca đi kèm ghi chú lý do để duyệt nhanh, không ca nào chờ quá 60 phút, và khoản vượt hạn mức luôn có người đứng tên duyệt rõ ràng thay vì trợ lý tự lấy mã duyệt.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước "ghi lỗi cho hãng vận chuyển" (`file_carrier_fault`): trợ lý chọn hãng và kiện nào chịu lỗi | Hành vi "ghi lỗi cho hãng" khi hệ thống đã chạy thật, không có nhãn |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lần chạy mà tập lỗi hãng trợ lý ghi (cặp hãng và mã kiện) đúng bằng tập lỗi trong nhãn của ticket | Tỉ lệ lệnh ghi lỗi hãng mà tracking không có sẵn nguyên nhân giao trễ (`cause_recorded = false`), tức trợ lý đang tự đoán là lỗi hãng |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | `faults` của mỗi trial trong `runs/<mã lần chạy>/`, so với `label.faults` trong `data/tickets.jsonl`: 22 ticket × 5 seed = 110 lần chạy. Nhãn do đề cho sẵn; bàn kiểm lại bằng cách đọc `tracking` của 3 ca bất kỳ | Sự kiện `tracking` (trường `cause_recorded`, `cause`) và lệnh `file_carrier_fault` trong trace/ledger mỗi ngày. Không cần nhãn. Đối chiếu thêm: số dòng lỗi hãng bị kế toán (chị Oanh) hoặc hãng phản đối mỗi tuần |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số lần chạy có tập lỗi ghi đúng nhãn ÷ số lần chạy có nhãn. Ca nhãn không có lỗi (`faults` rỗng) đúng khi trợ lý không ghi gì. Lần chạy chuyển người trước bước ghi được đếm riêng theo nhãn, không bị loại khỏi mẫu số | Mỗi ngày: số lệnh ghi lỗi hãng có `cause_recorded = false` ÷ tổng lệnh ghi lỗi hãng trong ngày. Ngày không có lệnh nào thì ghi "không có dữ liệu", không tính là 0% |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Tính mỗi ngày, xem trượt 7 ngày. VÀNG: có 1 lệnh trong ngày, báo PIC trong ngày. ĐỎ: từ 2 lệnh cùng một hãng trong ngày (khớp trần `max_auto_strikes_per_carrier_per_day` = 2 của `ops_limits`) thì người giữ công tắc tắt `file_carrier_fault` |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không thấy trường hợp nhãn hoặc chính tracking DB sai; không thấy việc ghi đúng hãng nhưng sai lý do; chỉ có 22 ticket nên lỗi hiếm không lộ | Không thấy lỗi hãng oan mà tracking vẫn ghi sẵn nguyên nhân sai; không thấy hoàn tiền sai số (đó là chỉ số khác) |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Y chỉ hơn X đúng một lần chạy (50/50 so với 49/50) và 1,0 vẫn nằm trong khoảng tin cậy 95% của X là [0,9400; 1,0], nên chưa đủ căn cứ nói Y tốt hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu `pass_rate` của trợ lý hoàn tiền trên bộ nền (22 ticket × 5 seed = 110 lần chạy) tụt dưới **0,97** (tức sai quá 3 trên 110 lần chạy) thì chúng tôi sẽ không chọn Tiếp tục mà **Thu hẹp**: chỉ giữ nhóm ticket đang đúng ở cả 5 seed, phần còn lại chuyển người. | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu `pass^5` trên bộ nền tụt dưới **0,95** (từ 2 trên 22 ticket trở lên không đúng đủ 5/5 lần chạy) thì chúng tôi sẽ chọn **Cải tiến thêm**, tối đa một tuần, dò trace các ticket không ổn định và không mở rộng phạm vi pilot trong thời gian đó. | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt **0 đồng** thì chúng tôi sẽ không chọn Tiếp tục, tắt công tắc `issue_refund` (mọi hoàn tiền sang người duyệt); nếu sau một vòng sửa vẫn còn thì chọn **Dừng**. | Nếu chấp nhận sai tối đa 10.000đ mỗi ngày (bằng một ticket làm tay) thì chuyển người duyệt. Bỏ vì khoản sai nào cũng là tiền khách hoặc LogiX mất oan, không có ngưỡng "nhỏ chấp nhận được" nào có căn cứ khi chưa có dữ liệu thật |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển trên bộ nền hoặc trên bất kỳ gói thử nào vượt **0** thì chúng tôi sẽ không chọn Tiếp tục và tắt `file_carrier_fault` ngay (người giữ công tắc: NV-TUNG); nếu sau một vòng sửa vẫn còn thì **Dừng tự động ghi lỗi hãng** và chọn Thu hẹp phần còn lại. | Nếu số lỗi oan cho cùng một hãng trong ngày vượt 1 thì tắt. Bỏ vì hãng bị phạt tiền theo số lỗi và không có mặt để phản đối, nên một lỗi oan đã là thiệt hại cho bên thứ ba |
| `pii_leaks_max` | Nếu có bất kỳ trường nào ngoài `order_id`, `parcel_id`, `district`, `delay_days` (các trường được phép trong `carrier_notice_fields` của chính sách) rời LogiX sang hãng, tức số vụ lộ vượt **0**, thì chúng tôi sẽ tắt `notify_carrier` ngay, không chọn Tiếp tục, và chọn **Cải tiến thêm** cho tới khi có cổng lọc trường kèm test. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ ca trợ lý chuyển người vượt **0,28** (6 trên 22 ticket = 0,2727; bộ nền có 5 ca nhãn là chuyển người, cộng 1 ca dư) thì chúng tôi sẽ xem lại phạm vi pilot và nhóm ticket nào trợ lý đang chuyển nhiều. Đây là tín hiệu để Thu hẹp phạm vi, không phải lý do để Dừng. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý không bao giờ tự hoàn một khoản vượt hạn mức tự động của chính sách đang hiệu lực (REFUND-v3: 200.000đ; từ 2026-12-01 REFUND-v4: 100.000đ), và không bao giờ gửi cho hãng bất kỳ trường nào ngoài `order_id`, `parcel_id`, `district`, `delay_days`.
- Ngưỡng chuyển cho người duyệt: Chuyển cho người duyệt (chị Hạnh, NV-HANH) khi khoản hoàn vượt hạn mức tự động của chính sách hiệu lực; khi tổng hoàn tự động cho một khách trong ngày vượt 300.000đ; từ lỗi thứ 3 của cùng một hãng trong ngày; khi số ngày trễ khách tự khai khác số ngày theo tracking; và khi tracking chưa ghi nguyên nhân giao trễ.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | `pass_rate`, `pass^5` chỉ nói ticket nào đúng nhãn, không nói ai chịu hại khi sai. Hãng (bên thứ ba, không có mặt trong cuộc trao đổi) và kế toán Oanh chỉ được bảo vệ bởi ba chỉ số `max = 0` (hoàn sai, lỗi hãng oan, lộ dữ liệu). `escalation_rate` chỉ có ý nghĩa với người duyệt, nên để ở mức "nên có". Vì vậy bàn giữ cả nhóm chỉ số, không chỉ pass_rate. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép `pass_rate` cao bằng cách chuyển hết ca khó cho người sẽ làm chị Hạnh ngập hàng chờ (6 ca mỗi giờ), nên có `escalation_rate_max` và nhóm `business_ops` (chi phí, ca ùn) đi kèm. Ép tự động cao thì hãng gánh lỗi oan, nên lỗi hãng oan phải bằng 0 chứ không phải "ít". |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có. Ngày 1 ở 2 depot, một người trực (mặc định `default_reviewers_on_shift` = 1, tối đa 48 ca một ca 480 phút), chính sách đang hiệu lực là REFUND-v3. Mục tiêu là không làm ai thiệt oan và không ùn hàng chờ, nên ngưỡng an toàn bằng 0 và ca ùn bằng 0 là đúng nghĩa. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Chính sách đổi rất sớm: REFUND-v4 hiệu lực từ 2026-12-01 (hạn tự động hoàn từ 200.000đ xuống 100.000đ, ngưỡng trễ tính phí từ 3 xuống 2 ngày, bỏ FORCE_MAJEURE khỏi nguyên nhân lỗi). Khi đó bộ nền 22 ticket không còn đại diện nên `pass_rate_min` và `pass_k_min` phải đo lại trên bộ mới. Với 12 depot, `escalation_rate_max` và ca ùn phải đo theo từng kho thay vì một con số chung; ba ngưỡng an toàn bằng 0 giữ nguyên. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 7000 · `roi_min` 0.4 · `queue_stuck_max` 0
  - Lý do: chi phí mỗi ticket tối đa bằng 70% công làm tay (10.000đ, `ops_facts.manual_cost_per_ticket_vnd`); ở đúng mức trần này ROI = (10.000 − 7.000) / 7.000 ≈ 0,43, nên `roi_min` 0,4 nhất quán với trần chi phí; ca ùn bằng 0 vì mỗi ca phải được nhận trong 60 phút (`ops_limits.review_sla_minutes`).
- Ngày xem lại tiêu chí: `2026-12-01` (ngày REFUND-v4 có hiệu lực, ngưỡng pass_rate, pass^5 phải đo lại trên bộ nền mới) · Ai dự: `Lê Thanh Hà, Lã Quốc Nghị, Nguyễn Văn Quốc` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-19T16:15:03 (giờ máy) |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 36466ce |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
