"""智能体实现与注册表。"""

from __future__ import annotations

from typing import Any, Callable

from .base import ReinforcementLearningAgent
from .q_learning import QLearningAgent


AgentFactory = Callable[[int, dict[str, Any]], ReinforcementLearningAgent]
AGENT_FACTORIES: dict[str, AgentFactory] = {
    "q_learning": QLearningAgent.from_config,
}


def create_agent(config: dict[str, Any], action_count: int) -> ReinforcementLearningAgent:
    """依据 config.json 的 agent 区块创建当前选定的智能体。"""
    name = config.get("name")
    settings = config.get("settings")
    if not isinstance(name, str):
        raise ValueError("agent.name 必须是字符串。")
    if not isinstance(settings, dict):
        raise ValueError("agent.settings 必须是对象。")
    if name not in AGENT_FACTORIES:
        available = ", ".join(sorted(AGENT_FACTORIES))
        raise ValueError(f"未知智能体 {name!r}；可用智能体：{available}")
    return AGENT_FACTORIES[name](action_count, settings)


__all__ = ["QLearningAgent", "ReinforcementLearningAgent", "create_agent"]
