from flask import Flask, render_template_string, session, redirect, url_for, request, Response
import random
import psutil
import json
import os
from datetime import datetime
from collections import Counter

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

RESULTS_FILE = 'test_results.json'

def save_survey(username, answers, test_results):
    """Save survey response linked to test results."""
    import csv
    from datetime import datetime
    
    # Handle checkbox lists properly
    accurate_cones = answers.getlist('accurate_cones') if hasattr(answers, 'getlist') else answers.get('accurate_cones', '').split(',')
    inaccurate_cones = answers.getlist('inaccurate_cones') if hasattr(answers, 'getlist') else answers.get('inaccurate_cones', '').split(',')
    too_high_cones = answers.getlist('too_high_cones') if hasattr(answers, 'getlist') else answers.get('too_high_cones', '').split(',')
    too_low_cones = answers.getlist('too_low_cones') if hasattr(answers, 'getlist') else answers.get('too_low_cones', '').split(',')
    
    # Convert lists to strings
    accurate_str = ','.join(accurate_cones) if accurate_cones else ''
    inaccurate_str = ','.join(inaccurate_cones) if inaccurate_cones else ''
    too_high_str = ','.join(too_high_cones) if too_high_cones else ''
    too_low_str = ','.join(too_low_cones) if too_low_cones else ''
    
    file_exists = os.path.isfile('survey_data.csv')
    with open('survey_data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                'timestamp', 'username', 'diagnosis', 'red_score', 'green_score', 'blue_score',
                'prior_belief', 'taken_other_tests', 'confidence', 
                'accurate_cones', 'inaccurate_cones', 'too_high_cones', 'too_low_cones', 'comments'
            ])
        writer.writerow([
            datetime.now().isoformat(),
            username,
            test_results.get('diagnosis', ''),
            test_results.get('red_score', ''),
            test_results.get('green_score', ''),
            test_results.get('blue_score', ''),
            answers.get('prior_belief', ''),
            answers.get('taken_other_tests', ''),
            answers.get('confidence', ''),
            accurate_str,
            inaccurate_str,
            too_high_str,
            too_low_str,
            answers.get('comments', '')
        ])

def save_result(username, diagnosis, scores):
    """Save a user's test result to a JSON file."""
    data = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            data = json.load(f)
    
    if username not in data:
        data[username] = []
    
    data[username].append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'diagnosis': diagnosis,
        'red_score': scores.get('red', 0),
        'green_score': scores.get('green', 0),
        'blue_score': scores.get('blue', 0)
    })
    
    with open(RESULTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_consistency(username):
    """Calculate consistency score for a user based on past results."""
    if not os.path.exists(RESULTS_FILE):
        return None
    
    with open(RESULTS_FILE, 'r') as f:
        data = json.load(f)
    
    if username not in data:
        return None
    
    results = data[username]
    if len(results) < 2:
        return {'message': 'Take the test at least twice to see consistency', 'total_sessions': len(results)}
    
    # Compare the actual diagnosis strings
    diagnoses = [r['diagnosis'] for r in results]
    most_common = Counter(diagnoses).most_common(1)[0][0]
    consistency_percent = (diagnoses.count(most_common) / len(diagnoses)) * 100
    
    return {
        'total_sessions': len(results),
        'consistency_percent': round(consistency_percent, 1),
        'primary_diagnosis': most_common,
        'all_diagnoses': diagnoses
    }

def get_all_results(username):
    """Get all results for a user for CSV export."""
    if not os.path.exists(RESULTS_FILE):
        return []
    
    with open(RESULTS_FILE, 'r') as f:
        data = json.load(f)
    
    if username not in data:
        return []
    
    return data[username]

# Number patterns
PATTERNS = {
    0: [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
    1: [[0,0,1,0,0],[0,1,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,1,1,1,0]],
    2: [[0,1,1,1,0],[1,0,0,0,1],[0,0,1,1,0],[0,1,0,0,0],[1,1,1,1,1]],
    3: [[0,1,1,1,0],[1,0,0,0,1],[0,0,1,1,0],[1,0,0,0,1],[0,1,1,1,0]],
    4: [[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1],[0,0,0,0,1],[0,0,0,0,1]],
    5: [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[0,0,0,0,1],[1,1,1,1,0]],
    6: [[0,1,1,1,0],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,1],[0,1,1,1,0]],
    7: [[1,1,1,1,1],[0,0,0,0,1],[0,0,1,1,0],[0,1,0,0,0],[1,0,0,0,0]],
    8: [[0,1,1,1,0],[1,0,0,0,1],[0,1,1,1,0],[1,0,0,0,1],[0,1,1,1,0]],
    9: [[0,1,1,1,0],[1,0,0,0,1],[0,1,1,1,1],[0,0,0,0,1],[0,1,1,1,0]],
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
        base_red = random.randint(80, 110)
        base_green = random.randint(80, 110)
        bg = [base_red, base_green, random.randint(60, 90)]
        fg = [base_red + random.randint(-10, 10), base_green + random.randint(-10, 10), random.randint(60, 90)]
    elif plate_type == 'deutan':
        bg = [random.randint(70, 100), random.randint(120, 150), random.randint(70, 100)]
        fg = [random.randint(120, 150), random.randint(40, 70), random.randint(70, 100)]
    elif plate_type == 'tritan':
        bg = [120, 120, 120]
        fg = [40, 40, 200]
    else:
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
        canvas { background: #0f0f1a; border-radius: 20px; margin: 20px; }
        button { background: #e94560; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; }
        button:hover { background: #ff6b8a; }
        input { padding: 10px; width: 100px; text-align: center; border-radius: 8px; border: none; font-size: 16px; }
        .progress { background: #2a2a3e; height: 8px; border-radius: 4px; margin: 20px 0; }
        .bar { background: #e94560; height: 8px; border-radius: 4px; width: 0%; }
        .result-card { background: #16213e; padding: 25px; border-radius: 20px; margin-top: 20px; max-width: 600px; margin-left: auto; margin-right: auto; }
        .score { font-size: 48px; font-weight: bold; margin: 10px; }
        .warning { background: #e94560; padding: 15px; border-radius: 10px; }
        .normal { background: #0f3460; padding: 15px; border-radius: 10px; }
        .instructions { background: #16213e; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .note { font-size: 12px; color: #888; margin-top: 20px; }
        h1 { color: #e94560; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 12px; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #444; }
        th { background: #0f0f1a; }
    </style>
</head>
<body>
    <h1>Color Vision Diagnostic Test</h1>
    {% if not done %}
    <div class="instructions">
        <strong>Instructions:</strong> A number is hidden in the circle of dots.<br>
        Type the number you see and press Enter, or click Submit.<br>
        If you do not see any number, click the <strong>No Number</strong> button.
    </div>
    
    <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #e94560; text-align: left;">
        <strong>⚠️ Disclaimer:</strong> This test is for informational and educational purposes only. 
        It is not a medical diagnosis. If you have concerns about your color vision, please consult 
        an eye care professional.
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
            <div>Blue Cone</div>
            <div class="score">{{ blue_score }}%</div>
            <progress value="{{ blue_score }}" max="100" style="width:100%; height:20px;"></progress>
        </div>
        
        <div style="margin: 20px 0;">
            <div>Green Cone</div>
            <div class="score">{{ green_score }}%</div>
            <progress value="{{ green_score }}" max="100" style="width:100%; height:20px;"></progress>
        </div>
        
        <div style="margin: 20px 0;">
            <div>Red Cone</div>
            <div class="score">{{ red_score }}%</div>
            <progress value="{{ red_score }}" max="100" style="width:100%; height:20px;"></progress>
        </div>
        
        <div class="note">Note: Scores below 60% indicate a possible deficiency.</div>
        
        <a href="/export-csv" download="color_vision_history.csv">
            <button style="background: #28a745; margin: 10px;">Export All Results to CSV</button>
        </a>
        
        {% if consistency %}
        <div style="background: #2a2a3e; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3>Your History</h3>
            <p>You have taken this test {{ consistency.total_sessions }} time(s).</p>
            {% if consistency.consistency_percent %}
            <p>Consistency: <strong>{{ consistency.consistency_percent }}%</strong></p>
            <p>Most common diagnosis: <strong>{{ consistency.primary_diagnosis }}</strong></p>
            <p>All diagnoses: {{ consistency.all_diagnoses|join(', ') }}</p>
            {% else %}
            <p>{{ consistency.message }}</p>
            {% endif %}
        </div>
        {% endif %}
        
        <a href="/survey">
            <button type="button" style="background: #6c757d; margin: 10px;">Help Improve Accuracy (Optional Survey)</button>
        </a>

        <form method="POST" action="/reset" style="display: inline;">
            <button type="submit">Take Test Again</button>
        </form>
        <form method="POST" action="/logout" style="display: inline;">
            <button type="submit" style="background: #6c757d;">Exit</button>
        </form>
    </div>
    {% endif %}
</body>
</html>
'''

SURVEY_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Help Improve Accuracy - Color Vision Test</title>
    <style>
        body { text-align: center; background: #1a1a2e; color: white; font-family: Arial; padding: 20px; }
        .survey-container { background: #16213e; padding: 25px; border-radius: 20px; max-width: 600px; margin: 0 auto; text-align: left; }
        h1 { color: #e94560; text-align: center; }
        h3 { margin-top: 20px; margin-bottom: 10px; color: #e94560; }
        label, input, select, textarea { margin: 5px 0; }
        input[type="checkbox"] { margin-right: 10px; }
        .checkbox-group { margin: 10px 0; }
        button { background: #e94560; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; margin-top: 20px; }
        button:hover { background: #ff6b8a; }
        .note { font-size: 12px; color: #888; margin-top: 20px; text-align: center; }
        .skip { text-align: center; margin-top: 15px; }
        .skip a { color: #888; text-decoration: none; }
    </style>
</head>
<body>
    <div class="survey-container">
        <h1>Help Improve Accuracy</h1>
        <p>Your answers to this optional survey will help me calibrate the test. No personal information is collected. Responses are anonymous.</p>
        <p><strong>Your survey responses will be linked to your test results for this session.</strong></p>

        <form method="POST">
            <h3>Before this test, what did you believe your color vision to be?</h3>
            <select name="prior_belief" required>
                <option value="">-- Select an option --</option>
                <option value="normal">Normal color vision</option>
                <option value="protan">Protan (red deficient)</option>
                <option value="deutan">Deutan (green deficient)</option>
                <option value="tritan">Tritan (blue deficient)</option>
                <option value="unsure">Unsure</option>
            </select>
            
            <h3>Have you taken other colorblindness tests before?</h3>
            <input type="radio" name="taken_other_tests" value="yes"> Yes
            <input type="radio" name="taken_other_tests" value="no"> No
            
            <h3>How confident are you in the accuracy of this test's results?</h3>
            <select name="confidence" required>
                <option value="">-- Select an option --</option>
                <option value="1">1 - Not confident</option>
                <option value="2">2 - Slightly confident</option>
                <option value="3">3 - Moderately confident</option>
                <option value="4">4 - Very confident</option>
                <option value="5">5 - Extremely confident</option>
            </select>
            
            <h3>Which cone scores seemed accurate? (check all that apply)</h3>
            <div class="checkbox-group">
                <input type="checkbox" name="accurate_cones" value="red"> Red (Protan)<br>
                <input type="checkbox" name="accurate_cones" value="green"> Green (Deutan)<br>
                <input type="checkbox" name="accurate_cones" value="blue"> Blue (Tritan)<br>
            </div>
            
            <h3>Which cone scores seemed inaccurate? (check all that apply)</h3>
            <div class="checkbox-group">
                <input type="checkbox" name="inaccurate_cones" value="red"> Red<br>
                <input type="checkbox" name="inaccurate_cones" value="green"> Green<br>
                <input type="checkbox" name="inaccurate_cones" value="blue"> Blue<br>
            </div>
            
            <h3>Which cone scores seemed too high?</h3>
            <div class="checkbox-group">
                <input type="checkbox" name="too_high_cones" value="red"> Red<br>
                <input type="checkbox" name="too_high_cones" value="green"> Green<br>
                <input type="checkbox" name="too_high_cones" value="blue"> Blue<br>
            </div>
            
            <h3>Which cone scores seemed too low?</h3>
            <div class="checkbox-group">
                <input type="checkbox" name="too_low_cones" value="red"> Red<br>
                <input type="checkbox" name="too_low_cones" value="green"> Green<br>
                <input type="checkbox" name="too_low_cones" value="blue"> Blue<br>
            </div>
            
            <h3>Other comments (optional)</h3>
            <textarea name="comments" rows="4" cols="50" style="width: 100%;"></textarea>
            
            <button type="submit">Submit Survey</button>
        </form>
        
        <div class="skip">
            <a href="/result">Skip and return to results</a>
        </div>
        <div class="note">Your responses are anonymous and will only be used to improve test accuracy.</div>
    </div>
</body>
</html>
'''

PROTAN_QUESTIONS = [12, 8, 5, 74, 29, 6, 3, 15]
DEUTAN_QUESTIONS = [12, 8, 5, 74, 29, 6, 3, 15]
TRITAN_QUESTIONS = [2, 9, 4]
CONTROL_QUESTIONS = [7, 0]

@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear()
    
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('test'))
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Color Vision Test - Login</title>
        <style>
            body { text-align: center; background: #1a1a2e; color: white; font-family: Arial; padding: 50px; }
            input, button { padding: 10px; margin: 10px; font-size: 16px; border-radius: 8px; }
            button { background: #e94560; color: white; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Color Vision Diagnostic Test</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Enter your name or email" required size="30">
            <button type="submit">Start Test</button>
        </form>
        <p style="margin-top: 30px; font-size: 12px; color: #888;">Your results will be saved to track consistency over time.</p>
    </body>
    </html>
    '''

@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if not session.get('initialized'):
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
    
    if request.method == 'POST':
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
    
    scores = {'red': red_score, 'green': green_score, 'blue': blue_score}
    min_type = min(scores, key=scores.get)
    
    if scores[min_type] < 60:
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
    
    username = session.get('username')
    if username:
        result_scores = {'red': red_score, 'green': green_score, 'blue': blue_score}
        save_result(username, diagnosis, result_scores)
        consistency = get_consistency(username)
    else:
        consistency = None
    
    return render_template_string(HTML, 
        done=True, 
        red_score=red_score,
        green_score=green_score,
        blue_score=blue_score,
        diagnosis=diagnosis,
        description=description,
        consistency=consistency)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get the most recent test results for this user
    username = session['username']
    results = get_all_results(username)
    latest_result = results[-1] if results else {}
    
    if request.method == 'POST':
        save_survey(username, request.form, latest_result)
        return redirect(url_for('result'))
    
    # GET request - show the survey form
    return render_template_string(SURVEY_HTML)

@app.route('/export-csv')
def export_csv():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    results = get_all_results(username)
    if not results:
        return "No results found", 404
    
    # Create CSV content
    csv_lines = ["Timestamp,Diagnosis,Red Score (Protan),Green Score (Deutan),Blue Score (Tritan)"]
    for r in results:
        csv_lines.append(f"{r['timestamp']},{r['diagnosis']},{r['red_score']},{r['green_score']},{r['blue_score']}")
    
    csv_content = "\n".join(csv_lines)
    
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=color_vision_history_{username}.csv"}
    )

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('answers', None)
    session.pop('step', None)
    session.pop('plates', None)
    session.pop('initialized', None)
    return redirect(url_for('test'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/debug/stats')
def debug_stats():
    return {
        'status': 'ok',
        'cpu_percent': psutil.cpu_percent(interval=0.1),
        'memory_percent': psutil.virtual_memory().percent,
        'active_sessions': len(session.keys()) if session else 0
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
