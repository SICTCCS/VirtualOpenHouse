
import os, io
from typing import Dict

from ruamel.yaml import YAML

from . import COURSE_PATH, l

def create_yaml():
    yaml = YAML()
    yaml.preserve_quotes = True # keep comments
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 75 # max line length
    return yaml

def get_file_path_from_slug(slug: str) -> str:
    return os.path.join(COURSE_PATH, f"{slug}.md")

def load_yaml_frontmatter(slug: str) -> Dict[str, int | float | str]:
    yml = load_yaml_frontmatter_raw(slug)
    yml['slug'] = slug
    return yml

def load_yaml_frontmatter_raw(slug: str) -> Dict[str, int | float | str]:
    filepath = get_file_path_from_slug(slug)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    if not content.startswith('---\n') and not content.startswith('---\r\n'):
        return {}
    
    # maxsplit=2 splits it into: ['', 'frontmatter content', 'markdown content']
    parts = content.split('---', 2)
    if len(parts) >= 3 and parts[1].strip():
        try:
            return create_yaml().load(parts[1])
        except Exception as err:
            l.error(f"Error loading yaml: {err}", exc_info=True)
    return {}

def save_yaml_frontmatter(slug: str, yml):
    if not yml: 
        l.error("Save data empty")
        return
    filepath = get_file_path_from_slug(slug)
    txt = ""
    try:
        with io.StringIO() as stream:
            create_yaml().dump(yml, stream)
            yaml_content = stream.getvalue()
        txt = f"---\n{yaml_content}---"
    except Exception as err:
        l.error(f"Error creating file txt: {err}", exc_info=True)

    if not txt: return
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(txt)

def update_all(to_update, data: dict):
    for key in data.keys():
        if key == "slug": continue
        to_update[key] = data[key]
    return to_update