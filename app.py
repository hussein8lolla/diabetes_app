from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'يجب تسجيل الدخول أولاً'
login_manager.login_message_category = 'warning'

# ✅ إضافة CSRF Protection العام
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ تهيئة الإضافات
    csrf.init_app(app)          # ← السطر المهم
    db.init_app(app)
    login_manager.init_app(app)

    # تسجيل الـ Blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.readings import readings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(readings_bp)

    @app.route('/')
    def index():
        return redirect(url_for('main.dashboard'))

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)