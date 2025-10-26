import pygame
from src.objects.bullet import Bullet

class Player:
    def __init__(self, x, y):
        """初始化玩家"""
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.color = (0, 255, 0)  # 绿色
        
    def handle_event(self, event):
        """处理事件"""
        pass
        
    def update(self):
        """更新玩家状态"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < 800 - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < 600 - self.height:
            self.y += self.speed
            
    def draw(self, screen):
        """绘制玩家"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def shoot(self):
        """射击"""
        return Bullet(self.x + self.width // 2, self.y)