#!/usr/bin/env bash
printf "\n\n######## dev ########\n"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


cd ${DIR}/..
source "../venv/bin/activate"
pip install -r requirements.txt
FLASK_RUN_PORT=${PORT:-5000} \
FLASK_ENV=development \
flask run
