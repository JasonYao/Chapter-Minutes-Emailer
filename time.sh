#!/usr/bin/env bash

set -e

# Write out current crontab
crontab -l > tempCron

echo "30 0 * * sat /server/minutes_emailer/run.sh" >> tempCron

# Adds a newline character
echo  >> tempCron;

# Installs new cron file
crontab tempCron
rm tempCron
