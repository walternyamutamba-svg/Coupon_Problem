import streamlit as st
import random
import math
import matplotlib.pyplot as plt

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
        coupon = random.randint(1, n)  # each coupon equally likely
        seen.add(coupon)
    return draws

def simulate(n: int, trials: int, seed: int = None):
    """Simulate `trials` experiments and return summary statistics (mean, std, min, max, all results)."""
    if seed is not None:
        random.seed(seed)
    results = [simulate_one(n) for _ in range(trials)]
    mean = sum(results) / len(results)
    var = sum((x - mean) ** 2 for x in results) / (len(results) - 1) if len(results) > 1 else 0.0
    std = math.sqrt(var)
    return {
        "n": n,
        "trials": trials,
        "mean": mean,
        "std": std,
        "min": min(results),
        "max": max(results),
        "all_results": results
    }

# --- STREAMLIT APP ---
st.title("🎯 Coupon Collector’s Problem Simulator")

st.markdown("""
This app simulates the **Coupon Collector's Problem**:
- There are `n` types of coupons.
- Each draw gives one coupon uniformly at random.
- We keep drawing until all `n` coupons are collected.
""")

# User inputs
n = st.number_input("Enter number of different coupons (n):", min_value=1, value=10, step=1)
trials = st.number_input("Enter number of trials for simulation:", min_value=1, value=100, step=1)

# Run simulation when button clicked
if st.button("Run Simulation"):
    analytic = analytic_expected_time(n)
    sim_summary = simulate(n, trials, seed=42)

    st.subheader("📊 Results")
    st.write(f"**Analytic expected waiting time:** {analytic:.5f}")
    st.json({k: v for k, v in sim_summary.items() if k != "all_results"})

    # Show all trial results
    with st.expander("See all trial results"):
        st.write(sim_summary["all_results"])

    # Histogram plot
    fig, ax = plt.subplots()
    ax.hist(sim_summary["all_results"], bins=20, edgecolor="black")
    ax.axvline(analytic, color="red", linestyle="dashed", linewidth=1, label="Analytic Expectation")
    ax.set_title("Distribution of Waiting Times")
    ax.set_xlabel("Number of Draws")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)
