import random
import math

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
    """Simulate `trials` experiments and return summary statistics (mean, std, min, max)."""
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
        "results_sample": results[:10]
    }

if __name__ == "__main__":
    # Ask user for input
    n = int(input("Enter number of different coupons (n): "))

    # Analytic expectation
    analytic = analytic_expected_time(n)
    print(f"\nAnalytic expected waiting time for n={n}: {analytic:.5f}")

    # Simulation
    trials = int(input("Enter number of trials for simulation: "))
    sim_summary = simulate(n, trials, seed=42)
    print("\nSimulation summary:")
    for k, v in sim_summary.items():
        print(f"{k}: {v}")
