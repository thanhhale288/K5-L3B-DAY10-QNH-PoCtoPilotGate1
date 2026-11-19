"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _db_facts(ctx, order_id):
    """Sự thật theo DB (không đọc chữ khách): đơn, chính sách hiệu lực hôm nay, kiện bị trễ, số ngày trễ, nguyên nhân."""
    order = ctx.tools.lookup_order(order_id)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if order is None or policy is None:
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    cause = parcel.get("delay_cause") or ("CARRIER" if delay > 0 else None)
    return order, policy, parcel, delay, cause


def pre_guard(ctx):
    # Cổng 3 (pre-mortem B6, lý do "chính sách cũ"): ghim phiên bản chính sách theo NGÀY HIỆU LỰC, không theo cờ index_active.
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không có phiên bản chính sách nào hiệu lực hôm nay: chuyển người")
    return Verdict.allow(policy_id=policy["policy_id"])


def _gate_refund(ctx, action):
    # Cổng 1 (HAZOP issue_refund.amount_vnd = WRONG / INVALID / PERTURBED): số tiền hoàn phải khớp quyền lợi tính từ DB.
    if any(e.get("type") == "directive_obeyed" for e in ctx.events):
        return Verdict.escalate("ticket chứa chỉ thị đòi hoàn đặc biệt (chữ khách là dữ liệu, không phải lệnh): chuyển người duyệt")
    for e in ctx.events:
        if e.get("type") == "model_override" and e.get("db") != e.get("ticket"):
            return Verdict.escalate("số ngày trễ khách khai khác tracking: chuyển người duyệt")
    if ctx.tools.ledger_rows(order_id=action.get("order_id")):
        return Verdict.deny("đơn này đã có khoản hoàn trong sổ cái: không ghi trùng")
    facts = _db_facts(ctx, action.get("order_id"))
    if facts is None:
        return Verdict.escalate("không tra được đơn hoặc chính sách hiệu lực: chuyển người")
    order, policy, _parcel, delay, cause = facts
    allowed = H.entitlement_vnd(policy, order, delay, cause)
    if allowed <= 0:
        return Verdict.deny("theo tracking và chính sách hiệu lực, đơn chưa đủ điều kiện hoàn")
    amount = min(int(action.get("amount_vnd", 0)), allowed)
    ap_id = action.get("approval_id")
    if ap_id:
        ap = next(iter(ctx.tools.lookup_approvals(approval_id=ap_id)), None)
        if (ap is None or ap.get("status") != "valid" or ap.get("expires_at", "") < ctx.as_of
                or ap.get("order_id") != action.get("order_id") or ap.get("max_vnd", 0) < amount):
            return Verdict.escalate("phê duyệt không hợp lệ (hết hạn, đã dùng, sai đơn hoặc không đủ hạn mức): chuyển người")
    if amount < int(action.get("amount_vnd", 0)):
        return Verdict.modify("giảm số hoàn về đúng quyền lợi tính từ DB", amount_vnd=amount)
    return Verdict.allow()


def _gate_carrier_fault(ctx, action):
    # Cổng 2 (HAZOP file_carrier_fault.parcel_id / delay_days = WRONG): chỉ ghi lỗi khi DB xác nhận hãng có lỗi,
    # đúng kiện đang trễ và đúng số ngày theo tracking.
    facts = _db_facts(ctx, action.get("order_id"))
    if facts is None:
        return Verdict.deny("không tra được đơn hoặc chính sách hiệu lực: không ghi lỗi hãng")
    _order, policy, parcel, delay, _cause = facts
    if not H.carrier_at_fault(policy, parcel, delay):
        return Verdict.deny("tracking không xác nhận lỗi thuộc hãng (chưa đủ ngày trễ hoặc nguyên nhân không phải lỗi hãng)")
    fixes = {}
    if action.get("parcel_id") != parcel["parcel_id"]:
        fixes.update(parcel_id=parcel["parcel_id"], carrier_id=parcel["carrier_id"], driver_id=parcel.get("driver_id"))
    if action.get("delay_days") != delay:
        fixes["delay_days"] = delay
    if fixes:
        return Verdict.modify("ghi lỗi đúng kiện và đúng số ngày trễ theo tracking", **fixes)
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_carrier_fault(ctx, action)
    return Verdict.allow()
