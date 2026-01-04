import streamlit as st
import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, type="call"):
    d1 = (np.log(S/K) + (r+0.5*sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    else: price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

st.set_page_config(page_title="Option Calculator")
st.title("Black-Scholes Pricing Model 📉")

st.sidebar.header("User Input Parameters")
S = st.sidebar.number_input("Current Asset Price (S)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Time to Maturity (Years)", value=1.0)
sigma = st.sidebar.slider("Volatility (σ)", 0.0, 1.0, 0.2)
r = st.sidebar.number_input("Risk-Free Interest Rate", value=0.05)

call_price = black_scholes(S, K, T, r, sigma, "call")
put_price = black_scholes(S, K, T, r, sigma, "put")

col1, col2 = st.columns(2)
col1.metric("Call Price", f"${call_price:.2f}")
col2.metric("Put Price", f"${put_price:.2f}")

st.subheader("Call Price Sensitivity (Spot Price)")
spot_range = np.linspace(S * 0.5, S * 1.5, 10)
vol_range = np.linspace(0.1, 1.0, 10)

st.write("Visualizing how volatility affects option prices...")
chart_data = [black_scholes(s, K, T, r, sigma, "call") for s in spot_range]
st.line_chart(chart_data)
