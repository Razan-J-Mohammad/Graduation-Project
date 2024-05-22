from tokenize import String
from wsgiref.validate import validator
from sqlalchemy import Column, String
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import  SelectField, StringField, PasswordField, SubmitField, BooleanField, RadioField,TextAreaField,IntegerField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
    URL,
)
from pythonic.model import User


class RegistrationForm(FlaskForm):
    fname = StringField(
        "الاسم الأول", validators=[DataRequired(), Length(min=2, max=25)]
    )
    lname = StringField("الاسم الثاني", validators=[DataRequired(), Length(min=2, max=25)])
    username = StringField(
        "اسم المستخدم", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("البريد الالكتروني", validators=[DataRequired(), Email()])
    password = PasswordField(
        "كلمة المرور",
        validators=[
            DataRequired(),
            Regexp(
                "^(?=.*[a-z])(?=.*\\d)(?=.*[@$!%*?&_])[A-Za-z\\d@$!%*?&_]{8,32}$"
            ),
        ],
    )
    confirm_password = PasswordField(
        "تأكيد كلمة المرور", validators=[DataRequired(), EqualTo("password")]
    )
    user_type = RadioField("نوع المستخدم", choices=[('طالب/ة', 'طالب/ة'), ('مشرف/ة', 'مشرف/ة')], validators=[DataRequired()])
    submit = SubmitField("تسجيل")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please chosse a different one"
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists! Please chosse a different one")

class AppointmentForm(FlaskForm):
    time = StringField('الوقت', validators=[DataRequired()])
    date = StringField('التاريخ', validators=[DataRequired()])
    description = StringField('ملاحظه', validators=[DataRequired()])
    user = SelectField('اسم المشرف', coerce=int, validators=[DataRequired()])
    user_id = StringField('User ID')  # Add user_id field as a hidden field
    submit = SubmitField("حفظ")
   
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.user.choices = [(user.id, f'{user.fname} {user.lname}') for user in User.query.all()]




class LoginForm(FlaskForm):
    email = StringField("البريد الالكتروني", validators=[DataRequired(), Email()])
    password = PasswordField(
        "كلمة المرور",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("دخول")

class QuranSurveyForm(FlaskForm):
    memorization_level = RadioField("Memorization Level", choices=[('جزء واحد', 'جزء واحد'), ('اكثر من جزء', 'اكثر من جزء'), ('اقل من جزء', 'اقل من جزء')], validators=[DataRequired()])
    tajweed_level = RadioField("Tajweed Level", choices=[('ممتاز', 'ممتاز'), ('متوسط', 'متوسط'), ('ضعيف', 'ضعيف')], validators=[DataRequired()])
    quran_listening_habits = RadioField("Quran Listening Habits", choices=[('ساعه يوميا', 'ساعه يوميا'), ('اكثر من ساعه', 'اكثر من ساعه'), ('اقل من ساعه', 'اقل من ساعه')], validators=[DataRequired()])
    free_time_hours = RadioField("Free Time Hours", choices=[('ساعه', 'ساعه'), ('ساعتان', 'ساعتان'), ('اقل من ذلك', 'اقل من ذلك')], validators=[DataRequired()])
    submit = SubmitField("حفظ")

class StudentSurveyForm(FlaskForm):
    question_1 = RadioField("كم تحفظ من القرآن الكريم؟", choices=[
        ('one_part', 'جزء واحد'),
        ('more_than', 'اكثر من ذلك'),
        ('less_than', 'اقل من ذلك')
    ], validators=[DataRequired()])
    
    question_2 = RadioField("مستوى التجويد لديك؟", choices=[
        ('weak', 'ضعيف'),
        ('average', 'متوسط'),
        ('excellent', 'ممتاز')
    ], validators=[DataRequired()])
    
    question_3 = RadioField("هل حصلت على شهادة تجويد؟", choices=[
        ('yes', 'نعم'),
        ('no', 'لاء')
    ], validators=[DataRequired()])
    
    question_4 = RadioField("كم تحتاج لحفظ صفحة من القرآن ", choices=[
        ('15_minutes', '15 دقيقة'),
        ('30_minutes', '30 دقيقة'),
        ('60_minutes', '60 دقيقة')
    ], validators=[DataRequired()])
    
    question_5 = RadioField("كم من الوقت تخصص للحفظ ", choices=[
        ('one_hour', 'ساعة'),
        ('two_hours', 'ساعتان'),
        ('more_than_two_hours', 'أكثر من ذلك')
    ], validators=[DataRequired()])
    
    question_6 = RadioField("من أي مكان تفضل الحفظ؟", choices=[
        ('from_beginning', 'من البدايه (البقرة)'),
        ('from_end', 'من النهايه(جزء عم)'),
        ('from_quarter', 'من ربع يس')
    ], validators=[DataRequired()])
    
    submit = SubmitField("حفظ")


from urllib.parse import urlparse

def validate_url(form, field):
    url = field.data
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValidationError('Invalid URL.')

class AddLinkForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), validate_url])
    submit = SubmitField('Submit')


class ReportForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired(), Length(max=100)])
    surah_name = StringField('Surah Name', validators=[DataRequired(), Length(max=100)])
    start_verse = StringField('Start Verse', validators=[DataRequired(), Length(max=10)])
    end_verse = StringField('End Verse', validators=[DataRequired(), Length(max=10)])
    part_number = StringField('Part Number', validators=[DataRequired(), Length(max=10)])
    recitation_mark = TextAreaField('Recitation Mark', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class ExamReportForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired(), Length(max=100)])
    number_of_topics = IntegerField('Number of Topics', validators=[DataRequired()])
    part_number = StringField('Part Number', validators=[DataRequired(), Length(max=10)])
    exam_mark = IntegerField('Exam Mark', validators=[DataRequired()])
    pass_or_fail = SelectField('Pass or Fail', choices=[('pass', 'Pass'), ('fail', 'Fail')], validators=[DataRequired()])
    level_number = SelectField('Level Number', choices=[(str(i), str(i)) for i in range(1, 7)], validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateProfileForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio")
    picture = FileField(
        "تحديث الصورة الشخصية", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "اسم المستخدم موجود بالفعل! الرجاء اختيار واحد مختلف"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "البريد الإلكتروني موجود بالفعل! الرجاء اختيار واحد مختلف"
                )

class UpdateProfileForm(FlaskForm):
    username = StringField(
        "اسم المستخدم", validators=[DataRequired(), Length(min=2, max=25)]
    )
    email = StringField("البريد الالكتروني", validators=[DataRequired(), Email()])
    picture = FileField(
        "تحديث الصورة الشخصية", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "اسم المستخدم موجود بالفعل! الرجاء اختيار واحد مختلف"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "البريد الإلكتروني موجود بالفعل! الرجاء اختيار واحد مختلف"
                )

class HistoryForm(FlaskForm):
    surah_name = StringField('اسم السورة', validators=[DataRequired()])
    start_verse = IntegerField('من آية رقم', validators=[DataRequired()])
    end_verse = IntegerField('إلى آية رقم', validators=[DataRequired()])
    part_number = IntegerField('رقم الجزء', validators=[DataRequired()])
    recitation_mark = IntegerField('علامة التسميع', validators=[DataRequired()])


class HistoryExamForm(FlaskForm):
    part_number = IntegerField('رقم الجزء', validators=[DataRequired()])
    number_of_topics = IntegerField('عدد المواضع', validators=[DataRequired()])
    exam_mark = IntegerField('علامة الامتحان', validators=[DataRequired()])
    level_number = IntegerField('رقم المستوى', validators=[DataRequired()])
    pass_part = StringField('ناجح/راسب', validators=[DataRequired()])
    