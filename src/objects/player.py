import pygame
from src.objects.bullet import Bullet
import os

class Player:
    def __init__(self, x, y, player_type=1):
        """初始化玩家
        Args:
            x: 初始x坐标
            y: 初始y坐标
            player_type: 玩家飞机类型 (1 或 2)，默认为1
        """
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.color = (0, 255, 0)  # 绿色
        self.player_type = player_type  # 记录飞机类型
        
        # 尝试加载对应类型的飞机图片
        self.image = None
        self._load_player_image(player_type)
        
    def _load_player_image(self, player_type):
        """加载玩家飞机图片"""
        try:
            if player_type == 1:
                image_path = os.path.join("assets", "images", "player.png")
                print("尝试加载第一个飞机样式: player.png")
            else:
                image_path = os.path.join("assets", "images", "player2.png")
                print("尝试加载第二个飞机样式: player2.png")
                
            if os.path.exists(image_path):
                print(f"找到图片文件: {image_path}")
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                print(f"成功加载飞机图片: {image_path}")
            else:
                print(f"图片文件不存在: {image_path}")
                # 如果指定的图片不存在，尝试加载默认的player.png
                default_path = os.path.join("assets", "images", "player.png")
                if os.path.exists(default_path):
                    print("尝试加载默认飞机图片")
                    self.image = pygame.image.load(default_path).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (self.width, self.height))
                    print(f"成功加载默认飞机图片: {default_path}")
                else:
                    print("默认图片也不存在，使用默认绘制")
        except Exception as e:
            # 如果加载失败，使用默认的矩形绘制
            print(f"加载飞机图片失败: {e}")
            print("使用默认绘制方式")
            self.image = None
        
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
        if self.image:
            # 使用图片绘制飞机
            screen.blit(self.image, (self.x, self.y))
        else:
            # 自定义绘制飞机形状
            # 机身
            pygame.draw.polygon(screen, self.color, [
                (self.x + self.width // 2, self.y),  # 顶部
                (self.x, self.y + self.height),      # 左下角
                (self.x + self.width, self.y + self.height)  # 右下角
            ])
            # 机翼
            pygame.draw.rect(screen, self.color, 
                           (self.x + 5, self.y + self.height - 15, 
                            self.width - 10, 10))
        
    def shoot(self):
        """射击"""
        return Bullet(self.x + self.width // 2, self.y)