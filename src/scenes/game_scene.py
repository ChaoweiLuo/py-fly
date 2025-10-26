import pygame
import random
from src.objects.player import Player
from src.objects.enemy import Enemy, Rock, EnemyPlane, Boss
from src.objects.bullet import EnemyBullet

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
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 60  # 生成敌人的间隔
        self.boss_spawned = False
        
        # 初始生成一些敌人
        self._spawn_initial_enemies()
            
    def _spawn_initial_enemies(self):
        """初始生成敌人"""
        for i in range(3):
            enemy_type = random.choice(['rock', 'plane'])
            x = random.randint(50, 750)
            
            if enemy_type == 'rock':
                self.enemies.append(Rock(x, -50))
            elif enemy_type == 'plane':
                self.enemies.append(EnemyPlane(x, -50))
    
    def _spawn_enemy(self):
        """随机生成敌人"""
        x = random.randint(50, 750)
        
        # 根据分数决定Boss是否出现
        if self.score >= 50 and not self.boss_spawned:
            self.enemies.append(Boss(x, -80))
            self.boss_spawned = True
        else:
            enemy_type = random.choices(
                ['rock', 'plane', 'normal'],
                weights=[40, 35, 25]  # 权重
            )[0]
            
            if enemy_type == 'rock':
                self.enemies.append(Rock(x, -50))
            elif enemy_type == 'plane':
                self.enemies.append(EnemyPlane(x, -50))
            else:
                self.enemies.append(Enemy(x, -50))
            
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = self.player.shoot()
                self.bullets.append(bullet)
                
        self.player.handle_event(event)
        
    def update(self):
        """更新游戏状态"""
        # 检查玩家是否死亡
        if self.player.is_dead():
            print(f"游戏结束！最终得分: {self.score}")
            # TODO: 处理游戏结束逻辑
        
        self.player.update()
        
        # 更新生成敌人计时器
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self._spawn_enemy()
            self.spawn_timer = 0
        
        # 更新玩家子弹
        for bullet in self.bullets[:]:
            bullet.update()
            # 移除超出屏幕的子弹
            if bullet.y < 0:
                self.bullets.remove(bullet)
        
        # 更新敌人子弹
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            # 移除超出屏幕的子弹
            if bullet.y > 600:
                self.enemy_bullets.remove(bullet)
                
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
                self.enemies.remove(enemy)
                self.score += 10
                if isinstance(enemy, Boss):
                    self.score += 100
                    self.boss_spawned = False
            
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
        
        # 绘制分数和生命值
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        hp_text = font.render(f'HP: {self.player.hp}/{self.player.max_hp}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(hp_text, (10, 50))
            
    def check_collisions(self):
        """检查碰撞"""
        # 检查玩家子弹和敌人的碰撞
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if self._check_collision(bullet, enemy):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    enemy.take_damage(1)
                    break
        
        # 检查敌人子弹和玩家的碰撞
        for bullet in self.enemy_bullets[:]:
            if self._check_collision(bullet, self.player):
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                self.player.take_damage(1)
        
        # 检查敌人和玩家的碰撞
        for enemy in self.enemies[:]:
            if self._check_collision(enemy, self.player):
                # 玩家受伤
                self.player.take_damage(1)
                # 敌人也受伤
                enemy.take_damage(1)
    
    def _check_collision(self, obj1, obj2):
        """检查两个对象是否碰撞"""
        return (abs(obj1.x - obj2.x) < 30 and 
                abs(obj1.y - obj2.y) < 30)