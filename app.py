import flask
from flask import Flask, render_template, request
import src.sessions_status_updater

app = Flask(__name__)
stored_inputs = []  # Array to store the inputs
page=''

@app.route('/')
def index():
    global page
    page = 'index.html'
    global stored_inputs
    stored_inputs = []
    return render_template('index.html', stored_inputs=stored_inputs)

@app.route('/process', methods=['POST'])
def process():
    global stored_inputs
    user_input = request.form['input']
    if len(user_input)>10:return render_template(page, stored_inputs=stored_inputs, status = "invalid format (ex:01:001:001)")
    for x in user_input:
        if x.isalpha():
            return render_template(page, stored_inputs=stored_inputs, status="Numbers Only!")  
    
    stored_inputs.append(user_input)
    return render_template(page, stored_inputs=stored_inputs, status=f"Added {user_input}")

@app.route('/course_snipe')
def course_snipe():
    global page
    page = 'courseNumSnipe.html'
    global stored_inputs
    stored_inputs = []
    return render_template('courseNumSnipe.html')

@app.route('/clear_list', methods=['POST'])
def clear_list():
    global stored_inputs
    stored_inputs = []
    return render_template(page,stored_inputs=[],status="Cleared")

@app.route('/start_sniper', methods=['POST'])
def start_sniper():
    with open('settings/indexSrc.txt',mode='w') as f:
        for x in stored_inputs:
            f.write(x + '\n')
    return render_template(page,stored_inputs=[],status="Starting Sniper....")

if __name__ == '__main__':
    stored_inputs = []
    page='index.html'
    app.run(debug=True)
