import re

def preprocess(text: str) -> str:
    text = text or ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s%₹$.,]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Placeholder for embeddings or more advanced NLP utilities
def extract_numbers(text: str):
    """Return numbers (ints/floats) found in text"""
    import re
    nums = re.findall(r"[\d,.]+", text)
    cleaned = []
    for n in nums:
        n2 = n.replace(",", "")
        try:
            if "." in n2:
                cleaned.append(float(n2))
            else:
                cleaned.append(int(n2))
        except:
            continue
    return cleaned
