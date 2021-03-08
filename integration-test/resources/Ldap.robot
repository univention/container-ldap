*** Settings ***
Library          ${CURDIR}/../libraries/ldap/ldap.py
Library          Collections
Library          String


*** Variables ***
${BASE_DN}           dc=univention-organization,dc=intranet
${SECONDS_IN_A_DAY}  86400

*** Keywords ***

Is LDAP Bind operation with username and password allowed
    [Arguments]    ${user}  ${password}  ${allowed}
    ${result} =  Is ldap bind successful  ${user}  ${password}
    ${expected} =  Evaluate  robot.utils.is_truthy($allowed)  modules=robot
    Should Be Equal  ${expected}  ${result}
    ...              "Bind operation result is not the expected"


Does the LDAP add operation have the expected result
    [Arguments]    ${dn}  ${object_class}  ${attributes}  ${expected}
    ${object_class} =  Evaluate  ${object_class}
    ${attributes} =  Evaluate  ${attributes}
    ${expected} =  Evaluate  ${expected}
    ${result} =  ldap add  cn=admin,${BASE_DN}  univention
    ...                    ${dn}  ${object_class}  ${attributes}
    Log Variables
    Dictionary Should Contain Sub Dictionary  ${result}  ${expected}


Remove Metasyntactic Test Users
    ldap delete  cn=admin,${BASE_DN}  univention  cn=baz,${BASE_DN}
    ldap delete  cn=admin,${BASE_DN}  univention  cn=qux,${BASE_DN}


Add Single Test User
    ldap delete  cn=admin,${BASE_DN}  univention  cn=testuser1,cn=users,${BASE_DN}
    Does the LDAP add operation have the expected result
    ...  cn=testuser1,cn=users,${BASE_DN}
         # OBJECTCLASS
    ...  ['shadowAccount', 'posixAccount', 'organizationalRole']
         # ATTRIBUTES
    ...  {'cn': 'testuser1', 'uid': 'testuser1', 'homeDirectory': '/home/testuser1', 'uidNumber': '111', 'gidNumber': '111', 'userPassword': '{CRYPT}$6$PKcL4BHL$.A81HQy61dqt2b8V2PFMXlSexHP51jsLGujbRpg/HlcsSFcdk0FE1cxWcJuwbrMBEy9D98ouXvKOXKshRBuzL.', 'shadowExpire': '0'}
         # EXPECTED RESULT
    ...  {'result': 0, 'description': 'success'}


Remove Single Test User
    ldap delete  cn=admin,${BASE_DN}  univention  cn=testuser1,cn=users,${BASE_DN}


Given an existing and previously working user
    ${result} =  ldap search
    ...  cn=testuser1,cn=users,${BASE_DN}
    ...  univention
    ...  cn=testuser1,cn=users,${BASE_DN}
    ...  (objectClass=*)


When user expiry is set to a date in the past
    # https://linux.die.net/man/5/shadow
    # account expiration date
    # The date of expiration of the account, expressed as the number of days since Jan 1, 1970.
    # That date is also know as the "Unix Epoch" and is the beginning of the "Unix Epoch Time"
    # https://en.wikipedia.org/wiki/Unix_time
    ${current_epoch_time} =  Get Time  result_format=epoch
    ${days_since_epoch} =  Set Variable  ${current_epoch_time // ${SECONDS_IN_A_DAY}}
    ${day_before_yesterday} =  Set Variable  ${days_since_epoch - 2}
    ${ldap_change} =  Create Dictionary  shadowExpire  ${day_before_yesterday}
    ldap_modify
    ...  cn=admin,${BASE_DN}
    ...  univention
    ...  cn=testuser1,cn=users,${BASE_DN}
    ...  ${ldap_change}


When user expiry is set to a date in the future
    ${current_epoch_time} =  Get Time  result_format=epoch
    ${days_since_epoch} =  Set Variable  ${current_epoch_time // ${SECONDS_IN_A_DAY}}
    ${day_after_tomorrow} =  Set Variable  ${days_since_epoch + 2}
    ${ldap_change} =  Create Dictionary  shadowExpire  ${day_after_tomorrow}
    ldap_modify
    ...  cn=admin,${BASE_DN}
    ...  univention
    ...  cn=testuser1,cn=users,${BASE_DN}
    ...  ${ldap_change}


Then consequent LDAP searches with the user fail
    ${result} =  ldap search
    ...  cn=testuser1,cn=users,${BASE_DN}
    ...  univention
    ...  cn=testuser1,cn=users,${BASE_DN}
    ...  (objectClass=*)
    Should Be Equal  LDAPBindError  ${result}[0]
    ...              Search result is not the expected


Then consequent LDAP searches with the user succeed
    ${result} =  ldap search
    ...  cn=testuser1,cn=users,${BASE_DN}
    ...  univention
    ...  cn=testuser1,cn=users,${BASE_DN}
    ...  (objectClass=*)
    Log Variables
    Length Should Be  ${result}  1
    ${entry_dn} =  Entry To DN  ${result}[0]
    Should Match  cn=testuser1,cn=users,${BASE_DN}  ${entry_dn}


Given a default configured LDAP server
    No Operation


When an anonymous LDAP search queries the
    [Arguments]    ${DN}
    ${results} =  ldap search without bind  ${DN}
    Set Test Variable  ${OPERATION_RESULT}  ${results}


When an anonymous user LDAP adds
    [Arguments]    ${DN}
    ${split_dn} =  Split String  ${DN}  ,
    ${split_cn} =  Split String  ${split_dn}[0]  =
    ${user} =  Set Variable  ${split_cn}[1]
    ${object_class} =  Evaluate  ['posixAccount','organizationalRole']
    ${attributes} =  Evaluate
    ...  {'cn': '${user}', 'uid': '${user}', 'homeDirectory': '/home/${user}', 'uidNumber': '1', 'gidNumber': '1'}
    ${results} =  ldap add without bind  ${DN}  ${object_class}  ${attributes}
    Set Test Variable  ${OPERATION_RESULT}  ${results}


When an anonymous user LDAP modifies
    [Arguments]    ${DN}  ${change}
    ${ldap_change} =  Evaluate  ${change}
    ${results} =  ldap modify without bind  ${DN}  ${ldap_change}
    Set Test Variable  ${OPERATION_RESULT}  ${results}


Then the query result fails
     @{FAILURE_RESULTS} =  Create List  LDAPInsufficientAccessRightsResult
     ...  LDAPStrongerAuthRequiredResult  LDAPChangeError
     Should Contain  ${FAILURE_RESULTS}  ${OPERATION_RESULT}[0]
