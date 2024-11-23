from flask import Flask, render_template, request, redirect, url_for
import db_functions

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Student Routes
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        age = request.form['age']
        degree = request.form['degree']
        branch = request.form['branch']
        db_functions.insert_student(student_id, name, age, degree, branch)
        return redirect(url_for('view_students'))
    return render_template('add_student.html')

@app.route('/view_students')
def view_students():
    students = db_functions.view_students()
    print(students)  # Debug print
    return render_template('students.html', students=students)

@app.route('/students_with_applications')
def students_with_applications():
    students = db_functions.view_students_with_applications()
    return render_template('students_with_applications.html', students=students)

@app.route('/students_without_applications')
def students_without_applications():
    students = db_functions.view_students_without_applications()
    return render_template('students_without_applications.html', students=students)

@app.route('/view_job_application_statistics')
def view_job_application_statistics():
    stats = db_functions.view_jobs_applied_per_student()
    return render_template('job_application_statistics.html', stats=stats)

@app.route('/view_placed_students')
def view_placed_students():
    students = db_functions.view_placed_students()
    return render_template('placed_students.html', students=students)

# Company Routes
@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company_id = request.form['company_id']
        name = request.form['name']
        location = request.form['location']
        sector = request.form['sector']
        db_functions.insert_company(company_id, name, location, sector)
        return redirect(url_for('view_companies'))
    return render_template('add_company.html')

@app.route('/view_companies')
def view_companies():
    companies = db_functions.view_companies()
    return render_template('companies.html', companies=companies)

# Job Posting Routes
@app.route('/add_job_posting', methods=['GET', 'POST'])
def add_job_posting():
    if request.method == 'POST':
        job_id = request.form['job_id']
        title = request.form['title']
        company_id = request.form['company_id']
        description = request.form['description']
        salary=request.form['salary']
        db_functions.insert_job_posting(job_id, title, company_id, description,salary)
        return redirect(url_for('view_job_postings'))
    return render_template('add_job_posting.html')

@app.route('/view_job_postings')
def view_job_postings():
    job_postings = db_functions.view_job_postings()
    return render_template('job_postings.html', job_postings=job_postings)

@app.route('/view_job_postings_with_company_info')
def view_job_postings_with_company_info():
    job_postings = db_functions.view_job_postings_with_company_info()
    return render_template('job_postings_with_company_info.html', job_postings=job_postings)

# Application Routes
'''@app.route('/apply_for_job/<int:job_id>', methods=['GET', 'POST'])
def apply_for_job(job_id):
    if request.method == 'POST':
        student_id = request.form['student_id']
        db_functions.apply_for_job(student_id, job_id)
        return redirect(url_for('view_job_postings'))
    return render_template('apply_for_job.html', job_id=job_id)'''

@app.route('/apply_for_job', methods=['GET', 'POST'])
def apply_for_job():
    if request.method == 'POST':
        application_id = request.form['application_id']  # Get APPLICATION_ID from the form
        student_id = request.form['student_id']
        job_id = request.form['job_id']
        db_functions.apply_for_job(application_id, student_id, job_id)  # Pass all three to the function
        return redirect(url_for('view_all_applications'))

    # Retrieve all available jobs with company name to display in the table
    job_postings = db_functions.view_job_postings_with_company_info()
    return render_template('apply_for_job.html', job_postings=job_postings)

@app.route('/view_all_applications')
def view_all_applications():
    applications = db_functions.view_all_applications()
    return render_template('application_details.html', applications=applications)

@app.route('/view_application_details/<int:application_id>')
def view_application_details(application_id):
    application_details = db_functions.view_application_details(application_id)
    return render_template('application_details.html', application_details=application_details)

@app.route('/schedule_interview', methods=['GET', 'POST'])
def schedule_interview():
    if request.method == 'POST':
        # Get form data
        application_id = request.form['application_id']
        interview_id = request.form['interview_id']
        scheduled_date = request.form['scheduled_date']
        status = request.form['status']
        location = request.form['location']
        
        # Schedule interview in the database
        db_functions.schedule_interview(application_id, interview_id, scheduled_date, status, location)
        
        # Redirect to the home page after scheduling
        return redirect(url_for('home'))
    return render_template('schedule_interview.html')

@app.route('/view_applications_by_status/<status>')
def view_applications_by_status(status):
    applications = db_functions.view_applications_by_status(status)
    return render_template('applications_by_status.html', applications=applications)

@app.route('/view_interviews_by_status', methods=['GET', 'POST'])
def view_interviews_by_status():
    interviews = []
    status = None
    
    if request.method == 'POST':
        # Get the status from the form
        status = request.form['status']
        
        # Fetch interviews with the specified status
        interviews = db_functions.get_interviews_by_status(status)
        
    # Render the page with the form and the results if any
    return render_template('view_interviews_by_status.html', interviews=interviews, status=status)


@app.route('/view_scheduled_applications_and_job_postings')
def view_scheduled_applications_and_job_postings():
    scheduled_apps = db_functions.view_scheduled_applications_and_job_postings()
    return render_template('scheduled_applications_and_job_postings.html', scheduled_apps=scheduled_apps)

# Specialized View Routes
@app.route('/view_specific_student_details/<student_id>')
def view_specific_student_details(student_id):
    student_details = db_functions.view_specific_student_details(student_id)
    return render_template('student_profile.html', student_details=student_details)


@app.route('/place_student', methods=['GET', 'POST'])
def place_student():
    if request.method == 'POST':
        application_id = request.form['application_id']
        
        # Fetch application details from the database
        application = db_functions.get_application_details(application_id)

        if application:
            return render_template('place_student.html', application=application)
        else:
            return render_template('place_student.html', error="Application ID not found.")

    return render_template('place_student.html')

@app.route('/confirm_placement', methods=['POST'])
def confirm_placement():
    application_id = request.form.get('application_id')
    if application_id:
        # Update the application status to 'Accepted' in the database
        db_functions.update_application_status(application_id, 'Accepted')
        print(f"Application {application_id} status updated to 'Accepted'")  # Debug message
    else:
        print("Application ID not received")  # Debug message

    return redirect(url_for('place_student'))


# Flask route for update/delete entries
@app.route('/update_delete_entries', methods=['GET', 'POST'])
def update_delete_entries():
    if request.method == 'POST':
        action = request.form.get('action')
        table = request.form.get('table')
        entry_id = request.form.get('entry_id')

        # Perform the respective action for each table
        if action == 'Update':
            if table == 'student':
                db_functions.update_student(entry_id, request.form)
            elif table == 'company':
                db_functions.update_company(entry_id, request.form)
            elif table == 'application':
                db_functions.update_application(entry_id, request.form)
            elif table == 'interview':
                db_functions.update_interview(entry_id, request.form)
            elif table == 'job_posting':
                db_functions.update_job_posting(entry_id, request.form)
        elif action == 'Delete':
            if table == 'student':
                db_functions.delete_student(entry_id)
            elif table == 'company':
                db_functions.delete_company(entry_id)
            elif table == 'application':
                db_functions.delete_application(entry_id)
            elif table == 'interview':
                db_functions.delete_interview(entry_id)
            elif table == 'job_posting':
                db_functions.delete_job_posting(entry_id)

        return redirect(url_for('update_delete_entries'))

    students = db_functions.view_students()
    companies = db_functions.view_companies()
    applications = db_functions.view_all_applications()
    interviews = db_functions.view_all_interviews()
    job_postings = db_functions.view_job_postings()

    return render_template('update_delete_entries.html', students=students, companies=companies, applications=applications, interviews=interviews, job_postings=job_postings)

if __name__ == '__main__':
    app.run(debug=True)
