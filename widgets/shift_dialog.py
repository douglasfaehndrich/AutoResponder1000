from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDateEdit, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtCore import QDate, QTime

class ShiftDialog(QWidget):
    def __init__(self, parent=None, shift_num=1):
        super().__init__(parent)
        self.setWindowTitle(f"Enter Shift {shift_num}")
        self.setGeometry(200, 200, 300, 220)
        self.shift_data = {}
        layout = QVBoxLayout()
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.start_time_combo = QComboBox()
        self.end_time_combo = QComboBox()
        time_options = []
        for h in range(24):
            for m in (0, 30):
                t = QTime(h, m)
                time_options.append(t.toString('hh:mm AP'))
        self.start_time_combo.addItems(time_options)
        self.end_time_combo.addItems(time_options)
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(QLabel("Start Time:"))
        layout.addWidget(self.start_time_combo)
        layout.addWidget(QLabel("End Time:"))
        layout.addWidget(self.end_time_combo)
        btn_layout = QHBoxLayout()
        self.another_btn = QPushButton("Add Another Shift")
        self.done_btn = QPushButton("Done")
        btn_layout.addWidget(self.another_btn)
        btn_layout.addWidget(self.done_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
