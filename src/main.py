import matplotlib.pyplot as plt
import numpy as np


time_file = open(
    "C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/time.txt"
    # "../data/time.txt"
)

intensity_file = open(
    "C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/intensity.txt"
    # "../data/intensity.txt"
)

# domnożyć sobie tabelkę żeby parę dni (6-10)
# wiele (2){im więcej tym lepiej} metod i pokazac różnice między nimi


intense = []
time = []
dayTime = []


for k in intensity_file:
    lineIntensity = k.strip()
    parts = lineIntensity.split("\t")  # Rozdzielenie danych

    if len(parts) == 2:
        dayTime.append(int(parts[0]))
        intense.append(float(parts[1].replace(",", ".")))


quarter_intensity = np.zeros(96)

for minute, intensity in zip(dayTime, intense):
    m = minute // 15
    quarter_intensity[m] += intensity

quarter_avg = quarter_intensity / 15

peak_q = np.argmax(quarter_avg)
peak_q_start = peak_q * 15
peak_q_end = peak_q_start + 15

print(
    f"Kwadrans największego ruchu występuje między (ADPQH): {peak_q_start/60}-{peak_q_end/60} h"
)

plt.plot(dayTime, intense, "b")

plt.xlabel("Czas w ciągu doby [min]")
plt.ylabel("Ilość połączeń w danej minucie")

plt.grid()
plt.show()
