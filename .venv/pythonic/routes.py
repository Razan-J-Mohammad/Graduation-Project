import os
import secrets
import io
import base64
import matplotlib.pyplot as plt
from PIL import Image
from flask import  jsonify, render_template, url_for, flash, redirect,request
from pythonic.model import User,Appointment,QuranSurvey,StudentSurvey,Link,Report,ExamReport,Student, Super,Booking,History,HistoryExam,Feedback
from  pythonic.form import RegistrationForm,LoginForm,AppointmentForm,QuranSurveyForm,StudentSurveyForm,AddLinkForm,ReportForm,ExamReportForm,UpdateProfileForm,HistoryForm,HistoryExamForm
from pythonic import app,bcrypt,db
from sqlalchemy import desc
from datetime import datetime, timedelta
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
    
)
from pythonic.decorators import permission_required

من_نحن= [
     {
        "title": "مشروع زلفى لحفظ القرآن الكريم",
         "icon": "about.jpg",
        "description": " هو مبادرة تهدف إلى توفير مساحة تعليمية عبر الإنترنت "
                  " للمساعدة في حفظ القرآن الكريم. يُعتبر هذا المشروع مبادرة طلابي"
                   "قامت بها طالبتان بجامعة النجاح الوطنية، بهدف تقديم دعم ومساعدة لأولئك الذين يسعون لحفظ كتاب الله الكريم."
                  " من خلال موقع زلفى، يتم توفير خطه للطلاب بناءً على مستوى كل فرد، مما يمكنهم من تحقيق أقصى"
                    "استفادة من جهودهم في تحفيظ القرآن. يسعى المشروع إلى تقديم تجربة تعليمية شاملة ومبتكرة تسهل عملية حفظ القرآن"
                   "وتحفيز الطلاب على التفوق في هذا النوع الفريد من التعلم الديني. بفضل هذه المبادرة الطموحة،"
                   " يتيح مشروع زلفى فرصة قيمة للأفراد للتقرب من كتاب الله الكريم وتحقيق أهدافهم الدينية بسهولة ويسر"
                    "سيوفر هذا التطبيق فرصة كبيرة لأولئك الذين يسعون لحفظ القرآن الكريم، حيث سيكون هناك مشرفون"
                    "مؤهلون يقومون بتقديم التسميع للطلاب بعد الانتهاء من عملية الحفظ. بالإضافة إلى ذلك، سيتضمن التطبيق"
                    "نظامًا لوضع علامات وإجراء امتحانات على أجزاء مختلفة من القرآن الكريم،"
                    "مما سيساعد الطلاب على قياس تقدمهم وتحفيزهم لتحقيق أهدافهم الدينية."
                    "وعلم أن الجنة حُفت بالمكاره وأن النار حُفت بالشهوات،"
                   " وعلم أن طريق الحفظ طويل"
                     "وأن الوصول لمن صدق، ومن صدق العزم وجد السبيل"
    }
]

الخدمات = [
     {
        "name": "مُشرِفين لتَسميع",
        "thumbnail": "tt.jpg",
        "description": "  لدينا مشرفين متخصصين في تسميع الطلاب والقيام بجلسات تسميع مخصصة حسب الأيام والأوقات المحددة مسبقًاويقوم الطالب باختيار الموعد المناسب له لتسميع. حيث يتم رصد أداء الطلاب وتسجيل العلامات في نهاية كل جلسة تسميع لتقييم تقدمهم وتحديد المجالات التي تحتاج إلى تطوير إضافي وايضا القيام بتطوير الخطه  .",
    },
    {
        "name": "خُطَ للحفظ",
        "thumbnail": "pln.jpg",
        "description": "سيتم تصميم خطة مخصصة لكل طالب بناءً على مستواه الحالي والمعلومات التي يتم الحصول عليها من الطالب ، سيتم تطوير هذه الخطة بشكل مستمر بناءً على تقييمنا لمستوى التقدم والمعرفة لدى الطالب. سيتم مراجعة الخطة بانتظام لضمان أنها ملائمة وفعالة وتلبي احتياجات الطالب بشكل كامل.",       
    },
      {
        "name": "امتحانات",
        "thumbnail": "quiz.jpg",
        "description": "  يجب على الطالب الاختبار بكل جزء من القران الكريم بعد تسميعه عند المشرف المسؤول ,وايضا يجب اختبار بكل خمس اجزاء بعد الانتهاء من تسميعها , ويجب ان تكون الاجزاء ممتاليه وبعدها يتم الانتقال للمرحله الثانيه وهي الخمسه التاليه من القران وهكذا حتى يتم الاختباربكل الاجزاء وايضا الخمسات ويمكن لطالب الاختبار بالمصحف كامل "
    },
]

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/user_pics", picture_name)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name

def estimate_memorization_time(student_id):
    total_parts = 30
    history_exam_entries = HistoryExam.query.filter_by(student_id=student_id).all()
    completed_parts_count = sum(1 for entry in history_exam_entries if entry.pass_part == "ناجح")
    remaining_parts_count = total_parts - completed_parts_count
    pages_per_week = 4 * 2  
    total_pages = remaining_parts_count * 20  
    total_weeks = total_pages / pages_per_week
    years = total_weeks // 52
    remaining_weeks = total_weeks % 52
    months = (remaining_weeks * 4) // 12
    return years, months





@app.route("/")
@app.route("/home")
def home():
    user=current_user
    return render_template("home.html", lessons=من_نحن, courses=الخدمات,user=user)

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        user_id = current_user.id  # Assuming user ID is stored in the User model
        appointment_id = request.form['appointment_id']
        appointment_time = request.form['appointment_time']

        # Retrieve user's name and email from the current_user object
        user_name = current_user.fname  # Assuming name is a property of the User model
        user_email = current_user.email  # Assuming email is a property of the User model

        # Create a new booking entry
        booking = Booking(user_id=user_id, user_name=user_name, user_email=user_email, appointment_id=appointment_id, appointment_time=appointment_time)
        db.session.add(booking)
        db.session.commit()

        return jsonify({'message': 'Booking saved successfully'})
    else:
        # Handle GET requests to the /book_appointment route (optional)
        return jsonify({'error': 'Method not allowed'}), 405  # Method Not Allowed status code



@app.route("/register", methods=["GET", "POST"])
def register():
    students = Student.query.all()
    form = RegistrationForm()
    all_students = Student.query.all()  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            user_type=form.user_type.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f"تم إنشاء الحساب بنجاح ل {form.username.data}", "success")
        
        if form.user_type.data == 'طالب/ة':
            student = Student(
                username=user.username,
                user_type=user.user_type,
                user_id=user.id  
            )
            db.session.add(student)
            db.session.commit()
            return redirect(url_for("student"))
        
        elif form.user_type.data == 'مشرف/ة':
            super_user = Super(
                username=user.username,
                user_type=user.user_type,
                user_id=user.id  
            )
            db.session.add(super_user)
            db.session.commit()
            return redirect(url_for("super"))
          
    return render_template("registar.html", title="Register", form=form, students=students)

   


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("لقد تم تسجيل الدخول!", "success")
            if user.user_type == 'طالب/ة':  
                return redirect(url_for("student"))  
            elif user.user_type == 'مشرف/ة':  
                return redirect(url_for("sidebar2"))
        else:
            flash("تسجيل الدخول غير ناجح. يرجى التحقق من بيانات الاعتماد", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/plan")
@login_required
def plan():
    student_id = current_user.id 

    student_survey = StudentSurvey.query.filter_by(student_id=student_id).first()

    if student_survey:
        print("Student Survey found:", student_survey)

        starting_surah = student_survey.question_6  

        starting_verse = 1 
        if student_survey.question_5 == 'two_hours':
            starting_verse = 6 
        elif student_survey.question_5 == 'more_than_two_hours':
            starting_verse = 11  

        monthly_plan = []
        for day in range(1, 32):  
            daily_plan = {
                "date": f"Day {day}",
                "surah": starting_surah,
                "start_verse": starting_verse,
                "end_verse": starting_verse + 5  
            }
            monthly_plan.append(daily_plan)

        return render_template("plan.html", title="Memorization Plan", monthly_plan=monthly_plan)
    else:  
        return render_template("plan.html", title="plan")



@app.route('/appointment', methods=['GET'])
@login_required
def appointment():
    form = AppointmentForm()
    return render_template('appointment.html',form=form, user=current_user)



@app.route('/appointment', methods=['POST'])
@login_required
def post_appointment():
    user = current_user 
    form = AppointmentForm()
    form.user.choices = [(user.id, user.fname) for user in User.query.all()]
    print(form.user.data)
    if form.validate_on_submit():
        print(form.description.data,form.time.data,form.date.data,form.user.data)

    appointment = Appointment(
        super_id=user.id,
        time=form.time.data,
        date=form.date.data,
        description=form.description.data,
        
    )
    db.session.add(appointment)
    db.session.commit()
    flash('تمت جدولة الموعد بنجاح!', 'success') 
    return render_template('appointment.html',form=form, user=user)




@app.route("/DisplayAppointment")
def DisplayAppointment():
    user=current_user
    appointments = Appointment.query.all()
    users = User.query.all()
    return render_template("DisplayAppointment.html", appointments=appointments,user=user,users=users)




@app.route('/super', methods=['GET'])
@login_required
def super_2():
    form = QuranSurveyForm()
    return render_template('super.html',form=form, user=current_user)


@app.route('/super', methods=['POST'])
def super():
    form = QuranSurveyForm()  
    user = current_user 
    if form.validate_on_submit():
        # Assuming each user has only one Super instance
        super_instance = Super.query.filter_by(user_id=user.id).first()

        if super_instance:
            new_survey = QuranSurvey(
                super_id=super_instance.super_id,
                memorization_level=form.memorization_level.data,
                tajweed_level=form.tajweed_level.data,
                quran_listening_habits=form.quran_listening_habits.data,
                free_time_hours=form.free_time_hours.data
            )
        
            db.session.add(new_survey)
            db.session.commit()
        
        if form.memorization_level.data == 'اكثر من جزء' and \
          form.tajweed_level.data == 'ممتاز' and \
          form.quran_listening_habits.data == 'اكثر من ساعه' and \
          form.free_time_hours.data == 'ساعتان':
          flash('تم إرسال الاستطلاع بنجاح!', 'success')
          return redirect(url_for('profile_super'))
        else:
          return redirect(url_for('super2'))


    flash('فشل التحقق من صحة النموذج. يرجى التحقق من المدخلات الخاصة بك.', 'error')
    return redirect(url_for('home'),form=form,user=user)


@app.route('/Recite', methods=['GET'])
@login_required
def Recite():
    form = AddLinkForm()
    user = current_user
    return render_template('Recite.html',form=form,user=user)

@app.route("/Recite", methods=['POST'])
@login_required
def recite():
    form = AddLinkForm(request.form)
    if form.validate():
        url = form.url.data
        link = Link(super_id=current_user.id, link=url)
        db.session.add(link)
        db.session.commit()
        flash(' تم الإرسال بنجاح!', 'success')
        return redirect(url_for('Recite'))
    else:
        flash('URL غير صالح.', 'error')
        return redirect(url_for('Recite'))


@app.route("/profile_super",methods=["GET", "POST"])
@login_required
def profile_super():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        db.session.commit()
        flash("تم تحديث ملفك الشخصي", "success")
        return redirect(url_for("profile_super"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template(
        "profile_super.html",
        title="profile_super",
        profile_form=profile_form,
        image_file=image_file,
    )

@app.route("/profile_student",methods=["GET", "POST"])
@login_required
def profile_student():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        db.session.commit()
        flash("تم تحديث ملفك الشخصي", "success")
        return redirect(url_for("profile_student"))
    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
    image_file = url_for("static", filename=f"user_pics/{current_user.image_file}")
    return render_template(
        "profile_super.html",
        title="profile_student",
        profile_form=profile_form,
        image_file=image_file,
    )
 
from flask_login import current_user

@app.route('/student', methods=['GET', 'POST'])
def student():
    form = StudentSurveyForm()

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Check if the user is authenticated
        if current_user.is_authenticated:
            student = Student.query.filter_by(user_id=current_user.id).first()
            if student:
                # Create a new survey record
                new_survey = StudentSurvey(
                    student_id=student.student_id,  # Using student_id as primary key
                    question_1=form.question_1.data,
                    question_2=form.question_2.data,
                    question_3=form.question_3.data,
                    question_4=form.question_4.data,
                    question_5=form.question_5.data,
                    question_6=form.question_6.data
                )
                try:
                    # Add the new survey to the database
                    db.session.add(new_survey)
                    db.session.commit()
                    flash('تم إرسال الاستطلاع بنجاح!', 'success')
                    return redirect(url_for('sidebar'))
                except Exception as e:
                    flash(f'An error occurred: {str(e)}', 'error')
            else:
                flash('لم يتم العثور على الطالب!', 'error')
        else:
            # User is not authenticated, you can handle this case according to your requirements
            flash('يجب تسجيل الدخول قبل ملء الاستبيان!', 'warning')
            # Optionally, redirect the user to the login page or display the form as read-only
            return redirect(url_for('login'))  # Redirect to the login page
        
    return render_template('student.html', form=form)




@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    user=current_user
    return render_template("dashboard.html", title="Dashboard",user=user)

@app.route("/report", methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm()
    user = current_user
    student_names = [student.username for student in Student.query.all()]
    form.student_name.choices = [(name, name) for name in student_names]

    if form.validate_on_submit():
        student_username = form.student_name.data  
        student = Student.query.filter_by(username=student_username).first()
        if student:
            super_entry = Super.query.filter_by(user_id=user.id).first()

            if super_entry is not None:
                report = Report(
                    student_name=student_username,  
                    surah_name=form.surah_name.data,
                    start_verse=form.start_verse.data,
                    end_verse=form.end_verse.data,
                    part_number=form.part_number.data,
                    recitation_mark=form.recitation_mark.data,
                    super_id=super_entry.super_id,
                    student_id=student.student_id
                )
                db.session.add(report)
                db.session.commit()

                history_entry = History(
                   student_id=student.student_id,
                   surah_name=report.surah_name,
                   start_verse=report.start_verse,
                   end_verse=report.end_verse,
                   part_number=report.part_number,
                   recitation_mark=report.recitation_mark
                )
                db.session.add(history_entry)
                db.session.commit()

                flash('تم إرسال التقرير بنجاح!', 'success')
                return redirect(url_for('report'))
            else:
                flash('Error: Super entry not found.', 'error')
        else:
            flash('Error: Student entry not found.', 'error')

    return render_template("report.html", title="Report", form=form, user=user)




from flask import request

from flask import request

@app.route('/Exam_report', methods=['GET', 'POST'])
@login_required
def Exam_report():
    user = current_user
    form = ExamReportForm()
    if form.validate_on_submit():
        student_username = form.student_name.data
        student = Student.query.filter_by(username=student_username).first()

        if student:
            super_entry = Super.query.filter_by(user_id=user.id).first()

            if super_entry:
                exam_report = ExamReport(
                    super_id=super_entry.super_id,
                    student_id=student.student_id,
                    student_name=student_username,
                    number_of_topics=form.number_of_topics.data,
                    part_number=form.part_number.data,
                    exam_mark=form.exam_mark.data,
                    pass_or_fail=form.pass_or_fail.data,
                    level_number=form.level_number.data
                )
                db.session.add(exam_report)
                db.session.commit()

                history_exam = HistoryExam(
                    student_id=student.student_id,
                    part_number=form.part_number.data,
                    number_of_topics=form.number_of_topics.data,
                    exam_mark=form.exam_mark.data,
                    level_number=form.level_number.data,
                    pass_part=form.pass_or_fail.data 
                )

                db.session.add(history_exam)
                db.session.commit()

                flash('تم إرسال تقرير الامتحان بنجاح!', 'success')
                return redirect(url_for('Exam_report'))
            else:
                flash('Error: Super entry not found.', 'error')
        else:
            flash('Error: Student entry not found.', 'error')

    return render_template('Exam_report.html', title='Exam_report', form=form, user=user)




@app.route("/rule")
@login_required
def rule():
    user = current_user 
    return render_template("rule.html", title="rule", user=user)


@app.route('/super2')
def super2():
    return render_template('super2.html')

def calculate_overall_performance(student_id):
    exam_reports = ExamReport.query.filter_by(student_id=student_id).all()

    if exam_reports:
        total_exam_mark = sum(report.exam_mark for report in exam_reports)
        num_exam_parts = len(set(report.part_number for report in exam_reports))  # Counting distinct exam parts

        if num_exam_parts > 0:
            average_exam_mark = total_exam_mark / num_exam_parts  # Adjusted for the number of exam parts
            return average_exam_mark
        else:
            return None  # Return None if the student hasn't taken any exam parts
    else:
        return None  # Return None if there are no exam reports for the student


@app.route('/sidebar2', methods=['GET'])
@login_required
def sidebar2():
    feedback_data = db.session.query(Feedback, Student, Super).\
        join(Student, Feedback.id_student == Student.student_id).\
        join(Super, Feedback.id_supervisor == Super.super_id).all()

    last_part_numbers = {}
    for feedback, student, supervisor in feedback_data:
        last_part_number = ExamReport.query.filter_by(student_id=student.student_id).order_by(ExamReport.part_number.desc()).first()
        if last_part_number:
            last_part_numbers[student.student_id] = last_part_number.part_number
        else:
            last_part_numbers[student.student_id] = None

    distinguished_student_id = None
    max_performance = float('-inf')  
    for feedback, student, supervisor in feedback_data:
        overall_performance = calculate_overall_performance(student.student_id)
        if overall_performance is not None and overall_performance > max_performance:
            max_performance = overall_performance
            distinguished_student_id = student.student_id

    distinguished_student = Student.query.get(distinguished_student_id)

    distinguished_user = User.query.filter_by(username=distinguished_student.username).first()

    if distinguished_user and distinguished_user.image_file:
        distinguished_student_image_file = distinguished_user.image_file
    else:
        distinguished_student_image_file = "default.png"

    return render_template('sidebar2.html', feedback_data=feedback_data, distinguished_student=distinguished_student, distinguished_student_image_file=distinguished_student_image_file, last_part_numbers=last_part_numbers)

















@app.route("/sidebar", methods=['GET', 'POST'])
@login_required
def sidebar():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        return redirect(url_for('login'))

    student = Student.query.filter_by(username=username).first()

    if student:
        student_id = student.student_id
        history_exam_entries = HistoryExam.query.filter_by(student_id=student_id).all()
        history_entries = History.query.filter_by(student_id=student_id).all()
        completed_parts_count = sum(1 for entry in history_exam_entries if entry.pass_part == "pass")
        not_completed_parts_count = 30 - completed_parts_count
        years, months = estimate_memorization_time(student_id)

        # Fetch feedback for the student
        feedback_entries = Feedback.query.filter_by(id_student=student_id).all()

        # Check if the request method is POST (i.e., form submission)
        if request.method == 'POST':
            supervisor_name = request.form['supervisor_name']
            feedback_text = request.form['feedback']

            # Fetch supervisor ID based on the name
            supervisor = Super.query.filter_by(username=supervisor_name).first()
            if supervisor:
                supervisor_id = supervisor.super_id
                # Save feedback to the database
                feedback = Feedback(id_student=student_id, id_supervisor=supervisor_id, feedback_text=feedback_text)
                db.session.add(feedback)
                db.session.commit()
                return redirect(url_for('sidebar'))
            else:
                return "Supervisor with given name doesn't exist."

        return render_template("sidebar.html", title="sidebar", student=student, 
                               history=history_entries, history_exam=history_exam_entries, 
                               completed_parts_count=completed_parts_count, 
                               not_completed_parts_count=not_completed_parts_count,
                               years=years, months=months,
                               feedback_entries=feedback_entries)  # Pass feedback_entries to the template
    else:
        return "Student not found"





if __name__ == "__main__":
    app.run(debug=True)




