"""所有可训练环境都应满足的最小接口。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable
from typing import Any


State = Hashable
Action = int


class ReinforcementLearningEnvironment(ABC):
    """将环境与具体算法解耦的统一接口。"""

    @property
    @abstractmethod
    def action_count(self) -> int:
        """可选动作数量。"""

    @property
    @abstractmethod
    def action_names(self) -> tuple[str, ...]:
        """用于日志与可视化的动作名称。"""

    @abstractmethod
    def reset(self) -> State:
        """开始新回合，并返回初始状态。"""

    @abstractmethod
    def step(self, action: Action) -> tuple[State, float, bool, dict[str, Any]]:
        """执行动作，返回下一状态、奖励、结束标记和附加信息。"""

    @abstractmethod
    def render(self, path: list[State] | None = None) -> str:
        """将当前环境渲染为终端文本；后续可替换为图形渲染。"""

    def validate_training_settings(self, max_steps: int) -> None:
        """环境可按需检查训练限制；默认环境无需额外检查。"""
