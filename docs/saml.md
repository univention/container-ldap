# SAML


## Disabling SAML support

SAML support is enabled based on the following UCR settings:

```
umc/saml/idp-server
umc/saml/idp-server-internal
```

These settings are used in `50-entrypoint.sh` to decide if SAML has to be
configured in the functions `fetch_saml_metadata` and `setup_sasl_mech_saml`.
