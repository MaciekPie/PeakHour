import sys
import numpy as np
from PyQt6.QtCore import Qt
from pathlib import Path
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QSpacerItem,
    QTextEdit,
    QFileDialog,
)
from PyQt6.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


time_file = "Projekty/Github/PeakHour/data/time.txt"  # "../data/time.txt"


intensity_file = (
    "Projekty/Github/PeakHour/data/intensity.txt"  # "../data/intensity.txt"
)


# TODO domnożyć sobie tabelkę żeby parę dni (6-10)
# TODO wiele (2){im więcej tym lepiej} metod i pokazac różnice między nimi
# TODO dodać slider w gui oraz opcję wyświetlania wykresów z wielu danych
# TODO i cyk do execa

# implementacja jednej metody sugerowanie tcbh
# plus uśredniony wykres ze wszystkiego na koniec
# podświetlenie tego gnr
# wartość uśredniona w tej godzinie


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


def intensity_grouped(filepath):
    combined_intensity = {}
    with open(filepath, "r") as file:

        for line in file:
            parts = line.strip().split("\t")

            if len(parts) == 2:
                temp_time = int(parts[0])
                temp_intese = float(parts[1].replace(",", "."))
                combined_intensity[temp_time] = temp_intese
    return combined_intensity


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


# TODO zrobić dynamiczne wybieranie plików do analizy
# Próby GUI
class TrafficAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analiza Ruchu Telekomunikacyjnego")
        self.setGeometry(100, 100, 800, 600)

        self.time_file = "Projekty/Github/PeakHour/data/time.txt"  # "../data/time.txt"

        self.intensity_file = (
            "Projekty/Github/PeakHour/data/intensity.txt"  # "../data/intensity.txt"
        )

        self.peak_start = None
        self.peak_end = None

        self.connection_time = load_time_data(self.time_file)
        self.day_time, self.intense = load_intensity_data(self.intensity_file)
        self.grouped_intensity = intensity_grouped(self.intensity_file)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)  # Ustawienie centralnego widgetu

        self.init_main_page()
        self.init_analysis_page()
        self.init_education_page()

    def init_main_page(self):
        self.main_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Projekt Analizy Ruchu Telekomunikacyjnego")
        label.setFont(QFont("Arial", 15))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-weight: bold;")
        layout.addWidget(label)

        btn_analysis = QPushButton("Działanie")
        btn_analysis.clicked.connect(
            lambda: {
                self.stacked_widget.setCurrentWidget(self.analysis_page),
                self.open_file_dialog(),
            }
        )
        layout.addWidget(btn_analysis)

        btn_education = QPushButton("Edukacja")
        btn_education.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.education_page)
        )
        layout.addWidget(btn_education)

        self.main_page.setLayout(layout)
        self.stacked_widget.addWidget(self.main_page)

    def init_analysis_page(self):
        # todo dorobic równoległe wykresy dla innych dni i metod

        self.analysis_page = QWidget()
        layout = QVBoxLayout()

        self.result_label = QLabel("Kliknij przycisk, aby obliczyć ADPQH")
        layout.addWidget(self.result_label)

        self.calc_active = False

        self.calc_button = QPushButton("Oblicz ADPQH")
        self.calc_button.clicked.connect(self.toggle_calculation_and_plot)
        layout.addWidget(self.calc_button)

        self.canvas = FigureCanvas(plt.figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)
        self.canvas.setVisible(False)

        back_button = QPushButton("Wróć")
        back_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.main_page)
        )
        layout.addWidget(back_button)

        self.analysis_page.setLayout(layout)
        self.stacked_widget.addWidget(self.analysis_page)

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(
            r"C:\Users\Lenovo\PycharmProjects\TeoriaRuchuAleDziała\PeakHour\data"
        )
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Text (*.txt)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.file_list.addItems([str(Path(filename)) for filename in filenames])

    def open_file_dialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik",
            "C:\\Users\\Lenovo\\PycharmProjects\\TeoriaRuchuAleDziała\\PeakHour\\data",
            "Text File (*.txt)",
        )
        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))

    def init_education_page(self):

        self.education_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Teoria i wzory dotyczące analizy ruchu")
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        label.setFont(QFont("Arial", 17))
        layout.addWidget(label)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setHtml(
            """
            <h3>📌 Godzina Największego Ruchu (GNR)</h3>
            <p>
            Godzina Największego Ruchu to okres <b>kolejnych 60 minut</b> w ciągu doby, w którym <b>średnie natężenie połączeń</b> jest największe.
            </p>
            <p>Oznaczenie matematyczne:</p>
            <pre>
GNR = argmax<sub>t∈[0,1380]</sub> ∑<sub>i=0</sub><sup>59</sup> A(t + i)
            </pre>
            
            <h3>📌 Erlang</h3>
            <p>
            Jednostka średniego natężenia ruchu telekomunikacyjnego. Nazwa wywodzi się od nazwiska Agnera Krarupa Erlanga, autora teorii masowej obsługi, która stanowi uogólnienie zjawisk zaobserwowanych w telekomunikacji.
            Dla danego systemu telekomunikacyjnego składającego się z 1 linii i czasu obserwacji równego 1 godzinie, jeśli linia ta zajęta jest cały czas przez pełną godzinę, to natężenie ruchu wynosi 1 erlang; odpowiednio, jeśli linia ta zajęta jest przez 30 minut, natężenie to wynosi 0,5 erlanga. 
            </p>

            <h3>📌 ADPQH – Average Daily Peak Quarter-Hour</h3>
            <p>
            Metoda polega na zsumowaniu połączeń w <b>każdym 15-minutowym interwale</b> i znalezieniu tego o najwyższej wartości.
            </p>
            <pre>
ADPQH = argmax<sub>q∈[0,95]</sub> (1/15) * ∑<sub>i=0</sub><sup>14</sup> A(15q + i)
            </pre>

            <h3>📌 FDMP – Fixed Duration Max Peak</h3>
            <p>
            FDMP to metoda podobna do GNR, ale analizująca <b>dowolny ustalony interwał</b> (np. 30 minut).
            </p>
            <pre>
FDMP = argmax<sub>t</sub> ∑<sub>i=0</sub><sup>D-1</sup> A(t + i)
            gdzie D = długość okna (np. 30 min)
            </pre>
             
             <h3>📌 TCBH - Time-Consistent Busy Hour</h3>
             <p>
             Metoda polegająca na ustaleniu, <b> na podstawie danych z wielu dni </b>, kiedy średnia ilość połączeń jest największa. 
             </p>
            """
        )
        layout.addWidget(text)

        back_button = QPushButton("Wróć")
        back_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.main_page)
        )
        layout.addWidget(back_button)

        self.education_page.setLayout(layout)
        self.stacked_widget.addWidget(self.education_page)

    def toggle_calculation_and_plot(self):
        if self.calc_active:
            # Cofnij obliczenia i schowaj wykres
            self.result_label.setText("Kliknij przycisk, aby obliczyć ADPQH")
            self.peak_start = None
            self.peak_end = None
            self.canvas.setVisible(False)
        else:
            # Oblicz i pokaż wykres
            self.calculate_adpqh()
            self.show_plot()
            self.canvas.setVisible(True)

        self.calc_active = not self.calc_active

    def calculate_adpqh(self):
        """Oblicza ADPQH i wyświetla wynik."""
        """
        #ecie pecie: próby poprawy algorytmu do adpqh
        
        quarter_intensity = np.zeros(96)

        for minute, intensity in zip(self.day_time, self.intense):
            m = minute // 15
            quarter_intensity[m] += intensity

        quarter_avg = quarter_intensity / 15
        peak_q = np.argmax(quarter_avg)
        peak_q_start = peak_q * 15
        peak_q_end = peak_q_start + 15            
        """

        avg_time = sum(self.connection_time) / len(self.connection_time)

        peak_start = 0
        interval = 60
        biggest = 0
        for counter in range(1, 1380):
            sum_intense = 0
            for h in range(counter, counter + interval):
                if h in self.grouped_intensity:
                    sum_intense += self.grouped_intensity.get(h)
            if sum_intense > biggest:
                biggest = sum_intense
                peak_start = counter
        peak_end = peak_start + interval
        self.result_label.setText(
            f"Średni czas trwania: {avg_time:.2f} s\n"
            f"Największy ruch: {peak_start//60:02d}:{peak_start%60:02d} - {peak_end//60:02d}:{peak_end%60:02d}"
        )

        self.peak_start = peak_start
        self.peak_end = peak_end

    """
    # TODO zrobić żeby pokazywało ilość erlandów na wykresie
    # poniżej jest wzór z wikipedi angielskiej od razu w pythonie

    def erlang_b(E, m: int) -> float:
        //Calculate the probability of call losses.
        inv_b = 1.0
        for j in range(1, m + 1):
            inv_b = 1.0 + inv_b * j / E
        return 1.0 / inv_b
    """

    def show_plot(self):
        """Tworzy wykres intensywności ruchu."""
        self.ax.clear()
        self.ax.plot(self.day_time, self.intense, "b")

        if self.peak_start is not None and self.peak_end is not None:
            self.ax.axvline(
                x=self.peak_start, color="red", linestyle="--", label="Początek GNR"
            )
            self.ax.axvline(
                x=self.peak_end, color="red", linestyle="--", label="Koniec GNR"
            )
            self.ax.legend()

        self.ax.set_xlabel("Czas w ciągu doby [min]")
        self.ax.set_ylabel("Ilość połączeń")
        self.ax.set_title("Intensywność ruchu")
        # TODO zmienić odstępy w siatce na 60 zamiast obecnych 200 dla większej czytelności
        self.ax.grid(True, which="major", linestyle="-", linewidth=0.75)
        self.canvas.draw()
        self.canvas.setVisible(True)


"""
time = load_time_data(time_file)
day_time, intense = load_intensity_data(intensity_file)


avg_time = sum(time) / len(time)
print(f"Średni czas trwania połączenia: {avg_time:.2f} s")


# Obliczenia metodą ADPQH i FDMH
calculate_adpqh(day_time, intense)


# Wykres intensywności
plot_intensity(day_time, intense)
"""


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

# Uruchomienie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrafficAnalysisApp()
    window.show()
    sys.exit(app.exec())
