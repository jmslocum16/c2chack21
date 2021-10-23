from flask import Flask, render_template
app = Flask(__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static')


skills = ['python', 'javascript', 'bootstrap', 'react', 'c++', 'sql']
profiles = [
  {
    'email': 'backendhacker@gmail.com',
    'username': 'Backend_Hacker1',
    'skills': ['python', 'sql']
  },
  {
    'email': 'frontendhacker@gmail.com',
    'username': 'FrontEndHacker123',
    'skills': ['javascript', 'bootstrap']
  }
]

positions = [
  {
    'title': 'Front End Developer',
    'company': 'Code2College',
    'description': 'Code2College is looking for a frontend developer to help builda new website.',
    'skills': ['javascript', 'react']
  }
]

def score_match(profile, position):
  matches = 0.0
  for skill in profile['skills']:
    if skill in position['skills']:
      matches += 1

  return matches / len(position['skills'])

@app.route('/match_seeker_side')
def match_seeker_side():
  best_position_match = {
    'title': 'Front End Developer',
    'company': 'Code2College',
    'description': 'Code2College is looking for a frontend developer to help builda new website.',
    'skills': ['javascript', 'react']
  }
  return render_template(
		'match_seeker_side.html',
		position=best_position_match
	)

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
