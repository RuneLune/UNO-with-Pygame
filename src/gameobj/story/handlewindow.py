from gameobj.story.nobtn import NoButton
from gameobj.story.yesbtn import YesButton
from gameobj.story.windowbg import WindowBackground
from gameobj.story.windowtxt import WindowText

class HandleWindow:
    def __init__(self) -> None:
        self.no_button = NoButton()
        self.yes_button = YesButton()
        self.window_background = WindowBackground()
        self.window_text = WindowText()

    def visible_window(self):
        self.no_button.visible()
        self.yes_button.visible()
        self.window_background.visible()
        self.window_text.visible()

        return None
    
    def invisible_window(self):
        self.no_button.invisible()
        self.yes_button.invisible()
        self.window_background.invisible()
        self.window_text.invisible()

        return None