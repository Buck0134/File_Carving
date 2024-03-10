from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='../client/templates')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def data():
    return jsonify({'message': 'Hello from the server'})

if __name__ == '__main__':
    app.run(debug=True)
