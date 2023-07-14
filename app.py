import src.sessions_status_updater
import src.partial_webscrape
import src.file_manipulations
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, Response
from time import sleep

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'amongus'
socketio = SocketIO(app, host='localhost', port=5000)
stored_inputs = []  # Array to store the inputs
page=''
sniper_running=False

@app.route('/')
def index():
    global page
    page = 'index.html'
    global stored_inputs
    stored_inputs = []
    return render_template('index.html', stored_inputs=stored_inputs)

@app.route('/course_snipe')
def course_snipe():
    global page
    page = 'courseNumSnipe.html'
    global stored_inputs
    stored_inputs = []
    return render_template('courseNumSnipe.html')

@app.route('/process', methods=['POST'])
def process():
    global stored_inputs
    user_input = request.form['input']
    if len(user_input)>5 and page=='index.html':return render_template(page, stored_inputs=stored_inputs, status = "invalid format (ex:00001)")
    if len(user_input)>10 and page=='courseNumSnipe.html':return render_template(page, stored_inputs=stored_inputs, status = "invalid format (ex:00:001:001)")
    if user_input in stored_inputs:return render_template(page, stored_inputs=stored_inputs, status = f"{user_input} was already entered.")
    for x in user_input:
        if x.isalpha():
            return render_template(page, stored_inputs=stored_inputs, status="Numbers Only!")  
    
    stored_inputs.append(user_input)
    if page == 'index.html':
        with open('settings/indexSrc.txt',mode='w') as f:
            for x in stored_inputs:
                f.write(x + '\n')
    elif page == 'courseNumSnipe.html':
        with open('settings/course_numbers.txt',mode='w') as f:
            for x in stored_inputs:
                f.write(x + '\n')
    return render_template(page, stored_inputs=stored_inputs, status=f"Added {user_input}")

@app.route('/clear_list', methods=['POST'])
def clear_list():
    global stored_inputs
    stored_inputs = []
    return render_template(page,stored_inputs=[],status="Cleared")

@app.route('/stop_sniper', methods=['POST'])
def stop_sniper():
    global sniper_running
    sniper_running = False
    return render_template(page,stored_inputs=[],status="Sniper stopped")

@socketio.on('start_sniper')
def handle_message():
    if page == "courseNumSnipe.html": src.partial_webscrape.get_indexes()
    global sniper_running
    sniper_running = True
    while(sniper_running):
        print('starting sniper process...')
        str = src.sessions_status_updater.return_data()
        emit('sex_with_andrewmama', str, broadcast=False)
        print('ending sniper process...')
        print(f"app.py:{str}/{type(str)}")
        sleep(5)



if __name__ == '__main__':
    stored_inputs = []
    page='index.html'
    socketio.run(app,debug='TRUE')
