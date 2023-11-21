from model import magic
from flask import Flask, render_template,request, Response
import sqlite3
import json
import threading
from constants import CURRENT_YEAR, DATABASE_PATH
import datetime

app = Flask(__name__)
database_path = DATABASE_PATH


@app.route('/')
def homepage():
   return render_template("test.html",content="This is gruop 19 Post")


@app.route('/refresh')
def start_new_prediction():
    t = threading.Thread(target=magic)
    t.daemon = True
    t.start()

    response = Response(json.dumps("Process started."))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

import pandas as pd

@app.route('/rankings')
def rankings():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()    
    cur.execute('SELECT * FROM prediction_rankings')
    rankings_raw = cur.fetchall()
    columns = [x[0] for x in cur.description]
    rankings = []
    for ranking in rankings_raw:
        ranking_on_date = {}
        for column, data in zip(columns[1:], ranking[1:]):
            ranking_on_date[column] = data
        rankings.append(ranking_on_date)

    # Chuyển đổi dữ liệu thành DataFrame
    df = pd.DataFrame(rankings)

    # Tạo bảng HTML Bootstrap
    table_html = df.to_html(index=False, classes='table table-striped table-bordered')

    # Tạo response
    response = Response(table_html)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



@app.route('/summary')
def summary():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()    
    cur.execute('SELECT * FROM summary')
    summary = cur.fetchall()[0]
    columns = [x[0] for x in cur.description]
    summary_dict = {}
    for column, data in zip(columns, summary):
        summary_dict[column] = data
    
    response = Response(json.dumps(summary_dict))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

import pandas as pd
from flask import Flask, Response

import urllib.parse
from flask import Flask, render_template, request







@app.route('/predictions', methods=['GET', 'POST'])
def predictions():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    # Thêm mã HTML cho trang chủ
    home_button = '<a class="btn btn-primary" href="/">Trang chủ</a>'

    # Xử lý yêu cầu lọc
    if request.method == 'POST':
        home_team = request.form['home_team']
        away_team = request.form['away_team']
        query_parts = []
        if home_team:
            query_parts.append(f"HomeTeam = '{home_team}'")
        if away_team:
            query_parts.append(f"AwayTeam = '{away_team}'")
        if query_parts:
            query = f"SELECT * FROM prediction_results WHERE {' AND '.join(query_parts)}"
        else:
            query = 'SELECT * FROM prediction_results'
    else:
        query = 'SELECT * FROM prediction_results'

    cur.execute(query)
    predictions_raw = cur.fetchall()
    columns = [x[0] for x in cur.description]
    predictions = []
    for prediction in predictions_raw:
        prediction_match = {}
        for column, data in zip(columns[1:], prediction[1:]):
            if column == 'Date':
                column = 'Ngày'
            elif column == 'HomeTeam':
                column = 'Đội nhà (H)'
            elif column == 'AwayTeam':
                column = 'Đội khách (A)'
            elif column == 'FTR':
                column = 'Kết quả'
            elif column == 'prob_A':
                column = 'Tỉ lệ thắng đội khách'
            elif column == 'prob_D':
                column = 'Tỉ lệ hòa'
            elif column == 'prob_H':
                column = 'Tỉ lệ thắng đội nhà'
            prediction_match[column] = data
        predictions.append(prediction_match)

    df = pd.DataFrame(predictions)

    # Thêm cột số thứ tự
    df.insert(0, 'STT', range(1, len(df) + 1))

    # Lấy danh sách tên đội để tạo datalist
    home_teams = sorted(df['Đội nhà (H)'].unique())
    away_teams = sorted(df['Đội khách (A)'].unique())

    # Chuyển đổi DataFrame thành HTML table với lớp CSS 'table' của Bootstrap
    table_html = df.to_html(index=False, classes='table table-striped table-bordered')

    # Thay thế các ký tự có dấu thành mã UTF-8 để tránh lỗi tiếng Việt
    table_html = urllib.parse.unquote(table_html)

    # Thêm mã CSS của Bootstrap và tùy chỉnh vào phản hồi
    response = Response(
        f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                th {{
                    text-align: left;
                    vertical-align: middle;
                    padding-left: 100px;
                }}
                td {{
                    text-align: left;
                    vertical-align: middle;
                    padding-left: 10px;
                }}
                .container {{
                    margin-top: 30px;
                }}
                .form-group {{
                    margin-bottom: 6px;
                }}
                .form-group input[type='submit'] {{
                    margin-top: 6px;
                }}
                .form-group select {{
                    width: 300px;
                }}
                .datalist-container {{
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    margin-bottom: 6px;
                }}
                .datalist-container input {{
                    width: 300px;
                    margin-right: 10px;
                }}
                .datalist-container datalist {{
                    width: 300px;
                }}
            </style>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h2>Dự đoán</h2>
                {home_button}  <!-- Thêm nút Trang chủ -->
                <br><br>
                <form method="post" action="/predictions">
                    <div class="form-group">
                        <label for="home_team">Đội nhà:</label>
                        <div class="datalist-container">
                            <input list="home_teams" class="form-control" id="home_team" name="home_team" placeholder="Nhập tên đội nhà">
                            <datalist id="home_teams">
                                {" ".join(f"<option value='{team}'></option>" for team in home_teams)}
                            </datalist>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="away_team">Đội khách:</label>
                        <div class="datalist-container">
                            <input list="away_teams" class="form-control" id="away_team" name="away_team" placeholder="Nhập tên đội khách">
                            <datalist id="away_teams">
                                {" ".join(f"<option value='{team}'></option>" for team in away_teams)}
                            </datalist>
                        </div>
                    </div>
                    <div class="form-group">
                        <button type="submit" class="btn btn-primary">Lọc</button>
                        <a href="/predictions" class="btn btn-primary">Trở lại</a>
                    </div>
                </form>
                <br>
                {table_html}
            </div>
        </body>
        </html>
        """
    )
    response.headers['Content-Type'] = 'text/html'
    return response




from flask import Flask, Response, jsonify

@app.route('/previous_results')
def previous_results():
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    
    season_start = datetime.datetime(CURRENT_YEAR, 7, 1).date().strftime('%Y-%m-%d')
    query = 'SELECT * FROM previous_results WHERE Date > "{}"'.format(season_start)
    req_params_raw = request.data
    if req_params_raw:
        req_params = json.loads(req_params_raw)
        query_type = 'AND' if 'against' in req_params else 'OR'
        teams = ["'" + team + "'" for team in req_params['teams']]
        teams = ",".join(teams)
        query += ' AND (HomeTeam IN ({}) {} AwayTeam IN ({}))'.format(teams, query_type, teams)
        
    cur.execute(query)
    previous_results_raw = cur.fetchall()
    columns = [x[0] for x in cur.description]
    previous_results = []
    for result in previous_results_raw:
        match_result = {}
        for column, data in zip(columns[1:], result[1:]):
            match_result[column] = data
        previous_results.append(match_result)

    return jsonify(previous_results)

if __name__ == '__main__':
	app.run(debug=True)
