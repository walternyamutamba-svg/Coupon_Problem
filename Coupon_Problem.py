import streamlit as st
import random
import math
import pandas as pd
from time import sleep

# --- Coupon Collector Functions ---
def harmonic_number(n: int) -> float:
    """Return the n-th harmonic number H_n = sum_{k=1}^n 1/k"""
    return sum(1.0 / k for k in range(1, n+1))

def analytic_expected_time(n: int) -> float:
    """Analytic expected waiting time to collect all n coupons: n * H_n"""
    return n * harmonic_number(n)

def simulate_one(n: int) -> int:
    """Simulate one experiment, returning the number of draws until the full set is collected."""
    seen = set()
    draws = 0
    while len(seen) < n:
        draws += 1
        coupon = random.randint(1, n)
        seen.add(coupon)
    return draws

def simulate(n: int, trials: int, seed: int = None):
    """Simulate multiple experiments with progress display."""
    if seed is not None:
        random.seed(seed)
    results = []
    progress_bar = st.progress(0)
    for i in range(trials):
        results.append(simulate_one(n))
        progress_bar.progress((i+1)/trials)
    mean = sum(results) / len(results)
    var = sum((x - mean) ** 2 for x in results) / (len(results) - 1) if len(results) > 1 else 0.0
    std = math.sqrt(var)
    return {
        "(n) Total distinct coupon types you need to collect": n,
        "(mean) Average number of cereal boxes needed to collect all n coupons": mean,
        "std (variability of draws)": std,
        "min draws": min(results),
        "max draws": max(results),
        "all_results": results
    }

# --- STREAMLIT APP ---
st.title("🎯 AIMS Group J Coupon Collector’s Problem Simulator")

# Group members nicely formatted
st.markdown("""
**Group Members:**  
- Walter Nyamutamba  
- Olaoluwasubomi Lois Ige  
- Maniraguha Viviane  
- Patrick Nizetimana  
- Irakoze Mireille
""")

st.markdown("""
This app simulates the **Coupon Collector's Problem**:
- There are `n` types of coupons.
- Each draw gives one coupon uniformly at random.
- We keep drawing until all `n` coupons are collected.
""")

# User inputs
n = st.number_input("Enter number of different coupons (n):", min_value=1, value=10, step=1)
trials = st.number_input("Enter number of trials for simulation:", min_value=1, value=50, step=1)

# Run simulation
if st.button("Run Simulation"):
    analytic = analytic_expected_time(n)
    sim_summary = simulate(n, trials, seed=42)

    st.subheader("📊 Results")
    st.write(f"**Analytic expected waiting time:** {analytic:.5f}")
    st.json({k: v for k, v in sim_summary.items() if k != "all_results"})

    # Show all trial results in expandable section
    with st.expander("See all trial results"):
        st.write(sim_summary["all_results"])

    # Histogram using Streamlit-native plotting
    counts, bins = pd.cut(sim_summary["all_results"], bins=20, retbins=True)
    hist_data = pd.Series(sim_summary["all_results"]).value_counts().sort_index()
    st.bar_chart(hist_data)
