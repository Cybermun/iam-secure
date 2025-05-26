from flask import Flask, request, jsonify
import jwt
import requests

app = Flask(__name__)

def get_public_key():
    # Dynamically fetch Keycloak's public key
    oidc_cfg = requests.get("http://keycloak:8080/realms/demo/.well-known/openid-configuration").json()
    jwks_uri = oidc_cfg["jwks_uri"]
    jwks = requests.get(jwks_uri).json()
    cert = jwks["keys"][0]["x5c"][0]
    return "-----BEGIN CERTIFICATE-----\n" + cert + "\n-----END CERTIFICATE-----"

@app.route("/public")
def public():
    return jsonify({"message": "This is a public endpoint!"})

@app.route("/protected")
def protected():
    auth = request.headers.get("Authorization", None)
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401
    token = auth.split(" ")[1]
    try:
        public_key = get_public_key()
        decoded = jwt.decode(token, public_key, algorithms=["RS256"], audience="flask-client")
        return jsonify({"message": "You are authenticated!", "user": decoded.get("preferred_username")})
    except Exception as e:
        return jsonify({"error": "Invalid token", "details": str(e)}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

