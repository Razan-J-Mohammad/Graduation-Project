from pythonic import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from math import floor

from pythonic import db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.image_file}', '{self.user_type}', '{self.super_id}', '{self.student_id}')"

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Super(db.Model):
    __tablename__ = 'super'
    super_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class Appointment(db.Model):
    Appointment_id = db.Column(db.Integer, primary_key=True)
    super_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    user = db.relationship('User', backref=db.backref('appointments', lazy=True))

    def __repr__(self):
        return f"Appointment('{self.date}', '{self.time}', '{self.description}')"

    
    
class QuranSurvey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    memorization_level = db.Column(db.String(50))
    tajweed_level = db.Column(db.String(50))
    quran_listening_habits = db.Column(db.String(50))
    free_time_hours = db.Column(db.String(50))
    super_id = db.Column(db.Integer, db.ForeignKey('super.super_id'))  # Define foreign key here
    
    # Define relationship to Super table
    super = db.relationship('Super', backref='quran_surveys')

    
class StudentSurvey(db.Model):
    __tablename__ = 'student_survey'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))  
    question_1 = db.Column(db.String(100), nullable=False)
    question_2 = db.Column(db.String(100), nullable=False)
    question_3 = db.Column(db.String(100), nullable=False)
    question_4 = db.Column(db.String(100), nullable=False)
    question_5 = db.Column(db.String(100), nullable=False)
    question_6 = db.Column(db.String(100), nullable=False)

    def __repr__(self):
     
       return f"StudentSurvey('{self.question_1}', '{self.question_2}', '{self.question_3}', '{self.question_4}', '{self.question_5}', '{self.question_6}')"
    


    
class Link(db.Model):
    link_id = db.Column(db.Integer, primary_key=True)
    super_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    user = db.relationship('User', backref=db.backref('links', lazy=True))

    def __repr__(self):
        return f"Link('{self.link}')"
    
class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    super_id = db.Column(db.Integer, db.ForeignKey('super.super_id'), nullable=False)  
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)  
    student_name = db.Column(db.String(100), nullable=False)
    surah_name = db.Column(db.String(100), nullable=False)
    start_verse = db.Column(db.String(10), nullable=False)
    end_verse = db.Column(db.String(10), nullable=False)
    part_number = db.Column(db.String(10), nullable=False)
    recitation_mark = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return f"Report('{self.student_name}','{self.student_id}','{self.super_id}', '{self.student_id}','{self.surah_name}', '{self.start_verse}', '{self.end_verse}', '{self.part_number}')"    
    

class ExamReport(db.Model):
    ExamReport_id = db.Column(db.Integer, primary_key=True)
    super_id = db.Column(db.Integer, db.ForeignKey('super.super_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)   
    student_name = db.Column(db.String(100), nullable=False)
    part_number = db.Column(db.String(10), nullable=False)
    number_of_topics = db.Column(db.Integer, nullable=False)
    exam_mark = db.Column(db.Integer, nullable=False)
    pass_or_fail = db.Column(db.String(10), nullable=False)
    level_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ExamReport(super_id={self.super_id}, student_name={self.student_name}, number_of_topics={self.number_of_topics}, part_number={self.part_number}, exam_mark={self.exam_mark}, pass_or_fail={self.pass_or_fail}, level_number={self.level_number})"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.Appointment_id'), nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f"Booking(user_id={self.user_id}, user_name='{self.user_name}', user_email='{self.user_email}', appointment_id={self.appointment_id}, appointment_time='{self.appointment_time}')"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    surah_name = db.Column(db.String(50), nullable=False)
    start_verse = db.Column(db.Integer, nullable=False)
    end_verse = db.Column(db.Integer, nullable=False)
    part_number = db.Column(db.Integer, nullable=False)
    recitation_mark = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"History(student_id={self.student_id}, surah_name='{self.surah_name}', " \
               f"start_verse={self.start_verse}, end_verse={self.end_verse}, " \
               f"part_number={self.part_number}, recitation_mark={self.recitation_mark})"


class HistoryExam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    part_number= db.Column(db.String(50), nullable=False)
    number_of_topics = db.Column(db.Integer, nullable=False)
    exam_mark = db.Column(db.Integer, nullable=False)
    level_number = db.Column(db.Integer, nullable=False)
    pass_part=db.Column(db.String(50), nullable=False)
    def __repr__(self):
         return f"HistoryExam(student_id={self.student_id}, part_number={self.part_number}, number_of_topics={self.number_of_topics}, exam_mark={self.exam_mark}, level_number={self.level_number}, pass_part={self.pass_part})"


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    id_supervisor = db.Column(db.Integer, db.ForeignKey('super.super_id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
   