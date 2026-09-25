"""GridWorld 的奖励规则。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GridWorldRewards:
    """将格子迷宫的奖励规则从环境移动逻辑中分离出来。"""

    normal_move: float
    invalid_move: float
    goal: float

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> "GridWorldRewards":
        required = ("normal_move", "invalid_move", "goal")
        missing = [name for name in required if name not in config]
        if missing:
            raise ValueError(f"grid_world rewards 缺少配置项：{', '.join(missing)}")
        for name in required:
            if not isinstance(config[name], (int, float)):
                raise ValueError(f"grid_world.rewards.{name} 必须是数字。")
        return cls(
            normal_move=float(config["normal_move"]),
            invalid_move=float(config["invalid_move"]),
            goal=float(config["goal"]),
        )
