from math import cos, sin, pi
from time import perf_counter
import csv


def fft(samples, inverse=False, count_operations=False):
    a = [complex(x) for x in samples]
    n = len(a)

    if n == 0 or (n & (n - 1)):
        raise ValueError("Кількість відліків має бути додатним степенем 2")

    multiplication_count = 0
    addition_count = 0

    j = 0
    for i in range(1, n):
        bit = n >> 1

        while j & bit:
            j ^= bit
            bit >>= 1

        j ^= bit

        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    sign = 1 if inverse else -1

    while length <= n:
        half = length // 2
        angle_step = sign * 2 * pi / length

        for block in range(0, n, length):
            for offset in range(half):
                angle = angle_step * offset
                w = complex(cos(angle), sin(angle))

                top = block + offset
                bottom = top + half

                # Множення
                temp = a[bottom] * w

                if count_operations:
                    multiplication_count += 1

                u = a[top]

                # Додавання
                a[top] = u + temp

                if count_operations:
                    addition_count += 1

                # Віднімання
                a[bottom] = u - temp

                if count_operations:
                    addition_count += 1

        length *= 2

    if inverse:
        a = [v / n for v in a]

    if count_operations:
        return a, multiplication_count, addition_count

    return a


def measure_time(signal):
    fft(signal)
    start = perf_counter()
    fft(signal)
    end = perf_counter()
    return end - start


def load_signal(filename):
    signal = []
    with open(filename, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file, delimiter=";")

        for row in reader:
            if not row:
                continue
            try:
                signal.append(int(row[-1]))
            except ValueError:
                continue

    if not signal:
        raise ValueError("Файл не містить числових даних")

    return signal

def main():
    filename = "signal_11.csv"
    signal = load_signal(filename)

    n = len(signal)
    print("Розмірність N = ", n)
    if n & (n - 1):
        raise ValueError(
            "Кількість відліків у файлі має бути степенем двійки"
        )

    fft_values = fft(signal)
    _, total_multiplications, total_additions = fft(
        signal,
        count_operations=True
    )

    # Вимірювання часу виконання
    time = measure_time(signal)

    print("\nПоказники обчислення:")
    print(f"Час обчислення: {time:.8f} с")
    print("Кількість комплексних множень:", total_multiplications)
    print("Кількість комплексних додавань:", total_additions)

if __name__ == "__main__":
    main()
