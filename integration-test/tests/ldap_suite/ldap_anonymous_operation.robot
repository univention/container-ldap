*** Settings ***
Documentation    Ensures that the anonymous LDAP operations are not allowed
Resource         ${CURDIR}/../../resources/Ldap.robot


*** Test Cases ***
Anonymous attempt to LDAP Search to Base DN
    Given a default configured LDAP server
    When an anonymous LDAP search queries the  ${BASE_DN}
    Then the query result fails


Anonymous attempt to LDAP Add a new user
    Given a default configured LDAP server
    When an anonymous user LDAP adds  cn=attacker,cn=users,${BASE_DN}
    Then the query result fails


Anonymous attempt to LDAP modify admin password
    Given a default configured LDAP server
    When an anonymous user LDAP modifies  cn=admin,${BASE_DN}  {'userPassword': 'H@ckedPwd'}
    Then the query result fails
