"""表格型 Q-learning 智能体。"""

from __future__ import annotations

import json
import random
from collections.abc import Hashable
from pathlib import Path
from typing import Any

from .base import Action, ReinforcementLearningAgent, State


class QLearningAgent(ReinforcementLearningAgent):
    """适用于有限离散动作空间的 Q-learning 智能体。"""

    def __init__(
        self,
        action_count: int,
        alpha: float,
        gamma: float,
        epsilon: float,
        epsilon_min: float,
        epsilon_decay: float,
    ) -> None:
        self.action_count = action_count
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q: dict[State, list[float]] = {}

    @classmethod
    def from_config(cls, action_count: int, settings: dict[str, Any]) -> "QLearningAgent":
        """从 agent.settings 创建 Q-learning 智能体。"""
        required = ("alpha", "gamma", "epsilon", "epsilon_min", "epsilon_decay")
        missing = [name for name in required if name not in settings]
        if missing:
            raise ValueError(f"q_learning settings 缺少配置项：{', '.join(missing)}")
        for name in required:
            if not isinstance(settings[name], (int, float)):
                raise ValueError(f"q_learning.settings.{name} 必须是数字。")

        alpha = float(settings["alpha"])
        gamma = float(settings["gamma"])
        epsilon = float(settings["epsilon"])
        epsilon_min = float(settings["epsilon_min"])
        epsilon_decay = float(settings["epsilon_decay"])
        if not 0 < alpha <= 1:
            raise ValueError("q_learning.settings.alpha 必须位于 (0, 1]。")
        if not 0 <= gamma <= 1:
            raise ValueError("q_learning.settings.gamma 必须位于 [0, 1]。")
        if not 0 <= epsilon_min <= epsilon <= 1:
            raise ValueError("必须满足 0 <= epsilon_min <= epsilon <= 1。")
        if not 0 < epsilon_decay <= 1:
            raise ValueError("q_learning.settings.epsilon_decay 必须位于 (0, 1]。")
        return cls(action_count, alpha, gamma, epsilon, epsilon_min, epsilon_decay)

    def values(self, state: State) -> list[float]:
        if state not in self.q:
            self.q[state] = [0.0] * self.action_count
        return self.q[state]

    def choose_action(self, state: State, explore: bool = True) -> Action:
        """epsilon-greedy：按探索率随机尝试，或选择当前最优动作。"""
        if explore and random.random() < self.epsilon:
            return random.randrange(self.action_count)

        action_values = self.values(state)
        best_value = max(action_values)
        best_actions = [index for index, value in enumerate(action_values) if value == best_value]
        return random.choice(best_actions)

    def learn(
        self,
        state: State,
        action: Action,
        reward: float,
        next_state: State,
        terminated: bool,
    ) -> None:
        """根据一次状态转移更新 Q(state, action)。"""
        old_q = self.values(state)[action]
        max_next_q = 0.0 if terminated else max(self.values(next_state))
        target = reward + self.gamma * max_next_q
        self.q[state][action] = old_q + self.alpha * (target - old_q)

    def end_episode(self) -> None:
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    @property
    def exploration_rate(self) -> float:
        return self.epsilon

    def save(self, filename: Path) -> None:
        """将 Q 表保存为容易查看和复用的 JSON 文件。"""
        serializable = {str(state): values for state, values in self.q.items()}
        filename.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
