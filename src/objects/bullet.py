import pygame

class Bullet:
    def __init__(self, x, y):
        """初始化子弹"""
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 10
        self.color = (255, 255, 0)  # 黄色
        
    def update(self):
        """更新子弹位置"""
        self.y -= self.speed
        
    def draw(self, screen):
        """绘制子弹"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))