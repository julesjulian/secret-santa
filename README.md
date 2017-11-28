Secret Santa
============

[![Build Status](https://travis-ci.org/julesjulian/secret-santa.svg?branch=master)](https://travis-ci.org/julesjulian/secret-santa)[![Coverage Status](https://coveralls.io/repos/github/julesjulian/secret-santa/badge.svg?branch=master)](https://coveralls.io/github/julesjulian/secret-santa?branch=master)

Intro
=====

**secret-santa** can help you manage a list of secret santa participants by
randomly assigning pairings and sending emails. It can avoid pairing 
couples to their significant other, and allows custom email messages to be 
specified.

Dependencies
------------

pytz
pyyaml

Usage
-----

Copy config.yml.template to config.yml and enter in the connection details 
for your outgoing mail server. Modify the participants and couples lists and 
the email message if you wish.

    cd secret-santa/
    cp config.yml.template config.yml

Once configured, call secret-santa:

    ./secret_santa.py

Calling secret-santa without arguments will output a test pairing of 
participants.

To send the emails, call using the `--send` argument

    ./secret_santa.py --send
