# Securecare Hospital Web Application 

WEB APP FOR HOSPITAL TO MANAGE PATIENTS DATA AND STROKE 

### Stakeholders
- Patients 
- Admin/Doctor

### Functionl Requirements
- New Users should be able to register
- Users should be able to login
- Admin/Doctor should be able to login with the right credentials
- Admin/Doctor should be able to view patients data
- Admin/Doctor should be able to delete patients record and also edit their information

### User Case
- Patients
  - View web app
  - Register as a new user
  - Login 

- Admin/Doctor
  - View patient information 
  - Update patient information
  - Edit patient information
  - Delete patient information  

### Use Case 1 — User Registration and Login
- Use Case Name: User Registration and Login
- Actor: Patients
- Goal: Authenticate user and login
- Preconditions: User must have a valid username and password and a good internet connection

- Main flow:

1. User navigates to the registration page. 
2. User enters details (username and password). 
3. System validates input and creates an account. 
4. User logs in using credentials. 
5. System authenticates user and displays dashboard.

- Alternative FLow:

1. If invalid credentials are entered, display an error message and prompt retry

- Post Conditions: 

1. User is successfully logged in and can access personal dashboard

- Security Controls:

1. encrypt password
2. encrypt information in transit and at rest
3. input validation



### Use Case 2 — Admin/Doctor Management
- Use Case Name: Admin/Doctor Management
- Actor: Admin/Doctor
- Goal: 
  - Authenticate admin login
  - Allow an authorized admin to access the admin dashboard, manage patient records, and view patient details
- Preconditions: 
  - Admin must already exist in the system (created beforehand)
  - Admin must provide valid admin credentials to log in
  - System must have an active database connection
  - Admin must have a stable internet connection

- Main flow:

1. Admin navigates to the admin login page
2. Admin enters admin username and password
3. System validates credentials and authenticates the admin
4. System redirects admin to the Admin Dashboard
5. Admin sees the list of patients registered in the hospital
6. Admin chooses to edit or delete patient records if needed
7. System updates or removes patient data accordingly

- Alternative FLow:

  - Invalid Admin Credentials

   1. Admin enters incorrect username or password
   2. System rejects login attempt and displays an error message
   3. Admin is prompted to try again

- Post Conditions: 

1. Admin is successfully authenticated and can manage hospital patient data
2. Any updates, deletions, or changes to patient records are saved in the system
3. Admin can view detailed patient information at any time

- Security Controls:

1. encrypt password
2. encryption in transit and at rest
3. input validation
4. Authentication & Authorization