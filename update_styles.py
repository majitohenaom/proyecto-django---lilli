import os
import re

dir_path = r"c:\Users\Usuario\OneDrive\Desktop\majito\django lili\djangoLilliana\sena\templates"

for filename in os.listdir(dir_path):
    if not filename.endswith(".html"): continue
    
    filepath = os.path.join(dir_path, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Make gradients solid magenta
    content = re.sub(r'background:\s*linear-gradient\([^)]+\);', 'background-color: #ff00ff;', content)
    content = re.sub(r'background:\s*linear-gradient\([^)]+\)\s*!important;', 'background-color: #ff00ff !important;', content)
    content = re.sub(r'style="background:\s*linear-gradient\([^)]+\);', 'style="background-color: #ff00ff;', content)
    
    # Replace purple and dark purple with pure magenta (#ff00ff) or darker magenta (#cc00cc)
    content = content.replace('#DDA0DD', '#ff00ff')
    content = content.replace('#dda0dd', '#ff00ff')
    content = content.replace('#4B0082', '#cc00cc')
    content = content.replace('#4b0082', '#cc00cc')
    
    # Remove all box-shadows that represent a glow (those starting with 0 0 or inset 0 0)
    # This covers things like box-shadow: 0 0 15px rgba(255, 0, 255, 0.4);
    content = re.sub(r'box-shadow:\s*(?:inset\s+)?0\s+0\s+\d+px\s*(?:rgba?\([^)]+\)|#[a-fA-F0-9]{3,6}|var\([^)]+\))[^;]*;', 'box-shadow: none;', content)
    
    # Specifically target any remaining var(--sena-glow) box-shadows or text-shadows
    content = re.sub(r'box-shadow:[^;]+var\(--sena-(?:purple-)?glow\)[^;]*;', 'box-shadow: none;', content)
    content = re.sub(r'text-shadow:[^;]+var\(--sena-(?:purple-)?glow\)[^;]*;', 'text-shadow: none;', content)
    
    # text-shadows with color glow
    content = re.sub(r'text-shadow:\s*0\s+0\s+\d+px\s*(?:rgba?\([^)]+\)|#[a-fA-F0-9]{3,6})[^;]*;', 'text-shadow: none;', content)
    
    # Reset specific variables in base_dashboard.html
    content = re.sub(r'--sena-dark:\s*#[a-fA-F0-9]+;', '--sena-dark: #cc00cc;', content)
    content = re.sub(r'--sena-purple:\s*#[a-fA-F0-9]+;', '--sena-purple: #ff00ff;', content)
    content = re.sub(r'--sena-glow:\s*rgba\([^)]+\);', '--sena-glow: transparent;', content)
    content = re.sub(r'--sena-purple-glow:\s*rgba\([^)]+\);', '--sena-purple-glow: transparent;', content)

    # For base dashboard header shadows
    content = content.replace('box-shadow: 0 0 20px var(--sena-glow), 0 0 40px var(--sena-purple-glow);', 'box-shadow: none;')
    content = content.replace('text-shadow: 0 0 5px #ff00ff;', 'text-shadow: none;')
    
    # For animation pulse
    content = re.sub(r'animation:\s*pulse\s+[^;]+;', 'animation: none;', content)
    
    # specific text-shadow fix in case
    content = re.sub(r'text-shadow:\s*[^;]*#ff00ff[^;]*;', 'text-shadow: none;', content)
    
    # Filter for sidebar link active
    content = re.sub(r'box-shadow:\s*0\s*0\s*15px\s*#ff00ff,\s*0\s*0\s*5px\s*#ff00ff;', 'box-shadow: none;', content)
    content = re.sub(r'filter:\s*drop-shadow\([^)]+\)[^;]*;', 'filter: none;', content)
    
    # card shadows
    content = re.sub(r'--card-shadow-hover:[^;]+;', '--card-shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.1);', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Styles updated.")
