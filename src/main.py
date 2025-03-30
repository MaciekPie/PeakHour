import matplotlib.pyplot as plt
import numpy as np


time_file = "C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/time.txt"
# "../data/time.txt"

intensity_file = (
    "C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/intensity.txt"
)
# "../data/intensity.txt"


# domnożyć sobie tabelkę żeby parę dni (6-10)
# wiele (2){im więcej tym lepiej} metod i pokazac różnice między nimi


def load_time_data(filepath):
    """Wczytuje dane o czasie trwania połączeń"""
    with open(filepath, "r") as file:
        time_data = [int(line.strip()) for line in file]
    return time_data


def load_intensity_data(filepath):
    """Wczytuje dane o intensywności ruchu"""
    day_time = []
    intense = []

    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split("\t")

            if len(parts) == 2:
                day_time.append(int(parts[0]))
                intense.append(float(parts[1].replace(",", ".")))

    return day_time, intense


def calculate_adpqh(day_time, intense):
    """Metoda ADPQH - kwadrans o największym ruchu"""
    quarter_intensity = np.zeros(96)  # 96 kwadransów w dobie

    for minute, intensity in zip(day_time, intense):
        m = minute // 15  # Grupa 15-minutowa
        quarter_intensity[m] += intensity

    quarter_avg = quarter_intensity / 15
    peak_q = np.argmax(quarter_avg)
    peak_q_start = peak_q * 15
    peak_q_end = peak_q_start + 15

    print(
        f"Kwadrans największego ruchu występuje między (ADPQH): {peak_q_start // 60:02d}:{peak_q_start % 60:02d} - "
        f"{peak_q_end // 60:02d}:{peak_q_end % 60:02d}"
    )


def plot_intensity(day_time, intense):
    """Tworzy wykres intensywności ruchu"""
    plt.figure(figsize=(10, 5))
    plt.plot(day_time, intense, "b", label="Intensywność ruchu")
    plt.xlabel("Czas w ciągu doby [min]")
    plt.ylabel("Ilość połączeń")
    plt.title("Intensywność ruchu w ciągu doby")
    plt.grid()
    plt.legend()
    plt.show()


time = load_time_data(time_file)
day_time, intense = load_intensity_data(intensity_file)


avg_time = sum(time) / len(time)
print(f"Średni czas trwania połączenia: {avg_time:.2f} s")


# Obliczenia metodą ADPQH i FDMH
calculate_adpqh(day_time, intense)


# Wykres intensywności
plot_intensity(day_time, intense)


"""
quarter_intensity = np.zeros(96)

for minute, intensity in zip(day_time, intense):
    m = minute // 15
    quarter_intensity[m] += intensity


quarter_avg = quarter_intensity / 15

peak_q = np.argmax(quarter_avg)
peak_q_start = peak_q * 15
peak_q_end = peak_q_start + 15

#print(f"Kwadrans największego ruchu występuje między (ADPQH): {peak_q_start/60}-{peak_q_end/60} h")
"""


"""
plt.plot(day_time, intense, "b")
plt.plot(day_time, intense)

plt.xlabel("Czas w ciągu doby [min]")
plt.ylabel("Ilość połączeń w danej minucie")

plt.grid()
plt.show()
"""
