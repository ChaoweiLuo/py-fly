import pygame
import random
from src.objects.player import Player
from src.objects.enemy import Enemy, Rock, EnemyPlane, Boss
from src.objects.bullet import EnemyBullet
from src.objects.explosion import Explosion

class GameScene:
    def __init__(self, game, player_type=1):
        """初始化游戏场景
        Args:
            game: 游戏主对象
            player_type: 玩家飞机类型 (1 或 2)
        """
        self.game = game
        self.player = Player(game.screen_width // 2, game.screen_height - 50, player_type)
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []  # 敌人子弹列表
        self.explosions = []  # 爆炸效果列表
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 60  # 生成敌人的间隔
        
        # 关卡系统
        self.current_level = 1  # 当前关卡 (1-3)
        self.enemies_killed = 0  # 当前关卡击杀的敌人数
        self.boss_spawned = False  # 当前关卡Boss是否已出现
        self.boss_defeated = False  # Boss是否被击败
        
        # 初始生成一些敌人
        self._spawn_initial_enemies()
            
    def _spawn_initial_enemies(self):
        """初始生成敌人"""
        for i in range(3):
            enemy_type = random.choice(['rock', 'plane'])
            x = random.randint(50, 750)
            
            if enemy_type == 'rock':
                self.enemies.append(Rock(x, -50, self.current_level))
            elif enemy_type == 'plane':
                self.enemies.append(EnemyPlane(x, -50, self.current_level))
    
    def _spawn_enemy(self):
        """随机生成敌人"""
        x = random.randint(50, 750)
        
        # 检查是否应该生成Boss（击杀100个小怪且Boss未出现）
        if self.enemies_killed >= 100 and not self.boss_spawned:
            boss = Boss(x, -80, self.current_level)
            self.enemies.append(boss)
            self.boss_spawned = True
            print(f"第{self.current_level}关Boss出现！")
        elif not self.boss_spawned:  # Boss未出现时才生成普通敌人
            enemy_type = random.choices(
                ['rock', 'plane', 'normal'],
                weights=[40, 35, 25]  # 权重
            )[0]
            
            if enemy_type == 'rock':
                self.enemies.append(Rock(x, -50, self.current_level))
            elif enemy_type == 'plane':
                self.enemies.append(EnemyPlane(x, -50, self.current_level))
            else:
                self.enemies.append(Enemy(x, -50, self.current_level))
            
    def handle_event(self, event):
        """处理事件"""
        # 手动射击（仅在非自动模式下有效）
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.player.auto_shoot:
                bullets = self.player.shoot()  # 现在返回子弹列表
                self.bullets.extend(bullets)  # 添加所有子弹
                
        self.player.handle_event(event)
        
    def update(self):
        """更新游戏状态"""
        # 检查玩家是否死亡
        if self.player.is_dead():
            print(f"游戏结束！最终得分: {self.score}")
            # TODO: 处理游戏结束逻辑
        
        self.player.update()
        
        # 自动射击
        if self.player.can_auto_shoot():
            bullets = self.player.shoot()
            self.bullets.extend(bullets)
        
        # 更新生成敌人计时器
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self._spawn_enemy()
            self.spawn_timer = 0
        
        # 更新玩家子弹
        for bullet in self.bullets[:]:
            bullet.update()
            # 移除超出屏幕的子弹（包括左右边界）
            if bullet.y < -50 or bullet.x < -50 or bullet.x > 850:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
        
        # 更新敌人子弹
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            # 移除超出屏幕的子弹
            if bullet.y > 600:
                self.enemy_bullets.remove(bullet)
        
        # 更新爆炸效果
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
                
        # 更新敌人
        for enemy in self.enemies[:]:
            enemy.update()
            
            # 敌机射击
            if isinstance(enemy, EnemyPlane) and enemy.can_shoot():
                self.enemy_bullets.append(enemy.shoot())
            
            # Boss行动
            if isinstance(enemy, Boss) and enemy.can_act():
                action_type, action_data = enemy.perform_action()
                if action_type == 'bullets':
                    if isinstance(action_data, list):
                        self.enemy_bullets.extend(action_data)
                elif action_type == 'rocks':
                    if isinstance(action_data, list):
                        self.enemies.extend(action_data)
                elif action_type == 'plane':
                    if action_data is not None:
                        self.enemies.append(action_data)
            
            # 移除死亡的敌人
            if enemy.is_dead():
                # 创建爆炸效果
                explosion_size = enemy.width if hasattr(enemy, 'width') else 30
                explosion = Explosion(enemy.x + explosion_size // 2, enemy.y + explosion_size // 2, explosion_size)
                self.explosions.append(explosion)
                
                self.enemies.remove(enemy)
                
                # 如果是Boss
                if isinstance(enemy, Boss):
                    self.score += 500
                    self.boss_defeated = True
                    print(f"第{self.current_level}关Boss被击败！")
                    
                    # 检查是否进入下一关
                    if self.current_level < 3:
                        self.current_level += 1
                        self.enemies_killed = 0
                        self.boss_spawned = False
                        self.boss_defeated = False
                        print(f"进入第{self.current_level}关！")
                    else:
                        print("恭喜通关！")
                else:
                    # 普通敌人
                    self.score += 10
                    self.enemies_killed += 1
            
            # 移除超出屏幕的敌人
            if enemy.y > 600:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                
        # 检查碰撞
        self.check_collisions()
        
    def draw(self, screen):
        """绘制游戏画面"""
        self.player.draw(screen)
        
        # 绘制玩家子弹
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # 绘制敌人子弹
        for bullet in self.enemy_bullets:
            bullet.draw(screen)
            
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # 绘制爆炸效果
        for explosion in self.explosions:
            explosion.draw(screen)
        
        # 绘制分数和生命值
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        hp_text = font.render(f'HP: {self.player.hp}/{self.player.max_hp}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(hp_text, (10, 50))
        
        # 绘制关卡信息
        level_text = font.render(f'Level: {self.current_level}/3', True, (255, 215, 0))
        screen.blit(level_text, (10, 90))
        
        # 绘制敌人计数
        small_font = pygame.font.Font(None, 24)
        if not self.boss_spawned:
            kills_text = small_font.render(f'Kills: {self.enemies_killed}/100', True, (200, 200, 200))
            screen.blit(kills_text, (10, 130))
        else:
            boss_text = small_font.render('BOSS FIGHT!', True, (255, 0, 0))
            screen.blit(boss_text, (10, 130))
        
        # 绘制武器提示
        weapon_names = ['普通子弹', '三连发', '散弹枪', '巨型子弹']
        weapon_text = small_font.render(f'Weapon[1-4]: {weapon_names[self.player.weapon_type]}', 
                                       True, (200, 200, 200))
        screen.blit(weapon_text, (10, 160))
        
        # 绘制射击模式提示
        shoot_mode = '自动射击' if self.player.auto_shoot else '手动射击'
        mode_color = (0, 255, 0) if self.player.auto_shoot else (255, 255, 0)
        mode_text = small_font.render(f'Mode[A]: {shoot_mode}', True, mode_color)
        screen.blit(mode_text, (10, 185))
            
    def check_collisions(self):
        """检查碰撞"""
        # 检查玩家子弹和敌人的碰撞
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if self._check_collision(bullet, enemy):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    # 使用子弹的伤害值
                    damage = getattr(bullet, 'damage', 1)
                    enemy.take_damage(damage)
                    break
        
        # 检查敌人子弹和玩家的碰撞
        for bullet in self.enemy_bullets[:]:
            if self._check_collision(bullet, self.player):
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                damage = getattr(bullet, 'damage', 1)
                self.player.take_damage(damage)
        
        # 检查敌人和玩家的碰撞
        for enemy in self.enemies[:]:
            if self._check_collision(enemy, self.player):
                # 玩家受伤
                self.player.take_damage(1)
                # 敌人也受伤
                enemy.take_damage(1)
    
    def _check_collision(self, obj1, obj2):
        """检查两个对象是否碰撞 - 考虑对象大小"""
        # 获取对象的宽高，默认值为30
        obj1_width = getattr(obj1, 'width', 30)
        obj1_height = getattr(obj1, 'height', 30)
        obj2_width = getattr(obj2, 'width', 30)
        obj2_height = getattr(obj2, 'height', 30)
        
        # 矩形碰撞检测
        return (obj1.x < obj2.x + obj2_width and
                obj1.x + obj1_width > obj2.x and
                obj1.y < obj2.y + obj2_height and
                obj1.y + obj1_height > obj2.y)