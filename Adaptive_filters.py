import numpy as np
from matplotlib import pyplot as plt

def NLMS_filter(noise, mixed, mu=0.7, order=20, epsilon=1e-6):
    # I try to get an estimate of n in the mixed signal and then I substract that estimate to obtain the desired underlying signal
    N = len(mixed)
    n_hat = np.zeros(N)
    w_hat = np.zeros(order)

    print("=== Filtering with a NLMS adaptive filter ===")

    for n in range(order,N):
        u = noise[n-order:n] # past samples used in each step
        e = mixed[n] - np.dot(w_hat,u)
        norm_factor = np.dot(u, u) + epsilon

        # Update the weights
        w_hat = w_hat + (mu/norm_factor)*e*u
        n_hat[n] = np.dot(w_hat,u)     

    # Obtain the denoised signal
    return mixed - n_hat


def RLS_filter(noise, mixed, forget_fact=0.9, order=2,epsilon=1e-6):
    """
    RLS (Recursive Least Squares) adaptive filter

    The filter tries to estimate the noise in the mixed signal from the recorded noise
    and substracts it to get the denoised signal
    
    Parameters:
    - noise: reference noise signal
    - mixed: noisy signal (desired signal + noise)
    - forget_fact: forgetting factor lambda (0 < lambda ≤ 1)
    - order: filter order
    - epsilon: small constant for R_inv matrix initialization
    
    Returns:
    - denoised signal
    """

    N = len(mixed)
    n_hat = np.zeros(N)  # estimated noise
    w_hat = np.zeros(order)  # filter coefficients
    
    # Initialize R_inv matrix (inverse correlation matrix of u)
    R_inv = np.eye(order) / epsilon


    print("=== Filtering with a RLS adaptive filter ===")
    
    for n in range(order, N):
        # Input vector (past noise samples, most recent first)
        u = noise[n-order:n]
        
        # A priori error (before filter update)
        e = mixed[n] - np.dot(w_hat, u)
        
        # --- RLS Update Equations ---
        # Compute gain vector
        Pi = R_inv @ u  # P * u
        denominator = forget_fact + u.T @ Pi  # λ + u^T * P * u
        k = Pi / denominator  # gain vector
        
        # Recursive update inverse correlation matrix
        R_inv = (R_inv - np.outer(k, Pi.T)) / forget_fact
        
        # Update filter coefficients
        w_hat = w_hat +  k * e
        
        # Estimate noise at current sample (a posteriori)
        n_hat[n] = np.dot(w_hat, u)
    
    # Obtain the denoised signal
    return mixed - n_hat

def show_performance_metrics(d, d_hat, mixed_signal):
    error = d - d_hat
    mse_before = np.mean((mixed_signal - d)**2)
    mse_after = np.mean(error**2)
    snr_improvement = 10 * np.log10(mse_before / mse_after) if mse_after > 0 else 0

    print(f"\n=== Noise Cancellation Results ===")
    print(f"MSE before filtering: {mse_before:.4f}")
    print(f"MSE after filtering: {mse_after:.4f}")
    print(f"SNR Improvement: {snr_improvement:.2f} dB")


def plot(mixed_signal, d_hat, d):
    # Plots
    plt.style.use('Solarize_Light2')

    plt.figure(figsize=(10,5))

    plt.plot(mixed_signal, label="Mixed signal (d + noise)", alpha=0.6)
    plt.plot(d_hat, label="Adaptive filter output", linewidth=2)
    plt.plot(d, label="Original clean signal d", linestyle="--")

    plt.xlabel("n")
    plt.ylabel("Amplitude")
    plt.title("LMS Noise Cancellation Result")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
