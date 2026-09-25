"""训练入口：根据 config.json 组合环境、奖励机制、智能体与训练循环。"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from rl_platform.agents import create_agent
from rl_platform.config import DEFAULT_CONFIG_PATH, apply_training_config, load_config, validate_training_config
from rl_platform.environments import create_environment
from rl_platform.training import demonstrate, train


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="可配置的强化学习训练入口")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH, help="配置文件路径")
    parser.add_argument("--episodes", type=int, default=None, help="训练回合数")
    parser.add_argument("--max-steps", type=int, default=None, help="每回合最大步数")
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    parser.add_argument("--report-sections", type=int, default=None, help="训练统计输出分段数")
    parser.add_argument("--save", type=Path, help="Q 表保存位置，例如 q_table.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    apply_training_config(args, config["training"])
    validate_training_config(args)
    random.seed(args.seed)

    environment = create_environment(config["environment"])
    environment.validate_training_settings(args.max_steps)
    agent = create_agent(config["agent"], environment.action_count)
    print(f"开始训练 {config['agent']['name']} 智能体（环境：{config['environment']['name']}）……")
    train(
        environment,
        agent,
        args.episodes,
        args.max_steps,
        args.report_sections,
    )
    demonstrate(environment, agent, args.max_steps)

    if args.save:
        agent.save(args.save)
        print(f"Q 表已保存到：{args.save.resolve()}")


if __name__ == "__main__":
    main()
