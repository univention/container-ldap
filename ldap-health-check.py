#!/usr/bin/env python3
"""
LDAP Health Check Sidecar
Provides HTTP endpoint for LDAP health checks via bind and search operations.
"""

import os
import logging
from flask import Flask, jsonify
from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
LDAP_HOST = os.getenv('LDAP_HOST', 'localhost')
LDAP_PORT = int(os.getenv('LDAP_PORT', '389'))
LDAP_BASE_DN = os.getenv('LDAP_BASE_DN', 'dc=openbaraza,dc=org')
LDAP_BIND_DN = os.getenv('LDAP_BIND_DN', 'cn=admin,dc=openbaraza,dc=org')
LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD', 'univention')
LDAP_USE_TLS = os.getenv('LDAP_USE_TLS', 'false').lower() == 'true'

def check_ldap_health():
    """Perform LDAP bind and search to verify health."""
    try:
        # Create server connection
        server = Server(LDAP_HOST, port=LDAP_PORT, get_info=ALL, use_ssl=LDAP_USE_TLS)
        
        # Attempt to bind
        conn = Connection(server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True)
        
        # Perform a simple search to verify functionality
        search_result = conn.search(
            search_base=LDAP_BASE_DN,
            search_filter='(objectClass=*)',
            search_scope=SUBTREE,
            size_limit=1
        )
        
        conn.unbind()
        
        if search_result:
            return True, "LDAP server is healthy"
        else:
            return False, "LDAP search failed"
            
    except LDAPException as e:
        logger.error(f"LDAP health check failed: {e}")
        return False, f"LDAP error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error during health check: {e}")
        return False, f"Unexpected error: {str(e)}"

@app.route('/health', methods=['GET'])
def health_check():
    """HTTP endpoint for health checks."""
    is_healthy, message = check_ldap_health()
    
    status_code = 200 if is_healthy else 503
    response = {
        'status': 'healthy' if is_healthy else 'unhealthy',
        'message': message,
        'ldap_host': LDAP_HOST,
        'ldap_port': LDAP_PORT
    }
    
    return jsonify(response), status_code

@app.route('/ready', methods=['GET'])
def readiness_check():
    """HTTP endpoint for readiness checks."""
    return health_check()

@app.route('/live', methods=['GET'])
def liveness_check():
    """HTTP endpoint for liveness checks."""
    return health_check()

if __name__ == '__main__':
    logger.info(f"Starting LDAP health check server on port 8080")
    logger.info(f"LDAP target: {LDAP_HOST}:{LDAP_PORT}")
    logger.info(f"Base DN: {LDAP_BASE_DN}")
    app.run(host='0.0.0.0', port=8080, debug=False)
