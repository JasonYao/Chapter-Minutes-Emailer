# Chapter-Minute-Emailer
By Jason Yao

## Description
Emails all active brothers with a link to the chapter minutes the day before a chapter meeting.

## Dependencies
The first dependency is the [gDrive](https://github.com/prasmussen/gdrive) binary - simply download that file and
move it to your `/usr/local/bin/` directory, and name it `drive`

The second dependency is python 3.5.x, and then installing the [requests](http://docs.python-requests.org/en/latest/) with the following:

```sh
# If you use a virtualenv (you should), activate it now
pip3 install requests
```

## Running commands
```sh
# If you use a virtualenv (you should), activate it now
python3 Emailer.py
```

## To automate this with a `cron` job
Setup a cronjob where the `cron` daemon will run a box-specific version of [run.sh](run.sh). 
An example script is the [time.sh](time.sh) script, which should only be run once, and will
add the job to be run once a week at saturday morning at 12:30am.

## License
This repo is distributed under the GNU GPL v2 license. A copy of that license may be found [here](LICENSE)
