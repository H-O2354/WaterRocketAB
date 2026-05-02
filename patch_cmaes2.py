import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I am completely lost on where my WASM CMA-ES logic went.
# Did I accidentally write it in a different file? No.
# I wrote it in test_cmaes.js? No.
# Ah, I added `pkg/cmaes_wasm.js`.
# Wait. Did I commit the WASM CMA-ES in `jules-17022902026543574026-4b231fbd`?
# Let's search my previous bash outputs. I wrote `async function optimizeRange() { ... es = new WasmCmaes ... }`
# I can just re-write it! It's better than trying to find it.
