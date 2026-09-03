# Server Setup

## Getting Info

Get the `SHEET_ID` from the Google Sheet URL.

Generate a `SECRET` from [random.org](https://www.random.org/strings/?num=2&len=32&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new) (put the 2 together) if you don't already have one stored in the Google Apps script Properties.

Get the `GOOGLE_APPS_SCRIPT_URL` from the `Deploy -> Manage Deployments` menu in the Google Apps script linked to the Google Sheet.

Get the `NGROK_TOKEN` and permanent dev url (`NGROK_URL`) from <https://dashboard.ngrok.com/get-started/gateway>.

Save the information in a `.env` file like this:

```env
SHEET_ID=
SECRET=
GOOGLE_APPS_SCRIPT_URL=
NGROK_TOKEN=
NGROK_URL=
```

## Initial Setup commands

***Must be in `api` directory***

```bash
python -m venv .

curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com bookworm main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
```

## Run

```bash
./run.sh
```
