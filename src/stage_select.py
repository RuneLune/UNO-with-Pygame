import pygame
import colors
import events
import pygame_gui

class Stage:
    def __init__(self, settings):
        self.__stage_num = 4
        self.__settings = settings
        self.__selected_stage = 0
        self.refresh()

        return super().__init__()

    def render(self):

        # screen size
        screen_size = self.__settings.get_screen_resolution()
        self.surface = pygame.Surface(screen_size)

        # font
        self.__title_font = pygame.font.Font("res/font/MainFont.ttf", round(screen_size[1] / 6))
        self.__back_font = pygame.font.Font("res/font/MainFont.ttf", round(screen_size[1] / 20))

        # title
        self.__title_text = self.__title_font.render("STAGE", True, colors.white)
        self.__title_rect = self.__title_text.get_rect()
        self.__title_rect.centerx = self.__screen.get_rect().centerx
        self.__title_rect.bottom = self.__screen.get_rect().centery / 2

        # back button
        self.__button_text.append(self.__back_font.render("◀ Back", True, colors.white))
        self.__button_rect.append(self.__button_text[-1].get_rect())
        self.__button_rect[0].right = self.__screen.get_rect().centerx / 3
        self.__button_rect[0].bottom = self.__screen.get_rect().centery / 5

        # stage image
        for i in range(self.__stage_num):
            image = pygame.image.load(f"res/img/stage/stage_{i+1}.png")
            self.__stage_img.append(image)
            self.__button_rect.append(self.__stage_img[i].get_rect())
            self.__button_rect[i+1].centery = self.__screen.get_rect().centery
            if i == 0:
                self.__button_rect[i+1].left =  self.__screen.get_rect().right/10
            elif i == 1:
                self.__button_rect[i+1].left =  self.__screen.get_rect().right/3.5
            elif i == 2: 
                self.__button_rect[i+1].left =  self.__screen.get_rect().right/2
            elif i == 3:
                self.__button_rect[i+1].right =  self.__screen.get_rect().right/1.2
        
        self.__selected_rect = pygame.Rect(0, 0, 130, 130)

        self.manager = pygame_gui.UIManager(screen_size)
        self.dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect(200, 150, 400, 200),
            manager=self.manager,
            window_title='Game Start',
            action_long_desc='Are you sure you want to start the game?',
            action_short_name='Start',
        )
            
            


    
    def refresh(self):
        pygame.display.set_caption("STAGE")
        flag = 0
        if self.__settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN        
        self.__screen = pygame.display.set_mode(self.__settings.get_screen_resolution(), flag)
        self.__button_text = []
        self.__button_rect = []
        self.__stage_img = []
        self.render()
        return None
    
    def draw(self):
        self.__screen.fill(colors.black)

        # title
        self.__screen.blit(self.__title_text, self.__title_rect)

        # back button
        self.__screen.blit(self.__button_text[0], self.__button_rect[0])

        # stage
        for i, img in enumerate(self.__stage_img):
            self.__screen.blit(img, self.__button_rect[i+1])
        
        # hover
        if self.__selected_stage != 0:
            # 첫 번째 메뉴 옵션을 제외한 나머지 메뉴 옵션 정보를 가져옴
            button_rects = self.__button_rect[1:]
            # 현재 선택된 메뉴 옵션의 위치와 크기 정보를 저장하는 객체
            selected_rect = pygame.Rect(0, 0, self.__selected_rect.width, self.__selected_rect.height)
            # 선택된 메뉴 옵션의 위치와 크기 정보를 현재 선택된 메뉴 옵션의 위치와 크기 정보로 설정
            selected_rect.center = button_rects[self.__selected_stage - 1].center
            # 화면에 선택된 메뉴 옵션에 흰색 테두리를 그림
            pygame.draw.rect(self.__screen, colors.white, selected_rect, 2)
        return None
    
    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__button_rect)):
                if self.__button_rect[i].collidepoint(mouse_pos):
                    self.__selected_stage = i
                    continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__button_rect)):
                if self.__button_rect[i].collidepoint(mouse_pos):
                    return self.__menu_func(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.__selected_stage -= 1
                if self.__selected_stage < 0:
                    self.__selected_stage = len(self.__button_rect) - 1
            elif event.key == pygame.K_DOWN:
                self.__selected_stage += 1
                if self.__selected_stage >= len(self.__button_rect):
                    self.__selected_stage = 0
            elif event.key == pygame.K_RETURN:
                return self.__menu_func(self.__selected_stage)

    
    def __menu_func(self, i):
        if i == 0:
            self.__settings.get_real_settings().update(previous_scene="stage")
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="main"))
        elif i == 1:
            self.manager.update(0)
            self.__screen.fill((255, 255, 255))
            self.manager.draw_ui(self.__screen)
            
            for event in pygame.event.get():
                # 다이얼로그 이벤트 처리
                self.manager.process_events(event)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # ESC 키를 누르면 다이얼로그를 닫음
                    self.dialog.hide()