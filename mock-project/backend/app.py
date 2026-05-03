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
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Colorblindness Checker Demo</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            input { width: 100%; padding: 8px; margin: 10px 0; font-family: monospace; }
            button { background: #0066cc; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            button:hover { background: #0052a3; }
            .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
            .pass { background: #d4edda; color: #155724; }
            .fail { background: #f8d7da; color: #721c24; }
            .color-preview { display: inline-block; width: 50px; height: 50px; margin: 5px; border: 1px solid #ccc; vertical-align: middle; }
            .disclaimer { background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 20px 0; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>Colorblindness Checker Demo</h1>
        <p style="font-style: italic;">A demonstration project for CSS 508 - Software Testing & Quality</p>
        
        <div class="disclaimer">
            <strong>Note:</strong> This is a simplified demonstration. The current version only knows that pure red (#FF0000) and pure green (#00FF00) are indistinguishable, and that pure red and pure blue (#0000FF) are distinguishable. For all other color pairs, it assumes they are distinguishable. A real implementation would use perceptual distance algorithms.
        </div>
        
        <label>Color 1 (hex):</label>
        <input type="text" id="color1" placeholder="#FF0000" value="#FF0000">
        <div class="color-preview" id="preview1" style="background-color:#FF0000"></div>
        
        <label>Color 2 (hex):</label>
        <input type="text" id="color2" placeholder="#00FF00" value="#00FF00">
        <div class="color-preview" id="preview2" style="background-color:#00FF00"></div>
        
        <button onclick="checkColors()">Check</button>
        
        <div id="result"></div>
        
        <script>
            document.getElementById('color1').addEventListener('input', function() {
                document.getElementById('preview1').style.backgroundColor = this.value;
            });
            document.getElementById('color2').addEventListener('input', function() {
                document.getElementById('preview2').style.backgroundColor = this.value;
            });
            
            async function checkColors() {
                const color1 = document.getElementById('color1').value;
                const color2 = document.getElementById('color2').value;
                const resultDiv = document.getElementById('result');
                
                resultDiv.innerHTML = '<p>Checking...</p>';
                
                try {
                    const response = await fetch('/check', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({color1: color1, color2: color2})
                    });
                    const data = await response.json();
                    
                    if (data.distinguishable === true) {
                        resultDiv.innerHTML = '<div class="result pass">✓ These colors are DISTINGUISHABLE (according to this simplified demo).</div>';
                    } else if (data.distinguishable === false) {
                        resultDiv.innerHTML = '<div class="result fail">✗ These colors are NOT DISTINGUISHABLE (according to this simplified demo).</div>';
                    } else if (data.error) {
                        resultDiv.innerHTML = '<div class="result fail">Error: ' + data.error + '</div>';
                    }
                } catch (error) {
                    resultDiv.innerHTML = '<div class="result fail">Error: Could not reach the API. Make sure the server is running.</div>';
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}

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
