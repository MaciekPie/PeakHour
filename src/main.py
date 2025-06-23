import sys
from PyQt6.QtCore import Qt
from pathlib import Path
from matplotlib.figure import Figure
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QTextEdit,
    QFileDialog,
    QFrame,
    QScrollArea,
    QSizePolicy,
)
from PyQt6.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


time_file = (
    # "c:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/time.txt"
    "../data/time.txt"
    "c:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/time.txt"
    # "../data/time.txt"
    ""
)


intensity_file = (
    # "c:/Users/macie/Programowanie/Projekty/Github/PeakHour/data/intense.txt"
    "../data/intensity.txt"
)

# todo wartości natężenia ruchu w tej godzinie
# todo deadline: 25.06.2025 !!!!
# TODO wiele (2){im więcej tym lepiej} metod i pokazac różnice między nimi
# TODO dodać slider w gui oraz opcję wyświetlania wykresów z wielu danych
# TODO i cyk do execa

# implementacja jednej metody sugerowanie tcbh
# plus uśredniony wykres ze wszystkiego na koniec
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


# Próby GUI
class TrafficAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analiza Ruchu Telekomunikacyjnego")
        self.setGeometry(300, 40, 1000, 750)

        self.intensity_files = []

        self.all_day_time = []
        self.all_intense = []
        self.all_peak_ranges = []

        self.peak_start = None
        self.peak_end = None

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
            lambda: {self.stacked_widget.setCurrentWidget(self.analysis_page)}
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

        self.result_label = QLabel("Kliknij przycisk, aby wybrać metodę obliczania GNR")
        layout.addWidget(self.result_label)

        self.calc_active = False

        self.figure = Figure(figsize=(9, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(900, 400)  # stały rozmiar głównego wykresu
        self.canvas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ax = self.figure.add_subplot(111)

        # Otocz canvas ramką (opcjonalne)
        self.canvas_frame = QFrame()
        canvas_layout = QVBoxLayout()
        canvas_layout.addWidget(self.canvas)
        self.canvas_frame.setLayout(canvas_layout)

        self.canvas.setVisible(False)

        # === Osobne wykresy pod spodem ===
        self.daily_charts_layout = QVBoxLayout()
        self.daily_charts_widget = QWidget()
        self.daily_charts_widget.setLayout(self.daily_charts_layout)

        # ——— QScrollArea OBJĘTA CAŁOŚCIĄ WYKRESÓW ———
        self.scroll_area = QScrollArea()
        scroll_contents = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(self.canvas_frame)
        scroll_layout.addWidget(self.daily_charts_widget)
        scroll_contents.setLayout(scroll_layout)

        self.scroll_area.setWidget(scroll_contents)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVisible(False)

        layout.addWidget(self.scroll_area)

        # === Przyciski ===
        self.calc_button = QPushButton("Oblicz ADPQH")
        self.calc_button.clicked.connect(self.toggle_calculation_and_plot)
        layout.addWidget(self.calc_button)

        back_button = QPushButton("Wróć")
        back_button.clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.main_page)
        )
        layout.addWidget(back_button)

        self.analysis_page.setLayout(layout)
        self.stacked_widget.addWidget(self.analysis_page)

    def open_file_dialog(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Wybierz pliki z intensywnością",
            "..\\data",
            "Text File (*.txt)",
        )
        if filenames:
            self.intensity_files = [Path(fname) for fname in filenames]

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
             
             <h3>📌 TCBH - Time-Consistent Busy Hour</h3>
             <p>
             Metoda polegająca na ustaleniu, <b> na podstawie danych z wielu dni </b>, kiedy średnia ilość połączeń jest największa. 
             </p>
             
             <h3>📌 Linki do dokumentów standaryzacyjnych</h3>
             <p>
             Definicje metod licznia GNR:         <b> https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-E.500-198811-S!!PDF-E&type=items </b>
             </p>
             
             <p>
             Definicje pojęć telekomunikacyjnych:   <b> https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-E.600-198811-S!!PDF-E&type=items </b>
             </p>
             
             <h3>📌 Linki do dokumentów organizacji standaryzujących </h3>
             <p>
             https://www.etsi.org/deliver/etsi_tr/145900_145999/145926/18.00.00_60/tr_145926v180000p.pdf
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

            # DODANE
            for attr in ["all_day_time", "all_intense", "all_peak_ranges"]:
                if hasattr(self, attr):
                    getattr(self, attr).clear()

            self.scroll_area.setVisible(False)

            # Usunięcie zawartości layoutu z wykresami dziennymi
            while self.daily_charts_layout.count():
                child = self.daily_charts_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        else:
            # Oblicz i pokaż wykres
            self.calculate_adpqh()
            self.show_plot()
            self.scroll_area.setVisible(True)

        self.calc_active = not self.calc_active

    def calculate_adpqh(self):
        """Oblicza ADPQH i wyświetla wynik."""
        self.time_file = time_file
        self.open_file_dialog()

        if self.intensity_files == [] or self.time_file == []:
            self.result_label.setText("Nie wybrano żadnych plików.")
            return  # zakończ jeśli nie ma plików

        self.all_day_time = []
        self.all_intense = []
        self.all_peak_ranges = []

        try:
            self.connection_time = load_time_data(self.time_file)
        except Exception as e:
            self.result_label.setText(f"Błąd przy wczytywaniu pliku z czasami: {e}")
            return

        if not self.connection_time:
            self.result_label.setText(
                "Plik z czasami połączeń jest pusty lub nieprawidłowy."
            )
            return

        avg_time = sum(self.connection_time) / len(self.connection_time)
        summary_text = f"Średni czas trwania połączenia: {avg_time:.2f} s\n\n"

        total_peak_start = 0
        total_peak_end = 0

        for i, path in enumerate(self.intensity_files):
            try:
                day_time, intense = load_intensity_data(path)
                grouped = intensity_grouped(path)
            except Exception as e:
                summary_text += f"Dzień {i+1}: Błąd wczytywania danych ({e})\n"
                continue  # pomiń ten plik

            peak_start = 0
            interval = 60
            biggest = 0
            for counter in range(1, 1380):
                sum_intense = sum(
                    grouped.get(h, 0) for h in range(counter, counter + interval)
                )
                if sum_intense > biggest:
                    biggest = sum_intense
                    peak_start = counter
            peak_end = peak_start + interval

            total_peak_start += peak_start
            total_peak_end += peak_end

            self.all_day_time.append(day_time)
            self.all_intense.append(intense)
            self.all_peak_ranges.append((peak_start, peak_end))

            summary_text += (
                f"Dzień {i+1}: największy ruch od "
                f"{peak_start // 60:02d}:{peak_start % 60:02d} "
                f"do {peak_end // 60:02d}:{peak_end % 60:02d} "
                f"Wartość natężenia ruchu w GNR: {biggest/60} Erl \n"
            )

        num_files = len(self.intensity_files)
        if num_files > 0:
            avg_peak_start = total_peak_start // num_files
            avg_peak_end = total_peak_end // num_files
            summary_text += (
                f"\nUśredniona GNR: {avg_peak_start // 60:02d}:{avg_peak_start % 60:02d} - "
                f"{avg_peak_end // 60:02d}:{avg_peak_end % 60:02d}"
            )

        self.result_label.setText(summary_text)
        # self.show_plot()

    def calculate_tcbh(self):
        self.open_file_dialog()
        self.connection_time = load_time_data(self.time_file)

        self.all_day_time = []
        self.all_intense = []
        self.all_peak_ranges = []
        temp_group = {}
        n = 0
        for path in self.intensity_files:
            if n == 0:
                day_time, intense = load_intensity_data(path)
                grouped = intensity_grouped(path)
                n += 1
            else:
                temp_group = intensity_grouped(path)
                for i in temp_group:
                    grouped[i] = grouped[i] + temp_group[i]
        peak_start = 0
        interval = 60
        biggest = 0
        for counter in range(1, 1380):
            grouped = grouped / len(self.intensity_files)
            sum_intense = sum(
                grouped.get(h, 0) for h in range(counter, counter + interval)
            )
            if sum_intense > biggest:
                biggest = sum_intense
                peak_start = counter
        peak_end = peak_start + interval

        self.all_peak_ranges.append((peak_start, peak_end))

    def show_plot(self):
        """Tworzy wykres zbiorczy oraz osobne wykresy dla każdego dnia."""
        if not hasattr(self, "all_day_time") or not self.all_day_time:
            self.result_label.setText(
                "Brak danych do wyświetlenia wykresu. Najpierw oblicz ADPQH."
            )
            return

        self.ax.clear()

        # Wykres zbiorczy
        for i in range(len(self.all_day_time)):
            day_time = self.all_day_time[i]
            intense = self.all_intense[i]
            peak_start, peak_end = self.all_peak_ranges[i]

            (line,) = self.ax.plot(day_time, intense, label=f"Dzień {i+1}", alpha=0.62)
            colour = line.get_color()
            self.ax.axvline(x=peak_start, linestyle="--", color=colour)
            self.ax.axvline(x=peak_end, linestyle="--", color=colour)

        self.ax.set_xlabel("Czas w ciągu doby [min]")
        self.ax.set_ylabel("Ilość połączeń")
        self.ax.set_title("Intensywność ruchu - wiele dni")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()
        self.canvas.setVisible(True)

        # === Osobne wykresy ===
        # Czyść poprzednie wykresy
        while self.daily_charts_layout.count():
            child = self.daily_charts_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Dodaj nowe osobne wykresy
        for i in range(len(self.all_day_time)):
            fig = Figure(figsize=(9, 4))
            ax = fig.add_subplot(111)
            canvas = FigureCanvas(fig)
            canvas.setFixedSize(900, 400)  # stały rozmiar każdego mniejszego wykresu
            canvas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            day_time = self.all_day_time[i]
            intense = self.all_intense[i]
            peak_start, peak_end = self.all_peak_ranges[i]

            ax.plot(day_time, intense, label=f"Dzień {i+1}")
            ax.axvline(x=peak_start, linestyle="--", color="red", label="Początek GNR")
            ax.axvline(x=peak_end, linestyle="--", color="red", label="Koniec GNR")
            ax.set_title(f"Dzień {i+1}")
            ax.set_xlabel("Minuty")
            ax.set_ylabel("Intensywność")
            ax.grid(True)
            ax.legend()

            self.daily_charts_layout.addWidget(canvas)


# Uruchomienie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrafficAnalysisApp()
    window.showMaximized()
    sys.exit(app.exec())
