import os
import re
import base64

def enhance_markdown(content):
    # Preserve original content
    original_content = base64.b64encode(content.encode()).decode()

    css_styles = """<style>
  .md-enhanced {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
  }
  .md-enhanced .container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
  }
  .md-enhanced h1, .md-enhanced h2 {
    color: #2c3e50;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
  }
  .md-enhanced .hero {
    background-color: #3498db;
    color: white;
    padding: 40px 20px;
    margin: -20px -20px 20px -20px;
    border-radius: 8px 8px 0 0;
    text-align: center;
  }
  .md-enhanced .hero h1 {
    font-size: 2.5em;
    margin: 0;
    border: none;
    color: white;
  }
  .md-enhanced .nav-bar {
    background-color: #2c3e50;
    margin: -20px -20px 20px -20px;
    padding: 10px;
  }
  .md-enhanced .nav-bar ul {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    padding: 0;
    list-style-type: none;
    margin: 0;
  }
  .md-enhanced .nav-bar ul li {
    margin: 5px 10px;
  }
  .md-enhanced .nav-bar ul li a {
    color: white;
    text-decoration: none;
    font-weight: bold;
    transition: color 0.3s ease;
  }
  .md-enhanced .nav-bar ul li a:hover {
    color: #3498db;
  }
  .md-enhanced pre {
    background-color: #f8f8f8;
    border-left: 4px solid #3498db;
    padding: 15px;
    overflow-x: auto;
  }
  .md-enhanced code {
    font-family: 'Courier New', Courier, monospace;
  }
  .md-enhanced .button {
    display: inline-block;
    background-color: #3498db;
    color: white;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }
  .md-enhanced .button:hover {
    background-color: #2980b9;
  }
</style>

"""

    # Remove Table of Contents (including HTML-enclosed versions) and everything until the first "# "
    content = re.sub(r'(?:(?:(?:<h2>)?\s*Table of Contents\s*(?:</h2>)?\n?(?:[-*].*\n?)*(?=\n#|\Z))|(?:<!-- TOC -->[\s\S]*?<!-- /TOC -->))|(.*?\n# )', '', content, flags=re.IGNORECASE | re.MULTILINE)

    # Extract headers before modifying the content
    headers = re.findall(r'^##\s*(.+)$', content, re.MULTILINE)

    # Wrap the content in a div with a class for scoping
    content = f'<div class="md-enhanced">\n<div class="container">\n\n{content.strip()}\n\n</div>\n</div>'

    # Extract title (first heading)
    title_match = re.search(r'^#\s*(.+)$|<h1>(.*?)</h1>', content, re.MULTILINE | re.IGNORECASE)
    if title_match:
        title = title_match.group(1) or title_match.group(2)
        hero_section = f'<div class="hero">\n  <h1>{title}</h1>\n</div>\n\n'
        content = re.sub(r'^#\s*.+$|<h1>.*?</h1>', hero_section, content, 1, re.MULTILINE | re.IGNORECASE)

    # Add navigation
    if headers:
        nav_items = '\n'.join([f'    <li><a href="#{h.lower().replace(" ", "-")}">{h}</a></li>' for h in headers])
        nav_section = f'<div class="nav-bar">\n  <ul>\n{nav_items}\n  </ul>\n</div>\n\n'
        # Insert nav section after the hero section
        content = re.sub(r'(</div>\n\n)', r'\1' + nav_section, content, 1)

    # Enhance code blocks
    content = re.sub(r'```(\w+)\n([\s\S]+?)```', lambda m: f'<pre><code class="{m.group(1)}">\n{m.group(2).strip()}\n</code></pre>', content)

    # Add CSS to the top of the file
    content = css_styles + content

    # Add original content as a comment
    content += f'\n\n<!-- ORIGINAL_CONTENT\n{original_content}\n-->'

    return content

def revert_to_markdown(content):
    # Extract original content
    original_match = re.search(r'<!-- ORIGINAL_CONTENT\n(.+?)\n-->', content, re.DOTALL)
    if original_match:
        original_content = base64.b64decode(original_match.group(1)).decode()
        return original_content
    else:
        # If original content is not found, fall back to removing enhanced elements
        content = re.sub(r'<style>[\s\S]*?</style>\s*', '', content)
        content = re.sub(r'<div class="md-enhanced">\s*<div class="container">\s*', '', content)
        content = re.sub(r'\s*</div>\s*</div>\s*$', '', content)
        hero_match = re.search(r'<div class="hero">\s*<h1>(.+?)</h1>\s*</div>', content)
        if hero_match:
            content = re.sub(r'<div class="hero">[\s\S]*?</div>\s*', '', content)
        content = re.sub(r'<div class="nav-bar">[\s\S]*?</div>\s*', '', content)
        content = re.sub(r'<pre><code class="(\w+)">\s*([\s\S]+?)\s*</code></pre>', r'```\1\n\2\n```', content)
        return content.strip()

def process_files(mode):
    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()

            if mode == 'enhance':
                new_content = enhance_markdown(content)
                new_filename = f"{os.path.splitext(filename)[0]}_enhanced.md"
                action = "Enhanced"
            elif mode == 'revert':
                if not filename.endswith('_enhanced.md'):
                    continue
                new_content = revert_to_markdown(content)
                new_filename = filename.replace('_enhanced.md', '.md')
                action = "Reverted"
            else:
                print(f"Invalid mode: {mode}")
                return

            with open(new_filename, 'w', encoding='utf-8') as file:
                file.write(new_content)

            print(f"{action} {filename} --> {new_filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 or sys.argv[1] not in ['enhance', 'revert']:
        print("Usage: python script.py [enhance|revert]")
    else:
        process_files(sys.argv[1])