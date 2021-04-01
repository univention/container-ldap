*** Settings ***
Documentation    Tests for verifying SASL functionality
Resource         ${CURDIR}/../../resources/Ldap.robot

*** Test Cases ***
Supported SASL mechanisms
    Given a default configured OpenLDAP container
    When the supportedsaslmechanisms are queried from the DSA
    Then the results include  GSSAPI  SAML
    And the results don't include any  DIGEST-MD5  CRAM-MD5  PLAIN  GSS-SPNEGO  NTLM  LOGIN
