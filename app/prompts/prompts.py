BASELINE_PROMPT = """
Classify the text into one of: toxic, spam, safe.
Text: "{text}"
"""

IMPROVED_PROMPT = """
You are a classification assistant.
Labels: toxic, spam, safe.

Examples:
"Buy cheap followers now!" -> spam
"You are an idiot!" -> toxic
"I love this product!" -> safe

Now classify:
"{text}"
"""

def get_prompt(variant: str, text: str) -> str:
    if variant == "baseline":
        return BASELINE_PROMPT.format(text=text)
    return IMPROVED_PROMPT.format(text=text)
