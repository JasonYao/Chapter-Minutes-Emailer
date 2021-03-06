import requests
import secrets
import os
import subprocess
import datetime

__author__ = 'Jason Yao'


def setup_logging():
    log = "logs"

    if not os.path.exists(log):
        os.makedirs(log)

    date = datetime.datetime.now()
    log_file_name = "logs/" + date.strftime('%Y-%m-%d') + ".log"
    return open(log_file_name, 'w'), date


def get_parent_id(log_file, date):
    # Starts the log file stuff
    start = "Chapter Minutes Emailer: " + date.strftime('%Y-%m-%d') + " START\n"
    log_file.write(start)

    # Figures out the file name
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    chapter_minutes_filename = tomorrow.strftime('%Y-%m-%d') + "_minutes.doc"

    # Initialisations for scoping reasons
    parent_id = ""
    file_id = bytes("", 'UTF-8')
    grep_output_list = [""]

    # Builds the bash commands required to go through them all
    drive_command = ["drive", "list"]

    if secrets.is_debug_mode:
        grep_command = ["grep", chapter_minutes_filename]
    else:
        grep_command = ["grep", "3-30-14_Minutes.doc"]  # A known fake document on google drive

    try:
        # Checks to see if the file is on the drive
        drive_output = subprocess.Popen(drive_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        grep_output = subprocess.check_output(grep_command, stdin=drive_output.stdout)
        drive_output.stdout.close()

        # Isolates the output into python-friendly lists
        grep_output_list = grep_output.split()

        file_id = grep_output_list[0]

    except subprocess.CalledProcessError:
        # The file has not been created yet, notifies the relevant parties
        log_file.write("Error: Unable to locate the file, emailing omega for help\n")
        message = "The file " + chapter_minutes_filename + " could not be found on drive. " \
                                                           "Sigma, please add the document to the drive folder," \
                                                           " then let the Omega know in order to re-run this program."
        recipients = [secrets.omega_email, secrets.sigma_email]
        subject = "[Phi Kappa Sigma] [Chapter Minutes Emailer] Shit is burning, halp"
        email(recipients, subject, message)
        log_file.close()
        exit(1)

    # Uses the file id to find the parent directory id
    drive_parent_command = ["drive", "info", "--id", file_id]

    try:
        drive_parent_output = subprocess.Popen(drive_parent_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        file_info = bytes(drive_parent_output.stdout.read()).decode()
        drive_parent_list = file_info.splitlines()[8]
        parent_id = drive_parent_list.split()[1]
    except subprocess.CalledProcessError:
        # The file has found, but an error occurred when getting the parent directory info
        log_file.write("Error: Unable to locate parent directory ID, emailing omega for help\n")
        message = "The file " + file_id.decode() + "'s parent directory ID could not be found on drive. Omega, please" \
                                                   " figure out why this is so."

        recipients = secrets.omega_email
        subject = "[Phi Kappa Sigma] [Chapter Minutes Emailer] Shit is burning, halp"
        email(recipients, subject, message)
        log_file.close()
        exit(1)

    # Logs the relevant meta information
    log_file.write("File name is:\t\t\t" + grep_output_list[1].decode() + "\nFile ID is:\t\t\t" +
                   grep_output_list[0].decode() + "\nFile parent directory is:\t" + parent_id + "\n")
    return parent_id, grep_output_list[1].decode()


def email(recipients, subject, message):
    return requests.post(
        "https://api.mailgun.net/v3/skullhouse.nyc/messages",
        auth=("api", secrets.api_key),
        data={"from": "Samuel Brown Wylie Mitchell <Samuel@skullhouse.nyc>",
              "to": recipients,
              "subject": subject,
              "text": message,
              })


def bcc_email(recipients, subject, message, bcc):
    return requests.post(
        "https://api.mailgun.net/v3/skullhouse.nyc/messages",
        auth=("api", secrets.api_key),
        data={"from": "Samuel Brown Wylie Mitchell <Samuel@skullhouse.nyc>",
              "to": recipients,
              "bcc": bcc,
              "subject": subject,
              "text": message})


def email_users(parent_id, file_name, log_file):
    directory_url = "https://drive.google.com/drive/folders/" + parent_id
    message = "Officers: Please add in your reports for tomorrow's Chapter here: " + directory_url + \
              ".\n All members: Please read through these reports in preparation for chapter tomorrow."

    # Send the email to all users
    subject = "[Phi Kappa Sigma] [Chapter Minutes] " + file_name[:-4]
    bcc_email(secrets.omega_email, subject, message, secrets.users)

    # Logs the email sending completion
    log_file.write("All members emailed (" + str(len(secrets.users)) + " users)\n")
    log_file.write("Chapter Minutes Emailer: " + datetime.datetime.now().strftime('%Y-%m-%d') + " END\n")
    return


def main():
    log_file, date = setup_logging()
    parent_id, file_name = get_parent_id(log_file, date)
    email_users(parent_id, file_name, log_file)
    log_file.close()


# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()
