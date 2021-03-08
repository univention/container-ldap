*** Settings ***
Documentation    The basic idea of these test cases comes from the ucs repository's
...              test/ucs-test/tests/10_ldap/11anonymous test suite.
Resource         ${CURDIR}/../../resources/Ldap.robot
Test Template    Is LDAP Bind Operation With Username And Password Allowed

*** Test Cases ***                      USERNAME                 PASSWORD            ALLOWED
Anonymous User                          ${EMPTY}                 ${EMPTY}            No
Anonymous User with random password     ${EMPTY}                 xXpwd123            No
Random User with random password        qU27xpvi                 4xb_a-rt            No
Random User without password            D7v87bnr                 ${EMPTY}            No
cn=admin with valid password            cn=admin,${BASE_DN}      univention          Yes
cn=backup with admin password           cn=backup,${BASE_DN}     univention          No
cn=admin without valid password         cn=admin,${BASE_DN}      ${EMPTY}            No
cn=admin without base DN                cn=admin                 univention          No
cn=backup without password              cn=backup,${BASE_DN}     ${EMPTY}            No
cn=backup without base DN               cn=backup                univention          No
