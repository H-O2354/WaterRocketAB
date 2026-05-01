import re

with open('index.html', 'r') as f:
    content = f.read()

# Make sure title is on one line by adjusting flex wrap or font size
content = content.replace("header h1 {", "header h1 {\n    white-space: nowrap;\n    font-size: 1.2rem;")

# Replace "Trục Y1 (Chính):"
content = content.replace("<label>Trục Y1 (Chính):</label>", "<label>Trục Y1:</label>")
content = content.replace("<label>Trục Y2 (Phụ):</label>", "<label>Trục Y2:</label>")

with open('index.html', 'w') as f:
    f.write(content)
