from flask import Flask, request, jsonify
import paho.mqtt.publish as publish
import ssl, json

app = Flask(__name__)

MQTT_HOST = "e04596125ad349cbb8a7733a01b6a57f.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "LumiVerse"
MQTT_PASS = "Alohomora7"
MQTT_TOPIC = "flutter/sound"

@app.route('/play-sound', methods=['POST'])
def play_sound():
    data = request.get_json()
    character = data.get("character")
    sound = data.get("sound")

    payload = json.dumps({"character": character, "sound": sound})

    try:
        # إرسال الرسالة فعليًا لـ MQTT
        publish.single(
            MQTT_TOPIC,
            payload,
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            auth={'username': MQTT_USER, 'password': MQTT_PASS},
            tls={'ca_certs': None, 'cert_reqs': ssl.CERT_NONE}
        )
        return jsonify({"status": "ok", "character": character, "sound": sound})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
