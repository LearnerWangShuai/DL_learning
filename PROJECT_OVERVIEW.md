# 项目说明

## 项目目标

这是一个面向零基础学习者的强化学习实践项目。项目从可解释的迷宫案例开始，逐步搭建包含环境、智能体、训练、评估与可视化的本地学习平台。

项目的重点是理解强化学习的基本链路：

```text
状态 → 选择动作 → 环境反馈奖励 → 更新策略 → 评估结果
```

## 当前内容

```text
DL/
├─ PROJECT_EDITING_GUIDELINES.md  # 项目编辑条例
├─ PROJECT_OVERVIEW.md            # 本文件
├─ requirements.txt                # Python 运行依赖
└─ reinforcement_learning_intro/  # 强化学习入门案例
   ├─ README.md                    # 案例说明与学习路线
   ├─ config.json                  # 训练参数、环境与奖励规则
   ├─ train.py                     # 当前训练入口
   └─ rl_platform/                 # 可扩展平台模块
      ├─ agents/                   # 智能体接口、算法实现与注册表
      ├─ environments/             # 环境接口、具体环境与注册表
      ├─ rewards/                  # 各环境的奖励机制
      ├─ config.py                 # 配置读取和校验
      └─ training.py               # 通用训练和演示循环
```

`train.py` 是唯一训练入口，默认读取同目录的 `config.json`。其中 `training` 只描述通用训练循环，`agent` 选择算法及其专属参数，`environment` 选择环境及其奖励机制。当前 `grid_world` 和 `q_learning` 都只是第一个注册实现。

## 当前运行环境

- Python：3.14.6
- Anaconda：安装在 `D:\Anaconda`
- 项目独立环境：`D:\Anaconda\envs\rl_learning_project`
- 可视化库：`pygame-ce 2.5.8`（代码导入名为 `pygame`）

项目依赖只能安装到独立环境，依赖清单见根目录的 `requirements.txt`。

## 运行入门案例

在项目根目录执行。直接调用项目环境的解释器，不依赖 Conda 激活或 PowerShell 配置：

```powershell
& "D:\Anaconda\envs\rl_learning_project\python.exe" .\reinforcement_learning_intro\train.py
```

调整训练回合数并导出 Q 表：

```powershell
& "D:\Anaconda\envs\rl_learning_project\python.exe" .\reinforcement_learning_intro\train.py --episodes 3000 --save q_table.json
```

## Windows PowerShell 中文显示

部分 Windows PowerShell 会使用 GBK（代码页 936）。本项目的运行命令直接调用环境中的 `python.exe`，Python 会据此输出 GBK，因此中文可以正常显示。

不要通过 `conda run` 启动本项目；该命令会把子进程输出转为 UTF-8，而 GBK 终端会将其误读为乱码。

如果你在其他项目中必须使用 `conda run`，先在当前 PowerShell 窗口执行以下命令，将终端切换到 UTF-8：

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [Console]::OutputEncoding
```

## 下一阶段

1. 为迷宫添加 Pygame 可视化窗口，逐步显示状态、动作、奖励与路径。
2. 添加训练回报、成功率等曲线，比较不同超参数的效果。
3. 将迷宫升级为可配置的模拟任务，练习状态、动作和奖励的设计。
4. 在理解基础概念后，引入 Gymnasium 与更完整的深度强化学习算法。

## 项目边界

本项目用于学习和模拟，不对第三方在线游戏或服务进行自动化操作。任何外部系统的实验应先确认其明确授权、规则与安全边界。
