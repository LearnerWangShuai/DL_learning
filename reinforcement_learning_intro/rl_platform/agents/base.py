"""所有智能体应满足的最小接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable


State = Hashable
Action = int


class ReinforcementLearningAgent(ABC):
    """让训练循环不依赖具体算法的统一接口。"""

    @abstractmethod
    def choose_action(self, state: State, explore: bool = True) -> Action:
        """根据状态选择动作。"""

    @abstractmethod
    def learn(
        self,
        state: State,
        action: Action,
        reward: float,
        next_state: State,
        terminated: bool,
    ) -> None:
        """从一条状态转移经验中学习。"""

    def end_episode(self) -> None:
        """每个回合结束后调用；无额外调度需求的算法可保持默认实现。"""

    @property
    def exploration_rate(self) -> float | None:
        """供训练日志显示；不使用探索率的算法返回 None。"""
        return None
