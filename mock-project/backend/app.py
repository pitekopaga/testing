from flask import Flask, request, jsonify

app = Flask(__name__)

def is_distinguishable(color1, color2):
    if color1 == color2:
        return False
    if (color1.lower() == "#ff0000" and color2.lower() == "#00ff00") or \
       (color1.lower() == "#00ff00" and color2.lower() == "#ff0000"):
        return False
    return True

@app.route('/')
def home():
    return "Colorblind API is running. Use POST /check with JSON body containing color1 and color2."

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    color1 = data.get('color1')
    color2 = data.get('color2')
    if not color1 or not color2:
        return jsonify({'error': 'Missing color parameters'}), 400
    result = is_distinguishable(color1, color2)
    return jsonify({'distinguishable': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
