"""配置文件读取、默认值合并与训练参数检查。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config.json"
TRAINING_CONFIG_FIELDS = (
    "episodes",
    "max_steps",
    "seed",
    "report_sections",
)


def load_config(filename: Path) -> dict[str, Any]:
    """读取 JSON，并验证平台级别的配置结构。"""
    try:
        config = json.loads(filename.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise FileNotFoundError(f"找不到配置文件：{filename}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"配置文件不是有效 JSON：{filename}（第 {error.lineno} 行）") from error

    if not isinstance(config, dict):
        raise ValueError("配置文件的最外层必须是 JSON 对象。")
    training = config.get("training")
    agent = config.get("agent")
    environment = config.get("environment")
    if not isinstance(training, dict) or not isinstance(agent, dict) or not isinstance(environment, dict):
        raise ValueError("配置文件必须包含 training、agent 和 environment 三个对象。")

    missing_training = [name for name in TRAINING_CONFIG_FIELDS if name not in training]
    if missing_training:
        raise ValueError(f"training 缺少配置项：{', '.join(missing_training)}")
    if not isinstance(agent.get("name"), str) or not isinstance(agent.get("settings"), dict):
        raise ValueError("agent 必须包含字符串 name 和对象 settings。")
    return config


def command_line_option_was_used(option: str) -> bool:
    """判断用户是否显式提供参数，以便只在未提供时采用配置文件默认值。"""
    return any(argument == option or argument.startswith(f"{option}=") for argument in sys.argv[1:])


def apply_training_config(args: argparse.Namespace, training: dict[str, Any]) -> None:
    """配置文件提供默认值；命令行参数具有更高优先级。"""
    options = {
        "episodes": "--episodes",
        "max_steps": "--max-steps",
        "seed": "--seed",
        "report_sections": "--report-sections",
    }
    for field, option in options.items():
        if not command_line_option_was_used(option):
            setattr(args, field, training[field])


def validate_training_config(args: argparse.Namespace) -> None:
    """在开始训练前给出清晰的参数错误提示。"""
    for name in ("episodes", "max_steps", "report_sections", "seed"):
        if not isinstance(getattr(args, name), int):
            raise ValueError(f"training.{name} 必须是整数。")
    if args.episodes <= 0 or args.max_steps <= 0 or args.report_sections <= 0:
        raise ValueError("episodes、max_steps 和 report_sections 必须为正数。")
