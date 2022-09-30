from cmath import phase
from certifi import contents
from flask import Flask, render_template, request, escape
from vsearch import search4letters
from DBcm import UseDataBase 


app = Flask(__name__)

#adicionando o dicionário de caracteŕisticas da conexão à configuração do aplicativo web
app.config['dbconfig'] = { 'host': '127.0.0.1',
                           'user': 'vsearch',
                           'password': 'Nikolas@271190',
                           'database': 'vsearchlogDB',
                         }

def log_request(req: 'flask_request', res: str) -> None:
    """Log details of the web request and the results"""
    
    '''
    #definindo as características de conexão
    dbconfig = { 'host': '127.0.0.1',
                 'user': 'vsearch',
                 'password': 'Nikolas@271190',
                 'database': 'vsearchlogDB',
                }
    #abaico, importamos o driver, estabelecemos uma conxão e criamos um cursos

    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    #criamos agor auma string contendo a consulta que vc deseja usa
    _SQL = """insert into log
              (phrase, letters, ip, browser_string, results)
              values
              (%s, %s, %s, %s, %s)"""

    #executando a consulta
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res,  
                          ))
    
    #fechando a conexão
    conn.commit()
    cursor.close()
    conn.close()
    
    #with open('vsearch.log', 'a') as log:
        #print(req.form, req.remote_addr, req.user_agent, res, file = log, sep='|')
        #print(req.form, file = log)
        #print(req.remote_addr, file = log)
        #print(req.user_agent, file = log)
        #print(res, file = log)
        #print(str(dir(req)), res, file = log)
'''

    with UseDataBase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
              (phrase, letters, ip, browser_string, results)
              values
              (%s, %s, %s, %s, %s)"""

        cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res,  
                          ))


@app.route('/search4', methods =["POST"])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results: '
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    #return str(search4letters(phrase, letters))
    return render_template('results.html',
                            the_phrase=phrase,
                            the_letters=letters,
                            the_title=title,
                            the_results=results,
                            )

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    with UseDataBase(app.config['dbconfig']) as cursor:
        _SQL = """select phrase, letters, ip, browser_string, results from log"""

        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')

    return render_template('viewlog.html',
                            the_title = ' View Log',
                            the_row_titles = titles,
                            the_data=contents,)
    #return escape(''.join(contents))

if __name__ == '__main__':
    app.run(debug=True)
    