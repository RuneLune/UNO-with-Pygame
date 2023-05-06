from overrides import overrides
import pygame

from util.resource_manager import font_resource
import util.colors as color
from .scene import Scene
from gameobj.gameobj import GameObject
from gameobj.txtobj import TextObject
from gameobj.txtbtnobj import TextButtonObject

from gameobj.story.storyAbtn import StoryAButton
from gameobj.story.storyBbtn import StoryBButton
from gameobj.story.storyCbtn import StoryCButton
from gameobj.story.storyDbtn import StoryDButton
from gameobj.story.storyAtxt import StoryAText
from gameobj.story.storyBtxt import StoryBText
from gameobj.story.storyCtxt import StoryCText
from gameobj.story.storyDtxt import StoryDText
from gameobj.story.nobtn import NoButton
from gameobj.story.yesbtn import YesButton
from gameobj.story.windowbg import WindowBackground
from gameobj.story.windowtxt import WindowText
from gameobj.story.handlewindow import HandleWindow




class StoryScene(Scene):
    @overrides
    def start(self) -> None:
        screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(screen_rect.size)
        background_surface.fill(color.black)
        title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 5
        )
        menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"), screen_rect.height // 12
        )
        
        self.background = GameObject(
            background_surface, "StoryScene_Background", z_index=-999)
        self.title_text = TextObject(
            "Story", title_font, color.white, "StoryScene_TitleText", z_index=997)
        self.back_button = TextButtonObject(
            "◀ Back", menu_font, color.white, "StoryScene_BackButton", z_index=997)

        self.story_a_button = StoryAButton()
        self.story_b_button = StoryBButton()
        self.story_c_button = StoryCButton()
        self.story_d_button = StoryDButton()

        self.story_a_text = StoryAText()
        self.story_b_text = StoryBText()
        self.story_c_text = StoryCText()
        self.story_d_text = StoryDText()
        
        self.yes_button = YesButton()
        self.no_button = NoButton()
        self.window_text = WindowText()

        handle_window = HandleWindow()

        self.no_button.on_mouse_up_as_button = lambda: handle_window.invisible_window()
    

        self.window_background = WindowBackground()
        
        self.story_a_button.rect.center = (
            screen_rect.right / 8.8, screen_rect.centery)
        self.story_b_button.rect.center = (
            screen_rect.right / 2.6, screen_rect.centery)
        self.story_c_button.rect.center = (
            screen_rect.right / 1.6, screen_rect.centery)
        self.story_d_button.rect.center = (
            screen_rect.right / 1.14, screen_rect.centery)

        self.title_text.rect.center = (
            screen_rect.centerx, screen_rect.centery / 2)
        self.back_button.rect.center = (
            screen_rect.centerx / 3, screen_rect.centery / 5)

        self.story_a_text.rect.center = (
            screen_rect.centerx, screen_rect.centery * 1.35)
        self.story_b_text.rect.center = (
            screen_rect.centerx, screen_rect.centery * 1.35)
        self.story_c_text.rect.center = (
            screen_rect.centerx, screen_rect.centery * 1.35)
        self.story_d_text.rect.center = (
            screen_rect.centerx, screen_rect.centery * 1.35)
        
        self.no_button.rect.center = (
            screen_rect.centerx * 1.5, screen_rect.centery * 1.7)
        self.yes_button.rect.center = (
            screen_rect.centerx * 0.5, screen_rect.centery * 1.7)
        self.window_text.rect.center = (
            screen_rect.centerx, screen_rect.centery * 1.35)


        
        self.back_button.on_mouse_up_as_button = lambda: self.scene_manager.load_scene(
            "main_menu")
        

        self.instantiate(self.background)
        self.instantiate(self.title_text)
        self.instantiate(self.back_button)
        self.instantiate(self.story_a_button)
        self.instantiate(self.story_b_button)
        self.instantiate(self.story_c_button)
        self.instantiate(self.story_d_button)
        self.instantiate(self.story_a_text)
        self.instantiate(self.story_b_text)
        self.instantiate(self.story_c_text)
        self.instantiate(self.story_d_text)
        self.instantiate(self.yes_button)
        self.instantiate(self.no_button)
        self.instantiate(self.window_background)
        self.instantiate(self.window_text)

        return None
