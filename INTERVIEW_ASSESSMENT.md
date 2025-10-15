# LDAP Health Check Sidecar - Interview Assessment

## Problem Statement
Extend the existing OpenLDAP Helm chart by adding an optional sidecar container that:
- Exposes HTTP endpoint on port 8080
- Performs real LDAP bind and search for health checks
- Configurable through values.yaml
- Uses Kubernetes Secrets for bind password

## Solution Overview
Created a Python Flask sidecar that performs actual LDAP operations instead of simple TCP checks, with dynamic probe switching based on sidecar availability.

## Files Added

### 1. `ldap-health-check.py` - Health Check Service
**Why**: Core sidecar application that performs real LDAP health checks
```python
# Key functionality:
- Flask HTTP server on port 8080
- LDAP bind + search operations using ldap3
- Environment-based configuration
- JSON responses with detailed status
```

### 2. `Dockerfile.health-check` - Container Image
**Why**: Containerize the health check service with security best practices
```dockerfile
# Key features:
- Python 3.11 slim base
- Non-root user (1001)
- Minimal dependencies
```

### 3. `requirements-health-check.txt` - Dependencies
**Why**: Minimal Python dependencies for the sidecar
```
ldap3==2.9.1
flask==3.1.2
```

## Files Modified

### 4. `helm/ldap-server/values.yaml` - Configuration
**Why**: Add sidecar configuration section while maintaining backward compatibility
```yaml
# Added healthCheckSidecar section with:
- enabled: false (default - no breaking changes)
- image configuration
- LDAP connection settings
- resource limits
- security context
```

### 5. `helm/ldap-server/templates/statefulset-primary.yaml` - Pod Definition
**Why**: Add conditional sidecar container to the StatefulSet
```yaml
# Added:
- Conditional sidecar container block
- Environment variables from values
- Health probe endpoints
- Resource limits
```

### 6. `helm/ldap-server/templates/_helpers.tpl` - Dynamic Probes
**Why**: Switch between HTTP (sidecar) and TCP/exec (default) probes automatically
```yaml
# Added helper templates:
- ldap-server.livenessProbe
- ldap-server.readinessProbe
- ldap-server.startupProbe
```

### 7. `helm/ldap-server/templates/secret-health-check.yaml` - Credentials
**Why**: Manage LDAP bind password securely via Kubernetes Secret
```yaml
# Creates secret when sidecar enabled
# Contains base64 encoded LDAP password
```

### 8. `helm/test-values.yaml` - Minimal Test Configuration
**Why**: Provides minimal required values for Helm template testing
```yaml
# Contains required SAML and LDAP configuration
# Enables template rendering without errors
```

## Quick Verification Commands

### 1. Test Health Check Service Locally
```bash
# Setup environment
python3 -m venv /tmp/health-env
source /tmp/health-env/bin/activate
pip install ldap3 flask

# Start local LDAP (if not running)
docker compose up ldap-server ldap-admin -d

# Test LDAP connectivity
python3 -c "
from ldap3 import Server, Connection, ALL, SUBTREE
server = Server('localhost', port=389, get_info=ALL)
conn = Connection(server, user='cn=admin,dc=openbaraza,dc=org', password='univention', auto_bind=True)
result = conn.search('dc=openbaraza,dc=org', '(objectClass=*)', SUBTREE, size_limit=1)
print(f'LDAP Health: {\"OK\" if result else \"FAIL\"}')
conn.unbind()
"

# Start health check service
python3 ldap-health-check.py &

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/ready
curl http://localhost:8080/live
```

### 2. Verify Helm Template Changes
```bash
# Check default behavior (sidecar disabled) - shows TCP probes
helm template test ./helm/ldap-server -f helm/test-values.yaml | grep -A 5 -B 5 "tcpSocket"

# Check with sidecar enabled - shows HTTP probes
helm template test ./helm/ldap-server -f helm/values-with-health-check.yaml | grep -A 5 -B 5 "httpGet"

# Verify sidecar container is added
helm template test ./helm/ldap-server -f helm/values-with-health-check.yaml | grep -A 10 -B 5 "health-check"
```

### 3. Validate Configuration Schema
```bash
# Lint the Helm chart
helm lint ./helm/ldap-server

# Template rendering test (works without K8s cluster)
helm template test ./helm/ldap-server -f helm/values-with-health-check.yaml > /dev/null && echo "Template renders successfully"

# Show complete sidecar configuration
helm template test ./helm/ldap-server -f helm/values-with-health-check.yaml | grep -A 20 "name.*health-check"
```

## Key Design Decisions

### 1. **Backward Compatibility**
- `healthCheckSidecar.enabled: false` by default
- Original probes preserved when sidecar disabled
- No breaking changes to existing deployments

### 2. **Dynamic Probe Switching**
- Helper templates in `_helpers.tpl` choose probe type
- HTTP probes when sidecar enabled
- Original TCP/exec probes when disabled

### 3. **Security First**
- Non-root sidecar execution
- Kubernetes Secrets for credentials
- Minimal container capabilities
- Resource limits

### 4. **Real Health Checks**
- Actual LDAP bind + search operations
- More accurate than TCP socket checks
- Detailed JSON error responses

## Expected Results

### With Sidecar Disabled (Default)
```yaml
livenessProbe:
  tcpSocket:
    port: 389
```

### With Sidecar Enabled
```yaml
livenessProbe:
  httpGet:
    path: /live
    port: 8080
```

### Health Endpoint Response
```json
{
  "status": "healthy",
  "message": "LDAP server is healthy",
  "ldap_host": "localhost",
  "ldap_port": 389
}
```
