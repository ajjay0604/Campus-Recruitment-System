import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='campus_recruitment',
            user='root',
            password='Declan@23'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()

# Student Functions
def insert_student(student_id, name, age, degree, branch):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO STUDENT (student_id, name, age, degree, branch) VALUES (%s, %s, %s, %s, %s)", 
                       (student_id, name, age, degree, branch))
        connection.commit()
        close_connection(connection)

def view_students():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM STUDENT")
        students = cursor.fetchall()
        close_connection(connection)
        if not students:
            print("No students found in the STUDENT table.")
        return students

def view_students_with_applications():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT S.student_id, S.name, COUNT(A.job_id) AS applications_count
            FROM STUDENT S
            LEFT JOIN APPLICATION A ON S.student_id = A.student_id
            GROUP BY S.student_id
            HAVING COUNT(A.job_id) > 0
        """)
        students = cursor.fetchall()
        close_connection(connection)
        return students

def view_students_without_applications():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT S.student_id, S.name, S.age, S.branch, COUNT(A.job_id) AS applications_count
            FROM STUDENT S
            LEFT JOIN APPLICATION A ON S.student_id = A.student_id
            GROUP BY S.student_id
            HAVING COUNT(A.job_id) = 0
        """)
        students = cursor.fetchall()
        close_connection(connection)
        return students

def view_jobs_applied_per_student():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT S.student_id, S.name, COUNT(A.job_id) AS job_applications
            FROM STUDENT S
            JOIN APPLICATION A ON S.student_id = A.student_id
            GROUP BY S.student_id
        """)
        students = cursor.fetchall()
        close_connection(connection)
        return students

# Company Functions
def insert_company(company_id, name, location, sector):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO COMPANY (company_id, name, location, sector) VALUES (%s, %s, %s, %s)",
                       (company_id, name, location, sector))
        connection.commit()
        close_connection(connection)

def view_companies():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM COMPANY")
        companies = cursor.fetchall()
        close_connection(connection)
        return companies

# Job Posting Functions
def insert_job_posting(job_id, title, company_id, description, salary):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO JOB_POSTING (job_id, title, company_id, description, salary) VALUES (%s, %s, %s, %s, %s)",
                       (job_id, title, company_id, description, salary))
        connection.commit()
        close_connection(connection)

def view_job_postings():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM JOB_POSTING")
        jobs = cursor.fetchall()
        close_connection(connection)
        return jobs

def view_job_postings_with_company_info():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT JP.job_id, JP.title, JP.description, C.name AS company_name, C.location, C.sector
            FROM JOB_POSTING JP
            JOIN COMPANY C ON JP.company_id = C.company_id
        """)
        job_postings = cursor.fetchall()
        close_connection(connection)
        return job_postings

# Application and Interview Management Functions
def apply_for_job(application_id, student_id, job_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO APPLICATION (APPLICATION_ID, STUDENT_ID, JOB_ID, STATUS) 
            VALUES (%s, %s, %s, 'Pending')
        """, (application_id, student_id, job_id))  # Insert all three fields into the table
        connection.commit()
        close_connection(connection)
def view_all_applications():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT A.application_id, A.status, S.name AS student_name, JP.title AS job_title, C.name AS company_name,
                   IFNULL(I.scheduled_date, '-') AS scheduled_date,
                   IFNULL(I.status, '-') AS interview_status,
                   IFNULL(I.location, '-') AS location
            FROM APPLICATION A
            JOIN STUDENT S ON A.student_id = S.student_id
            JOIN JOB_POSTING JP ON A.job_id = JP.job_id
            JOIN COMPANY C ON JP.company_id = C.company_id
            LEFT JOIN INTERVIEW I ON A.application_id = I.application_id
        """)
        applications = cursor.fetchall()
        close_connection(connection)
        return applications

def get_application_details(application_id):
    """
    Fetch application details based on application_id.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Query to get application details
    cursor.execute("SELECT * FROM application WHERE application_id = %s", (application_id,))
    application = cursor.fetchone()

    cursor.close()
    connection.close()
    
    return application

def update_application_status(application_id, status): 
    """
    Update the status of an application and its associated interviews.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Update the status of the application
    cursor.execute("UPDATE application SET status = %s WHERE application_id = %s", (status, application_id))

    # Update the status of the interviews linked to this application
    cursor.execute("UPDATE interview SET status = %s WHERE application_id = %s", (status, application_id))

    connection.commit()

    cursor.close()
    connection.close()

def view_application_details(application_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT A.application_id, A.status, S.name AS student_name, JP.title AS job_title, C.name AS company_name,
                   I.scheduled_date, I.status AS interview_status, I.location
            FROM APPLICATION A
            JOIN STUDENT S ON A.student_id = S.student_id
            JOIN JOB_POSTING JP ON A.job_id = JP.job_id
            JOIN COMPANY C ON JP.company_id = C.company_id
            LEFT JOIN INTERVIEW I ON A.application_id = I.application_id
            WHERE A.application_id = %s
        """, (application_id,))
        details = cursor.fetchone()
        close_connection(connection)
        return details

def schedule_interview(application_id, interview_id, scheduled_date, status, location):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO INTERVIEW (INTERVIEW_ID, APPLICATION_ID, SCHEDULED_DATE, STATUS, LOCATION)
            VALUES (%s, %s, %s, %s, %s)
        """, (interview_id, application_id, scheduled_date, status, location))
        connection.commit()
        close_connection(connection)


def view_applications_by_status(status):
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM APPLICATION WHERE status = %s", (status,))
        applications = cursor.fetchall()
        close_connection(connection)
        return applications
def view_all_interviews():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM INTERVIEW")
        interviews = cursor.fetchall()
        close_connection(connection)
        return interviews
    return []

def get_interviews_by_status(status):
    connection = get_connection()
    interviews = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT INTERVIEW.INTERVIEW_ID, INTERVIEW.APPLICATION_ID, INTERVIEW.SCHEDULED_DATE, 
                   INTERVIEW.STATUS, INTERVIEW.LOCATION, STUDENT.NAME AS STUDENT_NAME
            FROM INTERVIEW
            JOIN APPLICATION ON INTERVIEW.APPLICATION_ID = APPLICATION.APPLICATION_ID
            JOIN STUDENT ON APPLICATION.STUDENT_ID = STUDENT.STUDENT_ID
            WHERE INTERVIEW.STATUS = %s
        """, (status,))
        interviews = cursor.fetchall()
        close_connection(connection)
    return interviews

def delete_entry(table, entry_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table.upper()} WHERE {table.upper()}_ID = %s", (entry_id,))
        connection.commit()
        close_connection(connection)

def update_entry(table, entry_id, new_data):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        # Constructing dynamic update query
        update_query = f"UPDATE {table.upper()} SET " + ", ".join([f"{key} = %s" for key in new_data.keys()]) + \
                       f" WHERE {table.upper()}_ID = %s"
        values = list(new_data.values()) + [entry_id]
        cursor.execute(update_query, values)
        connection.commit()
        close_connection(connection)


def view_scheduled_applications_and_job_postings():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT A.application_id, S.name AS student_name, JP.title AS job_title, I.date_time, I.location
            FROM APPLICATION A
            JOIN STUDENT S ON A.student_id = S.student_id
            JOIN JOB_POSTING JP ON A.job_id = JP.job_id
            JOIN INTERVIEW I ON A.application_id = I.application_id
        """)
        scheduled_interviews = cursor.fetchall()
        close_connection(connection)
        return scheduled_interviews


def update_student_status_after_acceptance(application_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE APPLICATION SET status = 'Accepted' WHERE application_id = %s", (application_id,))
        connection.commit()
        close_connection(connection)

def view_placed_students():
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT S.student_id, S.name, JP.title AS job_title, JP.salary, C.name AS company_name
            FROM STUDENT S
            JOIN APPLICATION A ON S.student_id = A.student_id
            JOIN JOB_POSTING JP ON A.job_id = JP.job_id
            JOIN COMPANY C ON JP.company_id = C.company_id
            WHERE A.status = 'Accepted'
        """)
        placed_students = cursor.fetchall()
        close_connection(connection)
        return placed_students


def delete_student(student_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        delete_query = "DELETE FROM STUDENT WHERE STUDENT_ID = %s"
        cursor.execute(delete_query, (student_id,))
        connection.commit()
        close_connection(connection)

def delete_company(company_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        delete_query = "DELETE FROM COMPANY WHERE COMPANY_ID = %s"
        cursor.execute(delete_query, (company_id,))
        connection.commit()
        close_connection(connection)

def delete_application(application_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        delete_query = "DELETE FROM APPLICATION WHERE APPLICATION_ID = %s"
        cursor.execute(delete_query, (application_id,))
        connection.commit()
        close_connection(connection)

def delete_interview(interview_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        delete_query = "DELETE FROM INTERVIEW WHERE INTERVIEW_ID = %s"
        cursor.execute(delete_query, (interview_id,))
        connection.commit()
        close_connection(connection)

def delete_job_posting(job_id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        delete_query = "DELETE FROM JOB_POSTING WHERE JOB_ID = %s"
        cursor.execute(delete_query, (job_id,))
        connection.commit()
        close_connection(connection)

def update_student(student_id, form_data):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        update_query = """
            UPDATE STUDENT SET NAME = %s, AGE = %s, DEGREE = %s, BRANCH = %s
            WHERE STUDENT_ID = %s
        """
        cursor.execute(update_query, (
            form_data.get('name'),
            form_data.get('age'),
            form_data.get('degree'),
            form_data.get('branch'),
            student_id
        ))
        connection.commit()
        close_connection(connection)

def update_company(company_id, form_data):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        update_query = """
            UPDATE COMPANY SET NAME = %s, LOCATION = %s, SECTOR = %s
            WHERE COMPANY_ID = %s
        """
        cursor.execute(update_query, (
            form_data.get('name'),
            form_data.get('location'),
            form_data.get('sector'),
            company_id
        ))
        connection.commit()
        close_connection(connection)

def update_application(application_id, form_data):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        update_query = """
            UPDATE APPLICATION SET STUDENT_ID = %s, JOB_ID = %s, STATUS = %s
            WHERE APPLICATION_ID = %s
        """
        cursor.execute(update_query, (
            form_data.get('student_id'),
            form_data.get('job_id'),
            form_data.get('status'),
            application_id
        ))
        connection.commit()
        close_connection(connection)

def update_interview(interview_id, form_data):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        update_query = """
            UPDATE INTERVIEW SET APPLICATION_ID = %s, DATE = %s, STATUS = %s
            WHERE INTERVIEW_ID = %s
        """
        cursor.execute(update_query, (
            form_data.get('application_id'),
            form_data.get('date'),
            form_data.get('status'),
            interview_id
        ))
        connection.commit()
        close_connection(connection)

def update_job_posting(job_id, form_data):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        update_query = """
            UPDATE JOB_POSTING SET TITLE = %s, COMPANY_ID = %s, LOCATION = %s, DESCRIPTION = %s
            WHERE JOB_ID = %s
        """
        cursor.execute(update_query, (
            form_data.get('title'),
            form_data.get('company_id'),
            form_data.get('location'),
            form_data.get('description'),
            job_id
        ))
        connection.commit()
        close_connection(connection)