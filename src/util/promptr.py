def rstr(name: str) -> str:
    with open(name, "r", encoding="UTF-8") as f:
        return f.read()
    pass
