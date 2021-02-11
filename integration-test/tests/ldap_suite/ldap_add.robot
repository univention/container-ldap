*** Settings ***
Documentation    The basic idea of these test cases comes from the ucs repository's
...              test/ucs-test/tests/10_ldap/91_ldap_constraints test suite.
Resource         ${CURDIR}/../../resources/Ldap.robot
Suite Setup      Remove Metasyntactic Test Users
Suite Teardown   Remove Metasyntactic Test Users
Test Template    Does the LDAP add operation have the expected result


*** Test Cases ***


Adding a new user with uidNumber=0
     # DN
     cn=foo,${BASE_DN}
     # OBJECTCLASS
...  ['posixAccount','organizationalRole']
     # ATTRIBUTES
...  {'cn': 'foo', 'uid': 'foo', 'homeDirectory': '/home/foo', 'uidNumber': '0', 'gidNumber': '1'}
     # EXPECTED RESULT
...  {'message': 'add breaks constraint on uidNumber'}


Adding a new user with gidNumber=0
     # DN
     cn=bar,${BASE_DN}
     # OBJECTCLASS
...  ['posixAccount','organizationalRole']
     # ATTRIBUTES
...  {'cn': 'bar', 'uid': 'bar', 'homeDirectory': '/home/bar','uidNumber': '1', 'gidNumber': '0'}
     # EXPECTED RESULT
...  {'message': 'add breaks constraint on gidNumber'}


Adding a new user with uidNumber!=0 and gidNumber!=0
     # DN
     cn=baz,${BASE_DN}
     # OBJECTCLASS
...  ['posixAccount','organizationalRole']
     # ATTRIBUTES
...  {'cn': 'baz', 'uid': 'baz', 'homeDirectory': '/home/baz', 'uidNumber': '1', 'gidNumber': '1'}
     # EXPECTED RESULT
...  {'result': 0, 'description': 'success'}


Adding a new user with existing cn uid homeDirectory uidNumber gidNumber
     # DN
     cn=qux,${BASE_DN}
     # OBJECTCLASS
...  ['posixAccount','organizationalRole']
     # ATTRIBUTES
...  {'cn': 'baz', 'uid': 'baz', 'homeDirectory': '/home/baz', 'uidNumber': '1', 'gidNumber': '1'}
     # EXPECTED RESULT
...  {'result': 0, 'description': 'success'}
