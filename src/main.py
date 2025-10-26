import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.game import Game

def main():
    """游戏主函数"""
    pygame.init()
    game = Game()
    game.run()

if __name__ == "__main__":
    main()