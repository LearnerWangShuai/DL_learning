# 强化学习项目说明

这是面向零基础学习者的强化学习实践项目。本分支从一个可解释的迷宫案例开始，逐步搭建包含环境、智能体、训练、评估与可视化的本地学习平台。

项目的重点是理解强化学习的基本链路：

```text
状态 → 选择动作 → 环境反馈奖励 → 更新策略 → 评估结果
```

完整的项目说明保存在 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)；本 README 作为该说明在 GitHub 上的首页入口，内容概览如下。

## 当前内容

```text
DL/
├── PROJECT_EDITING_GUIDELINES.md  # 项目编辑条例
├── PROJECT_OVERVIEW.md            # 完整项目说明
├── requirements.txt                # Python 运行依赖
└── reinforcement_learning_intro/  # 强化学习入门案例
    ├── README.md                   # 案例说明与学习路线
    ├── config.json                 # 训练参数、环境与奖励规则
    ├── train.py                    # 当前唯一训练入口
    └── rl_platform/                # 可扩展平台模块
        ├── agents/                 # 智能体接口、算法实现与注册表
        ├── environments/           # 环境接口、具体环境与注册表
        ├── rewards/                # 各环境的奖励机制
        ├── config.py               # 配置读取和校验
        └── training.py             # 通用训练和演示循环
```

`train.py` 默认读取同目录的 `config.json`。其中 `training` 描述通用训练循环，`agent` 选择算法及其专属参数，`environment` 选择环境及其奖励机制。当前的 `grid_world` 与 `q_learning` 是第一组可替换实现。

## 当前运行环境

- Python：3.14.6
- Anaconda：`D:\Anaconda`
- 项目独立环境：`D:\Anaconda\envs\rl_learning_project`
- 可视化库：`pygame-ce 2.5.8`（导入名为 `pygame`）

依赖只能安装在项目独立环境内，详见根目录的 `requirements.txt` 与 `PROJECT_EDITING_GUIDELINES.md`。

## 运行入门案例

在项目根目录直接调用项目环境的解释器：

```powershell
& "D:\Anaconda\envs\rl_learning_project\python.exe" .\reinforcement_learning_intro\train.py
```

调整训练回合数并导出 Q 表：

```powershell
& "D:\Anaconda\envs\rl_learning_project\python.exe" .\reinforcement_learning_intro\train.py --episodes 3000 --save q_table.json
```

## Windows PowerShell 中文显示

请直接调用上述环境中的 `python.exe`，不要通过 `conda run` 启动项目。部分 PowerShell 使用 GBK 编码，而 `conda run` 会将子进程输出转为 UTF-8，从而造成中文乱码。

## 下一阶段

1. 为迷宫添加 Pygame 可视化窗口，逐步展示状态、动作、奖励与路径。
2. 添加训练回报、成功率等曲线，对比不同超参数的效果。
3. 将迷宫升级为可配置的模拟任务，练习状态、动作和奖励设计。
4. 理解基础概念后，引入 Gymnasium 与更完整的深度强化学习算法。

## 项目边界

本项目用于学习和模拟，不对第三方在线游戏或服务进行自动化操作。任何外部系统实验都应先确认明确授权、规则与安全边界。
