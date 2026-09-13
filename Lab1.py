import numpy as np
import matplotlib.pyplot as plt

# 1. Точне аналітичне обчислення заданої функції
def f(x):
    # Задана функція на інтервалі [0, pi]:  f(x) = 11 * sin(11 * pi * x)
    return 11 * np.sin(11 * np.pi * x)

# 2. Обчислення коефіцієнтів Фур'є
def calculate_a0():
    # Обчислення коефіцієнта a0 = 2/pi * integral f(x) dx на [0, pi]
    a0 = 2 * (1 - np.cos(11 * np.pi ** 2)) / (np.pi ** 2)
    return a0

def calculate_ak(k):
    # Обчислення коефіцієнта ak = 2/pi * integral f(x) * cos(2*k*x) dx на [0, pi]
    A = 11 * np.pi
    B = 2 * k

    # sin(Ax) * cos(Bx) = 1/2 [sin((A+B)x) + sin((A-B)x)]

    integral = (
        (1 - np.cos((A + B) * np.pi)) / (A + B)
        +
        (1 - np.cos((A - B) * np.pi)) / (A - B)
    )

    ak = 11 / np.pi * integral
    return ak

def calculate_bk(k):
    # Обчислення коефіцієнта bk = 2/pi * integral f(x) * sin(2*k*x) dx на [0, pi]

    A = 11 * np.pi
    B = 2 * k

    # sin(Ax) * sin(Bx) = 1/2 [cos((A-B)x) - cos((A+B)x)]

    integral = (
        np.sin((A - B) * np.pi) / (A - B)
        -
        np.sin((A + B) * np.pi) / (A + B)
    )

    bk = 11 / np.pi * integral
    return bk

def calculate_coefficients(N):
    # Обчислення коефіцієнтів Фур'є до порядку N
    a0 = calculate_a0()
    a = np.zeros(N + 1)
    b = np.zeros(N + 1)

    a[0] = a0

    for k in range(1, N + 1):
        a[k] = calculate_ak(k)
        b[k] = calculate_bk(k)

    return a, b

# 3. Обчислення наближення рядом Фур'є
def fourier_approximation(x, N):
    # Обчислення наближення функції рядом Фур'є S_N(x) = a0/2 + sum(ak*cos(2kx) + bk*sin(2kx))
    a, b = calculate_coefficients(N)
    result = a[0] / 2

    for k in range(1, N + 1):
        result += (
            a[k] * np.cos(2 * k * x)
            +
            b[k] * np.sin(2 * k * x)
        )

    return result

# 4. Побудова графіків гармонік і коефіцієнтів
def plot_harmonics(N=10):
    x = np.linspace(0, np.pi, 2000)
    a, b = calculate_coefficients(N)

    # Гармоніки
    plt.figure(figsize=(12, 7))

    # Нульова гармоніка
    plt.axhline(a[0] / 2, linestyle='--', label='k = 0')

    for k in range(1, N + 1):
        harmonic = (
            a[k] * np.cos(2 * k * x)
            +
            b[k] * np.sin(2 * k * x)
        )

        plt.plot(x, harmonic, label=f'k = {k}')

    plt.title('Гармоніки ряду Фур’є')
    plt.xlabel('x')
    plt.ylabel('Амплітуда')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Коефіцієнти ak
    k_values = np.arange(0, N + 1)
    plt.figure(figsize=(12, 6))
    plt.stem(k_values, a, basefmt=' ')

    plt.title('Коефіцієнти a_k у частотній області')
    plt.xlabel('k')
    plt.ylabel('a_k')
    plt.grid(True)
    plt.show()

    # Коефіцієнти bk
    plt.figure(figsize=(12, 6))
    plt.stem(k_values[1:], b[1:], basefmt=' '    )

    plt.title('Коефіцієнти b_k у частотній області')
    plt.xlabel('k')
    plt.ylabel('b_k')
    plt.grid(True)
    plt.show()

# 5. Оцінка відносної похибки
def relative_error(x, N):
    # Відносна похибка наближення error = ||f(x) - S_N(x)|| / ||f(x)|| * 100%

    exact = f(x)
    approximation = fourier_approximation(x, N)
    error = (
        np.linalg.norm(exact - approximation)
        /
        np.linalg.norm(exact)
    ) * 100

    return error

# 6. Збереження результатів у файл
def save_results(filename, N, a, b, error):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('Результати розкладу функції у ряд Фур’є\n')
        file.write('f(x) = 11 * sin(11 * pi * x)\n')
        file.write('Інтервал: [0, pi]\n')
        file.write('l = pi/2\n')
        file.write('Аргумент гармонік: 2*k*x\n\n')
        file.write(f'Порядок N = {N}\n\n')
        file.write('Коефіцієнти Фур’є:\n')
        file.write('k\t\tak\t\t\tbk\n')
        for k in range(N + 1):
            if k == 0:
                file.write(f'{k}\t\t{a[k]:.12f}\t\t---\n')
            else:
                file.write(f'{k}\t\t{a[k]:.12f}\t\t{b[k]:.12f}\n')

        file.write('\n')
        file.write(f'Відносна похибка: {error:.12f}%\n')

# 7. Головна програма
def main():
    # Порядок наближення
    N = 10
    # Інтервал [0, pi]
    x = np.linspace(0, np.pi, 2000)

    # Обчислення коефіцієнтів
    a, b = calculate_coefficients(N)

    print('Коефіцієнти ряду Фур’є:')
    print()

    print('k\t\tak\t\t\t\tbk')

    for k in range(N + 1):
        if k == 0:
            print(f'{k}\t\t{a[k]:.10f}\t\t---')
        else:
            print(f'{k}\t\t{a[k]:.10f}\t\t{b[k]:.10f}')

    # Обчислення наближення
    approximation = fourier_approximation(x, N)

    # Обчислення похибки
    error = relative_error(x, N)
    print()
    print(f'Порядок N = {N}')
    print(f'Відносна похибка = {error:.10f}%')

    # Графік точної функції та наближення
    plt.figure(figsize=(12, 6))
    plt.plot(x, f(x), label='Точна функція')
    plt.plot(x, approximation, '--', label=f'Ряд Фур’є, N = {N}')
    plt.title('Наближення функції рядом Фур’є')

    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Графіки гармонік та коефіцієнтів
    plot_harmonics(N)

    # Збереження результатів
    save_results('Lab1_fourier_results.txt', N, a, b, error)
    print()
    print('Результати збережено у файл fourier_results.txt')

# Запуск головної програми
if __name__ == '__main__':
    main()