from flask import Flask, render_template, request, redirect

app = Flask(__name__)

all_connections  = {}
all_servers = {}

@app.route('/index')
@app.route('/')
def index():
	return render_template('index.html', all_servers=all_servers, all_connections=all_connections)


@app.route('/addServer', methods=["POST"])
def addServer():
	if request.method == "POST":
		form = request.form
		name = request.form["name"]
		all_servers[name] = {}
		for key in form.keys():
			if key != "name":
				all_servers[name][key] = form[key]


		print(all_servers)


	return redirect('index')

@app.route('/addConnection', methods=["POST"])
def addConnection():
	if request.method == "POST":
		form = request.form
		name = request.form["name"]
		all_connections[name] = {}
		for key in form.keys():
			if key != "name":
				all_connections[name][key] = form[key]


		if "connections" not in all_servers[form['src']].keys():
			all_servers[form['src']]["connections"] = 1

		else:
			all_servers[form['src']]["connections"] += 1

		if "connections" not in all_servers[form['dst']].keys():
			all_servers[form['dst']]["connections"] = 1

		else:
			all_servers[form['dst']]["connections"] += 1


		print(all_connections)


	return redirect('index')



if __name__ == "__main__":
	app.run()