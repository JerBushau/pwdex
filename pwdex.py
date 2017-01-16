
from collections import OrderedDict
from getpass import getpass, getuser
import datetime
import os
import random
import string
import sys
import time

from peewee import *
import clipboard

db = SqliteDatabase('/home/user/pwdex/log.db')

class Entry(Model):
    """Database model."""
    timestamp = DateTimeField(default=datetime.datetime.now)
    account_name = CharField()
    username = CharField()
    password = CharField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def set_account_name():
    """Set account name."""
    while True:
        name = input('\nEnter product or application name: ')

        if name != '':
            return name
            break
        else:
            print('Enter an account name! ')
            continue


def set_username():
    """Set username."""
    while True:
        username = input('\nEnter the username: ')

        if username != '':
            return username
        else:
            print('Enter an username! ')
            continue


def set_pw():
    """Set password."""
    while True:
        option = input('\nGenerate 10 character pw or enter existing'
        ' pw? ')

        if option in ('e', 'existing'):
            while True:
                pw = input('\nEnter password: ').strip()

                if len(pw) >= 8:
                    password = pw
                    return password
                    break
                else:
                    print('Passwords must be at least 8 characters! ')
                    continue

        elif option in ('g', 'gen', 'generate'):
            return gen_pw()
        else:
            print('e | g')
            continue


def gen_pw():
    """Create pw from all possible characters."""
    # use string module to create a list of all possible chars
    possible_chars = (string.ascii_uppercase +
                      string.ascii_lowercase +
                      string.digits)
    return ''.join(random.choice(possible_chars) for _ in range(10))


def view_entries(search_query=None):
    """View all entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.account_name.contains(search_query))

    for entry in entries:
        clear()
        print('\n' + entry.account_name)
        print('^'*len(entry.account_name))
        print('Username: {}'.format(entry.username))
        print('Password: {}'.format(entry.password + '\n'))
        print('>>Options<<\n')
        next_ = input('m) main menu\n'
                      'c) copy password to clipboard\n'
                      'd) delete entry\n'
                      'n) next [press enter]\n\n>').lower().strip()

        if next_ == 'd':
            delete_entry(entry)
            input('press enter to continue. ')
        elif next_ == 'c':
            copy_pw(entry)
            input('press enter to continue. ')
        elif next_ == 'm':
            clear()
            break
    clear()
    print('Welcome back to the main menu.\n')


def copy_pw(entry):
    """Copy entry password to clipboard."""
    clipboard.copy(entry.password)
    print('\nPassword for {} copied. \n'.format(entry.account_name))


def search_query():
    """Search for account name."""
    view_entries(input('\nEnter your search query: ').lower().strip())


def delete_entry(entry):
    """Delete an entry."""
    if input('Sure? y/n ').lower() == 'y':
        entry.delete_instance()
        clear()
        print('\nEntry deleted.\n')


def quit_pwdex():
    """Quit pwdex."""
    clear()
    print('See You Space Cowboy.\n')
    time.sleep(2)
    os.system('echo -n | xclip -selection clipboard')
    os.system('reset')


def create_new_entry():
    """Create a new entry."""
    Entry.create(account_name=set_account_name(),
                 username=set_username(),
                 password=set_pw())
    clear()
    print('Entry saved.\n')


def validate():
    while True:
        pw = 'reallygoodpw'
        user_input = getpass('Enter password: ')
        if  user_input == pw:
            clear()
            welcome_msg = 'Welcome to Pwdex, ' + getuser() + '!'
            print('\n' + '<'*len(welcome_msg))
            print(welcome_msg)
            print('>'*len(welcome_msg) + '\n')
            break
        else:
            print('Are you sure that\'s your password?\n\nHint:'
            ' That\'s not your password.\n')
            continue


def main_menu():
    choice = None
    while choice != 'q':
        print('>>Options<<\n')
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\n> ').lower().strip()
        if choice in menu:
            clear()
            menu[choice]()
        else:
            clear()
            print('Enter a valid option.\n')


def clear():
    os.system('clear')


def main():
    validate()
    initialize()
    main_menu()


menu = OrderedDict([
    ('c', create_new_entry),
    ('v', view_entries),
    ('s', search_query),
    ('q', quit_pwdex)
])


if __name__ == '__main__':
    main()
