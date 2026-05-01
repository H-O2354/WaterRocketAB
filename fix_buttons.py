import re

with open('index.html', 'r') as f:
    content = f.read()

# Make the header flex wrap so buttons don't overflow on small screens
content = content.replace("header {\n    display: flex;\n    justify-content: space-between;", "header {\n    display: flex;\n    flex-wrap: wrap;\n    justify-content: space-between;")
content = content.replace(".header-controls button {\n    background: transparent;\n    color: var(--accent);\n    border: 1px solid var(--accent);\n    padding: 8px 15px;\n    margin-left: 10px;\n", ".header-controls button {\n    background: transparent;\n    color: var(--accent);\n    border: 1px solid var(--accent);\n    padding: 8px 15px;\n    margin: 5px 0 5px 10px;\n")

# Remove the theme selector as the user said "UI trắng đen ok nè" meaning B&W is fine, maybe we keep the light/dark mode but the previous design was okay. Actually let's just make it look good.
content = content.replace(".header-controls {\n    display: flex;\n    align-items: center;\n}", ".header-controls {\n    display: flex;\n    align-items: center;\n    flex-wrap: wrap;\n}")

with open('index.html', 'w') as f:
    f.write(content)
