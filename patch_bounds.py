with open('/app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all inputs with ones that have explicit realistic min/max bounds

replacements = {
    'id="in-v-bottle" value="0.5" step="0.1"': 'id="in-v-bottle" value="0.5" step="0.1" min="0.1" max="5.0"',
    'id="in-l-rocket" value="60"': 'id="in-l-rocket" value="60" min="10" max="200"',
    'id="in-d-body" value="65"': 'id="in-d-body" value="65" min="20" max="150"',
    'id="in-m-empty" value="0.1" step="0.01"': 'id="in-m-empty" value="0.1" step="0.01" min="0.01" max="1.0"',
    'id="in-m-ballast" value="0.005" step="0.01"': 'id="in-m-ballast" value="0.005" step="0.01" min="0" max="0.5"',
    'id="in-fin-root" value="25"': 'id="in-fin-root" value="25" min="5" max="100"',
    'id="in-fin-tip" value="25"': 'id="in-fin-tip" value="25" min="5" max="100"',
    'id="in-fin-span" value="25"': 'id="in-fin-span" value="25" min="5" max="100"',
    'id="in-water-ratio" value="33"': 'id="in-water-ratio" value="33" min="0" max="80"',
    'id="in-pressure" value="60"': 'id="in-pressure" value="60" min="10" max="200"',
    'id="in-burst" value="120"': 'id="in-burst" value="120" min="30" max="300"',
    'id="in-mass-salt" value="7.6"': 'id="in-mass-salt" value="7.6" min="1" max="100"',
    'id="in-vol-vinegar" value="109"': 'id="in-vol-vinegar" value="109" min="10" max="1000"',
    'id="in-acid-conc" value="5"': 'id="in-acid-conc" value="5" min="1" max="20"',
    'id="in-gas-eff" value="85"': 'id="in-gas-eff" value="85" min="10" max="100"',
    'id="in-popoff" value="70"': 'id="in-popoff" value="70" min="10" max="200"',
    'id="in-d-nozzle" value="21"': 'id="in-d-nozzle" value="21" min="5" max="50"',
    'id="in-l-tube" value="0.5" step="0.1"': 'id="in-l-tube" value="0.5" step="0.1" min="0" max="2.0"',
    'id="in-d-tube" value="21"': 'id="in-d-tube" value="21" min="5" max="50"',
    'id="in-angle" value="45"': 'id="in-angle" value="45" min="0" max="90"',
    'id="in-cd" value="0.45" step="0.01"': 'id="in-cd" value="0.45" step="0.01" min="0.1" max="2.0"',
    'id="in-temp" value="27"': 'id="in-temp" value="27" min="-10" max="50"'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open('/app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
