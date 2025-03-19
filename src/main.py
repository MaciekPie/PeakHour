import matplotlib.pyplot as plt


time_file = open(
    "C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/time.txt"
)  # "../data/time.txt"
intensity_file = open(
    "C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/intensity.txt"
)  # "../data/intensity.txt"

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

plt.plot(dayTime, intense)

plt.xlabel("Czas w ciągu doby [s]")
plt.ylabel("Ilość połączeń w danej sekundzie")

plt.grid()

plt.show()

print("Elo")
