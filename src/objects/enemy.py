import pygame
import random

class Enemy:
    """基础敌人类"""
    def __init__(self, x, y):
        """初始化敌人"""
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 2
        self.color = (255, 0, 0)  # 红色
        self.direction = random.choice([-1, 1])  # 随机方向
        self.hp = 1  # 生命值
        
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
    """石头敌人 - 从上方落下"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 30
        self.height = 30
        self.speed = random.uniform(2, 5)  # 随机下落速度
        self.hp = 1
        self.emoji = "🪨"
        
    def update(self):
        """更新石头位置 - 直接向下落"""
        self.y += self.speed
        
    def draw(self, screen):
        """绘制石头"""
        font = pygame.font.Font(None, 36)
        text = font.render(self.emoji, True, (100, 100, 100))
        screen.blit(text, (self.x, self.y))


class EnemyPlane(Enemy):
    """敌方飞机 - 会发射子弹"""
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 40
        self.height = 40
        self.speed = 1.5
        self.hp = 2  # 敌机有2点生命值
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
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 80
        self.height = 80
        self.speed = 2
        self.hp = 50  # Boss有50点生命值
        self.direction = 1
        self.action_cooldown = 0
        self.action_delay = 90  # 行动间隔
        self.emoji = random.choice(["👹", "👺", "👻", "👾", "🤖"])
        
    def update(self):
        """更新Boss位置"""
        self.x += self.speed * self.direction
        
        # 边界检测
        if self.x <= 0 or self.x >= 800 - self.width:
            self.direction *= -1
        
        # 更新行动冷却
        self.action_cooldown += 1
        
    def draw(self, screen):
        """绘制Boss"""
        # 绘制Boss表情
        font = pygame.font.Font(None, 72)
        text = font.render(self.emoji, True, (255, 0, 255))
        screen.blit(text, (self.x, self.y))
        
        # 绘制血条
        bar_width = self.width
        bar_height = 5
        health_ratio = max(0, self.hp / 50)
        pygame.draw.rect(screen, (255, 0, 0), 
                       (self.x, self.y - 10, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), 
                       (self.x, self.y - 10, bar_width * health_ratio, bar_height))
    
    def can_act(self):
        """检查是否可以执行行动"""
        if self.action_cooldown >= self.action_delay:
            self.action_cooldown = 0
            return True
        return False
    
    def perform_action(self):
        """执行随机行动 - 返回行动类型和对象"""
        action = random.choice(['shoot', 'throw_rock', 'summon_plane'])
        
        if action == 'shoot':
            # 发射子弹
            from src.objects.bullet import EnemyBullet
            bullets = [
                EnemyBullet(self.x + 20, self.y + self.height),
                EnemyBullet(self.x + 40, self.y + self.height),
                EnemyBullet(self.x + 60, self.y + self.height)
            ]
            return ('bullets', bullets)
        
        elif action == 'throw_rock':
            # 丢石头
            rocks = [
                Rock(self.x + random.randint(0, self.width), self.y + self.height)
            ]
            return ('rocks', rocks)
        
        elif action == 'summon_plane':
            # 召唤飞机
            plane = EnemyPlane(self.x + self.width // 2, self.y + self.height)
            return ('plane', plane)
        
        return (None, None)