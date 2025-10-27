import pygame
import pygame
from src.objects.bullet import Bullet, TripleBullet, ShotgunBullet, GiantBullet, ShotgunGiantBullet
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
        self.hp = 3  # 玩家生命值
        self.max_hp = 3  # 最大生命值
        self.weapon_type = 0  # 武器类型: 0-普通, 1-三连发, 2-散弹枪, 3-巨型子弹
        self.auto_shoot = True  # 自动射击开关
        self.shoot_cooldown = 0  # 射击冷却计时器
        self.shoot_delay = 15  # 射击间隔（帧数）
        
        # 无敌和闪烁系统
        self.invincible = False  # 是否无敌
        self.invincible_timer = 0  # 无敌计时器
        self.invincible_duration = 180  # 无敌持续时间（3秒 = 180帧）
        self.blink_timer = 0  # 闪烁计时器
        self.visible = True  # 是否可见（用于闪烁效果）
        
        # 尝试加载对应类型的飞机图片
        self.image = None
        self._load_player_image(player_type)
        
    def _load_player_image(self, player_type):
        """加载玩家飞机图片"""
        try:
            if player_type == 1:
                image_path = os.path.join("assets", "images", 'player', "1.bmp")
                print("尝试加载第一个飞机样式: player.bmp")
            elif player_type == 2:
                image_path = os.path.join("assets", "images", 'player', "2.bmp")
                print("尝试加载第二个飞机样式: player2.bmp")
            else:
                image_path = os.path.join("assets", "images", 'player', "3.bmp")
                print("尝试加载第二个飞机样式: player3.bmp")
                
            if os.path.exists(image_path):
                print(f"找到图片文件: {image_path}")
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
                print(f"成功加载飞机图片: {image_path}")
            else:
                print(f"图片文件不存在: {image_path}")
                # 如果指定的图片不存在，尝试加载默认的player.png
                default_path = os.path.join("assets", "images", 'player', "player.bmp")
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
        # 数字键切换武器类型
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.weapon_type = 0
                print("切换为：普通子弹")
            elif event.key == pygame.K_2:
                self.weapon_type = 1
                print("切换为：三连发子弹")
            elif event.key == pygame.K_3:
                self.weapon_type = 2
                print("切换为：散弹枪")
            elif event.key == pygame.K_4:
                self.weapon_type = 3
                print("切换为：巨型子弹")
            elif event.key == pygame.K_5:
                self.weapon_type = 4
                print("切换为：巨型散弹")
            elif event.key == pygame.K_a:
                # 切换自动/手动射击
                self.auto_shoot = not self.auto_shoot
                mode = "自动射击" if self.auto_shoot else "手动射击"
                print(f"切换为：{mode}")
        
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
        
        # 更新射击冷却
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        # 更新无敌状态
        if self.invincible:
            self.invincible_timer -= 1
            self.blink_timer += 1
            
            # 闪烁效果（每5帧切换一次可见性）
            if self.blink_timer % 5 == 0:
                self.visible = not self.visible
            
            # 无敌时间结束
            if self.invincible_timer <= 0:
                self.invincible = False
                self.visible = True
                self.blink_timer = 0
            
    def draw(self, screen):
        """绘制玩家"""
        # 如果不可见（闪烁状态），不绘制
        if not self.visible:
            return
        
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
        
        # 显示当前武器类型
        weapon_names = ['普通', '三连发', '散弹枪', '巨型', '巨型散弹']
        font = pygame.font.Font(None, 20)
        weapon_text = font.render(f'Weapon: {weapon_names[self.weapon_type]}', True, (255, 255, 255))
        screen.blit(weapon_text, (self.x - 10, self.y + self.height + 5))
        
    def shoot(self):
        """射击 - 根据武器类型返回不同的子弹"""
        # 检查冷却时间
        if self.shoot_cooldown > 0:
            return []
        
        # 设置冷却
        self.shoot_cooldown = self.shoot_delay
        
        center_x = self.x + self.width // 2
        shoot_y = self.y
        
        if self.weapon_type == 0:
            # 普通子弹
            return [Bullet(center_x, shoot_y)]
        
        elif self.weapon_type == 1:
            # 三连发子弹
            return [
                TripleBullet(center_x, shoot_y, -1),  # 左
                TripleBullet(center_x, shoot_y, 0),   # 中
                TripleBullet(center_x, shoot_y, 1)    # 右
            ]
        
        elif self.weapon_type == 2:
            # 散弹枪 - 5发扇形射击
            angles = [-30, -15, 0, 15, 30]  # 度数
            return [ShotgunBullet(center_x, shoot_y, angle) for angle in angles]
        
        elif self.weapon_type == 3:
            # 巨型子弹
            return [GiantBullet(center_x - 10, shoot_y - 20)]  # 调整位置使其居中
        elif self.weapon_type == 4:
            angles = [-30, -15, 0, 15, 30]  # 度数
            return [ShotgunGiantBullet(center_x, shoot_y, angle) for angle in angles]
        
        return [Bullet(center_x, shoot_y)]  # 默认返回普通子弹
    
    def can_auto_shoot(self):
        """检查是否可以自动射击"""
        return self.auto_shoot and self.shoot_cooldown == 0
    
    def take_damage(self, damage=1):
        """受到伤害"""
        # 如果处于无敌状态，不受伤害
        if self.invincible:
            return
        
        self.hp -= damage
        
        # 受伤后进入无敌状态
        self.invincible = True
        self.invincible_timer = self.invincible_duration
        self.blink_timer = 0
        self.visible = True
    
    def is_dead(self):
        """检查是否死亡"""
        return self.hp <= 0