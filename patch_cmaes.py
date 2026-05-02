import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to find the `function optimizeRange()` that I had previously written that uses WasmCmaes
# I'll just write it from scratch to be safe, because I'm not sure which commit I put it in
# before it got overwritten or deleted.
