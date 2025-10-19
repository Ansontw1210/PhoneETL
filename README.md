# phoneetl-modules

Small collection of text utility helpers used by PhoneETL.

Functions
- to_fullwidth(s): convert ASCII half-width characters to full-width.
- remove_spaces(s): remove spaces (including full-width and whitespace).
- remove_symbols(s): remove punctuation/symbols, keep letters/digits/CJK.

Usage
```
from Modules.text_utils import to_fullwidth, remove_spaces, remove_symbols

print(to_fullwidth('ABC 123!'))
print(remove_spaces(' a b\tc '))
print(remove_symbols('abc, 123。測試！'))
```

License
MIT
