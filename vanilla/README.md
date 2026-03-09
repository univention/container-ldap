# Vanilla slapd

Runs a plain OpenLDAP (slapd) process using the Univention `ldap-server` container image, bypassing all Univention-specific entrypoint logic, schemas, and overlays.

## Quick start

```bash
mkdir -m 777 data
docker compose up -d
```

- LDAP: `localhost:389`
- phpLDAPadmin: `http://localhost:8080`
- Bind DN: `cn=admin,dc=example,dc=org`
- Password: `admin`

## Files

| File | Purpose |
|---|---|
| `docker-compose.yaml` | Runs the ldap-server image with a custom entrypoint |
| `slapd.conf` | Minimal static config — standard schemas, MDB backend, simple ACL |
| `seed.ldif` | Initial directory content (base DN, `ou=people`, `ou=groups`) |
| `entrypoint.sh` | Hashes the admin password, seeds on first run, starts slapd |

## Configuration

### Admin password

Set via environment variable (default: `admin`):

```yaml
environment:
  LDAP_ADMIN_PW: mysecretpassword
```

Or mount a Docker secret at `/run/secrets/ldap_admin_pw`.

For production, you can skip the entrypoint password logic entirely by mounting a pre-hashed `rootpw.conf` directly:

```
# rootpw.conf
rootpw {SSHA}prehashed...
```

### Base DN

Edit `slapd.conf` and `seed.ldif` — both use `dc=example,dc=org` by default.

### Custom schemas

Add `.schema` files and reference them with `include` lines in `slapd.conf`.

### Log level

```yaml
environment:
  LDAP_LOG_LEVEL: stats  # default
```

## What's bypassed

The Univention image normally runs an entrypoint that:

- Templates `slapd.conf` from ~15 fragment files via UCR variable substitution
- Loads Univention-specific schemas (univentionObject, SAML, self-service, etc.)
- Enables overlays: translog, memberOf, unique, constraint, ppolicy, refint, etc.
- Fetches SAML/OIDC metadata from external services
- Configures SASL authentication
- Initializes a Univention-specific directory structure via `base.ldif`

This setup skips all of that and runs a stock slapd with only standard LDAP schemas.

## Persistent data

The MDB database is stored in `./data/` (bind mount). Seeding only happens on the first run (when `data/data.mdb` doesn't exist).

To start fresh:

```bash
docker compose down
rm -rf data/
mkdir -m 777 data
docker compose up -d
```
