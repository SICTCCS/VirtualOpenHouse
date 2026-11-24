


import os
from typing import Dict, List

from ..util import load_yaml_frontmatter, save_yaml_frontmatter, update_all
from .. import ROOT_DIR, l

def l_debug(msg):
    l.debug("[H: Course]: "+ msg)
def l_info(msg):
    l.info("[H: Course]: "+ msg)
def l_error(msg):
    l.error("[H: Course]: "+ msg)

def handle_data(data: List[Dict[str, int | float | str]]):
    # l_info(f"Handling course data: {data}")
    for course in data:
        slug = course.get("slug")
        if not slug: continue
        l_info("Saving course info for: " + slug)
        yml = load_yaml_frontmatter(slug)
        yml = update_all(yml, course)
        
        img_path = os.path.join(ROOT_DIR, "assets", "image", "courses", slug)
        if os.path.exists(img_path):
            files = os.listdir(img_path)
            img_num = len([f for f in files if f.endswith(".jpg")])
        else: img_num = 0
        if not "course" in yml: yml["course"] = {}
        yml["course"]["image_num"] = img_num
        
        save_yaml_frontmatter(slug, yml)