#!/bin/bash

## Runs both the API and Jekyll servers
## Both SETUP.md and API_SETUP.md must be followed before running

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

NM="voh"

/usr/bin/tmux kill-session -t "$NM" 2>/dev/null

/usr/bin/tmux new-session -d -s "$NM" \
  'while true; do bundle exec jekyll serve --host 0.0.0.0; rc=$?; if [ "$rc" -eq 0 ] || [ "$rc" -eq 130 ]; then break; fi; echo "Jekyll exited ($rc); retrying in 5s"; sleep 5; done; exec bash'

/usr/bin/tmux split-window -v -t "$NM" \
  'while true; do ./api/run.sh; rc=$?; if [ "$rc" -eq 0 ] || [ "$rc" -eq 130 ]; then break; fi; echo "API exited ($rc); retrying in 5s"; sleep 5; done; exec bash'


# to connect to this session:
# tmux a -t voh
