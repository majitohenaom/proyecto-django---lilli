import os
import urllib.request
import re

base_dir = r"c:\Users\Usuario\OneDrive\Desktop\majito\django lili\djangoLilliana\sena"
static_dir = os.path.join(base_dir, "static", "sena")
css_dir = os.path.join(static_dir, "css")
js_dir = os.path.join(static_dir, "js")
fonts_dir = os.path.join(static_dir, "fonts")

os.makedirs(css_dir, exist_ok=True)
os.makedirs(js_dir, exist_ok=True)
os.makedirs(fonts_dir, exist_ok=True)

# Assets to download
assets = [
    ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", os.path.join(css_dir, "bootstrap.min.css")),
    ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js", os.path.join(js_dir, "bootstrap.bundle.min.js")),
    ("https://unpkg.com/htmx.org@1.9.12/dist/htmx.min.js", os.path.join(js_dir, "htmx.min.js")),
    ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css", os.path.join(css_dir, "bootstrap-icons.min.css")),
    ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff2", os.path.join(fonts_dir, "bootstrap-icons.woff2")),
    ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff", os.path.join(fonts_dir, "bootstrap-icons.woff")),
]

for url, path in assets:
    print(f"Downloading {url}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Fix bootstrap-icons.min.css paths
bi_css_path = os.path.join(css_dir, "bootstrap-icons.min.css")
if os.path.exists(bi_css_path):
    with open(bi_css_path, "r", encoding="utf-8") as f:
        bi_css = f.read()
    bi_css = bi_css.replace("./fonts/", "../fonts/")
    with open(bi_css_path, "w", encoding="utf-8") as f:
        f.write(bi_css)

# Process templates
templates_dir = os.path.join(base_dir, "templates")
for filename in os.listdir(templates_dir):
    if not filename.endswith(".html"): continue
    
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Add {% load static %} if not present and if it's a root template or extends one
    # To be safe, just put {% load static %} at the top of login, registro, base_dashboard
    if filename in ["login.html", "registro.html", "base_dashboard.html"]:
        if "{% load static %}" not in content:
            # We must put {% load static %} after {% extends ... %} if it exists
            if "{% extends" in content:
                content = re.sub(r'({% extends [^}]+%})', r'\1\n{% load static %}', content, count=1)
            else:
                content = "{% load static %}\n" + content
            
    # Replace Bootstrap CSS
    content = re.sub(r'<link[^>]*href="[^"]*bootstrap\.min\.css"[^>]*>', '<link rel="stylesheet" href="{% static \'sena/css/bootstrap.min.css\' %}">', content)
    # Replace Bootstrap Icons
    content = re.sub(r'<link[^>]*href="[^"]*bootstrap-icons\.min\.css"[^>]*>', '<link rel="stylesheet" href="{% static \'sena/css/bootstrap-icons.min.css\' %}">', content)
    
    # Replace Bootstrap JS
    content = re.sub(r'<script[^>]*src="[^"]*bootstrap\.bundle\.min\.js"[^>]*></script>', '<script src="{% static \'sena/js/bootstrap.bundle.min.js\' %}"></script>', content)
    
    # Replace HTMX
    content = re.sub(r'<script[^>]*src="[^"]*htmx\.org[^"]*"[^>]*></script>', '<script src="{% static \'sena/js/htmx.min.js\' %}"></script>', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Local resources downloaded and templates updated.")
