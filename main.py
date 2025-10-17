import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PLL Parameters
# -----------------------------
w_ref = 2 * np.pi * 15.0      # Reference frequency [rad/s] (10 Hz)
w_free = 2 * np.pi * 15.5      # Free-running VCO frequency [rad/s] (9.5 Hz)
Kv = 200.0                    # VCO sensitivity [rad/s/V]
Kd = 1.0                      # Phase detector gain (multiplier type)
tau = 1                       # RC Loop filter time constant [s]
dt = 1e-4                     # Time step [s]
T = 5.0                       # Total time [s]

# -----------------------------
# Initialization
# -----------------------------
N = int(T / dt)
t = np.linspace(0, T, N, endpoint=False)
v_in = np.sin(w_ref * t)      # reference input
phi_out = np.zeros(N)
v_out = np.zeros(N)
v_d = np.zeros(N)
v_c = np.zeros(N)

phi_out[0] = 1.0              # initial phase offset
v_out[0] = np.sin(phi_out[0])
v_c[0] = 0.0

# -----------------------------
# Simulation loop
# -----------------------------
for k in range(1, N):
    # Phase detector: multiply input and VCO output
    v_d[k] = Kd * v_in[k-1] * v_out[k-1]

    # Loop filter (1st-order RC low-pass): dv_c/dt = (v_d - v_c)/tau
    # Simulates transient response
    v_c[k] = v_c[k-1] + (v_d[k] - v_c[k-1]) * dt / tau

    # VCO: dφ/dt = ω_free + Kv * v_c
    # Phase
    phi_out[k] = phi_out[k-1] + (w_free + Kv * v_c[k]) * dt
    # sinusoidal output
    v_out[k] = np.sin(phi_out[k])

# -----------------------------
# Plots (each in its own figure)
# -----------------------------
plt.figure()
plt.plot(t, v_in, label='Input (reference)')
plt.plot(t, v_out, label='VCO output', alpha=0.7)
plt.xlim(0, 0.5)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('PLL Input and Output (Sinusoidal)')
plt.legend()
plt.grid(True)


plt.figure()
plt.plot(t, v_d)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Phase Detector Output (v_d)')
plt.grid(True)


plt.figure()
plt.plot(t, v_c)
plt.xlabel('Time [s]')
plt.ylabel('Control voltage [V]')
plt.title('Loop Filter Output (v_c)')
plt.grid(True)
plt.show()

# -----------------------------
# Lock summary
# -----------------------------
inst_freq = w_free + Kv * v_c
freq_hz = inst_freq / (2 * np.pi)
steady_freq = np.mean(freq_hz[int(0.8*N):])
print(f"Approx. steady-state output frequency: {steady_freq:.7f} Hz")
print(f"Expected reference frequency: {w_ref/(2*np.pi):.7f} Hz")