import streamlit as st
from decimal import Decimal, ROUND_HALF_UP

# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ============================================================
# HÀM TIỆN ÍCH
# ============================================================

def format_money(value):
    """Định dạng tiền Việt Nam."""
    value = Decimal(str(value)).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    return f"{value:,.0f} VNĐ"


def calculate_simple_interest(principal, annual_rate, months):
    """
    Tính lãi đơn.

    Lãi = Gốc × lãi suất năm × số tháng / 12
    """
    rate = annual_rate / 100
    interest = principal * rate * months / 12
    total = principal + interest

    return interest, total


def calculate_compound_interest(principal, annual_rate, months):
    """
    Tính lãi kép theo tháng.

    Lãi suất tháng = lãi suất năm / 12
    Số kỳ = số tháng

    Tổng tiền = Gốc × (1 + lãi suất tháng)^số tháng
    """
    monthly_rate = (annual_rate / 100) / 12

    total = principal * ((1 + monthly_rate) ** months)
    interest = total - principal

    return interest, total


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")

st.markdown(
    """
    Công cụ tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**,
    với các hình thức nhận lãi:
    - 📅 Lãnh lãi theo tháng
    - 📆 Lãnh lãi theo quý
    - 🏦 Lãnh lãi cuối kỳ
    """
)

st.divider()

# ============================================================
# NHẬP THÔNG TIN
# ============================================================

st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    principal = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:
    months = st.number_input(
        "⏱️ Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

col3, col4 = st.columns(2)

with col3:
    interest_type = st.selectbox(
        "📈 Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

with col4:
    payout_type = st.selectbox(
        "💳 Hình thức lãnh lãi",
        [
            "Lãnh lãi theo tháng",
            "Lãnh lãi theo quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

annual_rate = st.number_input(
    "📊 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

st.divider()

# ============================================================
# TÍNH TOÁN
# ============================================================

if st.button("🧮 TÍNH TIỀN LÃI", type="primary", use_container_width=True):

    if principal <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if annual_rate < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # --------------------------------------------------------
    # TÍNH TỔNG LÃI
    # --------------------------------------------------------

    if interest_type == "Lãi đơn":
        total_interest, total_amount = calculate_simple_interest(
            principal,
            annual_rate,
            months
        )
    else:
        total_interest, total_amount = calculate_compound_interest(
            principal,
            annual_rate,
            months
        )

    # --------------------------------------------------------
    # XÁC ĐỊNH SỐ KỲ LÃNH LÃI
    # --------------------------------------------------------

    if payout_type == "Lãnh lãi theo tháng":
        payout_period_months = 1

    elif payout_type == "Lãnh lãi theo quý":
        payout_period_months = 3

    else:
        payout_period_months = months

    # --------------------------------------------------------
    # TÍNH TIỀN LÃI ĐỊNH KỲ
    # --------------------------------------------------------

    if payout_type == "Lãnh lãi cuối kỳ":
        periodic_interest = total_interest

    elif interest_type == "Lãi đơn":
        # Lãi đơn: tiền lãi mỗi tháng không đổi
        monthly_interest = (
            principal * (annual_rate / 100) / 12
        )

        periodic_interest = (
            monthly_interest * payout_period_months
        )

    else:
        # Lãi kép:
        # tiền lãi của mỗi kỳ được tính dựa trên số dư
        period_rate = (
            (1 + (annual_rate / 100) / 12)
            ** payout_period_months
        ) - 1

        periodic_interest = principal * period_rate

    # --------------------------------------------------------
    # HIỂN THỊ KẾT QUẢ
    # --------------------------------------------------------

    st.success("✅ Đã tính toán thành công!")

    st.subheader("📊 Kết quả")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.metric(
            "💰 Tiền lãi định kỳ",
            format_money(periodic_interest)
        )

    with result_col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(total_interest)
        )

    st.metric(
        "🏦 Tổng tiền gốc + lãi",
        format_money(total_amount)
    )

    st.divider()

    # --------------------------------------------------------
    # THÔNG TIN CHI TIẾT
    # --------------------------------------------------------

    st.subheader("📝 Chi tiết khoản gửi")

    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.write(f"**Số tiền gốc:** {format_money(principal)}")
        st.write(f"**Kỳ hạn:** {months} tháng")
        st.write(f"**Lãi suất:** {annual_rate:.2f}%/năm")

    with detail_col2:
        st.write(f"**Hình thức tính:** {interest_type}")
        st.write(f"**Hình thức lãnh lãi:** {payout_type}")

        if payout_type == "Lãnh lãi theo tháng":
            st.write("**Chu kỳ nhận lãi:** 1 tháng")

        elif payout_type == "Lãnh lãi theo quý":
            st.write("**Chu kỳ nhận lãi:** 3 tháng")

        else:
            st.write("**Chu kỳ nhận lãi:** Cuối kỳ")

    # --------------------------------------------------------
    # CÔNG THỨC
    # --------------------------------------------------------

    with st.expander("📐 Xem công thức tính"):

        if interest_type == "Lãi đơn":

            st.markdown(
                """
                ### Lãi đơn

                **Tiền lãi:**

                `Lãi = Tiền gốc × Lãi suất năm × Số tháng / 12`

                **Tổng tiền nhận được:**

                `Tổng tiền = Tiền gốc + Tiền lãi`
                """
            )

        else:

            st.markdown(
                """
                ### Lãi kép

                **Tổng tiền sau kỳ hạn:**

                `Tổng tiền = Tiền gốc × (1 + Lãi suất tháng)^Số tháng`

                Trong đó:

                `Lãi suất tháng = Lãi suất năm / 12`

                **Tổng tiền lãi:**

                `Tổng lãi = Tổng tiền - Tiền gốc`
                """ 
            )

# ============================================================
# GHI CHÚ
# ============================================================

st.divider()

st.caption(
    "⚠️ Kết quả mang tính chất tham khảo. "
    "Cách tính thực tế của ngân hàng có thể khác tùy sản phẩm tiền gửi, "
    "phương thức trả lãi và quy định về số ngày thực tế."
)
