from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import gspread
from google.oauth2 import service_account

import os, dotenv
import logging

dotenv.load_dotenv() # load .env file

app: Flask = Flask(__name__)

#### Logging

l = app.logger
l.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
try:
    from colorlog import ColoredFormatter
    formatter = ColoredFormatter("%(log_color)s%(levelname)s: %(message)s", log_colors={
        "DEBUG":"white","INFO":"green","WARNING":"yellow","ERROR":"red","CRITICAL":"bold_red"
    })
except:
    l.warning("ColorLog not available. Is it installed?")
    formatter = logging.Formatter("%(levelname)s:\n%(message)s")
handler.setFormatter(formatter)
l.handlers = [handler]

def l_info_x(msg): # log level is green but msg is not
  l.info("\033[0m"+msg)

#### Consts

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
l_info_x("Root dir: "+ROOT_DIR)
COURSE_PATH = os.path.join(ROOT_DIR, "_courses")
IMAGE_PATH = os.path.join(ROOT_DIR, "assets", "image", "courses")

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

#### Google

creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

from .handlers import course, classroom, image, teacher

#### Fetcher

# fetches data from the Google Sheet and updates the corresponding markdown files
def get_all_data():
    l.info("Fetching data...")
    spread = client.open_by_key(os.getenv("SHEET_ID"))
    
    course.handle_data(spread.get_worksheet(0).get_all_records())
    classroom.handle_data(spread.get_worksheet(1).get_all_records())
    teacher.handle_data(spread.get_worksheet(2).get_all_records())
    image.handle()


# get from sheet on schedule even if it may not have been updated
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_all_data, trigger="interval", seconds=1800) # 30 minutes

#### Routes

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
            course.handle_data(data)
        case 1:
            classroom.handle_data(data)
        case 2:
            teacher.handle_data(data)
        case 3:
            image.handle()
    return "API endpoint accessed successfully"
