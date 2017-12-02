from back import run
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():

    states = ['AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]

    if request.method == 'POST':
        state = str(request.form.get('state_dropdown'))
        num_districts = int(str(request.form.get('number_dropdown')))
        print('State: ' + state)
        print('Num_districts: ' + str(num_districts))
        run(state, num_districts)

    return render_template('template.html', states=states, numbers=numbers)

@app.route('/generate/')
def my_link():

    return 'Done'

if __name__ == '__main__':
  app.run(debug=True)