import math
import numpy as np
import matplotlib.pyplot as plt

# N = 96 + 11
number = 107

# 107 у двійковій системі: 1101011
# У 8-й розряд вставляємо 1
binary_number = "11101011"

# 8 відліків дискретизованого сигналу
signal = [int(bit) for bit in binary_number]
# Кількість відліків
N = len(signal)
# Інтервал спостереження
Tc = 16
# Інтервал між сусідніми відліками
T_delta = Tc / N

print(f"N = {number}")
print(f"Двійкове число = {binary_number}")
print(f"Відліки сигналу = {signal}")
print(f"Кількість відліків = {N}")
print(f"Інтервал дискретизації T_delta = {T_delta}")
print(f"Інтервал спостереження Tc = {Tc}")
print()

# Обчислення комплексних коефіцієнтів C_k
coefficients = []
for k in range(N):
    real_part = 0.0
    imaginary_part = 0.0
    for n in range(N):
        angle = 2 * math.pi * k * n / N
        real_part += signal[n] * math.cos(angle)
        imaginary_part -= signal[n] * math.sin(angle)
    real_part /= N
    imaginary_part /= N
    C_k = complex(real_part, imaginary_part)
    coefficients.append(C_k)

# Визначення |C_k| та φ_k
amplitudes  = []
phases = []
for k, C_k in enumerate(coefficients):
    A_k = C_k.real
    B_k = C_k.imag
    amplitude = math.sqrt(A_k**2 + B_k**2)
    phase = math.atan2(B_k, A_k)
    amplitudes.append(amplitude)
    phases.append(phase)
    print(
        f"k = {k}: "
        f"C_k = {C_k.real:.5f} {C_k.imag:+.5f}j, "
        f"|C_k| = {amplitude:.5f}, "
        f"φ_k = {phase:.5f} rad"
    )

# Відтворення первинного аналогового сигналу s(t)
t = np.linspace(0, Tc, 100)
reconstructed_signal = np.full_like(t, amplitudes[0])
for k in range(1, N // 2):
    reconstructed_signal += (2 * amplitudes[k] * np.cos(2 * math.pi * k * t / Tc + phases[k]))
k = N // 2
reconstructed_signal += (amplitudes[k] * np.cos(2 * math.pi * k * t / Tc + phases[k]))

print("\nВідтворений аналоговий сигнал s(t):")
expression = f"{amplitudes[0]:.5f}"
for k in range(1, N // 2):
    expression += (f"\n + {2 * amplitudes[k]:.5f} * cos(2*pi*{k}*t/Tc {phases[k]:+.5f})")
k = N // 2
expression += (f"\n + {amplitudes[k]:.5f} * cos(2*pi*{k}*t/Tc {phases[k]:+.5f})")
print("s(t) =", expression)

# Відтворений аналоговий сигнал
plt.figure(figsize=(10, 5))
plt.plot(t,
    reconstructed_signal,
    label="Відтворений аналоговий сигнал s(t)"
)
# Початкові дискретні відліки
sample_times = np.arange(N) * T_delta
plt.scatter(sample_times,
    signal,
    label="Дискретні відліки сигналу"
)
plt.xlabel("Час t")
plt.ylabel("Значення сигналу s(t)")
plt.title("Відтворення первинного аналогового сигналу")
plt.grid(True)
plt.legend()
plt.show()

# Таблиця значень відтвореного сигналу
t_table = np.arange(17) * (T_delta / 2)
table_signal = np.full_like(t_table, amplitudes[0], dtype=float)
for k in range(1, N // 2):
    table_signal += (
        2
        * amplitudes[k]
        * np.cos(
            2 * math.pi * k * t_table / Tc
            + phases[k]
        )
    )
k = N // 2
table_signal += (
    amplitudes[k]
    * np.cos(
        2 * math.pi * k * t_table / Tc
        + phases[k]
    )
)
print("\nТаблиця значень відтвореного сигналу:")
print(f"{'t/Tc':<10} {'s(t)':>10}")
for i in range(len(t_table)):
    print(
        f"{i}/16{'':<6} "
        f"{table_signal[i]:>10.4f}"
    )

#------------------------------------- 3 ---------------------------------------------
# Обернене дискретне перетворення Фур'є (ОДПФ)
# Відновлення відліків s(nT_delta) за коефіцієнтами C_k
reconstructed_samples = []
for n in range(N):
    s = 0j
    for k in range(N):
        angle = 2 * math.pi * k * n / N
        # s(nT_delta)= sum(C_k * exp(j * 2*pi*k*n/N))
        s += coefficients[k] * complex(math.cos(angle), math.sin(angle))
    if abs(s.real) < 1e-10:
        reconstructed_samples.append(0.0)
    else:
        reconstructed_samples.append(s.real)

print("Відновлені відліки сигналу за допомогою ЗДПФ:")
for n, s in enumerate(reconstructed_samples):
    print(f"n = {n}: s(nT_delta) = {s:.5f}")
print()