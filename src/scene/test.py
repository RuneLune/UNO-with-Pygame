from overrides import overrides
import pygame

from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject
from util.resource_manager import font_resource
import util.colors as color

from gameobj.achieve.iconA import IconA
from gameobj.achieve.iconB import IconB
from gameobj.achieve.iconC import IconC
from gameobj.achieve.iconD import IconD
from gameobj.achieve.iconE import IconE
from gameobj.achieve.iconF import IconF
from gameobj.achieve.iconG import IconG
from gameobj.achieve.iconH import IconH

from gameobj.achieve.textA import TextA
from gameobj.achieve.textB import TextB
from gameobj.achieve.textC import TextC
from gameobj.achieve.textD import TextD
from gameobj.achieve.textE import TextE
from gameobj.achieve.textF import TextF
from gameobj.achieve.textG import TextG
from gameobj.achieve.textH import TextH


class TestScene(Scene):
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
        self.back_button = TextButtonObject(
            "◀ Back", menu_font, color.white, "AchievementScene_BackButton", z_index=997)

        self.iconA = IconA()
        self.iconB = IconB()
        self.iconC = IconC()
        self.iconD = IconD()
        self.iconE = IconE()
        self.iconF = IconF()
        self.iconG = IconG()
        self.iconH = IconH()

        self.textA = TextA()
        self.textB = TextB()
        self.textC = TextC()
        self.textD = TextD()
        self.textE = TextE()
        self.textF = TextF()
        self.textG = TextG()
        self.textH = TextH()


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

        return None
