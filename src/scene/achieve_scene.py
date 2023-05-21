from overrides import overrides
import pygame

from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject
from util.resource_manager import font_resource
import util.colors as color

from gameobj.achieve.icon import Icon


from gameobj.achieve.text import Text


from gameobj.achieve.date import Date

from gameobj.achieve.backbtn import BackButton




class AchieveScene(Scene):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(screen_rect.size)
        background_surface.fill(color.black)
        title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 9
        )
        menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 15
        )

        self.background = GameObject(
            background_surface, "TestScene_Background", z_index=-999
        )
        self.title_text = TextObject(
            "Achievement", title_font, color.white, "AchievementScene_TitleText", z_index=-900
        )
        self.back_button = BackButton(
            "◀ Back", menu_font, color.white, "AchievementScene_BackButton", z_index=997).attach_mgr(self.scene_manager)

        self.iconA = Icon(name="0")
        self.iconB = Icon(name="1")
        self.iconC = Icon(name="2")
        self.iconD = Icon(name="3")
        self.iconE = Icon(name="4")
        self.iconF = Icon(name="5")
        self.iconG = Icon(name="6")
        self.iconH = Icon(name="7")

        self.textA = Text(name="0")
        self.textB = Text(name="1")
        self.textC = Text(name="2")
        self.textD = Text(name="3")
        self.textE = Text(name="4")
        self.textF = Text(name="5")
        self.textG = Text(name="6")
        self.textH = Text(name="7")

        self.dateA = Date(name="date_a")
        self.dateB = Date(name="date_b")
        self.dateC = Date(name="date_c")
        self.dateD = Date(name="date_d")
        self.dateE = Date(name="date_e")
        self.dateF = Date(name="date_f")
        self.dateG = Date(name="date_g")
        self.dateH = Date(name="date_h")



        self.title_text.rect.center = (
            screen_rect.centerx, screen_rect.centery / 4)
        self.back_button.rect.center = (
            screen_rect.centerx / 5, screen_rect.centery / 5)
        
        self.iconA.rect.center = (
            screen_rect.centerx / 5, screen_rect.centery / 2)
        self.iconB.rect.center = (
            screen_rect.right / 1.8, screen_rect.centery / 2)
        self.iconC.rect.center = (
            screen_rect.centerx / 5, screen_rect.centery / 1.2)
        self.iconD.rect.center = (
            screen_rect.right / 1.8, screen_rect.centery / 1.2)
        self.iconE.rect.center = (
            screen_rect.centerx / 5, screen_rect.bottom / 1.6)
        self.iconF.rect.center = (
            screen_rect.right / 1.8, screen_rect.bottom / 1.6)
        self.iconG.rect.center = (
            screen_rect.centerx / 5, screen_rect.bottom / 1.2)
        self.iconH.rect.center = (
            screen_rect.right / 1.8, screen_rect.bottom / 1.2)
        
        self.textA.rect.center = (
            screen_rect.centerx / 1.5, screen_rect.centery / 2.2)
        self.textB.rect.center = (
            screen_rect.right / 1.3, screen_rect.centery / 2.2)
        self.textC.rect.center = (
            screen_rect.centerx / 1.5, screen_rect.centery / 1.3)
        self.textD.rect.center = (
            screen_rect.right / 1.3, screen_rect.centery / 1.3)
        self.textE.rect.center = (
            screen_rect.centerx / 1.5, screen_rect.bottom / 1.7)
        self.textF.rect.center = (
            screen_rect.right / 1.3, screen_rect.bottom / 1.7)
        self.textG.rect.center = (
            screen_rect.centerx / 1.5, screen_rect.bottom / 1.3)
        self.textH.rect.center = (
            screen_rect.right / 1.3, screen_rect.bottom / 1.3)
        
        self.dateA.rect.center = (
            screen_rect.centerx / 1.5, screen_rect.centery / 1.8)
        self.dateB.rect.center = (
            screen_rect.right / 1.3, screen_rect.centery / 1.8)
        self.dateC.rect.center = (
            screen_rect.centerx / 1.5, screen_rect.centery / 1.1)
        self.dateD.rect.center = (
            screen_rect.right / 1.3, screen_rect.centery / 1.1)
        self.dateE.rect.center = (
            screen_rect.centerx / 1.5, screen_rect.bottom / 1.5)
        self.dateF.rect.center = (
            screen_rect.right / 1.3, screen_rect.bottom / 1.5)
        self.dateG.rect.center = (
            screen_rect.centerx / 1.5, screen_rect.bottom / 1.2)
        self.dateH.rect.center = (
            screen_rect.right / 1.3, screen_rect.bottom / 1.2)


        self.back_button.on_mouse_up_as_button = (
            lambda: self.scene_manager.load_previous_scene()
        )

        # 장면에 게임 오브젝트 추가
        self.instantiate(self.background)
        self.instantiate(self.title_text)
        self.instantiate(self.back_button)
        self.instantiate(self.iconA)
        self.instantiate(self.iconB)
        self.instantiate(self.iconC)
        self.instantiate(self.iconD)
        self.instantiate(self.iconE)
        self.instantiate(self.iconF)
        self.instantiate(self.iconG)
        self.instantiate(self.iconH)
        self.instantiate(self.textA)
        self.instantiate(self.textB)
        self.instantiate(self.textC)
        self.instantiate(self.textD)
        self.instantiate(self.textE)
        self.instantiate(self.textF)
        self.instantiate(self.textG)
        self.instantiate(self.textH)
        self.instantiate(self.dateA)
        self.instantiate(self.dateB)
        self.instantiate(self.dateC)
        self.instantiate(self.dateD)
        self.instantiate(self.dateE)
        self.instantiate(self.dateF)
        self.instantiate(self.dateG)
        self.instantiate(self.dateH)

        return None
