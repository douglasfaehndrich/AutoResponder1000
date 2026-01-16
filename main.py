import sys
import pyperclip
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QGroupBox, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import re

# Import modularized components
from utils.responses import load_responses, save_responses
from utils.clipboard import copy_to_clipboard, copy_html_to_clipboard
from widgets.pin_confirmation_section import PinConfirmationSection
from widgets.rate_approval_section import RateApprovalSection
from widgets.wb_report_section import WBReportSection
from widgets.settings_window import SettingsWindow
from widgets.shift_dialog import ShiftDialog
from widgets.rate_nte_window import RateNTEWindow

# Note: load_responses and save_responses are imported from utils.responses
# No need to redefine them here

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
        # Save signature when editing is finished (not on every keystroke)
        self.signature_text.textChanged.connect(self.on_signature_changed)
        self.signature_save_timer = None
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

    def on_signature_changed(self):
        """Debounce signature saving - wait for user to stop typing"""
        from PyQt5.QtCore import QTimer
        if self.signature_save_timer:
            self.signature_save_timer.stop()
        self.signature_save_timer = QTimer()
        self.signature_save_timer.setSingleShot(True)
        self.signature_save_timer.timeout.connect(self.save_signature)
        self.signature_save_timer.start(1000)  # Save 1 second after user stops typing

    def save_signature(self):
        """Save signature to responses.json"""
        try:
            self.responses["Default Signature"] = self.signature_text.toPlainText()
            save_responses(self.responses)
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Could not save signature: {e}")

    def save_responses(self, responses):
        """Save responses to JSON file - called by SettingsWindow"""
        save_responses(responses)
        self.responses = responses

    def process_subject(self):
        try:
            subject = self.subject_entry.text()
            pattern = r'\b(?:CB|SEPH|JJ|RLC|SC)\d+\b'
            store_codes = re.findall(pattern, subject, re.IGNORECASE)
            store_codes = [code.upper() for code in store_codes]
            if not store_codes:
                QMessageBox.warning(self, "No Codes Found", "No matching store codes were found in the subject.")
                return
            body_lines = [f"{code} - Guard clocked in on time." for code in store_codes]
            body = "\n".join(body_lines) + "\n\n" + self.get_signature()
            pyperclip.copy(body)
            QMessageBox.information(self, "Copied", f"Clock-in response for {len(store_codes)} store(s) copied to clipboard.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

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
        QMessageBox.information(self, "Copied", "Rate approval response copied to clipboard.")

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
        QMessageBox.information(self, "Copied", "PIN confirmation response copied to clipboard.")

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
        template = self.responses.get("WB Report", "Hello,\n\nThe following sites had security as scheduled:\n\n{Signature}")
        body = template.replace("{Date}", date).replace("{DayOfWeek}", day_of_week).replace("{Signature}", self.get_signature())
        import urllib.parse, webbrowser
        mailto_url = f"mailto:{urllib.parse.quote(recipients)}?cc={urllib.parse.quote(cc)}&subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        webbrowser.open(mailto_url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoResponderApp()
    window.show()
    sys.exit(app.exec_())
