import unicodedata
import re
from typing import Optional


def to_fullwidth(s: Optional[str]) -> Optional[str]:
    """Convert ASCII half-width characters to full-width equivalents.

    - Converts ASCII letters, digits, punctuation and space to full-width.
    - Leaves CJK characters unchanged.
    """
    if s is None:
        return None
    out = []
    for ch in s:
        code = ord(ch)
        # ASCII space to full-width space
        if code == 0x20:
            out.append('\u3000')
        # ASCII 33..126 -> fullwidth 65281..65374
        elif 0x21 <= code <= 0x7e:
            out.append(chr(code - 0x21 + 0xff01))
        else:
            out.append(ch)
    return ''.join(out)


def remove_spaces(s: Optional[str]) -> Optional[str]:
    """Remove all whitespace characters (space, tabs, newlines, and full-width spaces)."""
    if s is None:
        return None
    # \s covers ASCII whitespace; also remove IDEOGRAPHIC SPACE (U+3000)
    return re.sub(r"[\s\u3000]+", '', s)


def remove_symbols(s: Optional[str]) -> Optional[str]:
    """Remove all symbols and punctuation, leaving letters (a-zA-Z), digits and CJK characters.

    This keeps Chinese, Japanese, Korean ideographs, and Latin letters/digits. It removes punctuation
    marks, emoji, and other symbol categories.
    """
    if s is None:
        return None
    # Normalize to NFKC to separate compatibility forms
    norm = unicodedata.normalize('NFKC', s)
    # Keep: letters (Unicode category L), numbers (N), and CJK unified ideographs range
    # Remove everything that's in Unicode categories P (punctuation) or S (symbol)
    filtered = []
    for ch in norm:
        cat = unicodedata.category(ch)
        # Allow letters and numbers
        if cat.startswith('L') or cat.startswith('N'):
            filtered.append(ch)
            continue
        # Allow CJK Unified Ideographs (common Chinese/Japanese/Korean block)
        code = ord(ch)
        if (0x4E00 <= code <= 0x9FFF) or (0x3400 <= code <= 0x4DBF) or (0x20000 <= code <= 0x2A6DF):
            filtered.append(ch)
            continue
        # Otherwise skip (remove)
    return ''.join(filtered)
