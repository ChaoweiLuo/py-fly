# 打飞机游戏

这是一个使用Python和Pygame开发的简单打飞机游戏。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行游戏

```bash
# 使用默认飞机样式 (第一个飞机样式 player.png)
python src/main.py

# 明确选择飞机样式1 (player.png)
python src/main.py --player 1

# 选择飞机样式2 (player2.png)
python src/main.py --player 2
```

## 游戏操作

- 使用方向键控制飞机移动
- 按空格键发射子弹
- 击毁红色敌机获得分数

## 飞机样式

游戏支持两种飞机样式，默认使用第一个飞机样式：
- 样式1 (默认): 使用 assets/images/player.png
- 样式2: 使用 assets/images/player2.png

## 游戏结构

- `src/main.py`: 游戏入口文件
- `src/game.py`: 游戏主类
- `src/scenes/`: 游戏场景相关文件
- `src/objects/`: 游戏对象类（玩家、敌人、子弹等）