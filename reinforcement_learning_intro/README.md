# 强化学习入门：让智能体学会走迷宫

这个小案例不用任何第三方库。它通过一个 7×7 的迷宫，带你从零理解强化学习（Reinforcement Learning, RL），并给出一个可扩展成自己实验平台的最小骨架。

## 先用一句话理解它

强化学习不是告诉程序“每一步应该怎么走”，而是让程序不断尝试；到达目标时得到奖励，撞墙或走错路会有代价。它会逐渐学出“在当前情况采取哪种动作长期收益最大”。

生活中的类比：训练小狗时，并不把每块肌肉如何移动写成规则；完成指令就奖励，它会慢慢建立“情境 → 行为”的选择。

## 案例目标

智能体从左上角 `A` 出发，到右侧目标格 `G`。地图中的 `#` 是障碍物：

```text
A . . . . . .
. # . . . . .
. . # . . . .
. # # . . . .
. . . . . . .
. . . . . . G
. . . . . . .
```

每走一步奖励 `-1`，撞墙或障碍物奖励 `-3`，到达终点奖励 `+20`。因此它既要到终点，也会倾向于走较短且少碰撞的路径。

| 强化学习术语 | 在这个案例中 |
| --- | --- |
| 智能体（Agent） | 学习走路的程序 |
| 环境（Environment） | 迷宫以及它的规则 |
| 状态（State） | 当前格子坐标，例如 `(0, 2)` |
| 动作（Action） | 上、右、下、左 |
| 奖励（Reward） | 一次动作后的分数 |
| 策略（Policy） | 状态下如何选择动作的规则 |
| 回合（Episode） | 从出发到终点（或超步数）的一次尝试 |

## 运行

请在项目根目录执行：

```powershell
& "D:\Anaconda\envs\rl_learning_project\python.exe" .\reinforcement_learning_intro\train.py
```

也可调整训练量，或保存学到的 Q 表：

```powershell
& "D:\Anaconda\envs\rl_learning_project\python.exe" .\reinforcement_learning_intro\train.py --episodes 3000 --save q_table.json
```

## 配置文件

脚本默认读取同目录的 `config.json`。训练参数和迷宫规则都在这个文件中，修改它后，下次运行会自动生效，无需改动 Python 代码。

```text
config.json
├─ training       # 通用训练循环：回合数、最大步数、随机种子、日志频率
├─ agent          # 算法选择与算法专属参数，例如 Q-learning 的探索率
└─ environment    # 环境选择、地图规则与奖励机制
```

常见的可修改项：

- `training.episodes`：训练回合数。
- `training.max_steps`：一个回合允许的最大动作数；必须不小于当前地图从起点到终点的最短路径长度。当前地图至少需要 11 步，建议设置为 `50`。
- `agent.name`：当前使用的算法名称；目前为 `q_learning`。
- `agent.settings.alpha`、`gamma`、`epsilon`、`epsilon_min`、`epsilon_decay`：Q-learning 专属的学习与探索参数。
- `environment.walls`：障碍物坐标列表，例如 `[3, 1]` 表示第 4 行、第 2 列。
- `environment.rewards.normal_move`、`invalid_move`、`goal`：奖励设计。

命令行参数可临时覆盖通用训练循环的值，且只影响这一次运行。例如：

```powershell
& "D:\Anaconda\envs\rl_learning_project\python.exe" .\reinforcement_learning_intro\train.py --episodes 500 --max-steps 50
```

算法专属值（如 `alpha`、`gamma`、探索率）请修改 `agent.settings`，使每次实验都能由配置文件完整复现。

若要使用另一份配置文件，可传入 `--config`：

```powershell
& "D:\Anaconda\envs\rl_learning_project\python.exe" .\reinforcement_learning_intro\train.py --config .\my_config.json
```

## 可扩展项目布局

```text
reinforcement_learning_intro/
├─ config.json                  # 当前环境、奖励与训练参数
├─ train.py                     # 训练入口：组合各模块后运行
└─ rl_platform/
   ├─ agents/                   # 算法接口、算法实现与算法注册表
   │  ├─ base.py                # 所有智能体必须满足的统一接口
   │  └─ q_learning.py          # Q-learning 的动作选择、学习与探索调度
   ├─ environments/
   │  ├─ base.py                # 所有环境必须满足的统一接口
   │  └─ grid_world.py          # 当前迷宫的状态转移与渲染
   ├─ rewards/
   │  └─ grid_world.py          # 当前迷宫的奖励机制
   ├─ config.py                 # 配置读取、合并和检查
   └─ training.py               # 与具体环境无关的训练与演示循环
```

这意味着“环境怎样变化”“什么行为得到奖励”“智能体如何学习”已分别位于不同模块。以后新增环境时：

1. 在 `rl_platform/environments/` 新建环境类，实现 `reset()`、`step()`、`render()` 与动作信息。
2. 在 `rl_platform/rewards/` 新建对应奖励类，让奖励配置与移动/状态转移逻辑分离。
3. 在 `rl_platform/environments/__init__.py` 的 `ENVIRONMENT_FACTORIES` 中登记环境名称和工厂函数。
4. 在 `config.json` 的 `environment.name` 选择该名称，并为它提供 `settings` 和 `rewards`。

训练入口和现有智能体无需因为新增环境而重写。新增 DQN、PPO 等算法时，应在 `rl_platform/agents/` 实现并登记，然后在 `config.json` 的 `agent.name` 中选择它。

程序先训练，再以关闭随机探索的方式演示一次。输出中的 `*` 是智能体走过的路径；理想情况下它会从 `A` 走到 `G`，且避开 `#`。由于包含随机探索，每次训练过程的小数字可能不同，但最终路线应能收敛。

## 代码里最重要的一行

```python
new_q = old_q + alpha * (reward + gamma * max_next_q - old_q)
```

这就是 Q-learning 的更新公式：

- `old_q`：过去认为“在当前状态做这个动作”有多好；
- `reward`：这一步立刻得到的反馈；
- `max_next_q`：对下一状态最好的未来收益的估计；
- `gamma`：未来奖励的重要程度（折扣因子）；
- `alpha`：本次经验改变旧判断的速度（学习率）。

开始时 Q 表全是 0，智能体会随机试路。尝到“接近终点、最终成功”的累计收益后，相关状态—动作对的 Q 值会提高；重复许多回合后，选 Q 值最大的动作就能走出路线。

## 从这个案例扩展成自己的强化学习平台

现在的 `train.py` 已将环境、奖励机制、智能体与训练循环拆分。若你想训练自己的任务，只需新增符合下面接口的环境，并在环境注册表中登记：

```python
state = env.reset()
next_state, reward, terminated, info = env.step(action)
```

建议按这个顺序进阶：

1. **定义任务**：明确状态、动作、奖励、一次回合何时结束。奖励设计最重要；例如机器人应奖励安全前进、惩罚碰撞和耗时。
2. **先做可重复的模拟环境**：实现 `reset()`、`step()`、`render()`，固定随机种子，并为边界情况写测试。不要一开始连接昂贵或有风险的真实设备。
3. **记录实验**：保存参数、随机种子、每回合回报、成功率和模型。比较算法时一次只改变少量变量。
4. **按任务选算法**：本案例的表格 Q-learning 适合“状态和动作都有限”的任务。图像、连续控制或大规模状态空间需要函数逼近/深度强化学习；届时可学习 Gymnasium 环境接口，再使用 PyTorch 和 Stable-Baselines3。
5. **独立评估**：训练时允许探索；评估时关闭探索，并用从未参与训练的固定场景/种子测试。不要只看单次最高分。

一个实用的项目结构可以是：

```text
my_rl_project/
  envs/          # 每个任务的 reset / step / render
  agents/        # Q-learning、DQN、PPO 等算法
  configs/       # 超参数与任务配置
  runs/          # 日志、Q 表或模型权重（不提交大文件）
  train.py       # 训练入口
  evaluate.py    # 关闭探索后的独立评估
```

## 可自己动手的三个小改动

1. 把终点改到其他位置，或增加障碍物，观察训练需要多少回合。
2. 将“每步 `-1`”改成 `-0.1`，比较路线是否仍然足够短。
3. 增加一个“危险格”：进入即结束并给 `-20`，体会奖励设计如何影响行为。

> 注意：强化学习的奖励函数定义了“什么叫做好”。如果只奖励速度，智能体可能学会冒险；真实任务要把安全、约束和人工审核纳入环境与评估中。
