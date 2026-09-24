import os
from datetime import datetime, timedelta

STUDENT_FILE = "students.txt"
COURSE_FILE = "courses.txt"
PASSED_FILE = "passed.txt"

#main menu
def main():
    while True:
        print("\nYou may select one of the following:")
        print("    1) Add student")
        print("    2) Search student")
        print("    3) Search course")
        print("    4) Add course completion")
        print("    5) Show student's record")
        print("    0) Exit")
        
        choice = input("\nWhat is your selection? ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            search_student()
        elif choice == '3':
            search_course()
        elif choice == '4':
            add_course_completion()
        elif choice == '5':
            show_student_record()
        elif choice == '0':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

# step 1    
def load_students():
    students = []
    try:
        with open(STUDENT_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 7:
                        student = {
                            'id': parts[0],
                            'last_name': parts[1],
                            'first_name': parts[2],
                            'middle_name': parts[3],
                            'email': parts[4],
                            'start_year': parts[5],
                            'major': parts[6]
                        }
                        students.append(student)
    except FileNotFoundError:
        pass
    return students

def load_courses():
    courses = []
    try:
        with open(COURSE_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 3:
                        course = {
                            'code': parts[0],
                            'name': parts[1],
                            'credits': int(parts[2]),
                            'teachers': parts[3:]
                        }
                        courses.append(course)
    except FileNotFoundError:
        pass
    return courses

def load_passed_courses():
    passed = []
    try:
        with open(PASSED_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 4:
                        passed_course = {
                            'course_code': parts[0],
                            'student_id': parts[1],
                            'date': parts[2],
                            'grade': int(parts[3])
                        }
                        passed.append(passed_course)
    except FileNotFoundError:
        pass
    return passed

def save_passed_courses(passed_courses):
    with open(PASSED_FILE, 'w', encoding='utf-8') as file:
        for pc in passed_courses:
            line = f"{pc['course_code']},{pc['student_id']},{pc['date']},{pc['grade']}\n"
            file.write(line)

def save_students(students):
    with open(STUDENT_FILE, 'w', encoding='utf-8') as file:
        for student in students:
            line = f"{student['id']},{student['last_name']},{student['first_name']},{student['middle_name']},{student['email']},{student['start_year']},{student['major']}\n"
            file.write(line)

def add_student():
    print("\n--- Add Student ---")
    
    students = load_students()
    
    if students:
        max_id = max(int(student['id']) for student in students)
        new_id = max_id + 1
        
        if new_id > 99999:
            existing_ids = {int(student['id']) for student in students}
            new_id = None
            for potential_id in range(10000, 100000):
                if potential_id not in existing_ids:
                    new_id = potential_id
                    break
            if new_id is None:
                print("Error: No available student IDs!")
                return
    else:
        new_id = 10000
    
    new_id = str(new_id)
    
    first_name = input("Enter the first name of the student: ").strip()
    last_name = input("Enter the last name of the student: ").strip()
    middle_name = input("Enter the middle name (press enter if none): ").strip()
    
    email = f"{first_name.lower()}.{last_name.lower()}@lut.fi"
    
    current_year = datetime.now().year
    start_year = input(f"Enter start year (default {current_year}): ").strip()
    if not start_year:
        start_year = str(current_year)
    
    print("\nSelect student's major:")
    print("    CE: Computational Engineering")
    print("    EE: Electrical Engineering")
    print("    ET: Energy Technology")
    print("    ME: Mechanical Engineering")
    print("    SE: Software Engineering")
    
    while True:
        major = input("\nWhat is your selection? ").strip().upper()
        if major in ['CE', 'EE', 'ET', 'ME', 'SE']:
            break
        else:
            print("Invalid selection. Please choose from: CE, EE, ET, ME, SE")
    
    new_student = {
        'id': new_id,
        'last_name': last_name,
        'first_name': first_name,
        'middle_name': middle_name,
        'email': email,
        'start_year': start_year,
        'major': major
    }
    
    students.append(new_student)
    save_students(students)
    
    print(f"Student added successfully! Student ID: {new_id}")

# step 2
def search_student():
    print("\n--- Search Student ---")
    
    search_term = input("Give at least 3 characters of the students first, middle or last name: ").strip()
    
    if len(search_term) < 3:
        print("Please enter at least 3 characters.")
        return
    
    students = load_students()
    matches = []
    
    for student in students:
        first_name_match = search_term.lower() in student['first_name'].lower()
        last_name_match = search_term.lower() in student['last_name'].lower()
        middle_name_match = search_term.lower() in student['middle_name'].lower()
        
        if first_name_match or last_name_match or middle_name_match:
            matches.append(student)
    
    if matches:
        print("Matching students:")
        for student in matches:
            middle_display = f" {student['middle_name']}" if student['middle_name'] else ""
            print(f"ID: {student['id']}, {student['last_name']}, {student['first_name']}{middle_display}")
    else:
        print("No matching students.")

# step 3
def search_course():
    print("\n--- Search Course ---")
    
    search_term = input("Give at least 3 characters of the name of the course or the teacher: ").strip()
    
    if len(search_term) < 3:
        print("Please enter at least 3 characters.")
        return
    
    courses = load_courses()
    matches = []
    
    for course in courses:
        code_match = search_term.upper() in course['code'].upper()
        name_match = search_term.lower() in course['name'].lower()
        teacher_match = any(search_term.lower() in teacher.lower() for teacher in course['teachers'])
        
        if code_match or name_match or teacher_match:
            matches.append(course)
    
    if matches:
        for course in matches:
            teachers = ", ".join(course['teachers'])
            print(f"ID: {course['code']}, Name: {course['name']}, Teacher(s): {teachers}")
    else:
        print("No matching courses.")

# step 4
def add_course_completion():
    print("\n--- Add Course Completion ---")
    
    courses = load_courses()
    students = load_students()
    passed_courses = load_passed_courses()
    
    course_code = input("Give the course ID: ").strip().upper()
    
    course_exists = any(course['code'] == course_code for course in courses)
    if not course_exists:
        print("Course not found. Try again.")
        return
    
    while True:
        student_id = input("Give the student ID: ").strip()
        student_exists = any(student['id'] == student_id for student in students)
        if student_exists:
            break
        else:
            print("Student not found. Try again.")
    
    while True:
        try:
            grade = int(input("Give the grade: ").strip())
            if 1 <= grade <= 5:
                break
            else:
                print("Grade is not a correct grade.")
        except ValueError:
            print("Grade is not a correct grade.")
    
    while True:
        date_str = input("Enter a date (YYYY-MM-DD): ").strip()
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now()
            
            if date_obj > today:
                print("Input date is later than today. Try again!")
            elif today - date_obj > timedelta(days=30):
                print("Input date is older than 30 days. Contact 'opinto'.")
                return
            else:
                break
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD. Try again!")
    
    for pc in passed_courses:
        if pc['course_code'] == course_code and pc['student_id'] == student_id:
            if grade > pc['grade']:
                pc['grade'] = grade
                pc['date'] = date_str
            save_passed_courses(passed_courses)
            print("Course completion updated!")
            return
    
    new_completion = {
        'course_code': course_code,
        'student_id': student_id,
        'date': date_str,
        'grade': grade
    }
    passed_courses.append(new_completion)
    save_passed_courses(passed_courses)
    print("Course completion added successfully!")

# step 5
def show_student_record():
    print("\n--- Show Student's Record ---")
    
    students = load_students()
    courses = load_courses()
    passed_courses = load_passed_courses()
    
    student_id = input("Give the student ID: ").strip()
    
    student = None
    for s in students:
        if s['id'] == student_id:
            student = s
            break
    
    if not student:
        print("Student not found.")
        return
    
    major_names = {
        'CE': 'Computational Engineering',
        'EE': 'Electrical Engineering',
        'ET': 'Energy Technology',
        'ME': 'Mechanical Engineering',
        'SE': 'Software Engineering'
    }
    
    print(f"\nStudent ID: {student['id']}")
    middle_display = f" {student['middle_name']}" if student['middle_name'] else ""
    print(f"Name: {student['last_name']}, {student['first_name']}{middle_display}")
    print(f"Starting year: {student['start_year']}")
    print(f"Major: {major_names.get(student['major'], student['major'])}")
    print(f"Email: {student['email']}")
    
    student_passed = [pc for pc in passed_courses if pc['student_id'] == student_id]
    
    print("\nPassed courses:")
    
    if not student_passed:
        print("No passed courses.")
        return
    
    total_credits = 0
    total_grade_points = 0
    
    for passed_course in student_passed:
        course_info = None
        for course in courses:
            if course['code'] == passed_course['course_code']:
                course_info = course
                break
        
        if course_info:
            teachers = ", ".join(course_info['teachers'])
            print(f"\nCourse ID: {course_info['code']}, Name: {course_info['name']}, Credits: {course_info['credits']}")
            print(f"Date: {passed_course['date']}, Teacher(s): {teachers}, grade: {passed_course['grade']}")
            
            total_credits += course_info['credits']
            total_grade_points += passed_course['grade'] * course_info['credits']
    
    if total_credits > 0:
        average_grade = total_grade_points / total_credits
        print(f"\nTotal credits: {total_credits}, average grade: {average_grade:.1f}")

if __name__ == "__main__":
    main()