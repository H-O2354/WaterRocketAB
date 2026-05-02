import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_str = "<!-- ARCHITECTURE MODAL -->"
end_str = "<!-- SCRIPT SECTION -->"

start_idx = html.find(start_str)
end_idx = html.find(end_str)

arch_modal_html = html[start_idx:end_idx]

# Convert `<span class="tree-math">\( ... \)</span>` or just `\( ... \)` to plain text
# without ANY formatting

def remove_latex(text):
    text = re.sub(r'<span class="tree-math">\\\(\s*(.*?)\s*\\\)</span>', r'\1', text)
    text = re.sub(r'\\\(\s*(.*?)\s*\\\)', r'\1', text)

    # Very crude LaTeX command removal
    text = text.replace(r'\frac', '')
    text = text.replace(r'\sqrt', 'sqrt')
    text = text.replace(r'\rho', 'rho')
    text = text.replace(r'\gamma', 'gamma')
    text = text.replace(r'\theta', 'theta')
    text = text.replace(r'\cos', 'cos')
    text = text.replace(r'\sin', 'sin')
    text = text.replace(r'\mu', 'mu')
    text = text.replace(r'\dots', '...')
    text = text.replace(r'\left|', '|')
    text = text.replace(r'\right|', '|')
    text = text.replace(r'\cdot', '*')
    text = text.replace(r'_{', '_')
    text = text.replace(r'^{', '^')
    text = text.replace(r'}', '')
    text = text.replace(r'{', '')
    text = text.replace(r'\text', '')
    return text

arch_modal_html = remove_latex(arch_modal_html)

html = html[:start_idx] + arch_modal_html + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
