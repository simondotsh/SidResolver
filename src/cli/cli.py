from argparse import ArgumentParser
from getpass import getpass
from os.path import isfile, expanduser
from sys import exit

class Cli:
    @classmethod
    def parse_and_validate(cls):
        parser = cls.__get_parser()
        args = parser.parse_args()

        args.sids = cls.__parse_sids(args.sids)

        if (args.password is None and args.nt_hash is None):
            args.password = getpass(f'Password for {args.username}: ')

        # impacket needs the unset values to be equal to ''
        args.password = args.password if args.password else ''
        args.nt_hash = args.nt_hash if args.nt_hash else ''

        return args

    @staticmethod
    def __get_parser():
        parser = ArgumentParser()

        parser.add_argument('-u', '--username', dest='username', required=True,
            help='Username used to authenticate on targets.'
        )

        parser.add_argument('-d', '--domain', dest='domain', required=True,
            help='Domain to authenticate to.'
        )

        pw_group = parser.add_mutually_exclusive_group()

        pw_group.add_argument('-p', '--password', dest='password',
            help='Username\'s password. If a password or a hash is not '
                 'provided, a prompt will request the password on execution.'
        )

        pw_group.add_argument('-nt', '--nt-hash', dest='nt_hash',
            help='Username\'s NT hash.'
        )

        parser.add_argument('-t', '--timeout', dest='timeout', default=2, 
            type=int,
            help='Drops connection after x seconds when waiting to receive '
                 'packets from the target (default: 2).'
        )

        parser.add_argument('-s', '--sid', dest='sids', required=True,
            help='A single SID or path to a file containing SIDs.'
        )

        parser.add_argument('target', 
            help='Target to request SID resolving from (IP or hostname).'
        )

        return parser

    @classmethod
    def __parse_sids(cls, sid):
        entries = []

        # In case of tilde in path
        sid = expanduser(sid)

        if isfile(sid):
            entries = [line.rstrip() for line in open(sid)]
        else:
            entries.append(sid)

        return cls.__validate_sids(entries)

    # This does not validate much other than to avoid sending complete 
    # gibberish in the case where a random file with no valid SIDs is given.
    @staticmethod
    def __validate_sids(entries):
        valid_sid = []
        invalid_sid = []

        for sid in entries:
            if sid[:2] == 'S-':
                valid_sid.append(sid)
            else:
                invalid_sid.append(sid)

        if invalid_sid:
            count = len(invalid_sid)
            if count <= 20:
                print('The following SIDs are invalid:')
                for sid in invalid_sid:
                    print(sid)
            else:
                print(f'{count} SIDs are invalid. Validate your input file.')

            exit(0)

        return valid_sid