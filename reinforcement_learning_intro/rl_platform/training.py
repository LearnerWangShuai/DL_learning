"""与具体环境解耦的训练和演示循环。"""

from __future__ import annotations

from .agents.base import ReinforcementLearningAgent
from .environments.base import ReinforcementLearningEnvironment


def train(
    environment: ReinforcementLearningEnvironment,
    agent: ReinforcementLearningAgent,
    episodes: int,
    max_steps: int,
    report_sections: int,
) -> list[float]:
    """训练智能体，并返回每个回合的累计回报。"""
    rewards: list[float] = []
    report_interval = max(1, episodes // report_sections)

    for episode in range(1, episodes + 1):
        state = environment.reset()
        total_reward = 0.0
        for _ in range(max_steps):
            action = agent.choose_action(state, explore=True)
            next_state, reward, terminated, _ = environment.step(action)
            agent.learn(state, action, reward, next_state, terminated)
            state = next_state
            total_reward += reward
            if terminated:
                break
        rewards.append(total_reward)

        if episode % report_interval == 0:
            recent = rewards[-report_interval:]
            message = f"回合 {episode:5d}/{episodes} | 最近平均回报: {sum(recent) / len(recent):6.2f}"
            if agent.exploration_rate is not None:
                message += f" | 探索率: {agent.exploration_rate:.3f}"
            print(message)
        agent.end_episode()
    return rewards


def demonstrate(
    environment: ReinforcementLearningEnvironment,
    agent: ReinforcementLearningAgent,
    max_steps: int,
) -> None:
    """关闭探索，逐步执行训练后的当前最优策略。"""
    state = environment.reset()
    path = [state]
    moves: list[str] = []
    total_reward = 0.0
    success = False

    for _ in range(max_steps):
        action = agent.choose_action(state, explore=False)
        moves.append(environment.action_names[action])
        state, reward, terminated, info = environment.step(action)
        path.append(state)
        total_reward += reward
        if terminated:
            success = bool(info.get("success", True))
            break

    print("\n训练后的演示（* 为实际经过的路径）：")
    print(environment.render(path))
    print("动作序列：" + " → ".join(moves))
    print(f"总回报：{total_reward:.1f} | {'成功完成目标' if success else '未在步数限制内完成目标'}")
