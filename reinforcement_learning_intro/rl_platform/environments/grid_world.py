"""可配置的格子迷宫环境。"""

from __future__ import annotations

from collections import deque
from typing import Any

from ..rewards.grid_world import GridWorldRewards
from .base import Action, ReinforcementLearningEnvironment, State


GridState = tuple[int, int]


def state_from_config(value: Any, name: str) -> GridState:
    """将 JSON 中的 [row, col] 坐标转换为元组。"""
    if (
        not isinstance(value, list)
        or len(value) != 2
        or any(not isinstance(item, int) for item in value)
    ):
        raise ValueError(f"配置项 {name} 必须是两个整数构成的列表，例如 [0, 0]。")
    return value[0], value[1]


class GridWorld(ReinforcementLearningEnvironment):
    """离散迷宫：状态是坐标，动作为上、右、下、左。"""

    MOVES: dict[Action, GridState] = {
        0: (-1, 0),
        1: (0, 1),
        2: (1, 0),
        3: (0, -1),
    }
    ACTION_NAMES = ("上", "右", "下", "左")

    def __init__(
        self,
        rows: int,
        cols: int,
        start: GridState,
        goal: GridState,
        walls: set[GridState],
        rewards: GridWorldRewards,
    ) -> None:
        if not isinstance(rows, int) or not isinstance(cols, int) or rows <= 0 or cols <= 0:
            raise ValueError("迷宫的 rows 和 cols 必须是正整数。")
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.walls = walls
        self.rewards = rewards

        for name, position in (("start", self.start), ("goal", self.goal), *[("wall", wall) for wall in self.walls]):
            if not self.is_inside(position):
                raise ValueError(f"environment.{name} 坐标 {position} 位于迷宫范围外。")
        if self.start == self.goal:
            raise ValueError("起点和终点不能相同。")
        if self.start in self.walls or self.goal in self.walls:
            raise ValueError("起点和终点不能设置为障碍物。")
        self.position = self.start

    @classmethod
    def from_config(cls, settings: dict[str, Any], rewards: dict[str, Any]) -> "GridWorld":
        required_settings = ("rows", "cols", "start", "goal", "walls")
        missing = [name for name in required_settings if name not in settings]
        if missing:
            raise ValueError(f"grid_world settings 缺少配置项：{', '.join(missing)}")
        walls_config = settings["walls"]
        if not isinstance(walls_config, list):
            raise ValueError("grid_world.settings.walls 必须是坐标列表。")
        for name in ("rows", "cols"):
            if not isinstance(settings[name], int):
                raise ValueError(f"grid_world.settings.{name} 必须是整数。")

        return cls(
            rows=settings["rows"],
            cols=settings["cols"],
            start=state_from_config(settings["start"], "grid_world.settings.start"),
            goal=state_from_config(settings["goal"], "grid_world.settings.goal"),
            walls={
                state_from_config(value, f"grid_world.settings.walls[{index}]")
                for index, value in enumerate(walls_config)
            },
            rewards=GridWorldRewards.from_config(rewards),
        )

    @property
    def action_count(self) -> int:
        return len(self.MOVES)

    @property
    def action_names(self) -> tuple[str, ...]:
        return self.ACTION_NAMES

    def is_inside(self, position: GridState) -> bool:
        return 0 <= position[0] < self.rows and 0 <= position[1] < self.cols

    def reset(self) -> GridState:
        self.position = self.start
        return self.position

    def shortest_path_length(self) -> int | None:
        """使用广度优先搜索计算忽略奖励时的最短可行路径长度。"""
        queue = deque([(self.start, 0)])
        visited = {self.start}
        while queue:
            position, steps = queue.popleft()
            if position == self.goal:
                return steps
            for row_delta, col_delta in self.MOVES.values():
                next_position = (position[0] + row_delta, position[1] + col_delta)
                if (
                    self.is_inside(next_position)
                    and next_position not in self.walls
                    and next_position not in visited
                ):
                    visited.add(next_position)
                    queue.append((next_position, steps + 1))
        return None

    def validate_training_settings(self, max_steps: int) -> None:
        shortest_path = self.shortest_path_length()
        if shortest_path is None:
            raise ValueError("当前迷宫不存在从起点到终点的可行路径。")
        if max_steps < shortest_path:
            raise ValueError(
                f"max_steps={max_steps} 不足以到达终点；当前迷宫最短路径需要 {shortest_path} 步。"
            )

    def step(self, action: Action) -> tuple[GridState, float, bool, dict[str, Any]]:
        if action not in self.MOVES:
            raise ValueError(f"无效动作编号：{action}")
        row_delta, col_delta = self.MOVES[action]
        candidate = (self.position[0] + row_delta, self.position[1] + col_delta)

        if not self.is_inside(candidate) or candidate in self.walls:
            return self.position, self.rewards.invalid_move, False, {"invalid_move": True}

        self.position = candidate
        if self.position == self.goal:
            return self.position, self.rewards.goal, True, {"invalid_move": False, "success": True}
        return self.position, self.rewards.normal_move, False, {"invalid_move": False}

    def render(self, path: list[State] | None = None) -> str:
        path_cells = set(path or [])
        lines = []
        for row in range(self.rows):
            cells = []
            for col in range(self.cols):
                cell = (row, col)
                if cell == self.start:
                    cells.append("A")
                elif cell == self.goal:
                    cells.append("G")
                elif cell in self.walls:
                    cells.append("#")
                elif cell in path_cells:
                    cells.append("*")
                else:
                    cells.append(".")
            lines.append(" ".join(cells))
        return "\n".join(lines)
