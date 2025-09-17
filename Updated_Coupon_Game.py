import streamlit as st
import random
import math

# --- Coupon Collector Functions ---
def harmonic_number(n: int) -> float:
    return sum(1.0 / k for k in range(1, n+1))

def analytic_expected_time(n: int) -> float:
    return n * harmonic_number(n)

def simulate_one(n: int) -> int:
    seen = set()
    draws = 0
    while len(seen) < n:
        draws += 1
        coupon = random.randint(1, n)
        seen.add(coupon)
    return draws

def simulate(n: int, trials: int = 50, seed: int = 42):
    random.seed(seed)
    results = [simulate_one(n) for _ in range(trials)]
    mean = sum(results) / len(results)
    return mean

# --- STREAMLIT APP ---
st.title("🎯 AIMS Group J Coupon Collector’s Problem Simulator")

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
""")

# User input
n = st.number_input("Enter number of different coupons (n):", min_value=1, value=10, step=1)

# --- NEW: Automatically show results for default n ---
analytic = analytic_expected_time(n)
mean_simulation = simulate(n)

st.subheader("📊 Results")
st.write(f"**Analytic expected waiting time:** {analytic:.2f} draws")
#st.write(f"**Simulated average number of draws:** {mean_simulation:.2f} draws")


