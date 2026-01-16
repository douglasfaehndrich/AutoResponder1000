from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt, QDateTime
import pyperclip
from widgets.shift_dialog import ShiftDialog

class RateNTEWindow(QWidget):
    def __init__(self, parent, signature_func, rate_init, nte_init):
        super().__init__()
        self.setWindowTitle("Service Channel")
        self.setGeometry(200, 200, 500, 300)
        self.setWindowFlags(self.windowFlags() | Qt.Window)  # Make window moveable
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
        self.add_shift_btn = QPushButton("Add Shift(s) (removes current shifts)")
        self.add_shift_btn.clicked.connect(self.add_shift)
        layout.addWidget(self.add_shift_btn)
        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(False)  # Make the response field editable
        layout.addWidget(self.output_edit)
        self.copy_btn = QPushButton("Copy Response")
        self.copy_btn.clicked.connect(self.copy_response)
        layout.addWidget(self.copy_btn)
        self.setLayout(layout)

    def add_shift(self):
        self.shifts = []
        self._add_shift_recursive(1)

    def _add_shift_recursive(self, shift_num):
        dialog = ShiftDialog(self, shift_num)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.Window)  # Make popup moveable
        dialog.another_btn.clicked.connect(lambda: self._handle_shift(dialog, shift_num, another=True))
        dialog.done_btn.clicked.connect(lambda: self._handle_shift(dialog, shift_num, another=False))
        dialog.show()
        self.current_dialog = dialog

    def _handle_shift(self, dialog, shift_num, another):
        date = dialog.date_edit.date().toString("MM/dd/yyyy")
        # Use combo boxes for time selection
        start_time_str = dialog.start_time_combo.currentText()
        end_time_str = dialog.end_time_combo.currentText()

        # Parse times and calculate hours
        from PyQt5.QtCore import QTime
        start_time = QTime.fromString(start_time_str, "hh:mm AP")
        end_time = QTime.fromString(end_time_str, "hh:mm AP")

        # Calculate hours, handle overnight shifts
        start_dt = QDateTime(dialog.date_edit.date(), start_time)
        end_dt = QDateTime(dialog.date_edit.date(), end_time)
        if end_time <= start_time:
            end_dt = end_dt.addDays(1)
        hours = start_dt.secsTo(end_dt) / 3600.0
        if hours <= 0:
            QMessageBox.warning(self, "Invalid Input", "End time must be after start time.")
            return
        self.shifts.append({'date': date, 'start': start_time_str, 'end': end_time_str, 'hours': hours})
        dialog.close()
        if another:
            self._add_shift_recursive(shift_num + 1)
        else:
            self.generate_response()

    def generate_response(self):
        try:
            rate = float(self.rate_edit.text().strip())
            nte = float(self.nte_edit.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for rate and NTE.")
            return
        total_hours = sum(shift['hours'] for shift in self.shifts)
        total_cost = rate * total_hours + 50 * (total_hours / 12)
        lines = [f"We have staffed this request at ${rate:.2f}/hr for the following schedule:", ""]
        for shift in self.shifts:
            lines.append(f"{shift['date']} - {shift['start']} to {shift['end']}: {shift['hours']:.2f} hours")
        lines.append("")
        lines.append(f"The estimated total is ${rate:.2f}/hr x {total_hours:.2f} hours + taxes = ${total_cost:.2f}.")
        lines.append("")
        if total_cost > nte:
            lines.append("Please raise the NTE.")
        lines.append("")
        lines.append(self.signature_func())
        self.output_edit.setPlainText("\n".join(lines))

    def copy_response(self):
        pyperclip.copy(self.output_edit.toPlainText())
        QMessageBox.information(self, "Copied", "Response copied to clipboard.")
