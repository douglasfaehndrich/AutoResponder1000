<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This project is a Python app with a PyQt GUI that retrieves email responses form a JSON, copies them to the clipboard, and is intended for open-source distribution and packaging as a Windows .exe. Use best practices for modularity, security, and maintainability.
The app should be designed to be user-friendly, with a clean and intuitive interface.
The app should also include error handling and logging for debugging purposes.

There is a signature section at the top that has a field with a signature that is added to the end of most responses.

Each response section looks similar in the GUI: They all have a button and most have at least one input field that gets added somewhere into the response.

There is a JSON that contains the responses. This JSON can by changed by the user in the settings menu. 

The settings menu should show the email responses in the JSON and a placeholder for any inputs (except the signature) that are included in the response.

When I add a response to field to the app, it should add a button and any necessary input fields. 
It should match the GUI format and style of the other response sections. 
It should add the new response to the JSON and make it editable in the settings menu. 
It should add any processes that are necessary to implement the functionality to the response section.