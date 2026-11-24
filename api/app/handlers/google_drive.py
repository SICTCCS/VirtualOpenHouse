import io, os, shutil

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from .. import creds, l

def l_debug(msg):
    l.debug("[GDrive]: "+ msg)

service = build("drive", "v3", credentials=creds)

def list_files_in_folder(folder_id):
    all_files = []
    page_token = None
    query = (
        f"'{folder_id}' in parents and "
        "mimeType != 'application/vnd.google-apps.folder' and "
        "trashed = false"
    )

    while True:
        response = service.files().list(
            q=query,
            orderBy="name_natural",
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token,
            pageSize=100
        ).execute()

        all_files.extend(response.get("files", []))
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break

    return all_files

def list_folders_in_folder(folder_id):
    all_folders = []
    page_token = None
    query = (
        f"'{folder_id}' in parents and "
        "mimeType = 'application/vnd.google-apps.folder' and "
        "trashed = false"
    )

    while True:
        response = service.files().list(
            q=query,
            orderBy="name_natural",
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token,
            pageSize=100
        ).execute()

        all_folders.extend(response.get("files", []))
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break

    return all_folders

def download_to_folder(file_id, folder, file_name=None):
    # Source - https://stackoverflow.com/a/60114435 (modified heavily)
    # Posted by Aerials, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-11-17, License - CC BY-SA 4.0

    if not file_name:
        file_metadata = service.files().get(fileId=file_id, fields='mimeType, name').execute()
        file_name = file_metadata.get('name')
    l_debug(f"Downloading file: {file_name} to {folder}")

    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        l_debug("Download %d%%" % int(status.progress() * 100))

    # The file has been downloaded into RAM, now save it in a file
    fh.seek(0)
    with open(os.path.join(folder, file_name), "wb") as f:
        shutil.copyfileobj(fh, f, length=131072)

def download_all_to_folder(file_ids, folder):
    for id in file_ids:
        download_to_folder(id, folder)