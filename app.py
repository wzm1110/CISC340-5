#web browser.html

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
import read_serial
@app.route('/', methods = ['GET' , 'POST'])
def home():

    status = [False, False]
    tag = "disarm"
    if request.method == 'POST':
        tag = request.form['tag']

    if tag == 'arm':
	status = [False, False]
        status = read_serial.system(True, status)
    else:
        status =[False, False] #read_serial.system(False, status)
    return render_template('index.html',system_status = tag, fire = status[0], intruder = status[1])

'''
@app.route('/system_status/')
def sys_status():
    if request.method == 'POST':
        return redirect(url_for(('home')))
    else:
        return render_template('system_status.html')


@app.route('/arm_system/', methods = ['GET', 'POST'])
def arm_system(methods = ['POST']):
    #arm_disarm = request.form.get("arm_system")
    
    return render_template('arm_system.html', posts = posts)

'''
    


if __name__ == '__main__':
    app.run('0.0.0.0')
    #app.run()

