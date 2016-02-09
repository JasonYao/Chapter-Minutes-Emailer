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

## Setup
This program uses a configuration file called (secrets.py)[secrets.py.example], which follows the mantra of "config once, run every time".

Specifically on a clean install upon a PKS server, you'll need to do a few steps:

0.) Copy the mailgun API secret key, and paste it into where `key-yourApiKeyHere`. This can be found on the dashboard to mailgun.com.

1.) [ONLY IN PRODUCTION] Set `is_debug_mode` to `False` after testing functionality.

2.) Copy the brotherhood mailing list in the users array, making sure that everything is comma-deliminated as in the example.

3.) In mailgun.com's routing, make sure that omega & sigma plus addressing forwards to the correct mailbox.

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
