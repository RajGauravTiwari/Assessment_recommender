def clean_description(text: str) -> str:
    """
    Cleans assessment description by removing catalog/navigation boilerplate.
    Keeps content after the word 'description' if present.
    """
    if not text:
        return ""

    text_lower = text.lower()

    if "description" in text_lower:
        idx = text_lower.find("description")
        return text[idx + len("description"):].strip()

    return text.strip()
