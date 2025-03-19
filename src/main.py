import matplotlib.pyplot as plt

file=open("../data/time.txt")
file2=open("../data/intensity.txt")
intense=[]
time=[]
dayTime=[]
for i in file:
    line=i.strip()
    line=int(line)
    time.append(line)
suma=sum(time)
avgTime=suma/len(time)
print(avgTime)

for k in file2:
    lineIntensity = k.strip()
    parts = lineIntensity.split('\t')  # Rozdzielenie danych
    if len(parts) == 2:
        dayTime.append(int(parts[0]))
        intense.append(float(parts[1].replace(',', '.')))
plt.plot(dayTime,intense)
plt.xlabel("czas w ciągu doby [s]")
plt.ylabel("ilość połączeń w danej sekundzie")
plt.grid()
plt.show()