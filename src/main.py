import matplotlib.pyplot as plt
import numpy as np


time_file = open(
    #"C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/time.txt"
 "../data/time.txt")
intensity_file = open(
    #"C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/intensity.txt"
  "../data/intensity.txt")

intense = []
time = []
dayTime = []

for i in time_file:
    line = i.strip()
    line = int(line)
    time.append(line)

suma = sum(time)
avgTime = suma / len(time)
print(avgTime)

for k in intensity_file:
    lineIntensity = k.strip()
    parts = lineIntensity.split("\t")  # Rozdzielenie danych

    if len(parts) == 2:
        dayTime.append(int(parts[0]))
        intense.append(float(parts[1].replace(",", ".")))


hourly_intensity = np.zeros(24)

for hour, intensity in zip(dayTime, intense):
    h = hour // 60
    hourly_intensity[h] += intensity

hourly_avg = hourly_intensity / 60

peak_h= np.argmax(hourly_avg)
peak_h_start = peak_h * 60
peak_h_end = peak_h_start + 60

print(f"Godzina największego ruchu występuje między (ADPQH): {peak_h_start/60}-{peak_h_end/60} h")

plt.plot(dayTime, intense, 'o-')

plt.xlabel("Czas w ciągu doby [min]")
plt.ylabel("Ilość połączeń w danej minucie")

plt.grid()
plt.show()
