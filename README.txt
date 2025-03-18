Fitness Check-in System
A Django-based fitness check-in tracking and data analysis system designed to help users record fitness activities and track changes in body metrics.

Features
User Management
User registration/login/logout

Profile management (including height, weight, target weight, etc.)

Body metrics recording (weight, body fat percentage, body measurements, etc.)

Fitness Check-in
Record fitness activities (type, duration, calories burned, etc.)

Log specific exercises, sets, and weights during workouts

Create and manage fitness plans

Data Visualization
Trends in weight and body fat percentage

Distribution of workout frequency and categories

Calorie consumption statistics

BMI index and body measurement analysis

Tech Stack
Backend: Django 4.2

Frontend:

Bootstrap 5

Chart.js (data visualization)

Font Awesome (icons)

Database: SQLite (easily migratable to PostgreSQL or MySQL)
Project Structure
复制
fitness_tracker/
│
├── fitness_tracker/         # Main project directory
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   └── ...
│
├── users/                   # User application
│   ├── models.py            # User and body metrics models
│   ├── views.py             # View functions
│   └── ...
│
├── workouts/                # Fitness check-in application
│   ├── models.py            # Workout and plan models
│   ├── views.py             # View functions
│   └── ...
│
├── dashboard/               # Dashboard and data analysis application
│   ├── views.py             # View functions
│   └── ...
│
├── templates/               # HTML templates
├── static/                  # Static files
├── media/                   # User-uploaded files
└── manage.py                # Django management script
Key Models
CustomUser: Extends Django's user model with fitness-related fields

UserBodyRecord: Records user body metrics

WorkoutCategory: Fitness categories (e.g., cardio, strength training)

Exercise: Specific exercises (e.g., squats, bench press)

Workout: User workout records

WorkoutExercise: Records specific exercises within a workout

WorkoutPlan: User-created fitness plans

Feature Screenshots
Dashboard
Dashboard

Fitness Check-in
Fitness Check-in

Body Metrics Analysis
Body Metrics Analysis

Workout Analysis
Workout Analysis

Contribution
Contributions are welcome! Please fork the repository and create a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Thank you to everyone who contributed to this project!
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/)
