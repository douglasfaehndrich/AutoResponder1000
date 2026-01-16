from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import QDate, QTime

class ShiftDialog(QWidget):
    def __init__(self, parent=None, shift_num=1):
        super().__init__(parent)
        self.setWindowTitle(f"Enter Shift {shift_num}")
        self.setGeometry(200, 200, 300, 220)
        self.shift_data = {}
        layout = QVBoxLayout()

        # Date selector
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        # Time selectors using QTimeEdit (spinbox style)
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("hh:mm AP")
        self.start_time_edit.setTime(QTime.currentTime())

        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("hh:mm AP")
        self.end_time_edit.setTime(QTime.currentTime())

        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(QLabel("Start Time:"))
        layout.addWidget(self.start_time_edit)
        layout.addWidget(QLabel("End Time:"))
        layout.addWidget(self.end_time_edit)

        btn_layout = QHBoxLayout()
        self.another_btn = QPushButton("Add Another Shift")
        self.done_btn = QPushButton("Done")
        btn_layout.addWidget(self.another_btn)
        btn_layout.addWidget(self.done_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
