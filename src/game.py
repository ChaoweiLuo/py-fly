import pygame
import sys
from src.scenes.game_scene import GameScene
from src.objects.animation import WelcomeAnimation

class Game:
    def __init__(self, player_type=1):
        """初始化游戏
        Args:
            player_type: 玩家飞机类型 (1,2,3)
        """
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("打飞机游戏")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_type = player_type
        
        # 游戏状态
        self.game_state = 'welcome'  # welcome, playing
        self.welcome_animation = WelcomeAnimation(self.screen_width, self.screen_height)
        self.current_scene = None
        
    def run(self):
        """运行游戏主循环"""
        while self.running:
            # 处理事件
            self.handle_events()
            
            # 更新游戏状态
            self.update()
            
            # 绘制游戏画面
            self.draw()
            
            # 控制帧率
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 开场动画时，按任意键跳过
            if self.game_state == 'welcome':
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.welcome_animation.finished = True
            
            if self.current_scene:
                self.current_scene.handle_event(event)
            
    def update(self):
        """更新游戏状态"""
        if self.game_state == 'welcome':
            self.welcome_animation.update()
            if self.welcome_animation.is_finished():
                # 开场动画结束，开始游戏
                self.game_state = 'playing'
                self.current_scene = GameScene(self, self.player_type)
        elif self.game_state == 'playing' and self.current_scene:
            self.current_scene.update()
        
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill((0, 0, 0))  # 填充黑色背景
        
        if self.game_state == 'welcome':
            # 绘制开场动画
            self.welcome_animation.draw(self.screen)
        elif self.game_state == 'playing' and self.current_scene:
            # 绘制游戏场景
            self.current_scene.draw(self.screen)
            
            # 绘制FPS（右上角）
            fps = int(self.clock.get_fps())
            font = pygame.font.Font(None, 28)
            fps_text = font.render(f'FPS: {fps}', True, (255, 255, 255))
            fps_rect = fps_text.get_rect()
            fps_rect.topright = (self.screen_width - 10, 10)  # 右上角，留10像素边距
            self.screen.blit(fps_text, fps_rect)
        
        pygame.display.flip()