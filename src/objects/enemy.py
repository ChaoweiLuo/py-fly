import pygame
import random
import os

class Enemy:
    """基础敌人类"""
    def __init__(self, x, y, level=1):
        """初始化敌人
        Args:
            x: x坐标
            y: y坐标
            level: 关卡等级 (1-3)
        """
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 2
        self.color = (255, 0, 0)  # 红色
        self.direction = random.choice([-1, 1])  # 随机方向
        self.level = level
        self.hp = level  # 生命值等于关卡等级
        self.max_hp = level
        
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
    
    def is_dead(self):
        """检查是否死亡"""
        return self.hp <= 0
    
    def take_damage(self, damage=1):
        """受到伤害"""
        self.hp -= damage


class Rock(Enemy):
    """石头敌人 - 从上方落下，随机形状"""
    def __init__(self, x, y, level=1):
        super().__init__(x, y, level)
        self.width = 30
        self.height = 30
        self.speed = random.uniform(2, 5)  # 随机下落速度
        self.hp = level
        self.max_hp = level
        # 随机选择形状类型
        self.shape_type = random.choice(['circle', 'triangle', 'diamond', 'hexagon', 'star'])
        self.rotation = random.randint(0, 360)  # 随机旋转角度
        self.color = random.choice([
            (139, 69, 19),   # 棕色
            (128, 128, 128), # 灰色
            (105, 105, 105), # 暗灰色
            (169, 169, 169), # 淡灰色
            (160, 82, 45),   # 赭石色
        ])
        
    def update(self):
        """更新石头位置 - 直接向下落"""
        self.y += self.speed
        self.rotation += 2  # 缓慢旋转
        
    def draw(self, screen):
        """绘制石头 - 根据形状类型绘制不同形状"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        if self.shape_type == 'circle':
            # 圆形
            pygame.draw.circle(screen, self.color, (int(center_x), int(center_y)), self.width // 2)
            pygame.draw.circle(screen, (80, 80, 80), (int(center_x), int(center_y)), self.width // 2, 2)
            
        elif self.shape_type == 'triangle':
            # 三角形
            points = [
                (center_x, self.y),
                (self.x, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (80, 80, 80), points, 2)
            
        elif self.shape_type == 'diamond':
            # 菱形
            points = [
                (center_x, self.y),
                (self.x + self.width, center_y),
                (center_x, self.y + self.height),
                (self.x, center_y)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (80, 80, 80), points, 2)
            
        elif self.shape_type == 'hexagon':
            # 六边形
            import math
            points = []
            for i in range(6):
                angle = math.radians(60 * i + self.rotation)
                px = center_x + self.width // 2 * math.cos(angle)
                py = center_y + self.height // 2 * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (80, 80, 80), points, 2)
            
        elif self.shape_type == 'star':
            # 星形
            import math
            points = []
            for i in range(10):
                angle = math.radians(36 * i + self.rotation)
                radius = (self.width // 2) if i % 2 == 0 else (self.width // 4)
                px = center_x + radius * math.cos(angle - math.pi / 2)
                py = center_y + radius * math.sin(angle - math.pi / 2)
                points.append((px, py))
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (80, 80, 80), points, 2)


class EnemyPlane(Enemy):
    """敌方飞机 - 会发射子弹"""
    def __init__(self, x, y, level=1):
        super().__init__(x, y, level)
        self.width = 40
        self.height = 40
        self.speed = 1.5
        self.hp = level * 2  # 敌机血量是关卡等级的2倍
        self.max_hp = level * 2
        self.shoot_cooldown = 0
        self.shoot_delay = random.randint(60, 120)  # 随机射击间隔
        self.direction = random.choice([-1, 1])
        
    def update(self):
        """更新敌机位置"""
        self.x += self.speed * self.direction
        self.y += 0.5  # 缓慢向下移动
        
        # 边界检测
        if self.x <= 0 or self.x >= 800 - self.width:
            self.direction *= -1
        
        # 更新射击冷却
        self.shoot_cooldown += 1
        
    def draw(self, screen):
        """绘制敌机"""
        # 绘制飞机主体
        pygame.draw.polygon(screen, (200, 0, 0), [
            (self.x + self.width // 2, self.y + self.height),  # 底部
            (self.x, self.y),  # 左上角
            (self.x + self.width, self.y)  # 右上角
        ])
        # 绘制机翼
        pygame.draw.rect(screen, (150, 0, 0), 
                       (self.x + 5, self.y + 10, self.width - 10, 8))
    
    def can_shoot(self):
        """检查是否可以射击"""
        if self.shoot_cooldown >= self.shoot_delay:
            self.shoot_cooldown = 0
            self.shoot_delay = random.randint(60, 120)
            return True
        return False
    
    def shoot(self):
        """射击 - 返回敌人子弹"""
        from src.objects.bullet import EnemyBullet
        return EnemyBullet(self.x + self.width // 2, self.y + self.height)


class Boss(Enemy):
    """Boss - 怪物，能发射子弹、丢石头、召唤飞机"""
    def __init__(self, x, y, level=1):
        super().__init__(x, y, level)
        self.width = 80
        self.height = 80
        self.speed_x = 2  # 水平移动速度
        self.speed_y = 1.5  # 垂直移动速度
        self.level = level
        self.hp = level * 100  # Boss血量是关卡等级的00個
        self.max_hp = level * 100
        self.direction_x = 1  # 水平方向
        self.direction_y = 1  # 垂直方向
        self.action_cooldown = 0
        self.action_delay = 60  # 行动间隔更频繁
        
        # Boss出现在屏幕上方
        self.y = 50
        
        # 加载Boss图片
        self.image = None
        self._load_boss_image(level)
    
    def _load_boss_image(self, level):
        """加载Boss图片"""
        try:
            image_path = os.path.join("assets", "images", "enemy", "boss", f"{level}.bmp")
            if os.path.exists(image_path):
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                print(f"成功加载Boss图片: {image_path}")
            else:
                print(f"Boss图片不存在: {image_path}，使用默认绘制")
                self.image = None
        except Exception as e:
            print(f"加载Boss图片失败: {e}")
            self.image = None
        
    def update(self):
        """更新Boss位置 - 在屏幕上半部分上下左右移动"""
        # 水平移动
        self.x += self.speed_x * self.direction_x
        
        # 水平边界检测
        if self.x <= 0 or self.x >= 800 - self.width:
            self.direction_x *= -1
        
        # 垂直移动
        self.y += self.speed_y * self.direction_y
        
        # 垂直边界检测（只在屏幕上半部分移动）
        # 上边界: 50像素，下边界: 300像素（屏幕一半）
        if self.y <= 50:
            self.direction_y = 1  # 向下移动
        elif self.y >= 250:  # 留出空间给Boss高度
            self.direction_y = -1  # 向上移动
        
        # 更新行动冷却
        self.action_cooldown += 1
        
    def draw(self, screen):
        """绘制Boss"""
        if self.image:
            # 使用图片绘制Boss
            screen.blit(self.image, (self.x, self.y))
        else:
            # 使用默认绘制
            pygame.draw.rect(screen, (255, 0, 255), (self.x, self.y, self.width, self.height))
        
        # 绘制血条
        bar_width = self.width
        bar_height = 8
        health_ratio = max(0, self.hp / self.max_hp)
        pygame.draw.rect(screen, (255, 0, 0), 
                       (self.x, self.y - 15, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                       (self.x, self.y - 15, bar_width * health_ratio, bar_height))
        
        # 显示Boss血量数值
        font = pygame.font.Font(None, 20)
        hp_text = font.render(f'{int(self.hp)}/{self.max_hp}', True, (255, 255, 255))
        screen.blit(hp_text, (self.x + 5, self.y - 30))
    
    def can_act(self):
        """检查是否可以执行行动"""
        if self.action_cooldown >= self.action_delay:
            self.action_cooldown = 0
            return True
        return False
    
    def perform_action(self):
        """执行随机行动 - 返回行动类型和对象"""
        action = random.choice(['shoot', 'scatter_shot', 'triple_shot', 'throw_rock', 'summon_plane'])
        
        if action == 'shoot':
            # 发射普通子弹
            from src.objects.bullet import EnemyBullet
            bullets = [
                EnemyBullet(self.x + 20, self.y + self.height),
                EnemyBullet(self.x + 40, self.y + self.height),
                EnemyBullet(self.x + 60, self.y + self.height)
            ]
            return ('bullets', bullets)
        
        elif action == 'scatter_shot':
            # 散弹攻击 - 多方向射击
            from src.objects.bullet import BossShotgunBullet
            bullets = []
            center_x = self.x + self.width // 2
            # 发射扇形散弹
            for angle in range(-60, 70, 20):  # -60度到60度，间陔20度
                bullets.append(BossShotgunBullet(center_x, self.y + self.height, angle))
            return ('bullets', bullets)
        
        elif action == 'triple_shot':
            # 三连发弹幕
            from src.objects.bullet import EnemyBullet
            bullets = []
            for i in range(5):  # 5条线，每条线3发
                x_pos = self.x + i * 20
                for j in range(3):
                    bullets.append(EnemyBullet(x_pos, self.y + self.height + j * 15))
            return ('bullets', bullets)
        
        elif action == 'throw_rock':
            # 丢石头
            rocks = []
            for i in range(3):  # 一次丢3个石头
                rocks.append(Rock(self.x + random.randint(0, self.width), self.y + self.height, self.level))
            return ('rocks', rocks)
        
        elif action == 'summon_plane':
            # 召唤飞机
            plane = EnemyPlane(self.x + self.width // 2, self.y + self.height, self.level)
            return ('plane', plane)
        
        return (None, None)