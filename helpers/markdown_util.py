def escape_markdown_v2(text: str) -> str:
    to_escape = r"_*[]()~`>#+-=|{}.!"
    for char in to_escape:
        text = text.replace(char, f"\\{char}")
    return text
