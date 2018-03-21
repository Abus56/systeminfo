#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import system_state
import commands

def send_system_state(email, subject="report system state"):
    system_state.main(commands.system_state_commands, system_state.FILE_REPORT)
    system_state.main(commands.ss_state_commands, system_state.FILE_REPORT_SS)

    system_state.send_message_for_mail(
            email,
            subject,
            system_state.get_command("ps -Ao pid,user,comm"),
            (os.getcwd()+"/system_state.py", system_state.FILE_REPORT,
                system_state.FILE_REPORT_SS))
