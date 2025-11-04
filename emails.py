import streamlit as st
from dataclasses import dataclass

# ---------- Core logic ----------

@dataclass
class EmailScenario:
    name: str
    list_size: int                 # total subscribers
    sends_per_week: float          # emails per week
    open_rate: float               # as decimal (0.25 = 25%)
    click_rate: float              # of opens, as decimal
    conversion_rate: float         # of clicks, as decimal
    avg_order_value: float         # dollars per order
    gross_margin: float = 0.5      # profit margin, as decimal

    def yearly_metrics(self):
        sends_per_year = self.sends_per_week * 52

        total_sends = self.list_size * sends_per_year
        total_opens = total_sends * self.open_rate
        total_clicks = total_opens * self.click_rate
        total_buyers = total_clicks * self.conversion_rate

        revenue = total_buyers * self.avg_order_value
        profit = revenue * self.gross_margin

        return {
            "name": self.name,
            "sends_per_year": sends_per_year,
            "total_sends": total_sends,
            "total_opens": total_opens,
            "total_clicks": total_clicks,
            "total_buyers": total_buyers,
            "revenue": revenue,
            "profit": profit,
        }


def fmt(num):
    # nice formatting for big numbers
    return f"{num:,.0f}"


# ---------- Streamlit UI ----------

st.set_page_config(
    page_title="Daily Email Profit Calculator",
    layout="wide",
)

st.title("📧 Daily Email Profit Calculator")
st.write(
    "Model the impact of emailing your list more frequently — "
    "using **conservative** assumptions on open, click, and conversion rates."
)

st.markdown("---")

# ---------- Global Assumptions at the top ----------

st.markdown("### ⚙️ Global Assumptions")

with st.expander("Edit assumptions (tap to expand)", expanded=True):
    list_size = st.number_input(
        "List size (subscribers)",
        min_value=1,
        value=500_000,
        step=10_000
    )

    avg_order_value = st.number_input(
        "Average order value ($)",
        min_value=1.0,
        value=97.0,
        step=1.0
    )

    gross_margin_pct = st.slider(
        "Gross margin (%)",
        min_value=10,
        max_value=100,
        value=60,
        step=5
    )

gross_margin = gross_margin_pct / 100

st.caption("Adjust these to match a specific brand or portfolio.")

st.markdown("---")

# ---------- Current vs New Strategy Inputs ----------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Strategy")

    current_sends_per_week = st.number_input(
        "Emails per week (current)",
        min_value=0.0,
        value=2.0,
        step=0.5,
        key="current_sends"
    )

    current_open_rate = st.slider(
        "Open rate (%) – current",
        min_value=1,
        max_value=100,
        value=22,
        key="current_open"
    ) / 100

    current_click_rate = st.slider(
        "Click-through (% of opens) – current",
        min_value=1,
        max_value=100,
        value=6,
        key="current_click"
    ) / 100

    current_conversion_rate = st.slider(
        "Conversion rate (% of clicks) – current",
        min_value=1,
        max_value=100,
        value=3,
        key="current_conv"
    ) / 100

with col2:
    st.subheader("New Strategy (e.g. Daily Emails)")

    new_sends_per_week = st.number_input(
        "Emails per week (new)",
        min_value=0.0,
        value=7.0,
        step=0.5,
        key="new_sends"
    )

    st.caption("You can deliberately **handicap** these rates to be *worse* than current.")

    new_open_rate = st.slider(
        "Open rate (%) – new",
        min_value=1,
        max_value=100,
        value=20,
        key="new_open"
    ) / 100

    new_click_rate = st.slider(
        "Click-through (% of opens) – new",
        min_value=1,
        max_value=100,
        value=5,
        key="new_click"
    ) / 100

    new_conversion_rate = st.slider(
        "Conversion rate (% of clicks) – new",
        min_value=1,
        max_value=100,
        value=2,
        key="new_conv"
    ) / 100

# ---------- Create scenarios & compute metrics ----------

current = EmailScenario(
    name="Current",
    list_size=list_size,
    sends_per_week=current_sends_per_week,
    open_rate=current_open_rate,
    click_rate=current_click_rate,
    conversion_rate=current_conversion_rate,
    avg_order_value=avg_order_value,
    gross_margin=gross_margin,
)

new = EmailScenario(
    name="New",
    list_size=list_size,
    sends_per_week=new_sends_per_week,
    open_rate=new_open_rate,
    click_rate=new_click_rate,
    conversion_rate=new_conversion_rate,
    avg_order_value=avg_order_value,
    gross_margin=gross_margin,
)

cur = current.yearly_metrics()
n = new.yearly_metrics()

# ---------- Output: Yearly Impact ----------

st.markdown("---")
st.header("Yearly Impact")

mcol1, mcol2, mcol3 = st.columns(3)

with mcol1:
    st.subheader("Current")
    st.write(f"**Sends / year:** {fmt(cur['sends_per_year'])}")
    st.write(f"**Opens / year:** {fmt(cur['total_opens'])}")
    st.write(f"**Clicks / year:** {fmt(cur['total_clicks'])}")
    st.write(f"**Buyers / year:** {fmt(cur['total_buyers'])}")
    st.write(f"**Revenue / year:** ${fmt(cur['revenue'])}")
    st.write(f"**Profit / year:**  ${fmt(cur['profit'])}")

with mcol2:
    st.subheader("New")
    st.write(f"**Sends / year:** {fmt(n['sends_per_year'])}")
    st.write(f"**Opens / year:** {fmt(n['total_opens'])}")
    st.write(f"**Clicks / year:** {fmt(n['total_clicks'])}")
    st.write(f"**Buyers / year:** {fmt(n['total_buyers'])}")
    st.write(f"**Revenue / year:** ${fmt(n['revenue'])}")
    st.write(f"**Profit / year:**  ${fmt(n['profit'])}")

with mcol3:
    st.subheader("Uplift")

    rev_diff = n["revenue"] - cur["revenue"]
    prof_diff = n["profit"] - cur["profit"]

    st.write("**Extra revenue / year:**")
    st.markdown(f"### ${fmt(rev_diff)}")

    st.write("**Extra profit / year:**")
    st.markdown(f"### ${fmt(prof_diff)}")

    if rev_diff > 0:
        st.success("Even with conservative assumptions, you're adding serious top-line.")
    else:
        st.warning("With these assumptions, the new strategy doesn't beat the current one.")

st.markdown("---")
st.caption(
    "If you'd like to talk through these numbers and your options, "
    "send an email to zachary@zacharyhydewriter.com for a free consultation."
)
