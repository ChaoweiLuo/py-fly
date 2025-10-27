import pygame
import math

class Bullet:
    """玩家普通子弹"""
    def __init__(self, x, y):
        """初始化子弹"""
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 10
        self.color = (255, 255, 0)  # 黄色
        self.damage = 1  # 伤害值
        
    def update(self):
        """更新子弹位置"""
        self.y -= self.speed
        
    def draw(self, screen):
        """绘制子弹"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class TripleBullet(Bullet):
    """三连发子弹 - 一次发射三发"""
    def __init__(self, x, y, offset=0):
        """初始化三连发子弹
        Args:
            x: x坐标
            y: y坐标
            offset: 偏移量（-1左，0中，1右）
        """
        super().__init__(x, y)
        self.offset = offset
        self.x = x + offset * 15  # 根据偏移调整位置
        self.color = (0, 255, 255)  # 青色
        self.damage = 1


class ShotgunBullet(Bullet):
    """散弹枪子弹 - 扇形发射"""
    def __init__(self, x, y, angle=0):
        """初始化散弹枪子弹
        Args:
            x: x坐标
            y: y坐标
            angle: 发射角度（度数）
        """
        super().__init__(x, y)
        self.angle = math.radians(angle)  # 转换为弧度
        self.speed = 12
        self.color = (255, 165, 0)  # 橙色
        self.damage = 0.5  # 单发伤害较低
        self.width = 4
        self.height = 8
    
    def update(self):
        """更新散弹位置 - 按角度飞行"""
        self.x += self.speed * math.sin(self.angle)
        self.y -= self.speed * math.cos(self.angle)


class GiantBullet(Bullet):
    """巨型子弹 - 威力大，体积大"""
    def __init__(self, x, y):
        """初始化巨型子弹"""
        super().__init__(x, y)
        self.width = 20
        self.height = 30
        self.speed = 8  # 速度较慢
        self.color = (255, 50, 50)  # 红色
        self.damage = 5  # 高伤害
        self.glow_radius = 0  # 光晕效果
    
    def update(self):
        """更新巨型子弹位置"""
        self.y -= self.speed
        self.glow_radius = (self.glow_radius + 1) % 10  # 光晕动画
    
    def draw(self, screen):
        """绘制巨型子弹 - 带光晕效果"""
        # 绘制光晕
        for i in range(3):
            alpha = 100 - i * 30
            radius = self.width // 2 + self.glow_radius + i * 3
            glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.color, alpha), 
                             (radius, radius), radius)
            screen.blit(glow_surface, 
                       (self.x + self.width // 2 - radius, 
                        self.y + self.height // 2 - radius))
        
        # 绘制主体
        pygame.draw.ellipse(screen, self.color, 
                          (self.x, self.y, self.width, self.height))
        # 绘制高光
        pygame.draw.ellipse(screen, (255, 200, 200), 
                          (self.x + 5, self.y + 5, self.width - 10, self.height - 15))

class ShotgunGiantBullet(ShotgunBullet):
    """散弹枪巨型子弹 - 组合了散弹枪和巨型子弹的特性"""
    def __init__(self, x, y, angle=0):
        """初始化散弹枪巨型子弹
        Args:
            x: x坐标
            y: y坐标
            angle: 发射角度（度数）
        """
        super().__init__(x, y, angle)
        self.angle = math.radians(angle)  # 转换为弧度
        self.speed = 1
        self.color = (255, 165, 0)  # 橙色
        self.damage = 2.5  # 单发伤害较低
        self.width = 8
        self.height = 12
        self.glow_radius = 0

    def update(self):
        """更新散弹枪巨型子弹位置 - 按角度飞行"""
        super().update()
        self.x += self.speed * math.sin(self.angle)
        self.y -= self.speed * math.cos(self.angle)
    def draw(self, screen):
        """绘制散弹枪巨型子弹 - 带光晕效果"""
        # 绘制光晕
        for i in range(3):
            alpha = 100 - i * 30
            radius = self.width // 2 + self.glow_radius + i * 3
            glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.color, alpha), 
                             (radius, radius), radius)
            screen.blit(glow_surface, 
                       (self.x + self.width // 2 - radius, 
                        self.y + self.height // 2 - radius))
        # 绘制主体
        pygame.draw.ellipse(screen, self.color, 
                          (self.x, self.y, self.width, self.height))
        # 绘制高光
        pygame.draw.ellipse(screen, (255, 200, 200), 
                          (self.x + 5, self.y + 5, self.width - 10, self.height - 15))
        
class EnemyBullet:
    """敌人子弹 - 向下飞行"""
    def __init__(self, x, y):
        """初始化敌人子弹"""
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 5
        self.color = (255, 100, 100)  # 淡红色
        self.damage = 1
        
    def update(self):
        """更新子弹位置 - 向下移动"""
        self.y += self.speed
        
    def draw(self, screen):
        """绘制敌人子弹"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class BossShotgunBullet:
    """Boss散弹子弹 - 按角度飞行"""
    def __init__(self, x, y, angle=0):
        """初始化Boss散弹
        Args:
            x: x坐标
            y: y坐标
            angle: 发射角度（度数）
        """
        self.x = x
        self.y = y
        self.angle = math.radians(angle + 90)  # 转换为弧度，+90使0度向下
        self.speed = 6
        self.color = (255, 0, 255)  # 紫色
        self.damage = 1
        self.width = 6
        self.height = 6
    
    def update(self):
        """更新子弹位置 - 按角度飞行"""
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
    
    def draw(self, screen):
        """绘制Boss散弹"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)