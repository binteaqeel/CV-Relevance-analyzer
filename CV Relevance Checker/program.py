from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class CircularProgress(QWidget):
    def __init__(self, end_value, label, color):
        super().__init__()
        self.current_value = 0
        self.end_value = end_value
        self.label = label
        self.color = color
        self.setFixedSize(180, 180)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(20)

    def update_value(self):
        if self.current_value < self.end_value:
            self.current_value += 1
            self.update()
        else:
            self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        pen = QPen(QColor(230, 230, 230), 14)
        painter.setPen(pen)
        painter.drawEllipse(rect.adjusted(7, 7, -7, -7))

        pen.setColor(QColor(self.color))
        painter.setPen(pen)
        angle_span = int(self.current_value * 3.6 * 16)
        painter.drawArc(rect.adjusted(7, 7, -7, -7), -90 * 16, -angle_span)

        painter.setPen(QColor("black"))
        font = QFont("Arial", 12, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{self.current_value}%\n{self.label}")

class Spinner(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)
        self.setFixedSize(100, 100)

    def rotate(self):
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        for i in range(12):
            color = QColor(100, 100, 100)
            color.setAlphaF(i / 12.0)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(30, -5, 10, 10)
            painter.rotate(30)

class ResumeAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Job Relevance Analyzer")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f4f4f4;")
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()

        title = QLabel("Resume to Job Description Relevance Checker")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #333;")
        self.mainLayout.addWidget(title)

        uploadBtn = QPushButton("Upload CV (PDF)")
        uploadBtn.setStyleSheet("padding: 10px; font-size: 16px; background-color: #4CAF50; color: white; border-radius: 10px;")
        uploadBtn.clicked.connect(self.uploadFile)
        self.mainLayout.addWidget(uploadBtn, alignment=Qt.AlignCenter)

        self.jobDescInput = QTextEdit()
        self.jobDescInput.setPlaceholderText("Paste Job Description Here...")
        self.jobDescInput.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 10px;")
        self.mainLayout.addWidget(self.jobDescInput)

        analyzeBtn = QPushButton("Analyze")
        analyzeBtn.setStyleSheet("padding: 10px; font-size: 16px; background-color: #2196F3; color: white; border-radius: 10px;")
        analyzeBtn.clicked.connect(self.showSpinner)
        self.mainLayout.addWidget(analyzeBtn, alignment=Qt.AlignCenter)

        self.resultLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.resultLayout)

        self.setLayout(self.mainLayout)

    def uploadFile(self):
        QFileDialog.getOpenFileName(self, "Open CV File", "", "PDF Files (*.pdf)")

    def showSpinner(self):
        self.clearResults()
        self.spinner = Spinner()
        self.resultLayout.addWidget(self.spinner, alignment=Qt.AlignCenter)
        QTimer.singleShot(10000, self.showResults)  # 10-second delay

    def showResults(self):
        self.clearResults()
        progressLayout = QHBoxLayout()
        progressLayout.addWidget(CircularProgress(60, "ATS\nFriendly", "#FFC107"))
        progressLayout.addWidget(CircularProgress(76, "Requirements\nMatch", "#4CAF50"))
        progressLayout.addWidget(CircularProgress(30, "Soft Skill\nMatch", "#F44336"))
        progressLayout.addWidget(CircularProgress(79, "Tech Skills\nMatch", "#00BCD4"))
        self.resultLayout.addLayout(progressLayout)

        finalScore = QLabel("\n\n\n\nOverall Relevance Score: <b>61.25%</b>")
        finalScore.setFont(QFont("Segoe UI", 14))
        finalScore.setAlignment(Qt.AlignCenter)
        finalScore.setStyleSheet("color: #333;")
        self.mainLayout.addWidget(finalScore)

    def clearResults(self):
        while self.resultLayout.count():
            child = self.resultLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResumeAnalyzer()
    window.show()
    sys.exit(app.exec_())
