import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_str = "<!-- ARCHITECTURE MODAL -->"
end_str = "<!-- SCRIPT SECTION -->"

start_idx = html.find(start_str)
end_idx = html.find(end_str)

arch_modal_html = html[start_idx:end_idx]

# Remove the math tags entirely! The user said "bỏ mấy công thức latex đi" (remove latex formulas)
# Maybe they literally mean remove the UL lists with math formulas from that section?
# Wait, they said "Btw mục system architecture không cần viết công thức đâu, bỏ mấy công thức latex đi yeah"
# Let's replace the content of that modal with just the headings from the tree without math formulas.

# Or just use the original script with explicit strings to get clean formulas.
