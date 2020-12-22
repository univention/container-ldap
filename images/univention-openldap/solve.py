#!/usr/bin/env python3

# Replacement for "univention-config-registry" get and filter

import argparse
import collections
import sys
import re
from os import listdir

parser = argparse.ArgumentParser()

parser.add_argument('--ldapbase', type=str, required=True)

parser.add_argument('--domainname', type=str, required=True)

args = parser.parse_args()


class Registry(collections.UserDict):
    def is_true(self, key, default=None):
        return bool(self.data.get(key) or default)

    def is_false(self, key, default=None):
        return not self.is_true(key, default)


configRegistry = Registry(
    {
        'domainname':
            args.domainname,  #'fg-organization.intranet'
        'hostname':
            'ucs-6045',
        'ldap/acl/nestedgroups':
            'yes',
        'ldap/acl/read/anonymous':
            'no',
        'ldap/acl/slavepdc':
            'yes',
        'ldap/acl/user/password/change':
            'no',
        'ldap/attributeoptions':
            'entry-,lang-',
        'ldap/autostart':
            'yes',
        'ldap/base':
            args.ldapbase,  #'dc=fg-organization,dc=intranet'
        'ldap/binaryattributes':
            '',
        'ldap/cachesize':
            '20000',
        'ldap/client/retry/count':
            '10',
        'ldap/database/bdb/db_config_options':
            'set_flags',
        'ldap/database/bdb/checkpoint':
            '',
        'ldap/database/bdb/set_flags':
            'DB_LOG_AUTOREMOVE',
        'ldap/database/mdb/envflags':
            '',
        'ldap/database/mdb/maxsize':
            '2147483648',
        'ldap/database/type':
            'mdb',
        'ldap/debug/level':
            'none',
        'ldap/hostdn':
            'cn=ucs-6045,cn=dc,cn=computers,' + args.ldapbase,
        'ldap/idlcachesize':
            '20000',
        'ldap/idletimeout':
            '360',
        'ldap/index/approx':
            'cn,givenName,mail,sn,uid',
        'ldap/index/autorebuild':
            'yes',
        'ldap/index/eq':
            ','.join(
                'aRecord',
                'automountInformation',
                'cNAMERecord',
                'cn',
                'description',
                'dhcpHWAddress',
                'displayName',
                'entryUUID',
                'gidNumber',
                'givenName',
                'homeDirectory',
                'krb5PrincipalName',
                'macAddress',
                'mail',
                'mailAlternativeAddress',
                'mailPrimaryAddress',
                'memberUid',
                'objectClass',
                'ou',
                'pTRRecord',
                'relativeDomainName',
                'sambaAcctFlags',
                'sambaDomainName',
                'sambaGroupType',
                'sambaPrimaryGroupSID',
                'sambaSID',
                'sambaSIDList',
                'secretary',
                'shadowExpire',
                'sn',
                'uid',
                'uidNumber',
                'uniqueMember',
                'univentionAppID',
                'univentionCanonicalRecipientRewriteEnabled',
                'univentionDataType',
                'univentionInventoryNumber',
                'univentionLicenseModule',
                'univentionLicenseObject',
                'univentionMailHomeServer',
                'univentionNagiosHostname',
                'univentionObjectFlag',
                'univentionObjectType',
                'univentionPolicyReference',
                'univentionServerRole',
                'univentionService',
                'univentionShareGid',
                'univentionShareSambaName',
                'univentionShareWriteable',
                'univentionUDMOptionModule',
                'univentionUDMPropertyCLIName',
                'univentionUDMPropertyDefault',
                'univentionUDMPropertyDeleteObjectClass',
                'univentionUDMPropertyDoNotSearch',
                'univentionUDMPropertyHook',
                'univentionUDMPropertyLayoutOverwritePosition',
                'univentionUDMPropertyLayoutOverwriteTab',
                'univentionUDMPropertyLayoutPosition',
                'univentionUDMPropertyLayoutTabAdvanced',
                'univentionUDMPropertyLayoutTabName',
                'univentionUDMPropertyLdapMapping',
                'univentionUDMPropertyLongDescription',
                'univentionUDMPropertyModule',
                'univentionUDMPropertyMultivalue',
                'univentionUDMPropertyObjectClass',
                'univentionUDMPropertyOptions',
                'univentionUDMPropertyShortDescription',
                'univentionUDMPropertySyntax',
                'univentionUDMPropertyTranslationLongDescription',
                'univentionUDMPropertyTranslationShortDescription',
                'univentionUDMPropertyTranslationTabName',
                'univentionUDMPropertyValueMayChange',
                'univentionUDMPropertyValueRequired',
                'univentionUDMPropertyVersion',
                'zoneName',
            ),
        'ldap/index/pres':
            ','.join(
                'aRecord',
                'automountInformation',
                'cn',
                'description',
                'dhcpHWAddress',
                'displayName',
                'gidNumber',
                'givenName',
                'homeDirectory',
                'krb5PrincipalName',
                'macAddress',
                'mail',
                'mailAlternativeAddress',
                'mailPrimaryAddress',
                'memberUid',
                'name',
                'objectClass',
                'ou',
                'relativeDomainName',
                'shadowMax',
                'sn',
                'uid',
                'uidNumber',
                'uniqueMember',
                'univentionMailHomeServer',
                'univentionObjectFlag',
                'univentionPolicyReference',
                'univentionUDMPropertyCLIName',
                'univentionUDMPropertyDefault',
                'univentionUDMPropertyDeleteObjectClass',
                'univentionUDMPropertyDoNotSearch',
                'univentionUDMPropertyHook',
                'univentionUDMPropertyLayoutOverwritePosition',
                'univentionUDMPropertyLayoutOverwriteTab',
                'univentionUDMPropertyLayoutPosition',
                'univentionUDMPropertyLayoutTabAdvanced',
                'univentionUDMPropertyLayoutTabName',
                'univentionUDMPropertyLdapMapping',
                'univentionUDMPropertyLongDescription',
                'univentionUDMPropertyModule',
                'univentionUDMPropertyMultivalue',
                'univentionUDMPropertyObjectClass',
                'univentionUDMPropertyOptions',
                'univentionUDMPropertyShortDescription',
                'univentionUDMPropertySyntax',
                'univentionUDMPropertyTranslationLongDescription',
                'univentionUDMPropertyTranslationShortDescription',
                'univentionUDMPropertyTranslationTabName',
                'univentionUDMPropertyValueMayChange',
                'univentionUDMPropertyValueRequired',
                'univentionUDMPropertyVersion',
                'zoneName',
            ),
        'ldap/index/quickmode':
            'false',
        'ldap/index/sub':
            ','.join(
                'aRecord',
                'associatedDomain',
                'automountInformation',
                'cn',
                'default',
                'description',
                'displayName',
                'employeeNumber',
                'givenName',
                'macAddress',
                'mail',
                'mailAlternativeAddress',
                'mailPrimaryAddress',
                'name',
                'ou',
                'pTRRecord',
                'printerModel',
                'relativeDomainName',
                'sambaSID',
                'sn',
                'uid',
                'univentionInventoryNumber',
                'univentionOperatingSystem',
                'univentionSyntaxDescription',
                'univentionUDMPropertyLongDescription',
                'univentionUDMPropertyShortDescription',
                'zoneName',
            ),
        # This is normally not in UCR,
        # only something that evaluate to true in 31modules
        'ldap/k5pwd':
            True,
        'ldap/limits':
            'users time.soft=-1 time.hard=-1',
        'ldap/monitor':
            False,  # Would be nice to see a working monitor backend
        'ldap/monitor/acl/read/groups/':
            '',  # What is even a sensible default here?
        'ldap/pwd_scheme_kinit':
            True,
        'ldap/master/port':
            '7389',
        'ldap/master':
            'ucs-6045.' + args.domainname,
        'ldap/maxopenfiles':
            '8192',
        'ldap/overlay/lastbind':
            False,  # TODO Add lastbind.la to image
        'ldap/overlay/lastbind/precision':
            '3600',
        'ldap/overlay/memberof':
            'true',
        'ldap/overlay/memberof/objectclass':
            'posixGroup',
        'ldap/overlay/memberof/member':
            'uniqueMember',
        'ldap/overlay/memberof/memberof':
            'memberOf',
        'ldap/overlay/memberof/dangling':
            'ignore',
        'ldap/overlay/memberof/dangling/errorcode':
            '',
        'ldap/overlay/memberof/modifiersname':
            '',
        'ldap/overlay/memberof/refint':
            '',
        'ldap/policy/cron':
            '5 * * * *',
        'ldap/ppolicy':
            False,  # TODO See if this has dependencies
        'ldap/ppolicy/enabled':
            False,
        'ldap/ppolicy/default':
            '',
        'ldap/server/ip':
            '127.0.0.1',
        'ldap/server/name':
            'ucs-6045.' + args.domainname,
        'ldap/server/port':
            '389',
        'ldap/server/type':
            'master',
        'ldap/sizelimit':
            '400000',
        'ldap/shadowbind':
            'true',
        'ldap/shadowbind/ignorefilter':
            '(|(objectClass=univentionDomainController)(userPassword={KINIT}))',
        'ldap/threads':
            '16',
        'ldap/tls/ciphersuite':
            'HIGH:MEDIUM:!aNULL:!MD5:!RC4',
        'ldap/tls/minprotocol':
            '3.1',
        'ldap/tls/dh/paramfile':
            '/etc/ldap/dh_2048.pem',
        'ldap/tool-threads':
            '1',
        'ldap/translogfile':
            '/var/lib/univention-ldap/listener/listener',
        'slapd/port':
            '389',
    }
)

# TODO: Eventually admit that it's not
#       univention-config-registry anymore
WARNING_TEXT = '''\
# Warning: This file is auto-generated and might be overwritten by
#          univention-config-registry.
#          Please edit the following file(s) instead:
# Warnung: Diese Datei wurde automatisch generiert und kann durch
#          univention-config-registry ueberschrieben werden.
#          Bitte bearbeiten Sie an Stelle dessen die folgende(n) Datei(en):
#
'''  # noqa: E101


# TODO: Check if full porting of warning_string() is needed
def warning_string():
    print(WARNING_TEXT, end='')
    path = "/etc/univention/templates/files/etc/ldap/slapd.conf.d/"
    for f in sorted(listdir(path)):
        print('# \t' + path + f)


def resolve_variable(line):
    # VARIABLE_PATTERN = re.compile('@%@([^@]+)@%@')
    if '@%@ldap/debug/level@%@' in line:
        line = re.sub(
            '@%@ldap/debug/level@%@', configRegistry['ldap/debug/level'], line
        )
    if '@%@hostname@%@' in line:
        line = re.sub('@%@hostname@%@', configRegistry['hostname'], line)
    if '@%@domainname@%@' in line:
        line = re.sub('@%@domainname@%@', configRegistry['domainname'], line)
    if '@%@ldap/base@%@' in line:
        line = re.sub('@%@ldap/base@%@', configRegistry['ldap/base'], line)
    return line


# TODO: Complete this
def custom_groupname(x):
    return x


# TODO: Complete this
def custom_username(x):
    return x


inside_section, to_be_compiled = False, []

for line in sys.stdin:
    # The original implementation is in:
    # base/univention-config-registry/python/
    # univention/config_registry/handler.py
    if line == '@%@UCRWARNING=# @%@\n':
        warning_string()
        continue

    if '@%@' in line:
        line = resolve_variable(line)

    if line == '@!@\n':
        if not inside_section:
            inside_section = True

        else:
            inside_section = False
            exec(''.join(to_be_compiled))  # pylint: disable=exec-used
            print('')
            to_be_compiled = []

    else:
        if inside_section:
            # Workaround for some import that doesn't do much anyway
            # TODO: Complete this, if needed
            if line in (
                'from univention.lib.misc import custom_groupname\n',
                (
                    'from univention.lib.misc import '
                    'custom_username, custom_groupname\n'
                ),
            ):
                # line = 'custom_groupname = lambda x: x\n'
                continue
            to_be_compiled += line

        else:
            print(line, end='')
