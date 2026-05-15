import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')


def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)


@app.route('/parking')
def parking():
    return render_template('parking.html')


@app.route('/api/update/<int:idx>', methods=['POST'])
def update(idx):
    body = request.get_json()
    data = load_data()

    if idx < 0 or idx >= len(data['visits']):
        return jsonify({'error': '잘못된 인덱스'}), 400

    visit = data['visits'][idx]
    for field in ('arrive', 'consult', 'depart', 'remark'):
        if field in body:
            visit[field] = body[field]

    save_data(data)
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(debug=True)
