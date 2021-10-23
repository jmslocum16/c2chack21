from flask import Flask
app = Flask(__name__)

counter = 0

@app.route('/')
def hello_world():
  global counter 

  counter += 1
  print(counter)
  return '''
    
    <h1>Test</hi>
    <h1>
    <b> Counter: 
    <hr>
    
    ''' + str(counter)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
