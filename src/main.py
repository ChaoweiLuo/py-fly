import pygame
import sys
import os
import argparse

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game

def main():
    """游戏主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='打飞机游戏')
    parser.add_argument('--player', type=int, choices=[1, 2], default=1,
                       help='选择玩家飞机类型 (1 或 2)')
    args = parser.parse_args()
    
    pygame.init()
    game = Game(player_type=args.player)
    game.run()

if __name__ == "__main__":
    main()