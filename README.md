# AutoResponder1000

A simple Python app with a PyQt GUI that uses AI to generate email responses, copies them to the clipboard, and is designed for easy packaging as a Windows .exe. Intended for open-source distribution.

## Features
- PyQt-based GUI
- AI-powered response generation (OpenAI API or similar)
- One-click copy to clipboard
- Easy to package as .exe for Windows

## Setup
1. Install Python 3.8+
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the app:
   ```powershell
   python main.py
   ```

## Packaging as .exe
- Use `pyinstaller` or similar tools. See instructions in the code comments.

## License
- Open source. PyQt license respected (source code included).
