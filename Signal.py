import random
import csv

N = 2 ** 11
random.seed(42)

signal = [random.randint(-10, 10) for _ in range(N)]

with open("signal_11.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Відлік", "Значення"])

    for i, value in enumerate(signal):
        writer.writerow([i, value])
