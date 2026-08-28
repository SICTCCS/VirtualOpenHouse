from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

import json
from ruamel.yaml import YAML
import os, io, dotenv

from typing import List, Dict

dotenv.load_dotenv()

app: Flask = Flask(__name__)
app.logger.setLevel("DEBUG")
l = app.logger

def create_yaml():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 75
    return yaml

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPES)
client = gspread.authorize(creds)
# fetches data from the Google Sheet and updates the corresponding markdown files
def get_sheet_data():
    l.info("Fetching sheet data...")
    spread = client.open_by_key(os.getenv("SHEET_ID"))
    
    handle_course_data(spread.get_worksheet(0).get_all_records())
    handle_class_data(spread.get_worksheet(1).get_all_records())
    handle_teacher_data(spread.get_worksheet(2).get_all_records())

scheduler = BackgroundScheduler()
scheduler.add_job(func=get_sheet_data, trigger="interval", seconds=1800)
scheduler.start()

################### routes

# placeholder route for the home page
@app.route("/")
def home():
    return "Hello, nothing to see here :|"

# receives data from the Google Apps Script and updates the corresponding markdown files
@app.route("/api", methods=["POST"])
def api():
    if request.headers.get("Authorization") != os.environ.get("SECRET"):
        return "Unauthorized", 401
    sheet = int(request.args.get("sheet"))
    data = request.get_json()
    l.info(f"Received data for sheet {sheet}")
    match sheet:
        case 0:
            handle_course_data(data)
        case 1:
            handle_class_data(data)
        case 2:
            handle_teacher_data(data)
    return "API endpoint accessed successfully"

############### utils

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE_PATH = os.path.join(ROOT_DIR, "_courses")

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

############### save handlers

def handle_course_data(data: List[Dict[str, int | float | str]]):
    # l.info(f"Handling course data: {data}")
    for course in data:
        slug = course.get("slug")
        if not slug: continue
        l.info("Saving course info for: " + slug)
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

def handle_class_data(data: List[Dict[str, int | float | str]]):
    # l.info(f"Handling class data: {data}")
    for class_record in data:
        slug = class_record.get("slug")
        if not slug: continue
        l.info("Saving class info for: " + slug)
        yml = load_yaml_frontmatter(slug)
        yml = update_all(yml, class_record)
        save_yaml_frontmatter(slug, yml)
        

def handle_teacher_data(data: List[Dict[str, int | float | str]]):
    # l.info(f"Handling teacher data: {data}")
    course_teachers: dict[str, list[dict]] = {}
    
    for teacher in data:
        slug = teacher.get("slug")
        if not slug: continue
        teachers: list[dict] = course_teachers.get(slug, [])
        teachers.append(update_all({}, teacher))
        course_teachers[slug] = teachers
    for course in course_teachers.keys():
        teachers = course_teachers[course]
        l.info("Saving teacher for: " + course)
        yml = load_yaml_frontmatter(course)
        yml["teachers"] = teachers
        save_yaml_frontmatter(course, yml)

############### send data to Google Apps Script to update the Google Sheet

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

############# Run stuff

# import_all_to_spread() # Import all to Google Sheet (takes forever)
# import_to_spread("HSPP") # Import single

get_sheet_data() # Initial fetch from Google Sheets API
app.run(host="0.0.0.0", port=5000, debug=True)