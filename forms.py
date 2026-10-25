from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    IntegerField, FloatField, SelectField, TextAreaField, DateField, TimeField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, NumberRange, Optional
)


class RegisterForm(FlaskForm):
    username = StringField('اسم المستخدم',
        validators=[DataRequired(message='هذا الحقل مطلوب'), Length(min=3, max=64)])
    email = StringField('البريد الإلكتروني',
        validators=[DataRequired(), Email(message='بريد إلكتروني غير صالح')])
    password = PasswordField('كلمة المرور',
        validators=[DataRequired(), Length(min=6, message='6 أحرف على الأقل')])
    confirm_password = PasswordField('تأكيد كلمة المرور',
        validators=[DataRequired(), EqualTo('password', message='كلمتا المرور غير متطابقتين')])
    submit = SubmitField('إنشاء الحساب')


class LoginForm(FlaskForm):
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    remember = BooleanField('تذكرني')
    submit = SubmitField('دخول')


class ReadingForm(FlaskForm):
    date = DateField('التاريخ', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('الوقت', validators=[DataRequired()], format='%H:%M')
    value = IntegerField('قراءة السكر',
        validators=[DataRequired(), NumberRange(min=20, max=600, message='القيمة بين 20 و 600')])
    measurement_time = SelectField('وقت القياس', choices=[
        ('Morning', 'الصبح'),
        ('Noon', 'نص اليوم'),
        ('Afternoon', 'بعد الظهر'),
        ('Evening', 'بالليل'),
        ('Night', 'بليل'),
        ('Before Breakfast', 'قبل الفطار'),
        ('After Breakfast (2h)', 'بعد الفطار بساعتين'),
        ('Before Lunch', 'قبل الغداء'),
        ('After Lunch (2h)', 'بعد الغداء بساعتين'),
        ('Before Dinner', 'قبل العشاء'),
        ('After Dinner (2h)', 'بعد العشاء بساعتين'),
        ('Before Exercise', 'قبل التمرين'),
        ('After Exercise', 'بعد التمرين'),
        ('Before Sleep', 'قبل النوم'),
    ])
    medication_name = StringField('اسم الدواء', validators=[Optional(), Length(max=100)])
    medication_dose = FloatField('الجرعة', validators=[Optional(), NumberRange(min=0, max=200)])
    carbs = IntegerField('الكربوهيدرات (بالجرام)', validators=[Optional(), NumberRange(min=0, max=500)]) # ✅ تمت الإضافة
    note = TextAreaField('ملاحظات', validators=[Optional(), Length(max=500)])
    submit = SubmitField('حفظ القياس')