from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton

class RateApprovalSection(QGroupBox):
    def __init__(self, parent, copy_callback):
        super().__init__("Rate Approval")
        self.rate_input = QLineEdit()
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Rate:"))
        layout.addWidget(self.rate_input)
        btn = QPushButton("Copy 'Rate Approval' Response")
        btn.clicked.connect(lambda: copy_callback(self.rate_input))
        layout.addWidget(btn)
        self.setLayout(layout)
        self.copy_btn = btn
