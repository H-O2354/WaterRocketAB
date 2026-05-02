import re

with open('correct.html', 'r', encoding='utf-8') as f:
    correct_html = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    current_html = f.read()

# I see what happened. `correct.html` (commit 331591c) WAS ACTUALLY MISSING THE ENTIRE JAVASCRIPT!
# That means I committed a broken version of index.html in `331591c`.
