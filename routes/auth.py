from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from forms import RegisterForm, LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('البريد الإلكتروني مسجل بالفعل.', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=form.username.data).first():
            flash('اسم المستخدم موجود بالفعل.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower().strip()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('🎉 تم إنشاء حسابك بنجاح! سجل الدخول الآن.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'👋 مرحبًا بك، {user.username}!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        flash('❌ البريد الإلكتروني أو كلمة المرور غير صحيحة.', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('👋 تم تسجيل الخروج.', 'info')
    return redirect(url_for('auth.login'))