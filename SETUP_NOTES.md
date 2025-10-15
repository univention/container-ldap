# LDAP Server Setup Notes

## Problem
The original docker-compose.yaml uses private Univention registry images that are not publicly accessible, causing build failures.

## Solution
Created a docker-compose override file to use public OpenLDAP images from DockerHub.

## Files Created/Modified

### 1. Environment Configuration
```bash
cp .env.ldap-server.example .env.ldap-server
```

### 2. Docker Compose Override
Created `docker-compose.override.yml`:
- Uses `osixia/openldap:1.5.0` instead of private registry image
- Uses `osixia/phpldapadmin:0.9.0` for web interface
- Configured for `dc=openbaraza,dc=org` domain
- Admin password: `univention`

### 3. User Data Import
Created `users-groups.ldif` with:
- 3 users: jdoe, asmith, afares
- 3 groups: admins, developers, guests
- Removed `homeDirectory` attribute (requires `posixAccount` object class)

## Commands Used

### Start Services
```bash
docker compose up ldap-server ldap-admin
```

### Import User Data
```bash
ldapadd -H ldap://localhost:389 -x -D cn=admin,dc=openbaraza,dc=org -w univention -f users-groups.ldif
```

### Add Missing Group
```bash
echo "dn: cn=guests,ou=Groups,dc=openbaraza,dc=org
objectClass: top
objectClass: groupOfNames
cn: guests
description: Temporary users group
member: uid=asmith,ou=People,dc=openbaraza,dc=org" | ldapadd -H ldap://localhost:389 -x -D cn=admin,dc=openbaraza,dc=org -w univention
```

### Verify Data
```bash
# All entries
ldapsearch -H ldap://localhost:389 -x -D cn=admin,dc=openbaraza,dc=org -w univention -b dc=openbaraza,dc=org

# Users only
ldapsearch -H ldap://localhost:389 -x -D cn=admin,dc=openbaraza,dc=org -w univention -b ou=People,dc=openbaraza,dc=org

# Groups only
ldapsearch -H ldap://localhost:389 -x -D cn=admin,dc=openbaraza,dc=org -w univention -b ou=Groups,dc=openbaraza,dc=org
```

## Access Points

- **LDAP Server**: `ldap://localhost:389`
- **Web Admin**: `http://localhost:8001`
- **Admin DN**: `cn=admin,dc=openbaraza,dc=org`
- **Password**: `univention`

## Final Data Structure

### Users
- `uid=jdoe,ou=People,dc=openbaraza,dc=org` (John Doe)
- `uid=asmith,ou=People,dc=openbaraza,dc=org` (Alice Smith)
- `uid=afares,ou=People,dc=openbaraza,dc=org` (Jonson Fares)

### Groups
- `cn=admins,ou=Groups,dc=openbaraza,dc=org` (jdoe, afares)
- `cn=developers,ou=Groups,dc=openbaraza,dc=org` (jdoe, asmith)
- `cn=guests,ou=Groups,dc=openbaraza,dc=org` (asmith)

## Notes
- `homeDirectory` attribute was removed due to object class constraints
- To include `homeDirectory`, add `posixAccount` object class with required `uidNumber` and `gidNumber`

Example:

```ldif
dn: uid=jdoe,ou=People,dc=openbaraza,dc=org
objectClass: inetOrgPerson
objectClass: posixAccount
uid: jdoe
sn: Doe
givenName: John
cn: John Doe
displayName: John Doe
mail: jdoe@openbaraza.com
userPassword: password123
homeDirectory: /home/jdoe
uidNumber: 1001
gidNumber: 1001
```

- All user passwords are set to `password123`
