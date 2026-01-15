from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton

class PinConfirmationSection(QGroupBox):
    def __init__(self, parent, copy_callback):
        super().__init__("Send Work Order")
        self.pin_input = QLineEdit()
        layout = QHBoxLayout()
        layout.addWidget(QLabel("PIN:"))
        layout.addWidget(self.pin_input)
        btn = QPushButton("Copy 'Send Work Order' Response")
        btn.clicked.connect(lambda: copy_callback(self.pin_input))
        layout.addWidget(btn)
        self.setLayout(layout)
        self.copy_btn = btn
