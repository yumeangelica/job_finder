import random
import os
import json

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_user_agent_list = None


def _load_agents():
    """Load user agents from file lazily (only when first needed)."""
    global _user_agent_list

    if _user_agent_list is not None:
        return _user_agent_list

    # Read the agents file path from main_program_config, fall back to default
    config_path = os.path.join(_project_root, 'config', 'main_program_config.json')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        agents_file = config.get('agents_file', 'config/agents.txt')
    except (FileNotFoundError, json.JSONDecodeError):
        agents_file = 'config/agents.txt'

    agents_path = os.path.join(_project_root, agents_file)

    try:
        with open(agents_path, 'r', encoding='utf-8') as f:
            _user_agent_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(
            f"User agent file not found: {agents_path}\n"
            f"Create config/agents.txt in the project root."
        )

    if not _user_agent_list:
        raise ValueError(f"User agent file is empty: {agents_path}")

    return _user_agent_list


def user_agent_switcher():
    """Generator that yields a random user agent on each iteration."""
    agents = _load_agents()

    while True:
        agent = random.choice(agents)
        yield agent