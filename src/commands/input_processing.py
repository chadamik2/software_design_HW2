def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_float(prompt: str) -> float:
    return float(ask(prompt))


def ask_opt(prompt: str) -> str:
    s = input(prompt).strip()
    return s or ""