from flask import Flask, request, jsonify
from keycloak import KeycloakOpenID

app = Flask(__name__)

keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080",
    client_id="flask-app",
    realm_name="myrealm",
    client_secret_key="<PASTE_CLIENT_SECRET>"
)

@app.route('/protected')
def protected():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({"error": "Missing token"}), 401
    token = auth.split(' ')[1]
    data = keycloak_openid.introspect(token)
    if data.get('active'):
        return jsonify({"message": "Access granted", "user": data.get('username')}), 200
    return jsonify({"error": "Invalid or expired token"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0')
