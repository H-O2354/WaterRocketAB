import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

inputs_dict = {
    "in-v-bottle": {"min": "0.1", "max": "100.0"},
    "in-l-rocket": {"min": "10", "max": "5000"},
    "in-d-body": {"min": "20", "max": "500"},
    "in-m-empty": {"min": "0.01", "max": "20.0"},
    "in-m-ballast": {"min": "0", "max": "10.0"},
    "in-fin-root": {"min": "5", "max": "500"},
    "in-fin-tip": {"min": "5", "max": "500"},
    "in-fin-span": {"min": "5", "max": "500"},
    "in-water-ratio": {"min": "0", "max": "99"},
    "in-pressure": {"min": "10", "max": "500"},
    "in-burst": {"min": "30", "max": "1000"},
    "in-mass-salt": {"min": "1", "max": "1000"},
    "in-vol-vinegar": {"min": "10", "max": "5000"},
    "in-acid-conc": {"min": "1", "max": "100"},
    "in-gas-eff": {"min": "10", "max": "100"},
    "in-popoff": {"min": "10", "max": "500"},
    "in-d-nozzle": {"min": "5", "max": "200"},
    "in-l-tube": {"min": "0", "max": "10.0"},
    "in-d-tube": {"min": "5", "max": "200"},
    "in-angle": {"min": "0", "max": "90"},
    "in-cd": {"min": "0.01", "max": "5.0"},
    "in-temp": {"min": "-50", "max": "100"}
}

for inp_id, bounds in inputs_dict.items():
    pattern = r'(<input[^>]*id="' + inp_id + r'"[^>]*>)'
    def repl_func(match):
        tag = match.group(1)
        if 'min="' in tag:
            tag = re.sub(r'min="[^"]*"', f'min="{bounds["min"]}"', tag)
        else:
            tag = tag.replace('id=', f'min="{bounds["min"]}" id=')
        if 'max="' in tag:
            tag = re.sub(r'max="[^"]*"', f'max="{bounds["max"]}"', tag)
        else:
            tag = tag.replace('id=', f'max="{bounds["max"]}" id=')
        return tag
    html = re.sub(pattern, repl_func, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
