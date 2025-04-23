import os
import ssl
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, request, Response

# === Logging setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)

LE_CERTS_DIR = "/certs/live"

def get_cert_info(cert_path):
    try:
        cert = ssl._ssl._test_decode_cert(cert_path)
        not_after_str = cert["notAfter"]
        not_after = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
        days_remaining = (not_after - datetime.utcnow()).days
        return {
            "not_after": not_after.strftime("%Y-%m-%d %H:%M:%S"),
            "days_remaining": days_remaining,
            "subject": dict(x[0] for x in cert["subject"])["commonName"],
        }
    except Exception as e:
        logging.error(f"Failed to parse cert at {cert_path}: {e}")
        return {"error": str(e)}

def list_certificates():
    certs = []
    if not os.path.isdir(LE_CERTS_DIR):
        logging.error(f"Let's Encrypt directory not found: {LE_CERTS_DIR}")
        return []

    for domain in os.listdir(LE_CERTS_DIR):
        cert_path = Path(LE_CERTS_DIR) / domain / "cert.pem"
        if cert_path.exists():
            logging.info(f"Loading certificate for domain: {domain}")
            info = get_cert_info(str(cert_path))
            info["domain"] = domain
            certs.append(info)
        else:
            logging.warning(f"cert.pem not found for domain: {domain}")
    return certs

def get_filtered_certs_from_request() -> list:
    warn_days = request.args.get("warn_days", type=int)
    logging.info(f"warn_days param: {warn_days}")

    certs = list_certificates()
    if warn_days is not None:
        before = len(certs)
        certs = [c for c in certs if c.get("days_remaining", 9999) <= warn_days]
        logging.info(f"Filtered certs: {len(certs)} of {before} (<= {warn_days} days)")
    return certs

@app.route("/count", methods=["GET"])
def get_cert_count():
    certs = get_filtered_certs_from_request()
    count = len(certs)
    logging.info(f"Returning count: {count}")
    return Response(f"{count}", mimetype="text/plain")


@app.route("/", methods=["GET"])
def get_certs():
    certs = get_filtered_certs_from_request()
    logging.info(f"Returning {len(certs)} certs")
    return jsonify(certs)


if __name__ == "__main__":
    logging.info("🚀 Starting the certs API server...")
    app.run(host="0.0.0.0", port=8000)

