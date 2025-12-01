#!/usr/bin/env python3

import yaml
import re
import random
import getpass
import smtplib
import datetime
import pytz
import time
import socket
import sys
import getopt
import os
import subprocess

from cycles import get_all_full_cycles


HELP_MESSAGE = """
Use config.yml to specify participants and settings.

DONT_PAIR defines forbidden giver→receiver combinations.
SMTP settings are required for email delivery (skip login to use Signal only).

See README for details.
"""

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yml")

REQUIRED_CONFIG_KEYS = {
    "SMTP_SERVER",
    "SMTP_PORT",
    "TIMEZONE",
    "PARTICIPANTS",
    "DONT_PAIR",
    "FROM",
    "SUBJECT",
    "MESSAGE",
    "SENDER_SIGNAL_NUMBER",
}


HEADER = """Date: {date}
Content-Type: text/plain; charset="utf-8"
Message-Id: {message_id}
From: {frm}
To: {to}
Subject: {subject}

"""


# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------

class Person:
    def __init__(self, name, email, invalid_receivers=None):
        self.name = name
        self.email = email
        self.invalid_receivers = invalid_receivers or []

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Pair:
    def __init__(self, giver, receiver):
        self.giver = giver
        self.receiver = receiver

    def __str__(self):
        return f"{self.giver.name} ---> {self.receiver.name}"


# ---------------------------------------------------------
# Pair generation
# ---------------------------------------------------------

def create_pairs(givers, receivers):
    graph = {}

    for giver in givers:
        graph[giver] = {
            r for r in receivers if r.name not in giver.invalid_receivers
        }

    all_full_cycles = get_all_full_cycles(graph, list(graph.keys())[0])
    chosen_full_cycle = random.choice(all_full_cycles)

    return [
        Pair(giver, receiver)
        for giver, receiver in zip(chosen_full_cycle[:-1], chosen_full_cycle[1:])
    ]


# ---------------------------------------------------------
# Config + participant loading
# ---------------------------------------------------------

def load_config():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    missing = REQUIRED_CONFIG_KEYS - config.keys()
    if missing:
        raise ValueError(f"Missing required config keys: {missing}")

    return config


def load_participants(config):
    participants = []

    for raw in config["PARTICIPANTS"]:
        name, email = re.match(r"([^<]*)<([^>]*)>", raw).groups()
        name = name.strip()

        invalid = []
        for rule in config["DONT_PAIR"]:
            g, r = [p.strip() for p in rule.split("->")]
            if g == name:
                invalid.append(r)

        participants.append(Person(name, email, invalid))

    return participants


# ---------------------------------------------------------
# Notifier – centralizes email + Signal sending
# ---------------------------------------------------------

class Notifier:
    def __init__(self, config, enable_send):
        self.config = config
        self.enable_send = enable_send
        self.smtp = None

        if enable_send:
            self._maybe_setup_smtp()

    def _maybe_setup_smtp(self):
        username = input(f"Username for {self.config['SMTP_SERVER']} (blank = Signal only): ")

        if not username:
            return

        password = getpass.getpass()
        smtp = smtplib.SMTP(self.config["SMTP_SERVER"], self.config["SMTP_PORT"])
        smtp.starttls()
        smtp.login(username, password)
        self.smtp = smtp

    def send(self, giver, receiver):
        """Choose email or Signal based on giver's email format."""
        if not self.enable_send:
            return

        if giver.email.startswith("+"):
            self.send_signal(giver, receiver)
        else:
            self.send_email(giver, receiver)

    def send_email(self, giver, receiver):
        if self.smtp is None:
            print(f"Skipping email for {giver} (SMTP disabled).")
            return

        zone = pytz.timezone(self.config["TIMEZONE"])
        now = zone.localize(datetime.datetime.now())

        body = (HEADER + "\n" + self.config["MESSAGE"]).format(
            date=now.strftime("%a, %d %b %Y %T %Z"),
            message_id=f"<{time.time()}-{random.random()}@{socket.gethostname()}>",
            frm=self.config["FROM"],
            to=giver.email,
            subject=self.config["SUBJECT"].format(santa=giver.name, santee=receiver.name),
            santa=giver.name,
            santee=receiver.name,
        )

        self.smtp.sendmail(self.config["FROM"], [giver.email], body)
        print(f"Emailed {giver}")

    def send_signal(self, giver, receiver):
        msg = self.config["MESSAGE"].format(santa=giver.name, santee=receiver.name)

        try:
            subprocess.run(
                [
                    "signal-cli",
                    "-u",
                    self.config["SENDER_SIGNAL_NUMBER"],
                    "send",
                    "-m",
                    msg,
                    giver.email,
                ],
                check=True,
            )
            print(f"Signaled {giver}")
        except subprocess.CalledProcessError as e:
            print(f"Signal send failed for {giver}: {e}")

    def close(self):
        if self.smtp:
            self.smtp.quit()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main(argv=None):
    argv = argv or sys.argv

    opts, _ = getopt.getopt(argv[1:], "shc", ["send", "help"])
    send = any(opt in ("-s", "--send") for opt, _ in opts)

    if any(opt in ("-h", "--help") for opt, _ in opts):
        print(HELP_MESSAGE)
        return

    try:
        config = load_config()
        participants = load_participants(config)

        if len(participants) < 2:
            raise ValueError("At least two participants required.")

        pairs = create_pairs(participants, participants[:])

        if not send:
            print("Test pairings:\n")
            for p in pairs:
                print(p)
            print("\nRun with --send to notify participants.")
            return

        notifier = Notifier(config=config, enable_send=True)

        for p in pairs:
            notifier.send(p.giver, p.receiver)

        notifier.close()

    except Exception as e:
        print("ERROR:", e)
        print("Use --help for usage details.")
        raise


if __name__ == "__main__":
    main()
