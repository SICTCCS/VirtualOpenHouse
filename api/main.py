from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import yaml
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import dotenv

from typing import List, Dict

dotenv.load_dotenv()

app: Flask = Flask(__name__)
app.logger.setLevel("DEBUG")
l = app.logger

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPES)
client = gspread.authorize(creds)
def get_sheet_data():
    l.info("Fetching sheet data...")
    spread = client.open_by_key(os.getenv("SHEET_ID"))
    
    handle_course_data(spread.get_worksheet(0).get_all_records())
    handle_class_data(spread.get_worksheet(1).get_all_records())
    handle_teacher_data(spread.get_worksheet(2).get_all_records())

scheduler = BackgroundScheduler()
scheduler.add_job(func=get_sheet_data, trigger="interval", seconds=60)
scheduler.start()

@app.route("/")
def home():
    return "Hello, nothing to see here :|"

@app.route("/api")
def api():
    if request.headers.get("Authorization") != os.environ.get("SECRET"):
        return "Unauthorized", 401
    # TODO: Implement the actual API logic here
    sheet_number = request.args.get("sheet")
    # send to respective function
    return "API endpoint accessed successfully"

COURSE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_courses")

def handle_course_data(data: List[Dict[str, int | float | str]]):
    l.info(f"Handling course data: {data}")
    for course in data:
        slug = course.get("slug")
        l.info(f"Processing course: {slug}")
        l.info(COURSE_PATH)
        with open(f"{COURSE_PATH}/{slug}.md", "w") as f:
            lines = f.readlines()[1:-1] # ignore first and last lines
            yml = yaml.safe_load("\n".join(lines))
        l.info(f"Course YAML data: {yml}")
        

def handle_class_data(data: List[Dict[str, int | float | str]]):
    l.info(f"Handling class data: {data}")
    for class_record in data:
        slug = class_record.get("slug")
        l.info(f"Processing class: {slug}")

def handle_teacher_data(data: List[Dict[str, int | float | str]]):
    l.info(f"Handling teacher data: {data}")
    for teacher in data:
        slug = teacher.get("slug")
        l.info(f"Processing teacher: {slug}")


get_sheet_data() # Initial fetch
app.run(host="0.0.0.0", port=5000, debug=True)