import pygame
import colors
import events

class Stage:
    def __init__(self, settings):
        self.__stage_num = 4
        self.__settings = settings
        self.__is_confirm = False
        self.refresh()

        return super().__init__()

    def render(self):

        # screen size
        screen_size = self.__settings.get_screen_resolution()
        self.surface = pygame.Surface(screen_size)

        # font
        self.__title_font = pygame.font.Font("res/font/MainFont.ttf", round(screen_size[1] / 6))
        self.__back_font = pygame.font.Font("res/font/MainFont.ttf", round(screen_size[1] / 20))
        self.__imformation_font = pygame.font.Font("res/font/MainFont.ttf", round(screen_size[1] / 30))
        self.__window_font = pygame.font.Font("res/font/MainFont.ttf", round(screen_size[1] / 15))

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

        # 게임 정보
        for i in range(len(self.__imformation)):
            self.__imformation_text.append(self.__imformation_font.render(self.__imformation[i], True, colors.white))
        self.__imformation_rect = self.__imformation_text[-1].get_rect()
        self.__imformation_rect.top = self.__screen.get_rect().centery + 70
        self.__imformation_rect.left = self.__screen.get_rect().right/10


        # stage 
        self.button_rects = self.__touchable[1:] # 1번 인덱스는 back에 관련된 것이므로 1번부터 슬라이싱
        for i in range(self.__stage_num):
            if self.button_rects[i]:
                image = pygame.image.load(f"res/img/stage/stage_{i+1}.png")
            else:
                image = pygame.image.load(f"res/img/stage/stage_0.png")
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

        # window
        self.__window_text = self.__window_font.render("Do you want to start?", True, colors.black)
        self.__window_text_rect = self.__window_text.get_rect()
        self.__window_text_rect.top = self.__screen.get_rect().centery + 110
        self.__window_text_rect.center = self.__screen.get_rect().center

        self.__window_img.append(pygame.image.load(f"res/img/stage/yes.png"))
        self.__window_img.append(pygame.image.load(f"res/img/stage/no.png"))
        self.__window_rect.append(self.__window_img[0].get_rect())
        self.__window_rect.append(self.__window_img[1].get_rect())
        for i in range(len(self.__window_rect)):
            self.__window_rect[i].top = self.__screen.get_rect().centery + 200
            if i == 0:
                self.__window_rect[i].left = self.__screen.get_rect().right/10
            elif i == 1:
                self.__window_rect[i].right = self.__screen.get_rect().right/1.2

        self.__background = pygame.Surface((self.__screen.get_width(), self.__screen.get_height()))
        self.__background.fill((255, 255, 255))  
        self.__background.set_alpha(200) 

        
                
        # 하이라이트
        self.__selected_rect = pygame.Rect(0, 0, 130, 130)
        self.__selected_window_rect = pygame.Rect(0, 0, 130, 110)

        
    def refresh(self):
        pygame.display.set_caption("STAGE")
        flag = 0
        if self.__settings.get_settings().get("fullscreen", False) is True:
            flag |= pygame.FULLSCREEN        
        self.__screen = pygame.display.set_mode(self.__settings.get_screen_resolution(), flag)
        self.__button_text = []
        self.__button_rect = []
        self.__stage_img = []
        self.__window_img = []
        self.__imformation_text = []
        self.__imformation = [
            "첫분배에 컴퓨터가 기술 카드를 50% 더 높은 확률로 받음",
            "3명의 컴퓨터 플레이어와 대전, 카드는 같은 수로 분배 (첫 카드 제외)",
            "2명의 컴퓨터 플레이어와 대전, 매 5턴마다 낼 수 있는 카드 색 무작위 변경",
            "미정"
        ]
        # 첫번쨰 인덱스는 back 버튼을 위한 것. 2~5가 스테이지를 위한 엘리먼트들
        self.__touchable = [True, True, True, True, True]
        self.__window_rect = []
        self.__selected_stage = 0
        self.__selected_window = 0
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
            self.__screen.blit(self.__imformation_text[self.__selected_stage - 1], self.__imformation_rect)

        if self.__is_confirm:
            self.draw_window()
        return None
    
    def draw_window(self):

        self.__screen.blit(self.__background, (0, 0))

        self.__screen.blit(self.__window_text, self.__window_text_rect)

        for i, img in enumerate(self.__window_img):
            self.__screen.blit(img, self.__window_rect[i])


        selected_window_rect = pygame.Rect(0, 0, self.__selected_window_rect.width, self.__selected_window_rect.height)
        selected_window_rect.center = self.__window_rect[self.__selected_window].center
        pygame.draw.rect(self.__screen, colors.white, selected_window_rect, 2)
        

        
            
    def handle(self, event):
        if self.__is_confirm == False:
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(self.__button_rect)):
                    if self.__touchable[i] and self.__button_rect[i].collidepoint(mouse_pos):
                        self.__selected_stage = i
                        continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(self.__button_rect)):
                    if self.__touchable[i] and self.__button_rect[i].collidepoint(mouse_pos):
                        return self.__menu_func(i)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.__selected_stage -= 1
                    if self.__selected_stage < 0:
                        self.__selected_stage = len(self.__button_rect) - 1
                    while not self.__touchable[self.__selected_stage]:
                        self.__selected_stage -= 1
                        if self.__selected_stage < 0:
                            self.__selected_stage = len(self.__button_rect) - 1
                elif event.key == pygame.K_RIGHT:
                    self.__selected_stage += 1
                    if self.__selected_stage >= len(self.__button_rect):
                        self.__selected_stage = 0
                    while not self.__touchable[self.__selected_stage]:
                        self.__selected_stage += 1
                        if self.__selected_stage >= len(self.__button_rect):
                            self.__selected_stage = 0
                elif event.key == pygame.K_RETURN:
                    return self.__menu_func(self.__selected_stage)
                elif event.key == pygame.K_ESCAPE:
                    return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="main"))
        else:
            self.__window_handle(event, self.__selected_stage)

    def __window_handle(self, event, idx):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__window_rect)):
                if self.__window_rect[i].collidepoint(mouse_pos):
                    self.__selected_window = i
                    continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(self.__window_rect)):
                if self.__window_rect[i].collidepoint(mouse_pos):
                    return self.__window_func(i, idx)
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.__selected_window -= 1
                if self.__selected_window < 0:
                    self.__selected_window = len(self.__window_rect) - 1
            elif event.key == pygame.K_RIGHT:
                self.__selected_window += 1
                if self.__selected_window >= len(self.__window_rect):
                    self.__selected_window = 0
            elif event.key == pygame.K_RETURN:
                return self.__window_func(self.__selected_window, idx)
    
    def __menu_func(self, i):
        if i == 0:
            self.__settings.previous_stageselect()
            return pygame.event.post(pygame.event.Event(events.CHANGE_SCENE, target="main"))
        elif i == 1 or i == 2 or i == 3 or i == 4:
            self.__is_confirm = True
            pass
    
    def __window_func(self, i, idx):
        if i == 0:
            # 각 스테이지로 이동 idx 1부터 4까지 a~d 이동
            pass
        else:
            self.__is_confirm = False