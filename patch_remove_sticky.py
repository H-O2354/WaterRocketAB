with open('/app/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We need to completely remove the unused stickyTooltipPlugin since it was rejected by reviewer
content = re.sub(r'// Custom plugin for Sticky Tooltip.*?(?=// Using standard Chart\.js tooltips)', '', content, flags=re.DOTALL)

with open('/app/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
