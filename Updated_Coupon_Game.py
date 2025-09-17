import streamlit as st
import random
import math

# --- Coupon Collector Functions ---
def harmonic_number(n: int) -> float:
    """Approximate the n-th harmonic number for large n using H_n ≈ ln(n) + γ"""
    gamma = 0.5772156649  # Euler–Mascheroni constant
    if n > 1000:  # use approximation for large n
        return math.log(n) + gamma
    else:  # exact sum for small n
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
st.title("🎯Group J : Coupon Collector’s Problem Calculator")

st.markdown("""
**Group Members:**  
- Walter Nyamutamba  
- Olaoluwasubomi Lois Ige  
- Maniraguha Viviane  
- Patrick Nizetimana  
- Irakoze Mireille
""")

st.markdown("""
This Web Application calculates the **Coupon Collector's Problem**:
- There are `n` types of coupons.
""")

# User input
n = st.number_input("Enter number of different coupons (n) and press enter:", min_value=1, value=10, step=1)

# --- NEW: Automatically show results for default n ---
analytic = analytic_expected_time(n)
mean_simulation = simulate(n)

st.subheader("📊 Results")
st.write(f"**Expected waiting time:** {analytic:.2f} steps")
#st.write(f"**Simulated average number of draws:** {mean_simulation:.2f} draws")


