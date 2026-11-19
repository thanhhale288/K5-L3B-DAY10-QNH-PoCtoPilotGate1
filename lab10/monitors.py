"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def customer_daily_auto_refund_max_vnd(trials):
    """Tổng hoàn TỰ ĐỘNG (không có phê duyệt) lớn nhất của một khách trong một ngày vận hành. Trần Ops/Finance: 300.000đ.
    Dữ liệu: ledger của từng trial, cộng dồn theo (seed, day, khách). Lên sát hoặc quá trần = hệ thống đang hoàn rải nhiều khoản nhỏ."""
    per = {}
    for t in trials:
        for r in t.get("ledger") or []:
            if not r.get("approval_id"):
                k = (t["seed"], t["day"], r["customer_id"])
                per[k] = per.get(k, 0) + r["amount_vnd"]
    return max(per.values(), default=0)


def invalid_approval_rate(trials):
    """Tỉ lệ ticket mà cổng chặn vì mã phê duyệt không hợp lệ (hết hạn, đã dùng, thu hồi, sai đơn/khách/ticket, thiếu hạn mức).
    Dữ liệu: sự kiện guard 'approval_invalid' trong trace. Tăng = quy trình cấp mã đang có vấn đề, báo NV-HANH rà lại."""
    bad = sum(any(e.get("type") == "guard" and e.get("kind") == "approval_invalid" for e in (t.get("events") or []))
              for t in trials)
    return bad / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "customer_daily_auto_refund_max_vnd": customer_daily_auto_refund_max_vnd,
    "invalid_approval_rate": invalid_approval_rate,
}
STARTER_MONITORS = ("escalation_rate",)
