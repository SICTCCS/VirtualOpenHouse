from typing import Dict, List

from ..util import load_yaml_frontmatter, save_yaml_frontmatter, update_all
from .. import l

def l_debug(msg):
    l.debug("[H: Classroom]: "+ msg)
def l_info(msg):
    l.info("[H: Classroom]: "+ msg)
def l_error(msg):
    l.error("[H: Classroom]: "+ msg)

def handle_data(data: List[Dict[str, int | float | str]]):
    # l_info(f"Handling class data: {data}")
    for class_record in data:
        slug = class_record.get("slug")
        if not slug: continue
        l_info("Saving class info for: " + slug)
        yml = load_yaml_frontmatter(slug)
        yml = update_all(yml, class_record)
        save_yaml_frontmatter(slug, yml)