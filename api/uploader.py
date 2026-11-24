import json
import os

import requests

from .app.util import load_yaml_frontmatter
from .main import COURSE_PATH, l

###########################################################################
#                                                                         #
# This file is for uploading info from the MD files *TO* the Google Sheet #
# YOU SHOULD NOT RUN THIS UNLESS YOU KNOW WHAT YOU ARE DOING!!            #
#                                                                         #
###########################################################################


URL = os.environ.get("GOOGLE_APPS_SCRIPT_URL")
def send_to_sheet(data, sheet):
    response = requests.post(f"{URL}?sheet={sheet}&authorization={os.environ.get("SECRET")}", json=json.dumps(data))
    l.info(f"Response from Google Apps Script: {response.status_code} - {response.text}")

def import_to_spread(slug):
    l.info(f"Importing data for slug: {slug}")
    yml = load_yaml_frontmatter(slug)
    data = [
        yml.get("slug"),
        yml.get("title"),
        yml.get("description"),
        yml.get("short_description")
    ]
    send_to_sheet(data, 0)
    data = [
        yml.get("slug"),
        yml.get("kuula_id")
    ]
    send_to_sheet(data, 1)
    for teacher in yml.get("teachers", []):
        data = [
            yml.get("slug"),
            teacher.get("name"),
            teacher.get("program"),
            teacher.get("degree"),
            teacher.get("career_start"),
            teacher.get("certifications"),
            teacher.get("email"),
            teacher.get("phone"),
            teacher.get("room"),
            teacher.get("love_teaching"),
            teacher.get("fun_fact"),
        ]
        send_to_sheet(data, 2)

def import_all_to_spread():
    for filename in os.listdir(COURSE_PATH):
        if filename.endswith(".md"):
            slug = filename[:-3] # remove .md
            import_to_spread(slug) 

if __name__ == '__main__':
    import_all_to_spread() # Import all to Google Sheet (takes forever)
    # import_to_spread("HSPP") # Import single
