import streamlit as st
import random
import math

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

def simulate(n: int, trials: int = 50, seed: int = 42):
    """Simulate multiple experiments and return mean number of draws."""
    random.seed(seed)
    results = [simulate_one(n) for _ in range(trials)]
    mean = sum(results) / len(results)
    return mean

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

# User input
n = st.number_input("Enter number of different coupons (n):", min_value=1, value=10, step=1)

# Run simulation
if st.button("Run Simulation"):
    analytic = analytic_expected_time(n)
    mean_simulation = simulate(n)  # fixed 50 trials

    st.subheader("📊 Results")
    st.write(f"**Analytic expected waiting time:** {analytic:.2f} draws")
    st.write(f"**Simulated average number of draws:** {mean_simulation:.2f} draws")
