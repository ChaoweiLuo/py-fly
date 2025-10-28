import pygame
import sys
import os

class FontManager:
    """字体管理器，用于安全地处理字体加载"""
    
    def __init__(self):
        self.font_cache = {}
    
    def get_font(self, size):
        """获取指定大小的字体"""
        if size in self.font_cache:
            return self.font_cache[size]
        
        try:
            # 尝试使用系统字体
            font = pygame.font.Font(None, size)
            self.font_cache[size] = font
            return font
        except Exception as e:
            print(f"加载字体失败: {e}，使用系统默认字体")
            try:
                # 尝试使用系统默认字体
                font = pygame.font.SysFont(None, size)
                self.font_cache[size] = font
                return font
            except Exception as e2:
                print(f"使用系统默认字体也失败: {e2}，创建无字体渲染")
                # 最后的回退方案 - 创建一个简单的表面
                class DummyFont:
                    def __init__(self, size):
                        self.size = size
                    
                    def render(self, text, antialias, color):
                        # 创建一个简单的文本表面
                        surface = pygame.Surface((len(text) * self.size // 2, self.size), pygame.SRCALPHA)
                        surface.fill((0, 0, 0, 0))  # 透明背景
                        # 绘制简单的矩形代替文字
                        pygame.draw.rect(surface, color, (0, 0, surface.get_width(), surface.get_height()))
                        return surface
                
                font = DummyFont(size)
                self.font_cache[size] = font
                return font
    
    def get_chinese_font(self, size):
        """获取支持中文的字体"""
        cache_key = f"chinese_{size}"
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
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
                    '/System/Library/Fonts/Helvetica.ttc',
                    '/System/Library/Fonts/Arial Unicode.ttf',
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
                    self.font_cache[cache_key] = font
                    return font
            
            # 如果没有找到字体文件，使用pygame默认字体
            print(f"警告: 未找到中文字体，使用默认字体")
            font = self.get_font(size)
            self.font_cache[cache_key] = font
            return font
            
        except Exception as e:
            print(f"加载中文字体失败: {e}，使用默认字体处理")
            font = self.get_font(size)
            self.font_cache[cache_key] = font
            return font

# 创建全局实例
font_manager = FontManager()

# 便捷函数
def get_font(size):
    """获取指定大小的字体"""
    return font_manager.get_font(size)

def get_chinese_font(size):
    """获取支持中文的字体"""
    return font_manager.get_chinese_font(size)