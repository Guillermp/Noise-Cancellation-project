import numpy as np
import Adaptive_filters



N = 500 # Number of samples

# ------------- Signals ----------------
# The signal we want to recover
d = np.sin(np.linspace(0,3*4*np.pi, N)) 

# The noise source
t = np.arange(N)
noise_source = 0.5 * np.sin(2*np.pi*0.05*t) + 0.3 * np.sin(2*np.pi*0.1*t)  # Low frequency noise (deterministic component)
noise_source += 0.2 * np.random.normal(0, 1, N) # High frequency random componente



def acoustic_path(x):
    y = np.zeros_like(x)
    # Simple FIR filter to simulate room acoustics
    coeffs = [0.4, 0.3, 0.2, 0.1]  # Room impulse response
    for n in range(len(coeffs), len(x)):
        y[n] = sum(c * x[n-i] for i, c in enumerate(coeffs))
    return y

noise_measured = noise_source.copy() # Noise measured near the source
noise_at_mic = acoustic_path(noise_source) # Noise at the location where the desired signal was recorded


# The mixed signal (picked up by the mic)
mixed_signal = d + 5*noise_at_mic

# Using the filter
d_hat= Adaptive_filters.RLS_filter(noise_measured, mixed_signal,0.99, 2)
#d_hat= Adaptive_filters.NLMS_filter(noise_measured, mixed_signal, mu=0.05, order=2)

# Performance metrics
Adaptive_filters.show_performance_metrics(d, d_hat, mixed_signal)

# Plots
Adaptive_filters.plot(mixed_signal, d_hat, d)





        

    
    