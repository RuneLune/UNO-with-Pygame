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
from gameobj.story.keyinput import KeyInput
from gameobj.story.backbtn import BackButton
from manager.storymgr import StoryManager
from gameobj.story.cat import Cat

from gameobj.story.background import StoryBack

from gameobj.story.lock import Locker



class StoryScene(Scene):
    @overrides
    def start(self) -> None:
        self.touchable = StoryManager().get_stage_states().get("touchable")
        self.screen_rect = pygame.display.get_surface().get_rect()
        background_surface = pygame.Surface(self.screen_rect.size)
        background_surface.fill(color.light_gray)
        title_font = pygame.font.Font(
            font_resource("MainFont.ttf"), self.screen_rect.height // 5
        )
        menu_font = pygame.font.Font(
            font_resource("MainFont.ttf"), self.screen_rect.height // 12
        )
        
        self.background = GameObject(
            background_surface, "StoryScene_Background", z_index=-999)
        self.title_text = TextObject(
            "Story", title_font, color.white, "StoryScene_TitleText", z_index=997)
        self.back_button = BackButton(
            "◀ Back", menu_font, color.white, "StoryScene_BackButton", z_index=997).attach_mgr(self.scene_manager)

        self.cat = Cat()

        self.story_a_button = StoryAButton()
        self.story_b_button = StoryBButton()
        self.story_c_button = StoryCButton()
        self.story_d_button = StoryDButton()

        self.locker_b = Locker(name="b")
        self.locker_c = Locker(name="c")
        self.locker_d = Locker(name="d")

        self.story_a_text = StoryAText()
        self.story_b_text = StoryBText()
        self.story_c_text = StoryCText()
        self.story_d_text = StoryDText()
        
        self.yes_button = YesButton().attach_mgr(self.scene_manager)
        self.no_button = NoButton()
        self.window_text = WindowText()

        handle_window = HandleWindow()

        self.no_button.on_mouse_up_as_button = lambda: handle_window.invisible_window()
        self.yes_button.on_mouse_up = lambda: handle_window.invisible_window()
    

        self.window_background = WindowBackground()
        
        self.story_a_button.rect.center = (
            self.screen_rect.right / 4, self.screen_rect.centery * 1.1)
        self.story_b_button.rect.center = (
            self.screen_rect.right / 2, self.screen_rect.centery * 1.1)
        self.story_c_button.rect.center = (
            self.screen_rect.right / 1.35, self.screen_rect.centery * 1.1)
        self.story_d_button.rect.center = (
            self.screen_rect.right / 1.1, self.screen_rect.centery)
        
        self.locker_b.rect.center = (
            self.screen_rect.right / 2, self.screen_rect.centery * 1.1)
        self.locker_c.rect.center = (
            self.screen_rect.right / 1.35, self.screen_rect.centery * 1.1)
        self.locker_d.rect.center = (
            self.screen_rect.right / 1.1, self.screen_rect.centery)
        

        self.title_text.rect.center = (
            self.screen_rect.centerx, self.screen_rect.centery / 2)
        self.back_button.rect.center = (
            self.screen_rect.centerx / 3, self.screen_rect.centery / 5)

        self.story_a_text.rect.center = (
            self.screen_rect.centerx, self.screen_rect.centery / 2)
        self.story_b_text.rect.center = (
            self.screen_rect.centerx, self.screen_rect.centery / 2)
        self.story_c_text.rect.center = (
            self.screen_rect.centerx, self.screen_rect.centery / 2)
        self.story_d_text.rect.center = (
            self.screen_rect.centerx, self.screen_rect.centery / 2)
        
        self.no_button.rect.center = (
            self.screen_rect.centerx * 1.5, self.screen_rect.centery * 1.7)
        self.yes_button.rect.center = (
            self.screen_rect.centerx * 0.5, self.screen_rect.centery * 1.7)
        self.window_text.rect.center = (
            self.screen_rect.centerx, self.screen_rect.centery * 1.35)
        
    

        key_input = KeyInput()
        self.instantiate(key_input)

        self.temp_list = []
        self.temp_list.append(self.story_a_button)
        self.temp_list.append(self.story_b_button)
        self.temp_list.append(self.story_c_button)
        self.temp_list.append(self.story_d_button)
        self.stage_list = []
        for i in range(len(self.touchable)):
            if self.touchable[i]:
                self.stage_list.append(self.temp_list[i])
            else:
                break
        self.window_list = []
        self.window_list.append(self.yes_button)
        self.window_list.append(self.no_button)
        key_input.attach_stage(
            self.stage_list,
            self.window_list,
            self.back_button
        )
        

        self.instantiate(self.background)
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
        self.instantiate(self.locker_b)
        self.instantiate(self.locker_c)
        self.instantiate(self.locker_d)
        self.instantiate(self.cat)

        return None
