import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace 'X-Axis:' with 'Trục X:'
content = content.replace("innerHtml += `<tr><td>X-Axis: ${dataPoint.x.toFixed(3)}</td></tr>`;", "innerHtml += `<tr><td>Trục X: ${dataPoint.x.toFixed(3)}</td></tr>`;")
content = content.replace("innerHtml += `<tr><td>Y-Axis: ${dataPoint.y.toFixed(3)}</td></tr>`;", "innerHtml += `<tr><td>Trục Y: ${dataPoint.y.toFixed(3)}</td></tr>`;")

with open('index.html', 'w') as f:
    f.write(content)
