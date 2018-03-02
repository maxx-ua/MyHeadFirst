from flask import Flask, render_template, request, escape, session
from DBcm import UseDatabase
from vsearch import search4letters
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vs',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }

def log_request(req: 'flask_request', res:str) -> None:
    """Журналирует веб-запрос и возвращает результаты."""

    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = """insert into log
                (phrase, letters, ip, browser_string, results)
                values
                (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (req.form['phrase'],
                            req.form['letters'],
                            req.remote_addr,
                            req.user_agent.browser,
                            res, ))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase = phrase,
                           the_letters = letters,
                           the_results = results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    """Выводит содержимое файла журнала в виде HTML-таблицы"""
    with UseDatabase(app.config['dbconfig']) as log:
        sql = """select phrase, letters, ip, browser_string, results from log"""
        log.execute(sql)
        contents = log.fetchall()

    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')

    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,)

@app.route('/login')
def do_login() ->str:
    session['logged_in'] = True
    return 'You are logged in.'

@app.route('/logout')
def do_logout() ->str:
    session.pop('logged_in')
    return 'You are now logged out.'

app.secret_key = 'YouWillNeverGuessMySecretKey'

if __name__ == '__main__':
    app.run(debug=True)