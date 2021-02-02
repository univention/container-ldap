*** Settings ***
Documentation    Some of these test cases are based on 05K5KEY_userexpiry
...              some are new
Resource         ${CURDIR}/../../resources/Ldap.robot
Suite Setup      Add Single Test User
Suite Teardown   Remove Single Test User

*** Test Cases ***
Expiry in the past
    Given an existing and previously working user
    When user expiry is set to a date in the past
    Then consequent LDAP searches with the user fail

Expiry in the future
    Given an existing and previously working user
    When user expiry is set to a date in the future
    Then consequent LDAP searches with the user succeed
