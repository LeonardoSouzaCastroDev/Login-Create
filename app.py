from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
ARQUIVO = 'usuarios.txt'

def carregar_usuarios():
  if not os.path.exists(ARQUIVO):
    return{}
  with open(ARQUIVO, 'r') as f:
    return{linha.split(":")[0]: linha.strip().split(":")[1] for linha in f}

def salvar_usuario(usuario, senha):
  with open(ARQUIVO, 'a') as f:
    f.write(f"{usuario}:{senha}\n")

@app.route('/')
def home():
  return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
  usuarios = carregar_usuarios()
  usuario = request.form['usuario']
  senha = request.form['senha']
  if usuario in usuarios and usuarios[usuario] == senha:
    return render_template('sucesso.html', nome=usuario)
  else:
    return render_template('incorreto.html')

@app.route('/cadastro')
def cadastro():
  return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
  usuarios = carregar_usuarios()
  usuario = request.form['usuario']
  senha = request.form['senha']
  if usuario in usuarios:
    return "Usuário já existe. <a href='/cadastro'> Tentar outro </a>"
  salvar_usuario(usuario, senha)
  return redirect(url_for('home'))

if __name__ == '__main__':
  app.run(debug=True)