import pygame
import random

class Explosion:
    """爆炸动画效果"""
    def __init__(self, x, y, size=30):
        """初始化爆炸效果
        Args:
            x: 中心x坐标
            y: 中心y坐标
            size: 爆炸大小
        """
        self.x = x
        self.y = y
        self.size = size
        self.max_size = size * 2
        self.current_size = 0
        self.lifetime = 30  # 动画持续帧数
        self.timer = 0
        self.particles = []
        
        # 生成粒子
        for i in range(15):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 5)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': speed * random.choice([-1, 1]),
                'vy': speed * random.choice([-1, 1]),
                'size': random.randint(2, 6),
                'color': random.choice([
                    (255, 200, 0),   # 橙黄
                    (255, 100, 0),   # 橙红
                    (255, 50, 0),    # 红色
                    (255, 255, 100), # 浅黄
                ])
            })
    
    def update(self):
        """更新爆炸动画"""
        self.timer += 1
        
        # 扩散效果
        if self.current_size < self.max_size:
            self.current_size += 3
        
        # 更新粒子
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['size'] = max(1, particle['size'] - 0.2)
    
    def draw(self, screen):
        """绘制爆炸效果"""
        # 计算透明度
        alpha = int(255 * (1 - self.timer / self.lifetime))
        
        # 绘制扩散圆圈
        if self.current_size > 0:
            for i in range(3):
                radius = int(self.current_size - i * 5)
                if radius > 0:
                    color_alpha = max(0, alpha - i * 50)
                    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surface, (255, 150, 0, color_alpha), 
                                     (radius, radius), radius)
                    screen.blit(surface, (self.x - radius, self.y - radius))
        
        # 绘制粒子
        for particle in self.particles:
            if particle['size'] > 0:
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 
                                 int(particle['size']))
    
    def is_finished(self):
        """检查动画是否结束"""
        return self.timer >= self.lifetime
