ER Diagram :

![image](https://github.com/user-attachments/assets/890cbab4-86f1-4294-86bf-c8fca19a5495)

CREATION OF TABLES :


CREATE TABLE Student (
Student_ID NUMBER PRIMARY KEY, Name VARCHAR2(100),
Email VARCHAR2(100),
Phone_Number VARCHAR2(15), Department VARCHAR2(50), CGPA NUMBER(3,2),
Graduation_Year NUMBER(4)
);

CREATE TABLE Company (
Company_ID NUMBER PRIMARY KEY,
Company_Name VARCHAR2(100), Industry_Type VARCHAR2(50), Contact_Person VARCHAR2(100), Contact_Email VARCHAR2(100), Contact_Phone VARCHAR2(15)
);

CREATE TABLE Job_Posting ( Job_ID NUMBER PRIMARY KEY,
Position VARCHAR2(100), Salary NUMBER, Company_ID NUMBER,
FOREIGN KEY (Company_ID) REFERENCES
Company(Company_ID)
);

CREATE TABLE Application ( Application_ID NUMBER PRIMARY KEY, Application_Date DATE,
Student_ID NUMBER, Job_ID NUMBER, Status VARCHAR2(50),
FOREIGN KEY (Student_ID) REFERENCES
Student(Student_ID),
FOREIGN KEY (Job_ID) REFERENCES Job_Posting(Job_ID)
);
 
CREATE TABLE Interview_Schedule ( Interview_ID NUMBER PRIMARY KEY, Interview_Date DATE, Interview_Time VARCHAR2(20), Student_ID NUMBER,
Job_ID NUMBER,
FOREIGN KEY (Student_ID) REFERENCES
Student(Student_ID),
FOREIGN KEY (Job_ID) REFERENCES Job_Posting(Job_ID)
);


CREATE TABLE Feedback (
Feedback_ID NUMBER PRIMARY KEY,
Comments VARCHAR2(255), Rating NUMBER(1), Student_ID NUMBER, Company_ID NUMBER,
FOREIGN KEY (Student_ID) REFERENCES
Student(Student_ID),
FOREIGN KEY (Company_ID) REFERENCES
Company(Company_ID)
);

CREATE TABLE Placement_Event ( Event_ID NUMBER PRIMARY KEY,
Event_Name VARCHAR2(100), Event_Date DATE, Event_Location VARCHAR2(100), Company_ID NUMBER,
FOREIGN KEY (Company_ID) REFERENCES
Company(Company_ID)
);

