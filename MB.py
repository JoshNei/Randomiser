import ctypes
import logging
import os
from __main__ import __file__ as filename

# https://docs.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-messagebox?redirectedfrom=MSDN

log = logging.getLogger(__name__)

BTN_OK = 0x00000000                  # The message box contains one push button: OK. This is the default.
BTN_OKCANCEL = 0x00000001            # The message box contains two push buttons: OK and Cancel.
BTN_ABORTRETRYIGNORE = 0x00000002    # The message box contains three push buttons: Abort, Retry, and Ignore.
BTN_YESNOCANCEL = 0x00000003         # The message box contains three push buttons: Yes, No, and Cancel.
BTN_YESNO = 0x00000004               # The message box contains two push buttons: Yes and No.
BTN_RETRYCANCEL = 0x00000005         # The message box contains two push buttons: Retry and Cancel.
BTN_CANCELTRYCONTINUE = 0x00000006   # The message box contains three push buttons: Cancel, Try Again, Continue. Use this message box type instead of MB_ABORTRETRYIGNORE.

ICN_STOP = 0x00000010           # A stop-sign icon appears in the message box.
ICN_QUESTION = 0x00000020       # A question-mark icon appears in the message box. The question-mark message icon is no longer recommended because it does not clearly represent a specific type of message and because the phrasing of a message as a question could apply to any message type. In addition, users can confuse the message symbol question mark with Help information. Therefore, do not use this question mark message symbol in your message boxes. The system continues to support its inclusion only for backward compatibility.
ICN_WARNING = 0x00000030        # An exclamation-point icon appears in the message box.
ICN_INFORMATION = 0x00000040    # An icon consisting of a lowercase letter i in a circle appears in the message box.

DEFAULT_2 = 0x00000100  # The second button is the default button.
DEFAULT_3 = 0x00000200  # The third button is the default button.
DEFAULT_4 = 0x00000300  # The fourth button is the default button.

MB_HELP = 0x00004000        # Adds a Help button to the message box. When the user clicks the Help button or presses F1, the system sends a WM_HELP message to the owner.
MB_TOPMOST = 0x00040000     # The message box is created with the WS_EX_TOPMOST window style.

OK = 1           # The OK button was selected.
CANCEL = 2       # The Cancel button was selected.
ABORT = 3        # The Abort button was selected.
RETRY = 4        # The Retry button was selected.
IGNORE = 5       # The Ignore button was selected.
YES = 6          # The Yes button was selected.
NO = 7           # The No button was selected.
TRYAGAIN = 10    # The Try Again button was selected.
CONTINUE = 11    # The Continue button was selected.


def popup(text, title=os.path.basename(filename), style=0):
    log.debug("Popup created: \"" + text.replace("\n", " ") + "\"")
    button = ctypes.windll.user32.MessageBoxW(0, text, title, style)
    button_list = {1: "OK", 2: "Cancel", 3: "Abort", 4: "Retry", 5: "Ignore", 6: "Yes", 7: "No", 10: "Try Again", 11: "Continue"}
    log.debug(button_list[button] + " button clicked")
    return button
