from typing import Dict, List

from ..util import load_yaml_frontmatter, save_yaml_frontmatter, update_all
from .. import l

def l_debug(msg):
    l.debug("[H: Teacher]: "+ msg)
def l_info(msg):
    l.info("[H: Teacher]: "+ msg)
def l_error(msg):
    l.error("[H: Teacher]: "+ msg)

def handle_data(data: List[Dict[str, int | float | str]]):
    # l_info(f"Handling teacher data: {data}")
    course_teachers: dict[str, list[dict]] = {}
    
    for teacher in data:
        slug = teacher.get("slug")
        if not slug: continue
        teachers: list[dict] = course_teachers.get(slug, [])
        teachers.append(update_all({}, teacher))
        course_teachers[slug] = teachers
    for course in course_teachers.keys():
        teachers = course_teachers[course]
        l_info("Saving teacher for: " + course)
        yml = load_yaml_frontmatter(course)
        yml["teachers"] = teachers
        save_yaml_frontmatter(course, yml)