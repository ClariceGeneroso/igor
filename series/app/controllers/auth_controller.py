from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import UserModel
from app.middlewares import guest_only, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
@guest_only
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Retorna uma instância da classe UserModel (ou None)
        user = UserModel.get_by_username(username)

        # Usa o método de instância check_password e acede aos atributos como objeto (.id, .username)
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['user'] = user.username
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('main.index'))

        flash("Usuário ou senha incorretos.", "danger")

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
@guest_only
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash("Preencha todos os campos.", "warning")
            return render_template('register.html')

        # Verifica duplicidade
        if UserModel.get_by_username(username):
            flash("Nome de usuário já está em uso.", "danger")
            return render_template('register.html')

        # Cria a instância, gera o hash e guarda no banco
        novo_usuario = UserModel(username=username)
        novo_usuario.set_password(password)

        if novo_usuario.salvar():
            flash("Conta criada com sucesso! Faça login para continuar.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Erro ao cadastrar usuário.", "danger")

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Você saiu da conta.", "info")
    return redirect(url_for('auth.login'))