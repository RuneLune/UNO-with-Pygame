from gameobj.gamelobby.botNMbtn import BotNormalButton
from gameobj.gamelobby.botAbtn import BotAButton
from gameobj.gamelobby.botBbtn import BotBButton
from gameobj.gamelobby.botCbtn import BotCButton
from gameobj.gamelobby.botDbtn import BotDButton
from gameobj.gamelobby.botNMtxt import BotNormalText
from gameobj.gamelobby.botAtxt import BotAText
from gameobj.gamelobby.botBtxt import BotBText
from gameobj.gamelobby.botCtxt import BotCText
from gameobj.gamelobby.botDtxt import BotDText
from gameobj.gamelobby.botsltbg import BotSelectBackground
from gameobj.gamelobby.botslttxt import BotSelectText
from metaclass.singleton import SingletonMeta


class HandleBotSelect(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.botNM_button = BotNormalButton()
        self.botA_button = BotAButton()
        self.botB_button = BotBButton()
        self.botC_button = BotCButton()
        self.botD_button = BotDButton()
        self.botNM_text = BotNormalText()
        self.botA_text = BotAText()
        self.botB_text = BotBText()
        self.botC_text = BotCText()
        self.botD_text = BotDText()
        self.bot_select_background = BotSelectBackground()
        self.bot_select_text = BotSelectText()

    def visible_bot_select(self):
        self.botNM_button.visible()
        self.botA_button.visible()
        self.botB_button.visible()
        self.botC_button.visible()
        self.botD_button.visible()
        self.botNM_button.enable()
        self.botA_button.enable()
        self.botB_button.enable()
        self.botC_button.enable()
        self.botD_button.enable()
        self.bot_select_background.visible()
        self.bot_select_text.visible()
        return None

    def invisible_bot_select(self):
        self.botNM_button.invisible()
        self.botA_button.invisible()
        self.botB_button.invisible()
        self.botC_button.invisible()
        self.botD_button.invisible()
        self.botNM_button.disable()
        self.botA_button.disable()
        self.botB_button.disable()
        self.botC_button.disable()
        self.botD_button.disable()
        self.botNM_text.invisible()
        self.botA_text.invisible()
        self.botB_text.invisible()
        self.botC_text.invisible()
        self.botD_text.invisible()
        self.bot_select_background.invisible()
        self.bot_select_text.invisible()

        return None
