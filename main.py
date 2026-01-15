import sys
import pyperclip
import win32clipboard
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QGroupBox, QHBoxLayout, QLineEdit, QMessageBox, QSizePolicy, QSplitter, QScrollArea, QDateEdit, QTimeEdit, QComboBox
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime
import re
import json
import os

# Import modularized components
from utils.responses import load_responses, save_responses
from utils.clipboard import copy_to_clipboard, copy_html_to_clipboard
from widgets.pin_confirmation_section import PinConfirmationSection
from widgets.rate_approval_section import RateApprovalSection
from widgets.wb_report_section import WBReportSection
from widgets.settings_window import SettingsWindow
from widgets.shift_dialog import ShiftDialog
from widgets.rate_nte_window import RateNTEWindow

RESPONSES_FILE = os.path.join(os.path.dirname(__file__), "responses.json")

def load_responses():
    with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_responses(responses):
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=4)

class AutoResponderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.responses = load_responses()
        self.setWindowTitle('AutoResponder1000')
        self.setGeometry(100, 100, 600, 700)
        main_layout = QVBoxLayout()

        # Signature section
        self.signature_box = QGroupBox("Signature")
        sig_layout = QHBoxLayout()
        sig_label = QLabel("Signature:")
        self.signature_text = QTextEdit()
        self.signature_text.setFixedHeight(60)
        # Load signature from responses.json
        default_sig = self.responses.get("Default Signature", "Thank you,\n[Your Name]")
        self.signature_text.setPlainText(default_sig)
        # Save signature when it changes
        self.signature_text.textChanged.connect(self.save_signature)
        sig_layout.addWidget(sig_label)
        sig_layout.addWidget(self.signature_text)
        self.signature_box.setLayout(sig_layout)
        self.signature_box.setMaximumHeight(100)
        main_layout.addWidget(self.signature_box)

        # Strickland Clock Ins section
        self.clockin_box = QGroupBox("Strickland Clock Ins")
        clockin_layout = QVBoxLayout()
        clockin_layout.addWidget(QLabel("Email Subject Line:"))
        self.subject_entry = QLineEdit()
        clockin_layout.addWidget(self.subject_entry)
        self.clockin_btn = QPushButton("Copy Clock In Response")
        self.clockin_btn.clicked.connect(self.process_subject)
        clockin_layout.addWidget(self.clockin_btn)
        self.clockin_box.setLayout(clockin_layout)
        main_layout.addWidget(self.clockin_box)

        # Add Service Channel (was Rate/NTE Response) section in its own box above other responses
        from widgets.rate_nte_window import RateNTEWindow
        self.rate_nte_box = QGroupBox("Service Channel")
        rate_nte_layout = QVBoxLayout()
        rate_fields_layout = QHBoxLayout()
        rate_fields_layout.addWidget(QLabel("Hourly Rate:"))
        self.rate_nte_rate_edit = QLineEdit()
        rate_fields_layout.addWidget(self.rate_nte_rate_edit)
        rate_fields_layout.addWidget(QLabel("NTE:"))
        self.rate_nte_nte_edit = QLineEdit()
        rate_fields_layout.addWidget(self.rate_nte_nte_edit)
        rate_nte_layout.addLayout(rate_fields_layout)
        self.rate_nte_btn = QPushButton("Add Shift(s) and Generate Response")
        self.rate_nte_btn.clicked.connect(self.open_rate_nte_window)
        rate_nte_layout.addWidget(self.rate_nte_btn)
        self.rate_nte_box.setLayout(rate_nte_layout)
        main_layout.addWidget(self.rate_nte_box)

        # Add WB Report section
        self.wb_section = WBReportSection(self, self.create_wb_report_email)
        main_layout.insertWidget(main_layout.indexOf(self.rate_nte_box) + 1, self.wb_section)

        # Common responses
        self.response_buttons = {}
        self.response_inputs = {}
        # Add Send Work Order (PIN Confirmation) section
        if "PIN Confirmation" in self.responses:
            self.pin_section = PinConfirmationSection(self, self.copy_pin_confirmation)
            main_layout.addWidget(self.pin_section)
            self.response_inputs["PIN Confirmation"] = self.pin_section.pin_input
            self.response_buttons["PIN Confirmation"] = self.pin_section.copy_btn
        # Add Rate Approval section
        if "Rate Approval" in self.responses:
            self.rate_approval_section = RateApprovalSection(self, self.copy_rate_approval)
            main_layout.addWidget(self.rate_approval_section)
            self.response_inputs["Rate Approval"] = self.rate_approval_section.rate_input
            self.response_buttons["Rate Approval"] = self.rate_approval_section.copy_btn

        # Settings button
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)
        main_layout.addWidget(self.settings_btn)

        self.setLayout(main_layout)

    def get_signature(self):
        return self.signature_text.toPlainText().strip()

    def save_signature(self):
        """Save signature to responses.json when it changes"""
        self.responses["Default Signature"] = self.signature_text.toPlainText()
        save_responses(self.responses)

    def process_subject(self):
        subject = self.subject_entry.text()
        allowed_prefixes = r'CB|SEPH|JJ|RLC|SC'
        pattern = r'\b(?:CB|SEPH|JJ|RLC|SC)\d+\b'
        store_codes = re.findall(pattern, subject, re.IGNORECASE)
        store_codes = [code.upper() for code in store_codes]
        if not store_codes:
            QMessageBox.warning(self, "No Codes Found", "No matching store codes were found in the subject.")
            return
        body_lines = [f"{code} - Guard clocked in on time." for code in store_codes]
        body = "\n".join(body_lines) + "\n\n" + self.get_signature()
        pyperclip.copy(body)

    def copy_response(self, response_key):
        response_text = self.responses[response_key]
        sig = self.get_signature()
        if not response_text.strip().endswith(sig.strip()):
            response_text = response_text.rstrip() + "\n\n" + sig
        pyperclip.copy(response_text)

    def copy_schedule_for(self):
        name = self.name_entry.text()
        text = f"Hi {name},\n\nPlease see the attached schedule for your reference.\n\n{self.get_signature()}"
        pyperclip.copy(text)

    def copy_rate_approval(self, rate_input):
        rate = rate_input.text().strip()
        if not rate:
            QMessageBox.warning(self, "Missing Rate", "Please enter a rate.")
            return
        template = self.responses["Rate Approval"]["template"]
        response = template.replace("{{Rate}}", rate)
        response += "\n\n" + self.get_signature()
        pyperclip.copy(response)

    def copy_pin_confirmation(self, pin_input):
        pin = pin_input.text().strip()
        if not pin:
            QMessageBox.warning(self, "Missing PIN", "Please enter a PIN.")
            return
        template = self.responses["PIN Confirmation"]["template"]
        # Use HTML clipboard format for bold PIN
        html_pin = f"<b>{pin}</b>"
        response = template.replace("{{PIN}}", html_pin)
        response += "\n\n" + self.get_signature()
        copy_html_to_clipboard(response)

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def open_rate_nte_window(self):
        rate = self.rate_nte_rate_edit.text().strip()
        nte = self.rate_nte_nte_edit.text().strip()
        self.rate_nte_window = RateNTEWindow(self, self.get_signature, rate, nte)
        self.rate_nte_window.show()

    def create_wb_report_email(self):
        date = self.wb_section.date_edit.date().toString("MM/dd/yyyy")
        day_of_week = self.wb_section.date_edit.date().toString("dddd")
        recipients = self.responses.get("WB Report Recipients", "")
        cc = self.responses.get("WB Report CC", "")
        subject = f"Whataburger Results for {day_of_week} {date}"
        template = self.responses.get("WB Report", "Hello Michael,\n\nThe following sites has security as scheduled:\n\n{Signature}")
        body = template.replace("{Date}", date).replace("{DayOfWeek}", day_of_week).replace("{Signature}", self.get_signature())
        import urllib.parse, webbrowser
        mailto_url = f"mailto:{urllib.parse.quote(recipients)}?cc={urllib.parse.quote(cc)}&subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        webbrowser.open(mailto_url)

class SettingsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Edit Responses")
        self.setGeometry(150, 150, 400, 400)
        self.parent = parent
        layout = QVBoxLayout()
        self.text_edits = {}
        self.input_fields = {}
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        # Add WB Report to settings as its own box
        wb_group = QGroupBox("WB Report")
        wb_group_layout = QVBoxLayout()
        wb_group_layout.addWidget(QLabel("Template (placeholders: {Date}, {DayOfWeek}, {Signature})"))
        wb_edit = QTextEdit()
        wb_template = self.parent.responses.get("WB Report", "Hello Michael,\n\nThe following sites has security as scheduled:\n\n{Signature}")
        wb_edit.setPlainText(wb_template)
        wb_edit.setMinimumHeight(60)
        wb_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        wb_group_layout.addWidget(wb_edit)
        # Add email addresses field
        wb_group_layout.addWidget(QLabel("Recipient Email Addresses (comma separated):"))
        wb_recipients_edit = QLineEdit()
        wb_recipients_edit.setText(self.parent.responses.get("WB Report Recipients", ""))
        wb_group_layout.addWidget(wb_recipients_edit)
        wb_group.setLayout(wb_group_layout)
        self.text_edits["WB Report"] = wb_edit
        self.input_fields["WB Report Recipients"] = wb_recipients_edit
        content_layout.addWidget(wb_group)
        # Add all other responses, each in their own box
        for key, value in self.parent.responses.items():
            if key in ("WB Report", "WB Report Recipients", "WB Report CC", "Response 1", "Response 2"):
                continue
            group = QGroupBox(key)
            group_layout = QVBoxLayout()
            if isinstance(value, dict) and "template" in value:
                placeholders = value.get("fields", [])
                placeholder_str = ", ".join([f"{{{{{ph}}}}}" for ph in placeholders])
                label_text = f"Template (placeholders: {placeholder_str})" if placeholders else "Template:"
                group_layout.addWidget(QLabel(label_text))
                edit = QTextEdit()
                edit.setPlainText(value["template"])
                edit.setMinimumHeight(60)
                edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                group_layout.addWidget(edit)
                self.text_edits[key] = edit
                if placeholders:
                    for field in placeholders:
                        field_label = QLabel(f"Input field: {{{{{field}}}}}")
                        field_label.setStyleSheet("color: gray; font-style: italic;")
                        group_layout.addWidget(field_label)
            else:
                edit = QTextEdit()
                edit.setPlainText(value)
                edit.setMinimumHeight(60)
                edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                group_layout.addWidget(QLabel("Template:"))
                group_layout.addWidget(edit)
                self.text_edits[key] = edit
            group.setLayout(group_layout)
            content_layout.addWidget(group)
        content_layout.addStretch(1)
        content_widget.setLayout(content_layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)
        self.setLayout(layout)

    def save(self):
        for key, edit in self.text_edits.items():
            if key == "WB Report":
                self.parent.responses[key] = edit.toPlainText()
            elif isinstance(self.parent.responses[key], dict) and "template" in self.parent.responses[key]:
                self.parent.responses[key]["template"] = edit.toPlainText()
            else:
                self.parent.responses[key] = edit.toPlainText()
        # Save WB Report Recipients
        self.parent.responses["WB Report Recipients"] = self.input_fields["WB Report Recipients"].text()
        save_responses(self.parent.responses)
        QMessageBox.information(self, "Saved", "Responses updated.")
        self.close()
        # Optionally, refresh main window if needed

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
        # Use QTimeEdit for start and end times (no setInterval in PyQt5/6)
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("hh:mm AP")
        self.start_time_edit.setTime(QTime.currentTime())
        self.start_time_edit.setMinimumTime(QTime(0, 0))
        self.start_time_edit.setMaximumTime(QTime(23, 45))
        # Remove setInterval (not available in PyQt5/6)
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("hh:mm AP")
        self.end_time_edit.setTime(QTime.currentTime())
        self.end_time_edit.setMinimumTime(QTime(0, 0))
        self.end_time_edit.setMaximumTime(QTime(23, 45))
        # Remove setInterval (not available in PyQt5/6)
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

class RateNTEWindow(QWidget):
    def __init__(self, parent, signature_func, rate_init, nte_init):
        super().__init__()
        self.setWindowTitle("Service Channel")  # Changed window title
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
        date = dialog.date_edit.date().toString("MM/dd/yyyy")  # Changed date format
        # Use start_time_edit and end_time_edit instead of start_time_combo/end_time_combo
        start_time = dialog.start_time_edit.time()
        end_time = dialog.end_time_edit.time()
        start_time_str = start_time.toString("hh:mm AP")
        end_time_str = end_time.toString("hh:mm AP")
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoResponderApp()
    window.show()
    sys.exit(app.exec_())
