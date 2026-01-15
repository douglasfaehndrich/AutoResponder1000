from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QDateEdit, QPushButton
from PyQt5.QtCore import QDate

class WBReportSection(QGroupBox):
    def __init__(self, parent, create_callback):
        super().__init__("WB Report")
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)
        btn = QPushButton("Create WB Report Email")
        btn.clicked.connect(lambda: create_callback())  # Remove self.date_edit argument
        layout.addWidget(btn)
        self.setLayout(layout)
        self.create_btn = btn
