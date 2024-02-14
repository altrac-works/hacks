#!/usr/bin/env bash

if [ -f "committees.sqlite3" ]; then
    echo "Refusing to operate on an existing sqlite3 file"
    exit 1
fi
echo ".import --csv committees.csv committees" | sqlite3 committees.sqlite3
echo ".import --csv committee-members.csv committee_members" | sqlite3 committees.sqlite3
