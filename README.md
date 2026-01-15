# AutoResponder1000

A PyQt5 desktop application for generating customizable email responses. Originally designed for security dispatch operations, but adaptable for any workflow that uses templated email responses.

## Features
- **Customizable Response Templates** - Edit email templates with dynamic field placeholders
- **Persistent Signature** - Set your default signature once, saved between sessions
- **Quick Copy to Clipboard** - One-click copy of formatted responses
- **Special Response Types**:
  - Clock-in processing for specific store codes
  - Service Channel rate/NTE calculator with shift scheduling
  - Automated report email generation
- **Settings Interface** - Easy-to-use settings window for managing all templates
- **Modular Architecture** - Clean separation of UI components and utilities

## Setup

### Prerequisites
- Python 3.8 or higher
- Windows OS (uses win32clipboard for HTML formatting)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/douglasfaehndrich/AutoResponder1000.git
   cd AutoResponder1000
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your responses:
   - Copy `responses.template.json` to `responses.json`
   - Edit `responses.json` to add your signature and customize templates

5. Run the application:
   ```bash
   python main.py
   ```

## Configuration

Edit `responses.json` to customize:
- **Default Signature** - Your email signature
- **Response Templates** - Email templates with `{{Placeholder}}` fields
- **Email Recipients** - Default recipient and CC addresses

Templates support placeholders in the format `{{FieldName}}` which will create input fields in the UI.

## Packaging as .exe
To create a standalone Windows executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "responses.json;." main.py
```

## License
Open source. PyQt5 GPL license respected (source code included).
