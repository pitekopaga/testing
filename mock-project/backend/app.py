from flask import Flask, render_template_string, session, redirect, url_for, request
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Number patterns (5x5 grid)
PATTERNS = {
    0: [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    1: [
        [0,0,1,0,0],
        [0,1,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,1,1,1,0]
    ],
    2: [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,0,1,1,0],
        [0,1,0,0,0],
        [1,1,1,1,1]
    ],
    3: [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,0,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    4: [
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [0,0,0,0,1],
        [0,0,0,0,1]
    ],
    5: [
        [1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [0,0,0,0,1],
        [1,1,1,1,0]
    ],
    6: [
        [0,1,1,1,0],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    7: [
        [1,1,1,1,1],
        [0,0,0,0,1],
        [0,0,1,1,0],
        [0,1,0,0,0],
        [1,0,0,0,0]
    ],
    8: [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,0]
    ],
    9: [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [0,1,1,1,1],
        [0,0,0,0,1],
        [0,1,1,1,0]
    ],
}

def get_pattern(num):
    if num < 10:
        return PATTERNS.get(num, PATTERNS[0])
    tens = num // 10
    ones = num % 10
    p1 = PATTERNS.get(tens, PATTERNS[0])
    p2 = PATTERNS.get(ones, PATTERNS[0])
    combined = []
    for i in range(5):
        row = p1[i] + [0] + p2[i]
        combined.append(row)
    return combined

def make_plate(plate_type, number):
    if plate_type == 'protan':
        # Protan - make it VERY hard for red-deficient
        base_red = random.randint(80, 110)
        base_green = random.randint(80, 110)
        bg = [base_red, base_green, random.randint(60, 90)]
        fg = [base_red + random.randint(-10, 10), base_green + random.randint(-10, 10), random.randint(60, 90)]
    elif plate_type == 'deutan':
        # Deutan - medium difficulty
        bg = [random.randint(70, 100), random.randint(120, 150), random.randint(70, 100)]
        fg = [random.randint(120, 150), random.randint(40, 70), random.randint(70, 100)]
    elif plate_type == 'tritan':
        # Tritan - VERY easy for normal vision (high contrast)
        bg = [120, 120, 120]
        fg = [40, 40, 200]
    else:
        # Control - extremely easy
        bg = [60, 60, 60]
        fg = [220, 220, 220]
    
    for i in range(3):
        bg[i] = max(30, min(230, bg[i]))
        fg[i] = max(30, min(230, fg[i]))
    
    return {
        'num': number,
        'type': plate_type,
        'bg': bg,
        'fg': fg,
        'pattern': get_pattern(number)
    }

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Color Vision Test</title>
    <style>
        body { text-align: center; background: #1a1a2e; color: white; font-family: Arial; padding: 20px; }
        canvas { background: #0f0f1a; border-radius: 20px; margin: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        button { background: #e94560; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; }
        button:hover { background: #ff6b8a; }
        input { padding: 10px; width: 100px; text-align: center; border-radius: 8px; border: none; font-size: 16px; }
        .progress { background: #2a2a3e; height: 8px; border-radius: 4px; margin: 20px 0; }
        .bar { background: #e94560; height: 8px; border-radius: 4px; width: 0%; }
        .result-card { background: #16213e; padding: 25px; border-radius: 20px; margin-top: 20px; max-width: 500px; margin-left: auto; margin-right: auto; }
        .score { font-size: 48px; font-weight: bold; margin: 10px; }
        .warning { background: #e94560; padding: 15px; border-radius: 10px; }
        .normal { background: #0f3460; padding: 15px; border-radius: 10px; }
        .instructions { background: #16213e; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .note { font-size: 12px; color: #888; margin-top: 20px; }
        h1 { color: #e94560; }
    </style>
</head>
<body>
    <h1>Color Vision Diagnostic Test</h1>
    {% if not done %}
    <div class="instructions">
        <strong>Instructions:</strong> A number is hidden in the circle of dots. Type the number you see.<br>
        If you do not see any number, click the <strong>No Number</strong> button.
    </div>
    
    <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #e94560; text-align: left;">
        <strong>⚠️ Disclaimer:</strong> This test is for informational and educational purposes only. 
        It is not a medical diagnosis. If you have concerns about your color vision, please consult 
        an eye care professional. Results may vary and should not be used for official medical determinations.
    </div>
    
    <div class="progress"><div class="bar" style="width: {{ pct }}%"></div></div>
    <p>Plate {{ idx }} of {{ total }}</p>
    <canvas id="canvas" width="500" height="500"></canvas>
    <form method="POST">
        <div style="display: flex; gap: 10px; justify-content: center; margin-top: 10px;">
            <input type="number" name="answer" placeholder="Enter number" autofocus style="flex:1;">
            <button type="submit" style="background: #e94560;">Submit</button>
            <button type="submit" name="skip" value="skip" style="background: #6c757d;">No Number</button>
        </div>
    </form>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const cx = 250, cy = 250, rmax = 220;
        const pattern = {{ pattern|tojson }};
        const bg = {{ bg|tojson }};
        const fg = {{ fg|tojson }};
        const rows = pattern.length, cols = pattern[0].length;
        const cell = 45;
        const totalWidth = cols * cell;
        const totalHeight = rows * cell;
        const offX = cx - totalWidth / 2;
        const offY = cy - totalHeight / 2;
        function isNumberDot(x, y) {
            for (let i = 0; i < rows; i++) {
                for (let j = 0; j < cols; j++) {
                    if (pattern[i][j]) {
                        const dx = offX + j * cell + cell/2;
                        const dy = offY + i * cell + cell/2;
                        if (Math.hypot(x - dx, y - dy) < cell / 2) return true;
                    }
                }
            }
            return false;
        }
        for (let i = 0; i < 1400; i++) {
            const a = Math.random() * Math.PI * 2, r = Math.sqrt(Math.random()) * rmax;
            const x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r;
            const rgb = isNumberDot(x, y) ? fg : bg;
            const v = 25;
            ctx.fillStyle = `rgb(${Math.min(255,Math.max(0,rgb[0]+(Math.random()-0.5)*v))}, ${Math.min(255,Math.max(0,rgb[1]+(Math.random()-0.5)*v))}, ${Math.min(255,Math.max(0,rgb[2]+(Math.random()-0.5)*v))}`;
            ctx.beginPath();
            ctx.arc(x, y, 6 + Math.random() * 3, 0, Math.PI * 2);
            ctx.fill();
        }
    </script>
    {% else %}
    <div class="result-card">
        <h2>Your Color Blind Test Result</h2>
        <p><strong>{{ diagnosis }}</strong></p>
        <p>{{ description }}</p>
        
        <div style="margin: 20px 0;">
            <div>Blue Cone (Tritan)</div>
            <div class="score">{{ blue_score }}%</div>
            <progress value="{{ blue_score }}" max="100" style="width:100%; height:20px;"></progress>
        </div>
        
        <div style="margin: 20px 0;">
            <div>Green Cone (Deutan)</div>
            <div class="score">{{ green_score }}%</div>
            <progress value="{{ green_score }}" max="100" style="width:100%; height:20px;"></progress>
        </div>
        
        <div style="margin: 20px 0;">
            <div>Red Cone (Protan)</div>
            <div class="score">{{ red_score }}%</div>
            <progress value="{{ red_score }}" max="100" style="width:100%; height:20px;"></progress>
        </div>
        
        <div class="note">Note: Scores below 60% indicate a possible deficiency in that cone type.</div>
        
        <div style="margin: 20px 0;">
            <button onclick="exportToCSV()" style="background: #28a745; margin-right: 10px;">Export Results to CSV</button>
        </div>
        
        <form method="POST" action="/reset" style="margin-top: 20px;">
            <button type="submit">Take Test Again</button>
        </form>
    </div>
    <script>
        function exportToCSV() {
            const redScore = {{ red_score }};
            const greenScore = {{ green_score }};
            const blueScore = {{ blue_score }};
            const diagnosis = "{{ diagnosis }}";
            
            const csvContent = "data:text/csv;charset=utf-8," 
                + "Cone Type,Score (%)\\n"
                + "Red," + redScore + "\\n"
                + "Green," + greenScore + "\\n"
                + "Blue," + blueScore + "\\n"
                + "Diagnosis," + diagnosis;
            
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "color_vision_results.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
    {% endif %}
</body>
</html>
'''

PROTAN_QUESTIONS = [12, 8, 5, 74, 29, 6, 3, 15]
DEUTAN_QUESTIONS = [12, 8, 5, 74, 29, 6, 3, 15]
TRITAN_QUESTIONS = [2, 9, 4]
CONTROL_QUESTIONS = [7, 0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('initialized'):
        session.clear()
        plates = []
        for q in PROTAN_QUESTIONS:
            plates.append(make_plate('protan', q))
        for q in DEUTAN_QUESTIONS:
            plates.append(make_plate('deutan', q))
        for q in TRITAN_QUESTIONS:
            plates.append(make_plate('tritan', q))
        for q in CONTROL_QUESTIONS:
            plates.append(make_plate('control', q))
        random.shuffle(plates)
        
        session['plates'] = plates
        session['answers'] = []
        session['step'] = 0
        session['initialized'] = True
        session.modified = True
    
    if request.method == 'POST':
        # Handle the "No Number" button or regular number input
        if 'skip' in request.form:
            user_number = 0
        else:
            ans = request.form.get('answer', '0')
            try:
                user_number = int(ans)
            except:
                user_number = 0
        
        step = session.get('step', 0)
        plates = session.get('plates', [])
        
        if step < len(plates):
            answers = session.get('answers', [])
            answers.append({
                'user': user_number,
                'correct': plates[step]['num'],
                'type': plates[step]['type']
            })
            session['answers'] = answers
            session['step'] = step + 1
            session.modified = True
        
        if session.get('step', 0) >= len(plates):
            return redirect(url_for('result'))
    
    step = session.get('step', 0)
    plates = session.get('plates', [])
    
    if step >= len(plates) or not plates:
        return redirect(url_for('result'))
    
    p = plates[step]
    return render_template_string(HTML, 
        pattern=p['pattern'], 
        bg=p['bg'], 
        fg=p['fg'], 
        idx=step+1, 
        total=len(plates), 
        pct=(step/len(plates))*100, 
        done=False)

@app.route('/result')
def result():
    answers = session.get('answers', [])
    plates = session.get('plates', [])
    
    protan_correct = 0
    protan_total = 0
    deutan_correct = 0
    deutan_total = 0
    tritan_correct = 0
    tritan_total = 0
    
    for i, a in enumerate(answers):
        if i >= len(plates):
            continue
        plate_type = plates[i]['type']
        is_correct = (a['user'] == a['correct'])
        
        if plate_type == 'protan':
            protan_total += 1
            if is_correct:
                protan_correct += 1
        elif plate_type == 'deutan':
            deutan_total += 1
            if is_correct:
                deutan_correct += 1
        elif plate_type == 'tritan':
            tritan_total += 1
            if is_correct:
                tritan_correct += 1
    
    red_score = round((protan_correct / max(protan_total, 1)) * 100)
    green_score = round((deutan_correct / max(deutan_total, 1)) * 100)
    blue_score = round((tritan_correct / max(tritan_total, 1)) * 100)
    
    # Find the lowest score
    scores = {'red': red_score, 'green': green_score, 'blue': blue_score}
    min_type = min(scores, key=scores.get)
    min_score = scores[min_type]
    
    if min_score < 60:
        if min_type == 'red':
            diagnosis = "Protan Color Blind"
            description = "You have a stronger deficiency in your red color cone, which means you have a type of red-green color blindness called Protan."
        elif min_type == 'green':
            diagnosis = "Deutan Color Blind"
            description = "You have a stronger deficiency in your green color cone, which means you have a type of red-green color blindness called Deutan."
        else:
            diagnosis = "Tritan Color Blind"
            description = "You have a deficiency in your blue color cone, which means you have blue-yellow color blindness called Tritan."
    else:
        diagnosis = "Normal Color Vision"
        description = "Your color vision appears normal within the range of this test."
    
    return render_template_string(HTML, 
        done=True, 
        red_score=red_score,
        green_score=green_score,
        blue_score=blue_score,
        diagnosis=diagnosis,
        description=description)

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
