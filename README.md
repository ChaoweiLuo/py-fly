# 打飞机游戏

这是一个使用Python和Pygame开发的简单打飞机游戏。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行游戏

```bash
python src/main.py
```

## 游戏操作

- 使用方向键控制飞机移动
- 按空格键发射子弹
- 击毁红色敌机获得分数

## 游戏结构

- `src/main.py`: 游戏入口文件
- `src/game.py`: 游戏主类
- `src/scenes/`: 游戏场景相关文件
- `src/objects/`: 游戏对象类（玩家、敌人、子弹等）