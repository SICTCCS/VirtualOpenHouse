#!/bin/bash

## Runs both the API and Jekyll servers
## Both LINUX.md and APL_SETUP.md must be followed before running

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

NM="voh"

/usr/bin/tmux kill-session -t "$NM" 2>/dev/null

/usr/bin/tmux new-session -d -s "$NM" "bundle exec jekyll serve --host 0.0.0.0; exec bash"

/usr/bin/tmux split-window -v -t "$NM" "./api/run.sh; exec bash"


# to connect to this session:
# tmux a -t voh
