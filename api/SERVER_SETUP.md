# Server Setup

## Getting Info

Get the `SHEET_ID` from the Google Sheet URL.

Generate a `SECRET` from [random.org](https://www.random.org/strings/?num=2&len=32&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new) (put the 2 together) if you don't already have one stored in the Google Apps script Properties.

Get the `GOOGLE_APPS_SCRIPT_URL` from the `Deploy -> Manage Deployments` menu in the Google Apps script linked to the Google Sheet.

Get the `NGROK_TOKEN` and permanent dev url (`NGROK_URL`) from <https://dashboard.ngrok.com/get-started/gateway>.

***Must be in `api` directory***

Save the information in a `.env` file like this:

```env
SHEET_ID=
SECRET=
GOOGLE_APPS_SCRIPT_URL=
NGROK_TOKEN=
NGROK_URL=
```

If `.env` was created on Windows and copied to a Pi, run `dos2unix .env` to fix line endings (`sudo apt install dos2unix` to install command). NGrok will complain if there are CRLF line endings.

`credentials.json` is to be downloaded from the Google Cloud Console (Identity and Access -> Service Accounts) from a project with the Google Sheets API enabled. The email created for the service account should be added to the Google Sheet to give it access.

## Initial Setup commands

```bash
python -m venv . # set up python virtual environment
source bin/activate # switch to that venv
python -m pip install -r requirements.txt # install deps into venv

# NGrok install
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com bookworm main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
```

## Run

This starts the NGrok agent (already configured with a tunnel) and the Flask server together in the same terminal.

```bash
./run.sh
```

NGrok panel will be available on port 4040 where you can monitor requests live from another computer. You can see response codes to check for errors.
Flask API will be available on port 5000, which the NGrok tunnel connects to.
