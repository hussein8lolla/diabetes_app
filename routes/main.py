from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Reading
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    readings = (Reading.query
                .filter_by(user_id=current_user.id)
                .filter(Reading.date >= thirty_days_ago)
                .order_by(Reading.date.desc(), Reading.time.desc())
                .all())

    values = [r.value for r in readings]
    total = len(values)
    avg = round(sum(values) / total, 1) if total > 0 else 0
    low_count = sum(1 for v in values if v < 80)
    high_count = sum(1 for v in values if v > 180)
    normal_count = total - low_count - high_count

    return render_template('dashboard.html',
                           readings=readings, total=total, avg=avg,
                           low_count=low_count, normal_count=normal_count, high_count=high_count)