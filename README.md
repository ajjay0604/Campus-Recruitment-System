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


Images and functions :


![image](https://github.com/user-attachments/assets/ce15e48d-db37-4649-b622-ba0f6fea6a24)


![image](https://github.com/user-attachments/assets/7fcdb192-9361-47f4-9417-d2ca3a6013e5)


![image](https://github.com/user-attachments/assets/24fc6c6a-7806-4740-bcea-81581bda0440)


![image](https://github.com/user-attachments/assets/1780c302-6789-4bf7-9c36-28e00b72408f)


![image](https://github.com/user-attachments/assets/a9aa4fa6-fd8f-4833-8ad5-95ecbc363f49)


![image](https://github.com/user-attachments/assets/8d9795d6-df01-44bf-96af-1ca31a0f1b13)


![image](https://github.com/user-attachments/assets/c37af78e-5374-4b32-9bcb-f7c87360b548)


![image](https://github.com/user-attachments/assets/e39c2783-e7a2-4766-870d-5531397ca063)


![image](https://github.com/user-attachments/assets/e7fb1341-b0e5-4c6e-91c7-775409c132be)


![image](https://github.com/user-attachments/assets/39449d72-df70-43ec-bc58-c0d030fd251d)


![image](https://github.com/user-attachments/assets/4f80a66e-32a8-48b0-b744-776e1a649918)


![image](https://github.com/user-attachments/assets/b79e4015-b4fe-467f-be38-cc7ce30e9e09)


![image](https://github.com/user-attachments/assets/a196e25c-8353-49f5-8936-2d8fa868be31)


![image](https://github.com/user-attachments/assets/1e9dbdef-0d32-4083-a4a2-310981d134a3)


![image](https://github.com/user-attachments/assets/c81d4b5d-ee41-4ebb-af78-445d8a4f7612)


![image](https://github.com/user-attachments/assets/5d8a48c6-3d9d-4961-81bc-f12bd310bbaa)


![image](https://github.com/user-attachments/assets/3b2cd2ae-c341-48c7-ac77-62efd60f98c1)


![image](https://github.com/user-attachments/assets/41809232-b1a2-4a39-a835-e1fb661cf060)
