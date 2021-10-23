from flask import Flask, render_template
app = Flask(__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static')


# "database"
skills = ['python', 'javascript', 'bootstrap', 'react', 'c++', 'sql']

# map from profile name to profile
profiles = {}

# map from position name to position
positions = {}

# all votes a jobseeker has made
# map from username to map from position name to vote (true/false)
votes_by_profile = {}

# all votes a position has made
# map from position name to map from username to vote (true/false)
votes_by_position = {}

# logic for dealing with profiles and positions
def position_name(position):
  return (position.company, position.title)

def add_profile(profile):
  profiles[profile.username] = profile
  votes_by_profile[profile.username] = {}

def add_position(position):
  name = position_name(position)
  positions[name] = position
  votes_by_position[name] = {}

def score_match(profile, position):
  matches = 0.0
  for skill in profile['skills']:
    if skill in position['skills']:
      matches += 1

  return matches / len(position['skills'])

# Find the highest scoring position that the seeker has not already seen
def find_best_position(profile):
  best = None
  best_score = -1

  for position in positions:
    name = position_name(position)
    if not name in votes_by_profile[profile.username]:
      score = score_match(profile, position)
      if (score > best_score):
        best = position
        best_score = score
  
  return best

# Find the highest scoring profile that the position has not already seen
def find_best_profile(position):
  best = None
  best_score = -1

  name = position_name(position)

  for profile in profiles:
    if not profile.username in votes_by_position[name]:
      score = score_match(profile, position)
      if (score > best_score):
        best = position
        best_score = score
  
  return best

@app.route('/match_seeker_side')
def match_seeker_side():
  # FIXME: pass in from UI
  profile_name = 'FrontEndHacker123'
  profile = profiles[profile_name]
  best_match = find_best_position(profile)
  return render_template(
		'match_seeker_side.html',
		position=best_match
	)

@app.route('/match_position_side')
def match_position_side():
  # FIXME: pass in from UI
  company_name = 'Code2College'
  job_title = 'Front End Developer'
  position_name = (company_name, job_title)

  position = positions[position_name]
  best_match = find_best_profile(position)
  return render_template(
		'match_profile_side.html',
		profile=best_match
	)

# voting logic
@app.route('/record_vote_profile')
def record_vote_profile():
  # FIXME: pass in from UI
  profile_name = 'FrontEndHacker123'

  company_name = 'Code2College'
  job_title = 'Front End Developer'
  position_name = (company_name, job_title)

  vote = True

  votes_by_profile[profile_name][position_name] = vote

@app.route('/record_vote_position')
def record_vote_position():
  # FIXME: pass in from UI
  company_name = 'Code2College'
  job_title = 'Front End Developer'
  position_name = (company_name, job_title)

  profile_name = 'FrontEndHacker123'

  vote = False
  
  votes_by_position[position_name][profile_name] = vote


@app.route('/')
def home():
  return render_template(
		'home.html'
	)

def init_data():
  add_profile({
    'email': 'backendhacker@gmail.com',
    'username': 'Backend_Hacker1',
    'skills': ['python', 'sql']
  })
  add_profile({
    'email': 'frontendhacker@gmail.com',
    'username': 'FrontEndHacker123',
    'skills': ['javascript', 'bootstrap']
  })
  add_position({
    'title': 'Front End Developer',
    'company': 'Code2College',
    'description': 'Code2College is looking for a frontend developer to help builda new website.',
    'skills': ['javascript', 'react']
  })

if __name__ == '__main__':
  init_data()
  app.run(host='0.0.0.0', port=8080)
