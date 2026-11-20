
import json
import os
import re
from typing import List

import requests

from ..util import load_yaml_frontmatter, save_yaml_frontmatter, update_all
from .. import IMAGE_PATH, l
from . import google_drive

def l_debug(msg):
    l.debug("[H: Image]: "+ str(msg))
def l_info(msg):
    l.info("[H: Image]: "+ str(msg))
def l_error(msg):
    l.error("[H: Image]: "+ str(msg))

def handle():
    """The main function that updates all images
    """
    # handle_data(get_image_data()) # old, left for reference
    download_course_images()
    download_teacher_images()

def download_teacher_images():
    teacher_imgs = google_drive.list_files_in_folder(os.environ.get("GOOGLE_DRIVE_TEACHER_IMAGES_ID"))
    l_debug(teacher_imgs)
    
    for img in teacher_imgs:
        l_debug(img)
        slug_match = re.match(r"([A-Z]+)-([0-9]*)[A-Za-z\-]+", img.get("name"))
        if slug_match is None: continue
        slug: str = slug_match.group(1)
        num: int = slug_match.group(2)
        if not num: num = 0

        course_dir = os.path.join(IMAGE_PATH, slug)
        if not os.path.exists(course_dir): continue
        teacher_dir = os.path.join(course_dir, "teachers")
        os.makedirs(teacher_dir, exist_ok=True)

        l_info(f"Downloading {img.get("id")} -> {teacher_dir}/{num}.jpg")
        google_drive.download_to_folder(img.get("id"), teacher_dir, file_name=f"{num}.jpg")

def download_course_images():    
    course_img_folders = google_drive.list_folders_in_folder(os.environ.get("GOOGLE_DRIVE_COURSE_IMAGES_ID"))
    l_debug(course_img_folders)
    for dir in course_img_folders:
        slug = dir.get("name")
        if slug is None: continue
        course_dir = os.path.join(IMAGE_PATH, slug)

        imgs = google_drive.list_files_in_folder(dir["id"])
        l_info(f"Course {slug}: \033[0m"+str(imgs))
        google_drive.download_all_to_folder([img.get("id") for img in imgs], course_dir)


######################################################

def get_image_data():
    """**NOT USED ANYMORE.** left for reference/possible future use <br><br>
    Retrieves image info from Sheet using Google Apps Script

    Returns:
        dict: data with img URLS
    """
    resp = requests.request("GET", os.environ.get("GOOGLE_APPS_SCRIPT_URL")+f"?sheet=3&authorization={os.environ.get("SECRET")}")    
    return json.loads(resp.text)

def handle_data(data: List[dict[str, int | float | str]]):
    """**NOT USED ANYMORE.** left for reference/possible future use <br><br>
    Downloads images using URLs returned from `get_image_data()`
    """
    l_info(f"Handling image data: {data}")
    # return
    course_images: dict[str, list[dict]] = {}
    
    for image in data:
        slug = image.get("slug")
        if not slug: continue
        images: list[dict] = course_images.get(slug, [])
        images.append(update_all({}, image))
        course_images[slug] = images
    for course in course_images.keys():
        images = course_images[course]
        yml = load_yaml_frontmatter(course)
        yml["course"]["captions"] = [c["caption"] for c in images]
        l_info([c["caption"] for c in images])
        save_yaml_frontmatter(course, yml)
        l_info("Downloading images for: " + course)
        i = 0
        for img in images:
            l_info(img)
            image_url = img.get("image")
            if not image_url:
                continue

            try:
                response = requests.get(image_url, stream=True, timeout=30)
                response.raise_for_status()
                filename = f"{i}.jpg"

                destination = os.path.join(IMAGE_PATH, course)
                os.makedirs(destination, exist_ok=True)
                filepath = os.path.join(destination, filename)
                with open(filepath, "wb") as output:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            output.write(chunk)
                l_info("Saved image to: " + filepath)
                i += 1
            except requests.RequestException as error:
                l_error(f"Unable to download image {image_url}: {error}")
