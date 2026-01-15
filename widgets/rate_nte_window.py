from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit

class RateNTEWindow(QWidget):
    def __init__(self, parent, signature_func, rate_init, nte_init):
        super().__init__()
        self.setWindowTitle("Rate/NTE Response")
        self.setGeometry(200, 200, 500, 300)
        self.signature_func = signature_func
        self.shifts = []
        layout = QVBoxLayout()
        self.rate_edit = QLineEdit()
        self.nte_edit = QLineEdit()
        self.rate_edit.setText(rate_init)
        self.nte_edit.setText(nte_init)
        layout.addWidget(QLabel("Hourly Rate:"))
        layout.addWidget(self.rate_edit)
        layout.addWidget(QLabel("NTE:"))
        layout.addWidget(self.nte_edit)
        self.add_shift_btn = QPushButton("Add Shift(s)")
        layout.addWidget(self.add_shift_btn)
        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        layout.addWidget(self.output_edit)
        self.copy_btn = QPushButton("Copy Response")
        layout.addWidget(self.copy_btn)
        self.setLayout(layout)
