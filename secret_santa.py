#!/usr/bin/env python3

import yaml # sudo pip install pyyaml
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

help_message = '''
To use, fill out config.yml with your own participants. You can also specify 
DONT_PAIR so that people don't get assigned their significant other.

You'll also need to specify your mail server settings. An example is provided
for routing mail through gmail.

For more information, see README.
'''

REQRD = (
    'SMTP_SERVER',
    'SMTP_PORT',
    'TIMEZONE',
    'PARTICIPANTS',
    'DONT_PAIR',
    'FROM',
    'SUBJECT',
    'MESSAGE',
)

HEADER = """Date: {date}
Content-Type: text/plain; charset="utf-8"
Message-Id: {message_id}
From: {frm}
To: {to}
Subject: {subject}
        
"""

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')

class Person:
    def __init__(self, name, email, invalid_receivers=[]):
        self.name = name
        self.email = email
        self.invalid_receivers = invalid_receivers

    def __str__(self):
        return "%s <%s>" % (self.name, self.email)

class Pair:
    def __init__(self, giver, receiver):
        self.giver = giver
        self.receiver = receiver

    def __str__(self):
        return "%s ---> %s" % (self.giver.name, self.receiver.name)

def choose_receiver(giver, receivers):
    random.shuffle(receivers)
    for receiver in receivers:
        if receiver.name not in giver.invalid_receivers and giver != receiver:
            return receiver
    raise Exception("No receiver found for %s." % giver.name)

def create_pairs(givers, receivers):
    pairs = []
    for giver in givers:
        receiver = choose_receiver(giver, receivers)
        pairs.append(Pair(giver, receiver))
        receivers.remove(receiver)
    return pairs

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "shc", ["send", "help"])
        except getopt.error as msg:
            raise Exception(msg)

        # option processing
        send = False
        for option, value in opts:
            if option in ("-s", "--send"):
                send = True
            if option in ("-h", "--help"):
                print(help_message)

        config = yaml.load(open(CONFIG_PATH))
        for key in REQRD:
            if key not in config.keys():
                raise Exception('Required parameter %s not in yaml config file!' % key)

        participants = config['PARTICIPANTS']
        dont_pair = config['DONT_PAIR']
        if len(participants) < 2:
            raise Exception('Not enough participants specified.')
        givers = []
        for person in participants:
            name, email = re.match(r'([^<]*)<([^>]*)>', person).groups()
            name = name.strip()
            invalid_receivers = []
            for pair in dont_pair:
                names = [n.strip() for n in pair.split('->')]
                if names[0] == name:
                    invalid_receivers.append(names[1])
            person = Person(name, email, invalid_receivers)
            givers.append(person)
        pairs = create_pairs(givers, givers.copy())
        if not send:
            print( """Test pairings:\n\n%s\n\nTo send out emails with new pairings,
call with the --send argument:\n\n$ python secret_santa.py --send""" % ("\n".join([str(p) for p in pairs])))

        if send:
            server = smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT'])
            server.starttls()
            server.login(input('Username for {}: '.format(config['SMTP_SERVER'])), getpass.getpass())
        for pair in pairs:
            zone = pytz.timezone(config['TIMEZONE'])
            now = zone.localize(datetime.datetime.now())
            date = now.strftime('%a, %d %b %Y %T %Z') # Sun, 21 Dec 2008 06:25:23 +0000
            message_id = '<%s@%s>' % (str(time.time())+str(random.random()), socket.gethostname())
            frm = config['FROM']
            to = pair.giver.email
            subject = config['SUBJECT'].format(santa=pair.giver.name, santee=pair.receiver.name)
            body = (HEADER + '\n' + config['MESSAGE']).format(
                date=date,
                message_id=message_id,
                frm=frm,
                to=to,
                subject=subject,
                santa=pair.giver.name,
                santee=pair.receiver.name,
            )
            if send:
                result = server.sendmail(frm, [to], body)
                print( "Emailed %s <%s>" % (pair.giver.name, to))

        if send:
            server.quit()

    except Exception as e:
        print("ERROR: ", e)
        print( "For help, use --help")
        return 2


if __name__ == "__main__":
    main()
