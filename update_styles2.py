import os
import re

dir_path = r"c:\Users\Usuario\OneDrive\Desktop\majito\django lili\djangoLilliana\sena\templates"

for filename in os.listdir(dir_path):
    if not filename.endswith(".html"): continue
    
    filepath = os.path.join(dir_path, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Soft Magenta Palette (Tailwind Fuchsia 500 & 600)
    # primary: #d946ef (rgb: 217, 70, 239)
    # hover/dark: #c026d3 (rgb: 192, 38, 211)
    
    # Replace previous harsh magenta with soft magenta
    content = content.replace('#ff00ff', '#d946ef')
    content = content.replace('#FF00FF', '#d946ef')
    
    # Replace the previous hover color
    content = content.replace('#cc00cc', '#c026d3')
    content = content.replace('#CC00CC', '#c026d3')
    
    # Replace rgba usages of harsh magenta
    content = content.replace('rgba(255, 0, 255,', 'rgba(217, 70, 239,')
    content = content.replace('rgba(255,0,255,', 'rgba(217, 70, 239,')
    content = content.replace('rgba(255, 255, 255, 0.1)', 'rgba(255, 255, 255, 0.2)') # little brighter for badges

    # Fix card shadows to be completely neutral and beautiful
    # Replacing the old purple-tinted card shadow
    content = content.replace('rgba(75, 0, 130, 0.1)', 'rgba(0, 0, 0, 0.06)')
    content = content.replace('rgba(75, 0, 130, 0.05)', 'rgba(0, 0, 0, 0.03)')
    
    # Also in forms (login/registro) we can make borders softer
    # find form-control border
    content = re.sub(r'border:\s*1\.5px\s*solid\s*#e2e8f0;', 'border: 1px solid #e2e8f0;', content)
    
    # Replace border color for premium-card
    content = re.sub(r'border:\s*2px\s*solid\s*rgba\(255,\s*0,\s*255,\s*0\.5\);', 'border: 1px solid rgba(217, 70, 239, 0.3);', content)
    content = re.sub(r'border:\s*2px\s*solid\s*rgba\(217,\s*70,\s*239,\s*0\.5\);', 'border: 1px solid rgba(217, 70, 239, 0.3);', content)
    
    # Hover borders
    content = content.replace('border-color: #DDA0DD;', 'border-color: #d946ef;')
    
    # Update --card-shadow-hover to a soft lift without glow
    content = re.sub(r'--card-shadow-hover:\s*0\s*4px\s*12px\s*rgba\(0,\s*0,\s*0,\s*0\.1\);', '--card-shadow-hover: 0 12px 30px -10px rgba(0, 0, 0, 0.1), 0 8px 16px -8px rgba(0, 0, 0, 0.04);', content)
    
    # Add a subtle, non-glow shadow to the btn-sena-primary for elegance
    content = re.sub(r'\.btn-sena-primary\s*{\s*(?:[^}]+?\s*)?box-shadow:\s*none;\s*', '.btn-sena-primary {\n            box-shadow: 0 4px 6px -1px rgba(217, 70, 239, 0.2), 0 2px 4px -1px rgba(217, 70, 239, 0.1);\n            ', content)
    
    # Add beautiful hover effect for primary button
    content = re.sub(r'\.btn-sena-primary:hover\s*{\s*(?:[^}]+?\s*)?box-shadow:\s*none;\s*', '.btn-sena-primary:hover {\n            box-shadow: 0 10px 15px -3px rgba(217, 70, 239, 0.25), 0 4px 6px -2px rgba(217, 70, 239, 0.15);\n            ', content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Styles updated to soft magenta and polished.")
