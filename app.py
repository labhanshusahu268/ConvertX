import streamlit as st
import requests
import base64

st.set_page_config(layout="wide")


# ---------- Left Align Layout ----------
st.markdown("""
<style>
.block-container {
    max-width: 650px;
    padding-left: 0px;
    padding-right: 150px;
    margin-left: 0px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Background Function ----------
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: right center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("sl_020622_4930_21.jpg")

# ---------- Session State ----------
if "from_currency" not in st.session_state:
    st.session_state.from_currency = "USD"

if "to_currency" not in st.session_state:
    st.session_state.to_currency = "INR"

# ================= SIDEBAR =================
st.sidebar.title(" ConvertX Panel")

st.sidebar.markdown("###  Popular Pairs")

popular_pair = st.sidebar.selectbox(
    "Select Popular Pair",
    ["USD → INR", "INR → USD", "EUR → USD", "GBP → INR"]
)

if popular_pair:
    from_c, to_c = popular_pair.split(" → ")
    st.session_state.from_currency = from_c
    st.session_state.to_currency = to_c

st.sidebar.markdown("---")
st.sidebar.info("Real-time exchange rates powered by ExchangeRate API.")

st.sidebar.markdown(" About App ")
st.sidebar.write("""
ConvertX is a real-time forex converter  
designed for fast and accurate  
global currency exchange calculations.
""")
st.sidebar.success("Built by Labhanshu ")

# ================= MAIN PAGE =================

st.title("ConvertX")
st.subheader("Smart. Fast. Real-Time Forex Conversion Engine")

amount = st.number_input("Enter the amount", min_value=1.0)

currency_list = ["USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD"]

from_currency = st.selectbox(
    "From:",
    currency_list,
    key="from_currency"
)

to_currency = st.selectbox(
    "To:",
    currency_list,
    key="to_currency"
)

if st.button("Convert"):

    url = f"https://v6.exchangerate-api.com/v6/ef27fea14acf8cf80854edc4/latest/{from_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rate = data["conversion_rates"][to_currency]
        converted = rate * amount

        st.success(f"{amount} {from_currency} = {converted:.2f} {to_currency}")
    else:
        st.error("Failed to fetch conversion rate")

# ---------- Footer ----------
st.markdown("""
<style>
.footer { background-color: #222222; padding: 18px; border-radius: 12px; margin-top: 30px; }
.footer h4 { color: #FFFFFF; text-align: center; margin-bottom: 6px; }
.footer p { color: #D6E4F0; text-align: center; font-size: 13px; line-height: 1.6; }
.footer span { color: #FFD166; font-weight: bold; }
</style>
<div class="footer">
    <h4>🎓 Medi-Caps University</h4>
    <p>
    © 2026 All Rights Reserved<br>
    Developed by <span>Labhanshu Sahu</span> | B.Tech CSE (3rd Year)<br>
    </p>
</div>
""", unsafe_allow_html=True)
