import pygame
import json
import os
import ctypes # Get Resolution of PC


class Settings():
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        # Screen size
        self.screen_size = (1280, 720)

        # Key bindings
        self.key_left = pygame.K_LEFT
        self.key_right = pygame.K_RIGHT
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN
        self.key_select = pygame.K_RETURN
        self.key_cancel = pygame.K_ESCAPE

        # Colorblind mode
        self.colorblind_mode = False

        # load saved settings from file
        if os.path.isfile('settings.json'):
            try:
                with open('settings.json', 'r') as f:
                    saved_settings = json.load(f)
                    
                # Update settings with saved values
                self.screen_size = saved_settings.get('screen_size', self.screen_size)
                self.key_left = saved_settings.get('key_left', self.key_left)
                self.key_right = saved_settings.get('key_right', self.key_right)
                self.key_up = saved_settings.get('key_up', self.key_up)
                self.key_down = saved_settings.get('key_down', self.key_down)
                self.key_select = saved_settings.get('key_select', self.key_select)
                self.key_cancel = saved_settings.get('key_cancel', self.key_cancel)
                self.colorblind_mode = saved_settings.get('colorblind_mode', self.colorblind_mode)
            except:
                # Error occurred while loading settings from file
                pass

        return super().__init__()

    # Settings reset method
    def reset(self):
        # Screen size
        self.screen_size = (1280, 720)

        # Key bindings
        self.key_left = pygame.K_LEFT
        self.key_right = pygame.K_RIGHT
        self.key_up = pygame.K_UP
        self.key_down = pygame.K_DOWN
        self.key_select = pygame.K_RETURN
        self.key_cancel = pygame.K_ESCAPE

        # Colorblind mode
        self.colorblind_mode = False

        return self

    # Settings save method
    def save_settings(self):
        # Create a dictionary of current settings
        settings_dict = {
            'screen_size': self.screen_size,
            'key_left': self.key_left,
            'key_right': self.key_right,
            'key_up': self.key_up,
            'key_down': self.key_down,
            'key_select': self.key_select ,
            'key_cancel':self.key_cancel,
            'colorblind_mode':self.colorblind_mode
        }

        try:
            # Save settings to file
            with open("settings.json", 'w') as f:
                json.dump(settings_dict, f)
        except:
            # Return -1 if an error occurred
            return -1

        # Return 0 if save was successful
        return 0

    # 800*600 Screen
    def SVGA(self):
        self.screen_size = (800, 600)

        return self
    
    # 1280*720 Screen
    def HD(self):
        self.screen_size = (1280, 720)
        
        return self
    
    # 1920*1080 Screen
    def FHD(self):
        self.screen_size = (1920, 1080)

        return self
    
    # Fullscreen
    def fullScreen(self):
        user32 = ctypes.windll.user32
        self.screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) # Get resolution
        self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)  # Fullscreen setting

        return self
    
    