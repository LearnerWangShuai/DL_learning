"""环境注册表；新增环境时在此登记工厂函数。"""

from __future__ import annotations

from typing import Any, Callable

from .base import ReinforcementLearningEnvironment
from .grid_world import GridWorld


EnvironmentFactory = Callable[[dict[str, Any], dict[str, Any]], ReinforcementLearningEnvironment]
ENVIRONMENT_FACTORIES: dict[str, EnvironmentFactory] = {
    "grid_world": GridWorld.from_config,
}


def create_environment(config: dict[str, Any]) -> ReinforcementLearningEnvironment:
    """依据 config.json 的 environment 区块创建当前选定的环境。"""
    name = config.get("name")
    settings = config.get("settings")
    rewards = config.get("rewards")
    if not isinstance(name, str):
        raise ValueError("environment.name 必须是字符串。")
    if not isinstance(settings, dict) or not isinstance(rewards, dict):
        raise ValueError("environment.settings 和 environment.rewards 必须是对象。")
    if name not in ENVIRONMENT_FACTORIES:
        available = ", ".join(sorted(ENVIRONMENT_FACTORIES))
        raise ValueError(f"未知环境 {name!r}；可用环境：{available}")
    return ENVIRONMENT_FACTORIES[name](settings, rewards)


__all__ = ["GridWorld", "ReinforcementLearningEnvironment", "create_environment"]
