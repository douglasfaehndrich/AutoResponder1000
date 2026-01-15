import pyperclip
import win32clipboard

def copy_to_clipboard(text):
    pyperclip.copy(text)

def copy_html_to_clipboard(html):
    html = html.replace("\n", "<br>")
    html_clip = (
        "Version:0.9\r\n"
        "StartHTML:00000097\r\n"
        "EndHTML:{end_html:08d}\r\n"
        "StartFragment:00000131\r\n"
        "EndFragment:{end_fragment:08d}\r\n"
        "<html><body><!--StartFragment-->{fragment}<!--EndFragment--></body></html>"
    )
    fragment = html
    start_html = 97
    start_fragment = 131
    end_fragment = start_fragment + len(fragment)
    end_html = end_fragment + 20  # length of </body></html>
    html_clip = html_clip.format(
        end_html=end_html,
        end_fragment=end_fragment,
        fragment=fragment
    )
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.RegisterClipboardFormat('HTML Format'), html_clip.encode('utf-8'))
    win32clipboard.CloseClipboard()
