#!/usr/bin/env python3

# fake "univention-config-registry filter" for only resolving ldap/base

import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('--ldapbase',
                    type=str,
                    required=True)

parser.add_argument('--domainname',
                    type=str,
                    required=True)

args = parser.parse_args()


configRegistry = {
        'ldap/base': args.ldapbase,   #'dc=fg-organization,dc=intranet'
        'domainname': args.domainname #'fg-organization.intranet'
        }

inside_section, to_be_compiled = False, []

for line in sys.stdin:

    if line == '@!@\n':
        if not inside_section:
            inside_section = True

        else:
            inside_section = False
            exec(''.join(to_be_compiled))
            #print(to_be_compiled)
            to_be_compiled = []

        print('')

    else:
        if inside_section:
            to_be_compiled += line

        else:
            print(line, end='')
