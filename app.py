from flask import Flask, render_template
app = Flask(__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static')

counter = 0

@app.route('/')
def hello_world():
  global counter 

  counter += 1
  print(counter)
  return render_template(
		'home.html',
		counter=counter
	)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
