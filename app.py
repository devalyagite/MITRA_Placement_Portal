import os
import uuid
import random
import MySQLdb.cursors
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'Pob'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'clg_placement_portal'

mysql = MySQL(app)

# File Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'png', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']

        if not username or not email or not password:
            flash("Please fill in all required fields.", "danger")
        else:
            # Check if email is already registered
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
            count = cur.fetchone()[0]
            cur.close()

            if count > 0:
                flash("Email is already registered. Please use a different one.", "danger")
            else:

                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO users (username, email, password, phone, address) VALUES (%s, %s, %s, %s, %s)",
                    (username, email, password, phone, address))
                mysql.connection.commit()
                cur.close()

                flash("Signup successful! You can now log in.", "success")
                return redirect(url_for('login'))

    return render_template('user_signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Check if the provided email matches a record in your database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and user[2] == password:
            session['user_id'] = user[0]
            session['user_email'] = user[1]
            flash("You are logged in successfully!", "success")

            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid email or password", "error")

    return render_template('user_login.html')



@app.route('/')
def landing_page():
    return render_template('index.html')


@app.route('/user_dashboard')
def user_dashboard():
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash("You need to log in first", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_email = session['user_email']

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(*) AS total_job FROM jobpost")
    total_job = cur.fetchone()['total_job']
    cur.close()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(*) AS total_job1 FROM application WHERE user_id = %s", (user_id,))
    total_job1 = cur.fetchone()['total_job1']
    cur.close()

    return render_template('UserDashboard.html',user_email=user_email, total_job=total_job, total_job1=total_job1)


@app.route('/user_view_job_list', methods=['GET', 'POST'])
def user_view_job_list():
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash("You need to log in first", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_email = session['user_email']

    # If GET request, fetch the user's current data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobpost")
    jobs = cur.fetchall()
    cur.close()

    return render_template('user_view_job_list.html', jobs=jobs, user_email=user_email)


@app.route('/user_apply_job/<int:job_id>', methods=['GET', 'POST'])
def user_apply_job(job_id):
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash("You need to log in first", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_email = session['user_email']

    if request.method == 'POST':
        try:
            ssc = request.form['ssc']
            hsc = request.form['hsc']
            cgpa = request.form['cgpa']
            aggregate = request.form['aggregate']
            branch = request.form['branch']
            year = request.form['year']

            # Handle Resume Upload
            resume_filename = ''
            if 'resume' in request.files and request.files['resume'].filename != '':
                resume_file = request.files['resume']
                if allowed_file(resume_file.filename):
                    filename = secure_filename(resume_file.filename)
                    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    resume_file.save(resume_path)
                    resume_filename = filename  # Save only filename in DB

            # Insert application into the database
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO application (user_id, job_id, ssc, hsc, cgpa, aggregate, branch, year, user_resume) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (user_id, job_id, ssc, hsc, cgpa, aggregate, branch, year, resume_filename)
            )
            mysql.connection.commit()
            cur.close()

            flash("Your application has been submitted successfully!", "success")
            return redirect(url_for('user_dashboard'))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")

    # Fetch the specific job details
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM jobpost WHERE job_id = %s", (job_id,))
    job = cur.fetchone()  # Fetch a single job
    if not job:
        flash("Job not found!", "danger")
        return redirect(url_for('user_dashboard'))

    # Fetch user education details
    cur.execute("SELECT * FROM education WHERE user_id = %s", (user_id,))
    education = cur.fetchone()  # Fetch a single education record
    cur.close()

    return render_template('user_apply_job.html', job=job, education=education, user_email=user_email)





@app.route('/user_view_applied_job_history')
def user_view_applied_job_history():
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash("You need to log in first", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_email = session['user_email']

    # Fetch all jobs the user has applied for
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT a.id AS application_id, j.job_id, j.title AS job_title, j.cname AS company_name, 
               j.salary, j.location, j.jobtype, a.date AS application_date, a.user_resume, a.status
        FROM application a
        JOIN jobpost j ON a.job_id = j.job_id
        WHERE a.user_id = %s
        ORDER BY a.date DESC
    """, (user_id,))

    applications = cur.fetchall()
    cur.close()

    return render_template('user_view_applied_job_history.html', applications=applications, user_email=user_email)



@app.route('/delete_application/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    # Ensure user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': "You need to log in first"}), 403

    user_id = session['user_id']

    try:
        # Delete application from the database
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM application WHERE id = %s AND user_id = %s", (application_id, user_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({'success': True, 'message': "Application deleted successfully"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500






@app.route('/user_add_education', methods=['GET', 'POST'])
def user_add_education():
    if 'user_id' not in session:
        flash("You must be logged in to manage education details.", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_email = session['user_email']

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch existing education details
    cur.execute("SELECT * FROM education WHERE user_id = %s", (user_id,))
    education_details = cur.fetchall()

    if request.method == 'POST':
        ssc = request.form['ssc']
        hsc = request.form['hsc']
        cgpa = request.form['cgpa']
        aggregate = request.form['aggregate']
        branch = request.form['branch']
        year = request.form['year']

        # Insert new education record
        cur.execute(
            "INSERT INTO education (user_id, ssc, hsc, cgpa, aggregate, branch, year) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_id, ssc, hsc, cgpa, aggregate, branch, year))
        mysql.connection.commit()
        flash("Education details added successfully!", "success")

        return redirect(url_for('user_add_education'))  # Refresh page after insertion

    cur.close()
    return render_template('user_add_education.html', education_details=education_details, user_email=user_email)


@app.route('/delete_education/<int:edu_id>', methods=['POST'])
def delete_education(edu_id):
    if 'user_id' not in session:
        flash("Unauthorized action!", "danger")
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM education WHERE id = %s AND user_id = %s", (edu_id, session['user_id']))
    mysql.connection.commit()
    cur.close()

    flash("Education record deleted successfully!", "success")
    return redirect(url_for('user_add_education'))



##########################################################################

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "star":
            flash("Admin logged in successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('admin_login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(*) AS total_students FROM users")
    total_student = cur.fetchone()['total_students']
    cur.close()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT COUNT(*) AS total_students1 FROM jobpost")
    total_student1 = cur.fetchone()['total_students1']
    cur.close()

    return render_template('admin_dashboard.html', total_student=total_student, total_job=total_student1)


@app.route('/admin_add_job_post', methods=['GET', 'POST'])
def admin_add_job_post():
    if request.method == 'POST':
        title = request.form['job-title']
        description = request.form['job-description']
        location = request.form['job-location']
        category = request.form['job-category']
        jobtype = request.form['job-type']
        salary = request.form['salary']
        cname = request.form['company']  # 🔥 Fixed: Proper variable name

        # Handle Resume Upload
        resume_filename = ''
        if 'resume' in request.files and request.files['resume'].filename != '':
            resume_file = request.files['resume']
            if resume_file and allowed_file(resume_file.filename):
                unique_filename = f"{uuid.uuid4().hex}_{secure_filename(resume_file.filename)}"
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

                try:
                    resume_file.save(resume_path)
                    resume_filename = unique_filename  # 🔥 Store only filename in DB
                    flash(f'Company logo uploaded successfully: {unique_filename}', 'info')
                except Exception as e:
                    flash(f'Error saving file: {e}', 'danger')

        # Insert into Database
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO jobpost (title, description, location, category, jobtype, salary, resume, cname) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",  # 🔥 Fixed: Correct placeholders
                (title, description, location, category, jobtype, salary, resume_filename, cname))

            mysql.connection.commit()
            cur.close()

            flash("Job post added successfully!", "success")
            return redirect(url_for('admin_add_job_post'))

        except Exception as e:
            flash(f'Database error: {str(e)}', 'danger')

    return render_template('AdminJobPost.html')




@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    if 'user_id' not in session:
        flash("You need to log in first", "warning")
        return redirect(url_for('login'))

    user_id = session['user_id']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']

        # Update password only if provided (without hashing)
        if password:
            cur.execute("UPDATE users SET username=%s, email=%s, phone=%s, address=%s, password=%s WHERE id=%s",
                        (username, email, phone, address, password, user_id))
        else:
            cur.execute("UPDATE users SET username=%s, email=%s, phone=%s, address=%s WHERE id=%s",
                        (username, email, phone, address, user_id))

        mysql.connection.commit()
        cur.close()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('user_profile'))

    # Fetch user data
    cur.execute("SELECT username, email, phone, address, password FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    cur.close()

    return render_template('user_profile.html', user=user)



@app.route('/admin_view_jobs')
def admin_view_jobs():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM jobpost ORDER BY date DESC")  # Fetch jobs ordered by latest
    jobs = cur.fetchall()
    cur.close()

    return render_template('admin_view_jobs.html', jobs=jobs)


@app.route('/admin_delete_job/<int:job_id>', methods=['GET'])
def admin_delete_job(job_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM jobpost WHERE job_id = %s", (job_id,))
    mysql.connection.commit()
    cur.close()

    flash("Job deleted successfully!", "success")
    return redirect(url_for('admin_view_jobs'))


@app.route('/admin_job_post_all_view')
def admin_job_post_all_view():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch all job posts with application count
    cur.execute("""
        SELECT j.job_id, j.title, j.cname, j.location, j.jobtype, j.salary, j.date, j.resume,
               COUNT(a.id) AS total_applications,
               SUM(CASE WHEN a.year = 'Fresher' THEN 1 ELSE 0 END) AS fresher_count
        FROM jobpost j
        LEFT JOIN application a ON j.job_id = a.job_id
        GROUP BY j.job_id
        ORDER BY j.date DESC
    """)

    jobs = cur.fetchall()
    cur.close()

    return render_template('admin_job_post_all_view.html', jobs=jobs)


@app.route('/admin_view_apply_fresher_list/<int:job_id>')
def admin_view_apply_fresher_list(job_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
        SELECT a.id, a.ssc, a.hsc, a.cgpa, a.aggregate, a.branch, a.year, a.date, a.status, a.user_resume,
               u.username, u.email, u.phone, j.title AS job_title, j.cname AS company_name
        FROM application a
        JOIN users u ON a.user_id = u.id
        JOIN jobpost j ON a.job_id = j.job_id
        WHERE a.job_id = %s
    """, (job_id,))

    freshers = cur.fetchall()
    cur.close()

    return render_template('admin_view_apply_fresher_list.html', freshers=freshers)


@app.route('/update_application_status', methods=['POST'])
def update_application_status():
    try:
        data = request.get_json()
        application_id = data.get('id')
        new_status = data.get('status')

        # Ensure both ID and status are provided
        if not application_id or not new_status:
            return jsonify({"success": False, "message": "Missing application ID or status"}), 400

        cur = mysql.connection.cursor()
        cur.execute("UPDATE application SET status = %s WHERE id = %s", (new_status, application_id))
        mysql.connection.commit()
        cur.close()

        return jsonify({"success": True, "message": "Status updated successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@app.route('/admin_view_students')
def admin_view_students():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Fetch all students & count how many jobs they applied for
        cur.execute("""
            SELECT u.id, u.username, u.email, u.phone, u.address, 
                   COUNT(a.id) AS total_applied_jobs
            FROM users u
            LEFT JOIN application a ON u.id = a.user_id
            GROUP BY u.id
        """)

        students = cur.fetchall()
        cur.close()

        return render_template('admin_view_students.html', students=students)

    except Exception as e:
        return f"Database error: {str(e)}", 500


@app.route('/admin_student_criteria', methods=['GET', 'POST'])
def admin_student_criteria():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Default Query (Fetch All Students with Education Info)
    query = """
        SELECT users.username, users.email, education.ssc, education.hsc, education.cgpa, 
               education.aggregate, education.branch, education.year
        FROM users 
        INNER JOIN education ON users.id = education.user_id
    """

    cur.execute(query)  # Execute the query before fetching data
    students = cur.fetchall()  # Fetch all student records
    cur.close()

    return render_template('admin_student_criteria.html', students=students)


######################################################################









if __name__ == '__main__':
    app.run(debug=True)
