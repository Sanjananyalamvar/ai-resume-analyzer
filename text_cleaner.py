import re


def clean_text(text):
    """Lower-case text so skills can be matched reliably.

    Keeps + # . - so C++, C#, Node.js and scikit-learn survive, but separates
    slashes ("Python/SQL") and drops full stops at the end of a word ("...using Python.")
    so those skills are still found.
    """
    text = (text or '').lower()
    text = text.replace('&', ' and ').replace('/', ' / ')
    text = re.sub(r'[^a-z0-9+#.\-/ ]+', ' ', text)
    text = re.sub(r'(?<=[a-z0-9+#])\.+(?=\s|$)', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()
