from flask import Flask, render_template, redirect, url_for, request
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
  return (position['company'], position['title'])

def add_profile(profile):
  profiles[profile['username']] = profile
  votes_by_profile[profile['username']] = {}

def add_position(position):
  name = position_name(position)
  positions[name] = position
  votes_by_position[name] = {}

def score_match(profile, position):
  matches = 0
  for skill in profile['skills']:
    if skill in position['skills']:
      matches += 1
    
  score = 100.0 * (matches / len(position['skills']))
  print(profile['username'] + ' + ' + str(position_name(position)) + ' = ' + str(score))
  return score

# Find the highest scoring position that the seeker has not already seen
def find_best_position(profile):
  best = None
  best_score = -1

  for position in positions.values():
    name = position_name(position)
    if not name in votes_by_profile[profile['username']]:
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

  for profile in profiles.values():
    if not profile['username'] in votes_by_position[name]:
      score = score_match(profile, position)
      if (score > best_score):
        best = profile
        best_score = score
  
  return best

# Find all matches for a profile. Specifically, for each of the positions the profile voted yes on, check if that position also voted yes on the profile
def find_profile_matches(profile):
  matches = []
  for position_name, vote in votes_by_profile[profile['username']].items():
    if vote and profile['username'] in votes_by_position[position_name] and votes_by_position[position_name][profile['username']]:
      matches.append(positions[position_name])
  return matches

  
# Find all matches for a position. Specifically, for each of the profiles the position voted yes on, check if that profile also voted yes on the position
def find_position_matches(position):
  name = position_name(position)
  matches = []
  for username, vote in votes_by_position[name].items():
    if vote and name in votes_by_profile[username] and votes_by_profile[username][name]:
      matches.append(profiles[username])
  return matches


@app.route('/seeker_creation_page', methods=['GET'])
def seeker_creation_page():
  return render_template('seeker_creation_page.html')

@app.route('/seeker_creation_page', methods=['POST'])
def submit_seeker_creation():
  print(request.form)
  # FIXME: get everything from the form
  username = request.form['username']
  email = request.form['email']
  job_field = request.form['job_field']
  skill1 = request.form['skill_1']
  skill2 = request.form['skill_2']
  location = request.form['prefer_location']

  profile = {}
  profile['username'] = username
  profile['email'] = email
  profile['job_field'] = job_field
  profile['skills'] = [skill for skill in [skill1, skill2] if len(skill) > 0]
  profile['location'] = location
  print(profile)
  add_profile(profile)

  return redirect('/match_seeker_side/'+username)

#adds app route to employer creation page
@app.route('/employer_creation_page')
def employer_creation_page():
  return render_template('employer_creation_page.html')

@app.route('/employer_creation_page', methods=['POST'])
def submit_position_creation():
  print(request.form)
  # FIXME: get everything from the form
  position = {}
  add_profile(position)

  return redirect(url_for('match_position_side'))


# matching for seeker
@app.route('/match_seeker_side/<username>', methods=['GET'])
def match_seeker_side(username):
  print('match seeker for ' + username)
  # FIXME: pass in from UI
  profile = profiles[username]
  best_match = find_best_position(profile)
  print(best_match)
  return render_template(
		'match_seeker_side.html',
    username=username,
		position=best_match
	)

@app.route('/match_seeker_side/<username>', methods=['POST'])
def record_vote_profile(username):
  print('match submitted')
  print(username)
  # FIXME: pass in from UI
  profile_name = username

  company_name = request.form['company_name']
  job_title = request.form['title']
  position_name = (company_name, job_title)
  vote = 'match' in request.form

  print(profile_name + ' matched ' + company_name + ':' + job_title + ' with ' + str(vote))
  votes_by_profile[profile_name][position_name] = vote

  # re-populate matching page
  return redirect('/match_seeker_side/'+profile_name)

#matching for positions
@app.route('/match_position_side', methods=['GET'])
def match_position_side():
  # FIXME: pass in from UI
  company_name = 'Code2College'
  job_title = 'FrontEndDeveloper'
  position_name = (company_name, job_title)

  position = positions[position_name]
  best_match = find_best_profile(position)
  return render_template(
		'match_position_side.html',
		profile=best_match,
    position=position
	)

@app.route('/record_vote_position')
def record_vote_position():
  # FIXME: pass in from UI
  company_name = 'Code2College'
  job_title = 'FrontEndDeveloper'
  position_name = (company_name, job_title)

  profile_name = 'FrontEndHacker123'

  vote = False
  
  votes_by_position[position_name][profile_name] = vote

  # re-populate matching page

@app.route('/my_matches_seeker')
def my_matches_seeker():
  #
  username = 'FrontEndHacker123'

  # matches = find_profile_matches(profiles[username])
  matches = [ positions[('Code2College', 'FrontEndDeveloper')] ]
  return render_template('my_matches_seeker.html', username=username, matches=matches)

@app.route('/my_matches_position')
def my_matches_position():
  #
  company = 'Code2College'
  title = 'FrontEndDeveloper'

  # matches = find_profile_matches(profiles[username])
  matches = [ profiles['FrontEndHacker123'] ]
  return render_template('my_matches_seeker.html', company=company, title=title, matches=matches)

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
    'title': 'FrontEndDeveloper',
    'company': 'Code2College',
    'description': 'Code2College is looking for a frontend developer to help build a new website.',
    'skills': ['javascript', 'react']
  })

if __name__ == '__main__':
  init_data()
  # print(positions)
  # print(profiles)

  # tests
  #print(find_best_profile(positions[('Code2College', 'FrontEndDeveloper')]))

  app.run(host='0.0.0.0', port=8080)
