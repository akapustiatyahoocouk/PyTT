"""
    Private classes and services required for Tk/Ttk integration.
"""

def _tk_analyze_label(label: str) -> tuple[str, int]:
    """ Given a "label" of an AWT control (i.e. button text, menu
        item text, etc.) where '&' can be used to mark the 'hotchar',
        returns a tuple of Tk-style widget label and the underline
        char position. """
    text = ""
    underline = None
    i = 0
    while i < len(label):
        if (label[i] == "&") and (i + 1 < len(label)) and (label[i+1] == '&'):
            #   && -> &
            text += "&"
            i += 2;
        elif (label[i] == "&") and (i + 1 < len(label)) and (underline is None):
            underline = len(text)
            text += label[i+1]
            i += 2
        else:
            text += label[i]
            i += 1
    return (text, underline)


