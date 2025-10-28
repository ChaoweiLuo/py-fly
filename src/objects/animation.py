import pygame
import random
import math
import sys
import os

class Animation:
    """动画基类"""
    def __init__(self):
        self.finished = False
        # 加载支持中文的字体
        self.chinese_font_cache = {}
    
    def get_chinese_font(self, size):
        """获取支持中文的字体"""
        if size in self.chinese_font_cache:
            return self.chinese_font_cache[size]
        
        try:
            # 尝试使用系统中文字体
            if sys.platform == 'win32':
                # Windows系统
                font_paths = [
                    'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
                    'C:/Windows/Fonts/simhei.ttf',  # 黑体
                    'C:/Windows/Fonts/simsun.ttc',  # 宋体
                ]
            elif sys.platform == 'darwin':
                # macOS系统
                font_paths = [
                    '/System/Library/Fonts/PingFang.ttc',
                    '/System/Library/Fonts/STHeiti Light.ttc',
                ]
            else:
                # Linux系统
                font_paths = [
                    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                    '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                ]
            
            # 尝试加载字体
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = pygame.font.Font(font_path, size)
                    self.chinese_font_cache[size] = font
                    return font
            
            # 如果没有找到字体文件，使用pygame默认字体
            print(f"警告: 未找到中文字体，使用默认字体")
            font = pygame.font.Font(None, size)
            self.chinese_font_cache[size] = font
            return font
            
        except Exception as e:
            print(f"加载字体失败: {e}，使用默认字体")
            font = pygame.font.Font(None, size)
            self.chinese_font_cache[size] = font
            return font
    
    def update(self):
        """更新动画"""
        pass
    
    def draw(self, screen):
        """绘制动画"""
        pass
    
    def is_finished(self):
        """检查动画是否结束"""
        return self.finished


class WelcomeAnimation(Animation):
    """开场欢迎动画"""
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.timer = 0
        self.duration = 180  # 3秒
        self.stars = []
        
        # 生成星星背景
        for i in range(50):
            self.stars.append({
                'x': random.randint(0, screen_width),
                'y': random.randint(0, screen_height),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.5, 2)
            })
    
    def update(self):
        """更新动画"""
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True
        
        # 更新星星
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > self.screen_height:
                star['y'] = 0
                star['x'] = random.randint(0, self.screen_width)
    
    def draw(self, screen):
        """绘制动画"""
        # 绘制星空背景
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), 
                             (int(star['x']), int(star['y'])), star['size'])
        
        # 标题淡入效果
        alpha = min(255, self.timer * 3)
        if self.timer > 120:  # 最后1秒淡出
            alpha = 255 - (self.timer - 120) * 4
        
        # 绘制标题 - 使用支持中文的字体
        title_font = self.get_chinese_font(80)
        subtitle_font = self.get_chinese_font(40)
        
        # 主标题
        title_text = title_font.render('打飞机游戏', True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 200))
        
        # 创建带透明度的surface
        title_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
        title_surface.fill((255, 215, 0, alpha))
        title_surface.blit(title_text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(title_surface, title_rect)
        
        # 副标题
        subtitle_text = subtitle_font.render('准备战斗！', True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 280))
        
        subtitle_surface = pygame.Surface(subtitle_text.get_size(), pygame.SRCALPHA)
        subtitle_surface.fill((255, 255, 255, alpha))
        subtitle_surface.blit(subtitle_text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(subtitle_surface, subtitle_rect)
        
        # 提示文字（闪烁效果）
        if self.timer > 60 and (self.timer // 15) % 2 == 0:
            hint_font = self.get_chinese_font(28)
            hint_text = hint_font.render('按任意键开始...', True, (200, 200, 200))
            hint_rect = hint_text.get_rect(center=(self.screen_width // 2, 400))
            screen.blit(hint_text, hint_rect)


class LevelIntroAnimation(Animation):
    """关卡介绍动画"""
    def __init__(self, screen_width, screen_height, level, player_score):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        self.player_score = player_score
        self.timer = 0
        self.duration = 120  # 2秒
        self.particles = []
        
        # 生成装饰粒子
        for i in range(30):
            self.particles.append({
                'x': random.randint(0, screen_width),
                'y': random.randint(-100, 0),
                'speed': random.uniform(2, 5),
                'size': random.randint(2, 5),
                'color': random.choice([(255, 215, 0), (255, 255, 255), (0, 255, 255)])
            })
    
    def update(self):
        """更新动画"""
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True
        
        # 更新粒子
        for particle in self.particles:
            particle['y'] += particle['speed']
            if particle['y'] > self.screen_height:
                particle['y'] = random.randint(-50, 0)
                particle['x'] = random.randint(0, self.screen_width)
    
    def draw(self, screen):
        """绘制动画"""
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # 绘制粒子
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), particle['size'])
        
        # 缩放效果
        scale = min(1.0, self.timer / 30)
        
        # 关卡标题 - 使用支持中文的字体
        level_font = self.get_chinese_font(100)
        level_text = level_font.render(f'第 {self.level} 关', True, (255, 215, 0))
        level_rect = level_text.get_rect(center=(self.screen_width // 2, 200))
        
        # 应用缩放
        scaled_width = int(level_text.get_width() * scale)
        scaled_height = int(level_text.get_height() * scale)
        if scaled_width > 0 and scaled_height > 0:
            scaled_text = pygame.transform.scale(level_text, (scaled_width, scaled_height))
            scaled_rect = scaled_text.get_rect(center=(self.screen_width // 2, 200))
            screen.blit(scaled_text, scaled_rect)
        
        # 提示信息
        if self.timer > 30:
            info_font = self.get_chinese_font(36)
            
            # 当前分数
            score_text = info_font.render(f'当前分数: {self.player_score}', True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.screen_width // 2, 300))
            screen.blit(score_text, score_rect)
            
            # 关卡提示
            hints = {
                1: '消灭 100 个敌人召唤Boss！',
                2: '敌人更强了，小心应对！',
                3: '最终关卡，全力以赴！'
            }
            hint_text = info_font.render(hints.get(self.level, '加油！'), True, (0, 255, 255))
            hint_rect = hint_text.get_rect(center=(self.screen_width // 2, 350))
            screen.blit(hint_text, hint_rect)


class LevelCompleteAnimation(Animation):
    """关卡完成动画"""
    def __init__(self, screen_width, screen_height, level, score, kills):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        self.score = score
        self.kills = kills
        self.timer = 0
        self.duration = 180  # 3秒
        self.fireworks = []
        
        # 生成烟花
        for i in range(5):
            self.fireworks.append({
                'x': random.randint(100, screen_width - 100),
                'y': random.randint(100, 300),
                'timer': random.randint(0, 60),
                'exploded': False,
                'particles': []
            })
    
    def update(self):
        """更新动画"""
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True
        
        # 更新烟花
        for firework in self.fireworks:
            firework['timer'] += 1
            if firework['timer'] > 30 and not firework['exploded']:
                firework['exploded'] = True
                # 生成爆炸粒子
                for i in range(30):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 6)
                    firework['particles'].append({
                        'x': firework['x'],
                        'y': firework['y'],
                        'vx': speed * math.cos(angle),
                        'vy': speed * math.sin(angle),
                        'life': 60,
                        'color': random.choice([
                            (255, 0, 0), (0, 255, 0), (0, 0, 255),
                            (255, 255, 0), (255, 0, 255), (0, 255, 255)
                        ])
                    })
            
            # 更新粒子
            for particle in firework['particles']:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.2  # 重力
                particle['life'] -= 1
    
    def draw(self, screen):
        """绘制动画"""
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # 绘制烟花
        for firework in self.fireworks:
            if not firework['exploded']:
                # 上升的火焰
                pygame.draw.circle(screen, (255, 200, 0), 
                                 (int(firework['x']), int(firework['y'])), 5)
            else:
                # 爆炸粒子
                for particle in firework['particles']:
                    if particle['life'] > 0:
                        alpha = int(255 * (particle['life'] / 60))
                        size = max(1, int(3 * (particle['life'] / 60)))
                        pygame.draw.circle(screen, particle['color'],
                                         (int(particle['x']), int(particle['y'])), size)
        
        # 标题 - 使用支持中文的字体
        title_font = self.get_chinese_font(80)
        title_text = title_font.render('关卡完成！', True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)
        
        # 统计信息
        info_font = self.get_chinese_font(40)
        y_offset = 250
        
        stats = [
            f'关卡: {self.level}',
            f'总分: {self.score}',
            f'击杀: {self.kills}',
        ]
        
        for stat in stats:
            stat_text = info_font.render(stat, True, (255, 255, 255))
            stat_rect = stat_text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 50
        
        # 提示文字
        if self.timer > 60:
            hint_font = self.get_chinese_font(32)
            hint_text = hint_font.render('准备进入下一关...', True, (0, 255, 255))
            hint_rect = hint_text.get_rect(center=(self.screen_width // 2, 450))
            screen.blit(hint_text, hint_rect)


class BossVictoryAnimation(Animation):
    """Boss战胜利动画（带烟花效果）"""
    def __init__(self, screen_width, screen_height, level):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        self.timer = 0
        self.duration = 150  # 2.5秒
        self.fireworks = []
        self.sparkles = []
        
        # 生成多个烟花
        for i in range(8):
            self.fireworks.append({
                'x': random.randint(100, screen_width - 100),
                'y': random.randint(50, 250),
                'delay': i * 15,  # 延迟爆炸
                'exploded': False,
                'particles': []
            })
        
        # 生成闪烁星星
        for i in range(100):
            self.sparkles.append({
                'x': random.randint(0, screen_width),
                'y': random.randint(0, screen_height),
                'size': random.randint(1, 4),
                'alpha': random.randint(100, 255),
                'speed': random.choice([-2, -1, 1, 2])
            })
    
    def update(self):
        """更新动画"""
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True
        
        # 更新烟花
        for firework in self.fireworks:
            if self.timer > firework['delay'] and not firework['exploded']:
                firework['exploded'] = True
                # 生成大量爆炸粒子
                for i in range(50):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(3, 8)
                    firework['particles'].append({
                        'x': firework['x'],
                        'y': firework['y'],
                        'vx': speed * math.cos(angle),
                        'vy': speed * math.sin(angle),
                        'life': random.randint(40, 80),
                        'max_life': 80,
                        'size': random.randint(2, 5),
                        'color': random.choice([
                            (255, 50, 50), (50, 255, 50), (50, 50, 255),
                            (255, 255, 50), (255, 50, 255), (50, 255, 255),
                            (255, 150, 50), (255, 255, 255)
                        ])
                    })
            
            # 更新粒子
            for particle in firework['particles'][:]:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.15  # 重力效果
                particle['vx'] *= 0.98  # 空气阻力
                particle['life'] -= 1
                if particle['life'] <= 0:
                    firework['particles'].remove(particle)
        
        # 更新闪烁星星
        for sparkle in self.sparkles:
            sparkle['alpha'] += sparkle['speed']
            if sparkle['alpha'] >= 255:
                sparkle['alpha'] = 255
                sparkle['speed'] = -abs(sparkle['speed'])
            elif sparkle['alpha'] <= 100:
                sparkle['alpha'] = 100
                sparkle['speed'] = abs(sparkle['speed'])
    
    def draw(self, screen):
        """绘制动画"""
        # 绘制半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 50, 200))
        screen.blit(overlay, (0, 0))
        
        # 绘制闪烁星星
        for sparkle in self.sparkles:
            color = (sparkle['alpha'], sparkle['alpha'], 255)
            pygame.draw.circle(screen, color,
                             (sparkle['x'], sparkle['y']), sparkle['size'])
        
        # 绘制烟花
        for firework in self.fireworks:
            for particle in firework['particles']:
                if particle['life'] > 0:
                    # 计算透明度和大小
                    alpha = int(255 * (particle['life'] / particle['max_life']))
                    size = max(1, int(particle['size'] * (particle['life'] / particle['max_life'])))
                    
                    # 绘制粒子（带光晕效果）
                    for glow in range(2, 0, -1):
                        glow_alpha = alpha // (3 - glow)
                        glow_color = tuple(min(255, c + 50) for c in particle['color'])
                        pygame.draw.circle(screen, glow_color,
                                         (int(particle['x']), int(particle['y'])), 
                                         size + glow)
                    
                    pygame.draw.circle(screen, particle['color'],
                                     (int(particle['x']), int(particle['y'])), size)
        
        # 胜利文字（脉冲效果）
        pulse = abs(math.sin(self.timer / 10)) * 20 + 60
        title_font = self.get_chinese_font(int(pulse) + 20)
        
        # 主标题
        title_text = title_font.render('Boss 击败！', True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 200))
        
        # 绘制发光效果
        glow_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
        for offset in range(5, 0, -1):
            alpha = 100 // offset
            glow_font = self.get_chinese_font(int(pulse) + 20)
            glow_text = glow_font.render('Boss 击败！', True, (255, 215, 0, alpha))
            glow_rect = glow_text.get_rect(center=(self.screen_width // 2, 200))
            screen.blit(glow_text, (glow_rect.x - offset, glow_rect.y - offset))
            screen.blit(glow_text, (glow_rect.x + offset, glow_rect.y + offset))
        
        screen.blit(title_text, title_rect)
        
        # 副标题
        subtitle_font = self.get_chinese_font(50)
        subtitle_text = subtitle_font.render('恭喜胜利！', True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 280))
        screen.blit(subtitle_text, subtitle_rect)


class GameCompleteAnimation(Animation):
    """游戏通关动画"""
    def __init__(self, screen_width, screen_height, final_score):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.final_score = final_score
        self.timer = 0
        self.duration = 240  # 4秒
        self.fireworks = []
        
        # 生成持续的烟花
        self.firework_spawn_timer = 0
    
    def update(self):
        """更新动画"""
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True
        
        # 持续生成烟花
        self.firework_spawn_timer += 1
        if self.firework_spawn_timer > 20:
            self.firework_spawn_timer = 0
            self.fireworks.append({
                'x': random.randint(100, self.screen_width - 100),
                'y': random.randint(100, 300),
                'exploded': False,
                'timer': 0,
                'particles': []
            })
        
        # 更新烟花
        for firework in self.fireworks[:]:
            firework['timer'] += 1
            if firework['timer'] > 10 and not firework['exploded']:
                firework['exploded'] = True
                # 生成粒子
                for i in range(40):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 7)
                    firework['particles'].append({
                        'x': firework['x'],
                        'y': firework['y'],
                        'vx': speed * math.cos(angle),
                        'vy': speed * math.sin(angle),
                        'life': 60,
                        'color': random.choice([
                            (255, 100, 100), (100, 255, 100), (100, 100, 255),
                            (255, 255, 100), (255, 100, 255), (100, 255, 255)
                        ])
                    })
            
            # 更新粒子
            for particle in firework['particles'][:]:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.2
                particle['life'] -= 1
                if particle['life'] <= 0:
                    firework['particles'].remove(particle)
            
            # 移除完成的烟花
            if firework['exploded'] and len(firework['particles']) == 0:
                self.fireworks.remove(firework)
    
    def draw(self, screen):
        """绘制动画"""
        # 绘制背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 200))
        screen.blit(overlay, (0, 0))
        
        # 绘制烟花
        for firework in self.fireworks:
            for particle in firework['particles']:
                if particle['life'] > 0:
                    alpha = int(255 * (particle['life'] / 60))
                    size = max(1, int(4 * (particle['life'] / 60)))
                    pygame.draw.circle(screen, particle['color'],
                                     (int(particle['x']), int(particle['y'])), size)
        
        # 绘制文字
        title_font = self.get_chinese_font(100)
        title_text = title_font.render('恭喜通关！', True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 180))
        screen.blit(title_text, title_rect)
        
        # 最终分数
        score_font = self.get_chinese_font(60)
        score_text = score_font.render(f'最终得分: {self.final_score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, 300))
        screen.blit(score_text, score_rect)
        
        # 感谢文字
        thank_font = self.get_chinese_font(40)
        thank_text = thank_font.render('感谢游玩！', True, (0, 255, 255))
        thank_rect = thank_text.get_rect(center=(self.screen_width // 2, 400))
        screen.blit(thank_text, thank_rect)


class GameOverAnimation(Animation):
    """游戏结束动画（玩家死亡）"""
    def __init__(self, screen_width, screen_height, final_score, level):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.final_score = final_score
        self.level = level
        self.timer = 0
        self.duration = 300  # 5秒，留出续命时间
        self.particles = []
        
        # 生成下落的粒子效果
        for i in range(100):
            self.particles.append({
                'x': random.randint(0, screen_width),
                'y': random.randint(-500, 0),
                'vy': random.uniform(1, 3),
                'size': random.randint(2, 6),
                'color': random.choice([
                    (128, 128, 128), (100, 100, 100), (150, 150, 150)
                ])
            })
    
    def update(self):
        """更新动画"""
        self.timer += 1
        if self.timer >= self.duration:
            self.finished = True
        
        # 更新下落粒子
        for particle in self.particles:
            particle['y'] += particle['vy']
            if particle['y'] > self.screen_height:
                particle['y'] = random.randint(-50, 0)
                particle['x'] = random.randint(0, self.screen_width)
    
    def draw(self, screen):
        """绘制动画"""
        # 绘制半透明暗色背景
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        # 绘制下落粒子
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'],
                             (int(particle['x']), int(particle['y'])), particle['size'])
        
        # 主标题 - 闪烁效果
        pulse = abs(math.sin(self.timer / 20)) * 30 + 70
        title_font = self.get_chinese_font(int(pulse) + 30)
        title_text = title_font.render('GAME OVER', True, (255, 50, 50))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)
        
        # 统计信息
        info_font = self.get_chinese_font(40)
        y_offset = 250
        
        stats = [
            f'关卡: {self.level}/3',
            f'最终得分: {self.final_score}',
        ]
        
        for stat in stats:
            stat_text = info_font.render(stat, True, (255, 255, 255))
            stat_rect = stat_text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 60
        
        # 续命提示（闪烁效果）
        if (self.timer // 20) % 2 == 0:
            revive_font = self.get_chinese_font(48)
            revive_text = revive_font.render('按 R 键续命（恢复3点生命值）', True, (0, 255, 0))
            revive_rect = revive_text.get_rect(center=(self.screen_width // 2, 420))
            screen.blit(revive_text, revive_rect)
        
        # 退出提示
        hint_font = self.get_chinese_font(28)
        hint_text = hint_font.render('按 ESC 退出游戏', True, (200, 200, 200))
        hint_rect = hint_text.get_rect(center=(self.screen_width // 2, 520))
        screen.blit(hint_text, hint_rect)
