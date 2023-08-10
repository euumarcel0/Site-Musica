from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Chave secreta para uso das sessões

# Configurações do banco de dados SQL Server
server = 'DESKTOP-23G0ANQ'
database = 'app'
username = 'sa'
password = '26012006'

# Função para estabelecer conexão com o banco de dados
def create_connection():
    return pyodbc.connect(f'SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Rota da página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica as credenciais do usuário no banco de dados
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Configura a sessão para o usuário autenticado
            session['username'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', message='Usuário ou senha incorretos.')

    return render_template('index.html')

# Rota da página de cadastro
@app.route('/cadastre-se', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se o usuário já está cadastrado
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        if cursor.fetchone():
            return render_template('register.html', message='Usuário já cadastrado.')

        # Caso o usuário não esteja cadastrado, insere as informações no banco de dados
        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# Rota da página de dashboard após o login
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Rota para fazer logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Rota da página do menu
@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True)
