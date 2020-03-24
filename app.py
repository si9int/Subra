import wrapper
from flask import Flask, render_template, request, redirect, Response

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'xxx'

@app.route('/')
def index():
	scans = wrapper.load_scans()
	return render_template('index.html', title='Index', scans=scans, idle=wrapper.get_idle())

@app.route('/new')
def new_scan():
	return render_template('new_scan.html', title='New Scan')

@app.route('/new', methods=['POST'])
def run_scan():
	wrapper.run_subfinder(request.form['domain'], request.form['args'])
	return redirect('/')

@app.route('/options')
def options():
	return render_template('options.html', title='Options', config=wrapper.read_config())

@app.route('/options', methods=['POST'])
def save_options():
	wrapper.save_config(request.form['config'])
	return redirect('/options')

@app.route('/result/<domain>')
def result(domain):
	return render_template('result.html', title='Result: {}'.format(domain), result=wrapper.get_result(domain))

@app.route('/remove/<domain>')
def delete(domain):
	wrapper.delete_target(domain)
	return redirect('/')

@app.route('/export/<domain>/<type>')
def export(domain, type):
	data = wrapper.get_text(domain, type)
	return Response(data, mimetype='text/plain', headers={'Content-disposition' : 'attachment; filename={}.txt'.format(domain)})