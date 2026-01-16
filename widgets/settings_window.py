from PyQt5.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QTextEdit, QLineEdit,
    QPushButton, QSizePolicy, QHBoxLayout, QSpacerItem
)
from PyQt5.QtCore import Qt

class SettingsWindow(QWidget):  # <-- Inherit from QWidget
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Edit Responses")
        self.setGeometry(150, 150, 500, 600)
        self.parent = parent
        self.text_edits = {}
        self.input_fields = {}

        # Main content widget and layout
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(24, 24, 24, 24)

        # Professional style: Section title
        title = QLabel("Edit Email Response Templates")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 12px;")
        content_layout.addWidget(title, alignment=Qt.AlignHCenter)

        # Add each response as a group box
        for key, value in self.parent.responses.items():
            if key.endswith("Recipients") or key.endswith("CC"):
                continue  # Recipients/CC handled in main template group if needed

            # Special handling for Default Signature
            if key == "Default Signature":
                group = QGroupBox("Default Signature")
                group.setStyleSheet("""
                    QGroupBox {
                        font-size: 15px;
                        font-weight: bold;
                        border: 2px solid #0078d7;
                        border-radius: 8px;
                        margin-top: 8px;
                    }
                    QGroupBox:title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 3px 0 3px;
                    }
                """)
                group_layout = QVBoxLayout()
                group_layout.setSpacing(8)
                group_layout.addWidget(QLabel("Your default signature (added to most responses):"))
                edit = QTextEdit()
                edit.setPlainText(value)
                edit.setMinimumHeight(60)
                edit.setMaximumHeight(80)
                edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                edit.setStyleSheet("font-family: Consolas, monospace; font-size: 13px;")
                group_layout.addWidget(edit)
                self.text_edits[key] = edit
                group.setLayout(group_layout)
                content_layout.addWidget(group)
                continue

            # Special handling for Strickland Clock Ins
            if key == "Strickland Clock Ins":
                group = QGroupBox("Strickland Clock Ins Settings")
                group.setStyleSheet("""
                    QGroupBox {
                        font-size: 15px;
                        font-weight: bold;
                        border: 2px solid #0078d7;
                        border-radius: 8px;
                        margin-top: 8px;
                    }
                    QGroupBox:title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 3px 0 3px;
                    }
                """)
                group_layout = QVBoxLayout()
                group_layout.setSpacing(8)

                # Prefixes field
                group_layout.addWidget(QLabel("Store Code Prefixes (comma-separated):"))
                prefixes_edit = QLineEdit()
                prefixes_edit.setText(value.get("prefixes", "CB, SEPH, JJ, RLC, SC"))
                prefixes_edit.setPlaceholderText("e.g. CB, SEPH, JJ, RLC, SC")
                group_layout.addWidget(prefixes_edit)
                self.input_fields["Strickland Clock Ins Prefixes"] = prefixes_edit

                # Response template field
                group_layout.addWidget(QLabel("Response Template (use {{CODE}} for store code):"))
                template_edit = QLineEdit()
                template_edit.setText(value.get("response_template", "{{CODE}} - Guard clocked in on time."))
                template_edit.setPlaceholderText("{{CODE}} - Guard clocked in on time.")
                group_layout.addWidget(template_edit)
                self.input_fields["Strickland Clock Ins Template"] = template_edit

                # Info label
                info_label = QLabel("The app will search email subjects for codes like CB0123, SEPH0456, etc.")
                info_label.setStyleSheet("color: #888; font-style: italic; font-size: 12px;")
                group_layout.addWidget(info_label)

                group.setLayout(group_layout)
                content_layout.addWidget(group)
                continue

            group = QGroupBox(key)
            group.setStyleSheet("""
                QGroupBox {
                    font-size: 15px;
                    font-weight: bold;
                    border: 1px solid #bbb;
                    border-radius: 8px;
                    margin-top: 8px;
                }
                QGroupBox:title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
            """)
            group_layout = QVBoxLayout()
            group_layout.setSpacing(8)
            # Template field
            group_layout.addWidget(QLabel("Template:"))
            edit = QTextEdit()
            edit.setPlainText(value if isinstance(value, str) else value.get("template", ""))
            edit.setMinimumHeight(60)
            edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            edit.setStyleSheet("font-family: Consolas, monospace; font-size: 13px;")
            group_layout.addWidget(edit)
            self.text_edits[key] = edit

            # Show placeholders for fields (except signature)
            if isinstance(value, dict) and "fields" in value:
                for field in value["fields"]:
                    if field.lower() != "signature":
                        field_label = QLabel(f"Input field: {{{{{field}}}}}")
                        field_label.setStyleSheet("color: #888; font-style: italic;")
                        group_layout.addWidget(field_label)

            # Add Recipients/CC fields if this is WB Report
            if key == "WB Report":
                rec_label = QLabel("Recipient Email Addresses (comma separated):")
                rec_label.setStyleSheet("margin-top: 8px;")
                group_layout.addWidget(rec_label)
                wb_recipients_edit = QLineEdit()
                wb_recipients_edit.setText(self.parent.responses.get("WB Report Recipients", ""))
                wb_recipients_edit.setPlaceholderText("e.g. user1@email.com, user2@email.com")
                group_layout.addWidget(wb_recipients_edit)
                self.input_fields["WB Report Recipients"] = wb_recipients_edit

                cc_label = QLabel("CC Email Addresses (comma separated):")
                cc_label.setStyleSheet("margin-top: 4px;")
                group_layout.addWidget(cc_label)
                wb_cc_edit = QLineEdit()
                wb_cc_edit.setText(self.parent.responses.get("WB Report CC", ""))
                wb_cc_edit.setPlaceholderText("e.g. cc1@email.com, cc2@email.com")
                group_layout.addWidget(wb_cc_edit)
                self.input_fields["WB Report CC"] = wb_cc_edit

            group.setLayout(group_layout)
            content_layout.addWidget(group)

        content_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Save button at the bottom, centered
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 15px;
                padding: 8px 24px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
        """)
        save_btn.clicked.connect(self.save)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(save_btn)
        btn_layout.addStretch(1)
        content_layout.addLayout(btn_layout)

        content_widget.setLayout(content_layout)

        # Add scroll area to main layout
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def save(self):
        for key, edit in self.text_edits.items():
            if isinstance(self.parent.responses[key], dict) and "template" in self.parent.responses[key]:
                self.parent.responses[key]["template"] = edit.toPlainText()
            else:
                self.parent.responses[key] = edit.toPlainText()

        # Save WB Report Recipients and CC
        if "WB Report Recipients" in self.input_fields:
            self.parent.responses["WB Report Recipients"] = self.input_fields["WB Report Recipients"].text()
        if "WB Report CC" in self.input_fields:
            self.parent.responses["WB Report CC"] = self.input_fields["WB Report CC"].text()

        # Save Strickland Clock Ins settings
        if "Strickland Clock Ins Prefixes" in self.input_fields:
            if "Strickland Clock Ins" not in self.parent.responses:
                self.parent.responses["Strickland Clock Ins"] = {}
            self.parent.responses["Strickland Clock Ins"]["prefixes"] = self.input_fields["Strickland Clock Ins Prefixes"].text()
        if "Strickland Clock Ins Template" in self.input_fields:
            if "Strickland Clock Ins" not in self.parent.responses:
                self.parent.responses["Strickland Clock Ins"] = {}
            self.parent.responses["Strickland Clock Ins"]["response_template"] = self.input_fields["Strickland Clock Ins Template"].text()

        self.parent.save_responses(self.parent.responses)

        # Update the main window's signature field if it was changed
        if "Default Signature" in self.text_edits:
            self.parent.signature_text.blockSignals(True)  # Prevent triggering save again
            self.parent.signature_text.setPlainText(self.parent.responses["Default Signature"])
            self.parent.signature_text.blockSignals(False)

        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Saved", "Responses updated.")
        self.close()
