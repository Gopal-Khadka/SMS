# Student Management System


## PROCEDURES

### Navigation Bar
Since the NavBar is common for all pages (except logins), it is the first obstacle to clear. We will use Bootstrap 5 to decorate the navigation bar.

### Login Page
Login Page is added from Bootstrap examples `SignIn Form`. The authentication will later be handled by respective views function.

### Authentication (Logging In and Out)
The authentication is handled by the functions provided by the Django framework.

### Index Page
The index page is made simple with example `Cover` provided by Bootstrap.

### Contact Page
A form is provided to the user for contacting the administration. Just the UI is made but not the backend logic.

### NavBar Active Page
When I click the button in the navigation bar, I want it to highlight the active page in a lighter color. An external js(jquery code) file is added to the navbar html page. Additionally, if-else statements are also added to navbar file because the `active` state of the navbar links gets refreshed when page loads handled by python views function.

### Services Page
Simple services page is made in this step just for display purposes.

### Dashboard Page
This is going to be our main page where all the main functionalities and features will be located and managed. In this section, we will only make UI and looks.

### Defining necessary models
The model represents the database in the Django project. 

1. `SessionYearModel`
2. `CustomUser`
3. `AdminHOD`
4. `Staffs`
5. `Courses`
6. `Subjects`
7. `Students`
8. `Attendance`
9. `AttendanceReport`
10. `LeaveReportStudent`
11. `LeaveReportStaff`
12. `FeedBackStudent`
13. `FeedBackStaffs`
14. `NotificationStudent`
15. `NotificationStaffs`
16. `StudentResult`

Each model class have their own importance and usage in this project. Refer to `models.py` file for more information.