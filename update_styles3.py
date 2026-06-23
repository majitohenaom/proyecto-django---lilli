import os
import re

dir_path = r"c:\Users\Usuario\OneDrive\Desktop\majito\django lili\djangoLilliana\sena\templates"

for filename in os.listdir(dir_path):
    if not filename.endswith(".html"): continue
    
    filepath = os.path.join(dir_path, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Change soft magenta to an opaque, classic magenta/plum
    # #d946ef -> #9d174d (Tailwind Pink 800)
    # #c026d3 -> #831843 (Tailwind Pink 900)
    content = content.replace('#d946ef', '#9d174d')
    content = content.replace('#c026d3', '#831843')
    content = content.replace('rgba(217, 70, 239,', 'rgba(157, 23, 77,')

    # Fix body background for login and registro
    if filename in ["login.html", "registro.html"]:
        # We need to change the body background back to white, without affecting the brand-panel which should be magenta
        # Let's target the body specifically
        content = re.sub(r'(body\s*{[^}]*?background-color:\s*)#[a-f0-9]+;([^}]*?})', r'\1#ffffff;\2', content)

    # Add HTML5 validation patterns to inputs
    # For numero_documento
    content = re.sub(
        r'(<input[^>]*?name="numero_documento"[^>]*?)>',
        r'\1 pattern="^[a-zA-Z0-9]+$" title="Solo se permiten letras y números.">',
        content
    )
    # Ensure we don't add pattern twice
    content = re.sub(r'pattern="[^"]+"\s+pattern="[^"]+"', 'pattern="^[a-zA-Z0-9]+$"', content)
    content = re.sub(r'title="[^"]+"\s+title="[^"]+"', 'title="Solo se permiten letras y números."', content)
    
    # For username
    content = re.sub(
        r'(<input[^>]*?name="username"[^>]*?)>',
        r'\1 pattern="^[a-zA-Z0-9]+$" title="Solo se permiten letras y números.">',
        content
    )

    # For password
    content = re.sub(
        r'(<input[^>]*?name="password[^"]*"[^>]*?)>',
        r'\1 pattern="^[a-zA-Z0-9!@#\$%\^&\*\-_]+$" title="Caracteres especiales limitados por seguridad.">',
        content
    )
    # Cleanup duplicate attributes if any
    content = re.sub(r'(pattern="[^"]+")\s+\1', r'\1', content)
    content = re.sub(r'(title="[^"]+")\s+\1', r'\1', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Styles updated to opaque magenta, login background fixed, and html validation added.")
