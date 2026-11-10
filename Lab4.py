import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

n = 11
N = 100 * n
power = (2 * n + 1) / 3

T_values = [4, 8, 16, 32, 64, 128]
K_MAX= 10

def f(t):
    return np.sign(t) * abs(t) ** power

# Обчислення k-го члена інтеграла Фур'є
def fourier_integral(k, T):
    w = 2 * np.pi * k / T

    # Заміна змінної t = N * x
    scale = N ** (power + 1)

    real_integral, real_error = quad(
        lambda x: np.sign(x) * abs(x) ** power,
        -1,
        1,
        weight='cos',
        wvar=w * N,
        epsabs=1e-10,
        epsrel=1e-10,
        limit=500
    )

    real_integral *= scale

    if k == 0:
        imag_integral = 0.0
    else:
        imag_integral, imag_error = quad(
            lambda x: np.sign(x) * abs(x) ** power,
            -1,
            1,
            weight='sin',
            wvar=w * N,
            epsabs=1e-10,
            epsrel=1e-10,
            limit=500
        )

    imag_integral *= scale

    return complex(real_integral, imag_integral), w

def amplitude_spectrum(F):
    return np.sqrt(F.real ** 2 + F.imag ** 2)

k_values = np.arange(0, K_MAX + 1)
results = {}
file = open('fourier_results.txt', 'w', encoding='utf-8')
for T in T_values:
    print(f"\nT = {T}")
    real_values = []
    amplitude_values = []
    for k in k_values:
        F, w = fourier_integral(k, T)
        print(f"k = {k}")
        print(f"w_k = {w:.6f}")
        print(f"F(w_k) = {F.real:.10e} + j({F.imag:.10e})")
        print(f"|F(w_k)| = {amplitude_spectrum(F):.10e}\n")

        file.write(f"T = {T}\n")
        file.write(f"k = {k}\n")
        file.write(f"w_k = {w:.6f}\n")
        file.write(f"F(w_k) = {F.real:.10e} + j({F.imag:.10e})\n")
        file.write(f"|F(w_k)| = {amplitude_spectrum(F):.10e}\n\n")

        real_values.append(F.real)
        amplitude_values.append(amplitude_spectrum(F))

    results[T] = {
        'real': real_values,
        'amplitude': amplitude_values
    }

file.close()

# Графік дійсної частини інтеграла Фур'є
plt.figure(figsize=(12, 6))
for T in T_values:
    plt.plot(
        k_values,
        results[T]['real'],
        label=f'T = {T}'
    )

plt.title('Дійсна частина інтеграла Фур’є')
plt.xlabel('Номер гармоніки k')
plt.ylabel('Re F(w_k)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Графік амплітудного спектра
plt.figure(figsize=(12, 6))
for T in T_values:
    plt.plot(
        k_values,
        results[T]['amplitude'],
        label=f'T = {T}'
    )

plt.title('Амплітудний спектр інтеграла Фур’є')
plt.xlabel('Номер гармоніки k')
plt.ylabel('|F(w_k)|')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
