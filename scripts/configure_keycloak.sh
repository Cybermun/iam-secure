#!/bin/bash
set -e

# Wait for Keycloak to start
sleep 20

/opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin

# Create demo realm
/opt/keycloak/bin/kcadm.sh create realms -s realm=demo -s enabled=true

# Create client
/opt/keycloak/bin/kcadm.sh create clients -r demo -s clientId=flask-client -s publicClient=false -s 'redirectUris=["http://localhost:5000/*"]' -s protocol=openid-connect -s enabled=true -s secret=secret

# Create user
/opt/keycloak/bin/kcadm.sh create users -r demo -s username=testuser -s enabled=true
/opt/keycloak/bin/kcadm.sh set-password -r demo --username testuser --new-password testpassword
