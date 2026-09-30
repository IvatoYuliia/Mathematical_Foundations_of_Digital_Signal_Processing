import math
import random
import time
import matplotlib.pyplot as plt

# Обчислення одного члена ряду Фур'є
def calculate_fourier_term(f_i, i, k, N):
    angle = (2 * math.pi / N) * k * i
    A_k = (1 / N) * f_i * math.cos(angle)
    B_k = -(1 / N) * f_i * math.sin(angle)
    multiplication_count = 2
    addition_count = 0
    return A_k, B_k, multiplication_count, addition_count

# Обчислення коефіцієнта Фур'є C_k = A_k + jB_k
def calculate_fourier_coefficient(signal, k):
    N = len(signal)
    A_k = 0.0
    B_k = 0.0
    multiplication_count = 0
    addition_count = 0

    for i in range(N):
        A_term, B_term, multiplications, additions = calculate_fourier_term(signal[i], i, k, N)
        A_k += A_term
        B_k += B_term
        multiplication_count += multiplications
        addition_count += additions

        if i > 0:
            addition_count += 2

    C_k = complex(A_k, B_k)
    return C_k, multiplication_count, addition_count

# Головна програма обчислення ДПФ
def calculate_dft(signal):
    N = len(signal)
    spectrum = []
    total_multiplications = 0
    total_additions = 0
    start_time = time.perf_counter()

    # Обчислення коефіцієнтів C_k
    for k in range(N):
        C_k, multiplications, additions = calculate_fourier_coefficient(signal, k)
        spectrum.append(C_k)
        total_multiplications += multiplications
        total_additions += additions

    end_time = time.perf_counter()
    calculation_time = end_time - start_time
    return (spectrum, calculation_time, total_multiplications, total_additions)

# Формування вхідного вектора
N = 21
random.seed(42)
signal = [random.randint(-10, 10) for _ in range(N)]

print("Вхідний вектор:")
print(signal)
print("Розмірність N =", N)

# Обчислення ДПФ
(spectrum, calculation_time, total_multiplications, total_additions) = calculate_dft(signal)
amplitudes = []
phases = []

# Виведення коефіцієнтів Фур'є
print("Коефіцієнти Фур'є:")
for k, C_k in enumerate(spectrum):
    A_k = C_k.real
    B_k = C_k.imag

    # Обчислення амплітуди коефіцієнта
    amplitude = math.sqrt(A_k**2 + B_k**2)
    amplitudes.append(amplitude)
    # Обчислення фази коефіцієнта
    phase = math.atan2(B_k, A_k)
    phases.append(phase)
    print(f"k = {k:2d}: A_k = {A_k:10.5f}, B_k = {B_k:10.5f}, C_k = {A_k:10.5f} {B_k:+10.5f}j, "
        f"|C_k| = {amplitude:10.5f}, φ_k = {phase:10.5f} рад"
    )

print("\nПоказники обчислення:")
print(f"Час обчислення: {calculation_time:.8f} с")
print(f"Кількість множень: {total_multiplications}")
print(f"Кількість додавань: {total_additions}")

# Побудова амплітудного спектру
plt.figure(figsize=(10, 5))
markerline, stemlines, baseline = plt.stem(range(N), amplitudes)
baseline.set_visible(False)
plt.title(f"Амплітудний спектр, N = {N}")
plt.xlabel("k")
plt.ylabel("|C_k|")
plt.xticks(range(N))
plt.grid(True)
plt.show()

# Побудова фазового спектру
plt.figure(figsize=(10, 5))
markerline, stemlines, baseline = plt.stem(range(N), phases)
baseline.set_visible(False)
plt.title(f"Фазовий спектр, N = {N}")
plt.xlabel("k")
plt.ylabel("φ_k, рад")
plt.xticks(range(N))
plt.grid(True)
plt.show()