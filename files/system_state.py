#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import socket

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

FILE_REPORT="/tmp/system_perfomance_info.txt"
FILE_REPORT_SS="/tmp/netstat.txt"
DELIMETER_STRING = "====================================="

SMTP_SERVER = os.environ.get('SMTP_SERVER', "smtp.yandex.ru")
SMTP_PORT = os.environ.get('SMTP_PORT', "465")
SMTP_USER = os.environ.get('SMTP_USER', "")
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', "")

def get_command(command):
    if not isinstance(command, (list, tuple)):
        command = [command]

    stdin = subprocess.PIPE

    try:
        for comm in command:
            proc = subprocess.Popen(comm.split(), stdin=stdin, stdout=subprocess.PIPE)
            stdin = stdin=proc.stdout
        output = str(proc.stdout.read())
    except OSError:
        output = "command not found"

    return  output

def new_report_file(filename):
    return open(filename, "w")

def report_command(command, text_report, file_report):
    if isinstance(command, (list, tuple)):
        command = " | ".join(command)
    for text in (DELIMETER_STRING, command, DELIMETER_STRING, text_report, DELIMETER_STRING):
        file_report.write("\n")
        file_report.write(text)

def send_message_for_mail(to, subject, body, files):
    from_message = SMTP_USER

    msg = MIMEMultipart()
    msg['From'] = from_message
    # msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)



    try:
        if str(SMTP_PORT) == "465":
            smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        else:
            smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        if SMTP_USER and SMTP_PASSWORD:
            smtp.login(SMTP_USER, SMTP_PASSWORD)

        smtp.ehlo()
        smtp.sendmail(SMTP_USER, to, msg.as_string())
    except smtplib.SMTPSenderRefused as error:
        sys.stderr.write("error send email: %s \n" %error)
        smtp.close()
    except socket.gaierror as error:
        sys.stderr.write("no connection server: %s \n" %error)
    except smtplib.SMTPAuthenticationError as error:
        sys.stderr.write("incorect login or pass: %s \n" %error)

        return False
        # sys.exit(1)
    smtp.close()

    return True

def main(commands, filename):
    file_report = new_report_file(filename)
    for command in commands:
        responce = get_command(command)
        report_command(command,  responce, file_report)
    file_report.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please email")
        sys.exit(1)

    send_to = sys.argv[1]
    commands = (
            "ps -aux",
            ("ps -eo pcpu,pid,user,args", "sort -r -k1 ", "head"),
            ("ps -eo user,pcpu,pmem,pid,cmd", "sort -r -n -k3",  "head"),
            "free -m",
            "df -h",
            "iostat -m",
            )

    commands_ss = ("ss -ltusxw", "ss state connected -tu")
    main(commands, FILE_REPORT)
    main(commands_ss, FILE_REPORT_SS)

    send_message_for_mail(send_to,
            "отчет о загруженности системы",
            get_command("ps -Ao pid,user,comm"),
            (os.getcwd()+"/"+sys.argv[0], FILE_REPORT,FILE_REPORT_SS))
