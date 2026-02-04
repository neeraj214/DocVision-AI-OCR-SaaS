import re


def clean_text(text: str) -> str:
    t = text.replace("\r", "\n")
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()


def to_structured(text: str):
    lines = [line.strip() for line in text.split("\n")]
    paragraphs = []
    current: list[str] = []
    for line in lines:
        if line == "":
            if current:
                paragraphs.append({"lines": current})
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append({"lines": current})
    return {"paragraphs": paragraphs}
