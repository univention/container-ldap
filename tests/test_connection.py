import time

import ldap3


def test_connection(ldap_server, admin_dn, admin_password):
    """Try to connect to the LDAP server."""
    server = ldap3.Server(ldap_server, get_info=ldap3.ALL)

    print()
    # try for no more than 3 minutes to reach the LDAP server
    for _i in range(60):
        try:
            print("Trying to connect to LDAP server...", flush=True)
            ldap3.Connection(server, admin_dn, admin_password, auto_bind=True)
        # pylint: disable=W0718
        except Exception as err:
            print("Could not connect to LDAP server:", err, flush=True)
            time.sleep(3)
        else:
            print("Connection established!", flush=True)
            break
