# AutoResponder1000 - Distribution Guide

## For Users (Your Coworkers)

### First Time Setup

1. **Download the package** - You should receive two files:
   - `AutoResponder1000.exe` - The application
   - `responses.template.json` - Template configuration file

2. **Run the application**:
   - Double-click `AutoResponder1000.exe`
   - The app will automatically create `responses.json` from the template on first run
   - Keep both files in the same folder

3. **Customize your settings**:
   - Click the "Settings" button in the app
   - Update:
     - Your default signature (replace `[Your Name]` with your name)
     - Email addresses for WB Report
     - Store code prefixes for Strickland Clock Ins (if needed)
     - Response templates as needed
   - Click "Save"

4. **You're ready to go!**
   - The app will remember all your settings
   - Your `responses.json` file contains your personal configuration

### Using the Application

**Signature Section:**
- Your default signature is added to most responses automatically
- Changes are auto-saved 1 second after you stop typing

**Strickland Clock Ins:**
- Paste the email subject line
- Click "Copy Clock In Response"
- The app finds store codes (CB, SEPH, JJ, RLC, SC, etc.) and generates the response

**Service Channel:**
- Enter hourly rate and NTE
- Click "Add Shift(s) and Generate Response"
- Add one or more shifts with dates and times
- Click "Done" to generate the formatted response
- Click "Copy Response" to copy to clipboard

**Send Work Order (PIN Confirmation):**
- Enter the PIN
- Click the copy button
- Response is copied with HTML formatting (bold PIN)

**Rate Approval:**
- Enter the rate
- Click the copy button

**WB Report:**
- Select the date
- Click "Create WB Report Email"
- Opens your default email client with pre-filled template

### Troubleshooting

**"responses.json not found" or template errors:**
- Make sure `responses.template.json` is in the same folder as the .exe
- The app will automatically create `responses.json` from the template
- If you deleted `responses.json`, just restart the app to recreate it

**Settings not saving:**
- Check that the folder is not read-only
- Make sure you have write permissions

**Application won't start:**
- Contact IT support
- May need to allow the application in antivirus/firewall

---

## For Building/Packaging (Developer Use)

### Building the Executable

1. **Prerequisites**:
   ```bash
   pip install pyinstaller
   ```

2. **Build**:
   ```bash
   # Option 1: Use the build script (Windows)
   build.bat

   # Option 2: Manual build
   pyinstaller --clean AutoResponder1000.spec
   ```

3. **Output**:
   - Executable: `dist/AutoResponder1000.exe`
   - Include `responses.template.json` when distributing

### Distribution Package

Create a distribution folder containing:
```
AutoResponder1000-Distribution/
├── AutoResponder1000.exe
├── responses.template.json
└── README.txt (instructions for users)
```

### Notes

- The .exe is standalone and includes all Python dependencies
- Users do NOT need Python installed
- The app creates/modifies `responses.json` in the same directory as the .exe
- Settings persist between sessions via the JSON file
