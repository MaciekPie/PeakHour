import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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


# Próby GUI
class TrafficAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analiza Ruchu Telekomunikacyjnego")
        self.setGeometry(100, 100, 800, 600)

        self.time_file = (
            "C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/time.txt"
        )
        self.intensity_file = (
            "C:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/intensity.txt"
        )

        self.time = load_time_data(self.time_file)
        self.day_time, self.intense = load_intensity_data(self.intensity_file)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)  # Ustawienie centralnego widgetu

        self.init_main_page()
        self.init_analysis_page()
        self.init_education_page()

    def init_main_page(self):
        self.main_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Projekt Analizy Ruchu Telekomunikacyjnego")
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("font-weight: bold;")
        layout.addWidget(label)

        btn_analysis = QPushButton("Działanie")
        btn_analysis.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.analysis_page)
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
        self.analysis_page = QWidget()
        layout = QVBoxLayout()

        self.result_label = QLabel("Kliknij przycisk, aby obliczyć ADPQH")
        layout.addWidget(self.result_label)

        self.calc_button = QPushButton("Oblicz ADPQH")
        self.calc_button.clicked.connect(self.calculate_adpqh)
        layout.addWidget(self.calc_button)

        self.plot_button = QPushButton("Pokaż wykres")
        self.plot_button.clicked.connect(self.show_plot)
        layout.addWidget(self.plot_button)

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

    def init_education_page(self):
        self.education_page = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Teoria i wzory dotyczące analizy ruchu")
        layout.addWidget(label)

        back_button = QPushButton("Wróć")
        back_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.main_page)
        )
        layout.addWidget(back_button)

        self.education_page.setLayout(layout)
        self.stacked_widget.addWidget(self.education_page)

    def calculate_adpqh(self):
        """Oblicza ADPQH i wyświetla wynik."""
        avg_time = sum(self.time) / len(self.time)
        quarter_intensity = np.zeros(96)

        for minute, intensity in zip(self.day_time, self.intense):
            m = minute // 15
            quarter_intensity[m] += intensity

        quarter_avg = quarter_intensity / 15
        peak_q = np.argmax(quarter_avg)
        peak_q_start = peak_q * 15
        peak_q_end = peak_q_start + 15
        self.result_label.setText(
            f"Średni czas trwania: {avg_time:.2f} s\n"
            f"Największy ruch: {peak_q_start//60:02d}:{peak_q_start%60:02d} - {peak_q_end//60:02d}:{peak_q_end%60:02d}"
        )

    def show_plot(self):
        """Tworzy wykres intensywności ruchu."""
        self.ax.clear()
        self.ax.plot(self.day_time, self.intense, "b")
        self.ax.set_xlabel("Czas w ciągu doby [min]")
        self.ax.set_ylabel("Ilość połączeń")
        self.ax.set_title("Intensywność ruchu")
        self.ax.grid()
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
