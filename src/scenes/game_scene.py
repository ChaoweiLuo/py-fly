import pygame
from src.objects.player import Player
from src.objects.enemy import Enemy

class GameScene:
    def __init__(self, game):
        """初始化游戏场景"""
        self.game = game
        self.player = Player(game.screen_width // 2, game.screen_height - 50)
        self.enemies = []
        self.bullets = []
        
        # 创建一些敌人
        for i in range(5):
            enemy = Enemy(100 + i * 100, 50 + i * 30)
            self.enemies.append(enemy)
            
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = self.player.shoot()
                self.bullets.append(bullet)
                
        self.player.handle_event(event)
        
    def update(self):
        """更新游戏状态"""
        self.player.update()
        
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            # 移除超出屏幕的子弹
            if bullet.y < 0:
                self.bullets.remove(bullet)
                
        # 更新敌人
        for enemy in self.enemies:
            enemy.update()
            
        # 简单的碰撞检测
        self.check_collisions()
        
    def draw(self, screen):
        """绘制游戏画面"""
        self.player.draw(screen)
        
        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw(screen)
            
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(screen)
            
    def check_collisions(self):
        """检查碰撞"""
        # 检查子弹和敌人的碰撞
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (abs(bullet.x - enemy.x) < 20 and 
                    abs(bullet.y - enemy.y) < 20):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    break