import pygame
import random

class Enemy:
    def __init__(self, x, y):
        """初始化敌人"""
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 2
        self.color = (255, 0, 0)  # 红色
        self.direction = random.choice([-1, 1])  # 随机方向
        
    def update(self):
        """更新敌人位置"""
        self.x += self.speed * self.direction
        
        # 边界检测，碰到边界后改变方向并向下移动
        if self.x <= 0 or self.x >= 800 - self.width:
            self.direction *= -1
            self.y += 20
            
    def draw(self, screen):
        """绘制敌人"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))