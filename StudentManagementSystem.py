import json
import os

# ============================================================
#             STUDENT MANAGEMENT SYSTEM
# ============================================================

FILE_NAME = "students.json"


# ============================================================
#                    COLOR CODES
# ============================================================

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"


# ============================================================
#                    DECORATION FUNCTIONS
# ============================================================

def line(char="═", length=70):
    print(char * length)


def title(text):
    line("═")
    print(f"{Colors.CYAN}{Colors.BOLD}"
          f"        {text}"
          f"{Colors.RESET}")
    line("═")


def section(text):
    print()
    print(f"{Colors.YELLOW}{Colors.BOLD}>>> {text}{Colors.RESET}")
    line("─")


def pause():
    input(f"\n{Colors.MAGENTA}Press ENTER to continue...{Colors.RESET}")


# ============================================================
#                    FILE HANDLING
# ============================================================

def load_students():
    """Load student data from JSON file."""

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_students(students):
    """Save student data into JSON file."""

    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


# ============================================================
#                    INPUT VALIDATION
# ============================================================

def get_student_id():
    while True:
        student_id = input("Enter Student ID: ").strip()

        if student_id.isdigit():
            return int(student_id)

        print(f"{Colors.RED}Invalid ID! Enter numbers only.{Colors.RESET}")


def get_name():
    while True:
        name = input("Enter Student Name: ").strip()

        if name and all(char.isalpha() or char.isspace()
                        for char in name):
            return name.title()

        print(f"{Colors.RED}Invalid name!{Colors.RESET}")


def get_age():
    while True:
        try:
            age = int(input("Enter Age: "))

            if 5 <= age <= 100:
                return age

            print(f"{Colors.RED}Age must be between 5 and 100.{Colors.RESET}")

        except ValueError:
            print(f"{Colors.RED}Enter a valid number.{Colors.RESET}")


def get_marks():
    while True:
        try:
            marks = float(input("Enter Marks (0-100): "))

            if 0 <= marks <= 100:
                return marks

            print(f"{Colors.RED}Marks must be between 0 and 100.{Colors.RESET}")

        except ValueError:
            print(f"{Colors.RED}Enter a valid number.{Colors.RESET}")


def get_course():
    while True:
        course = input("Enter Course: ").strip()

        if course:
            return course.upper()

        print(f"{Colors.RED}Course cannot be empty.{Colors.RESET}")


def get_gender():
    while True:
        gender = input("Enter Gender (M/F/O): ").strip().upper()

        if gender in ["M", "F", "O"]:
            return gender

        print(f"{Colors.RED}Enter M, F or O only.{Colors.RESET}")


# ============================================================
#                    GRADE CALCULATION
# ============================================================

def calculate_grade(marks):

    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


# ============================================================
#                    ADD STUDENT
# ============================================================

def add_student(students):

    section("ADD NEW STUDENT")

    student_id = get_student_id()

    # Check duplicate ID
    for student in students:
        if student["id"] == student_id:
            print(f"{Colors.RED}Student ID already exists!{Colors.RESET}")
            return

    name = get_name()
    age = get_age()
    gender = get_gender()
    course = get_course()
    marks = get_marks()

    grade = calculate_grade(marks)

    student = {
        "id": student_id,
        "name": name,
        "age": age,
        "gender": gender,
        "course": course,
        "marks": marks,
        "grade": grade
    }

    students.append(student)
    save_students(students)

    print(f"\n{Colors.GREEN}{Colors.BOLD}"
          f"Student added successfully!"
          f"{Colors.RESET}")


# ============================================================
#                    DISPLAY STUDENTS
# ============================================================

def display_students(students):

    section("ALL STUDENTS")

    if not students:
        print(f"{Colors.YELLOW}No student records found.{Colors.RESET}")
        return

    print(
        f"{'ID':<6}"
        f"{'Name':<20}"
        f"{'Age':<6}"
        f"{'Gender':<8}"
        f"{'Course':<15}"
        f"{'Marks':<10}"
        f"{'Grade':<8}"
    )

    line("─", 73)

    for student in students:

        print(
            f"{student['id']:<6}"
            f"{student['name']:<20}"
            f"{student['age']:<6}"
            f"{student['gender']:<8}"
            f"{student['course']:<15}"
            f"{student['marks']:<10.2f}"
            f"{student['grade']:<8}"
        )


# ============================================================
#                    SEARCH STUDENT
# ============================================================

def search_student(students):

    section("SEARCH STUDENT")

    if not students:
        print(f"{Colors.YELLOW}No records available.{Colors.RESET}")
        return

    print("1. Search by ID")
    print("2. Search by Name")
    print("3. Search by Course")

    choice = input("\nEnter choice: ").strip()

    results = []

    if choice == "1":

        student_id = get_student_id()

        results = [
            student for student in students
            if student["id"] == student_id
        ]

    elif choice == "2":

        name = input("Enter name: ").strip().lower()

        results = [
            student for student in students
            if name in student["name"].lower()
        ]

    elif choice == "3":

        course = input("Enter course: ").strip().upper()

        results = [
            student for student in students
            if student["course"] == course
        ]

    else:
        print(f"{Colors.RED}Invalid choice.{Colors.RESET}")
        return

    if results:
        display_students(results)
    else:
        print(f"{Colors.RED}Student not found.{Colors.RESET}")


# ============================================================
#                    UPDATE STUDENT
# ============================================================

def update_student(students):

    section("UPDATE STUDENT")

    student_id = get_student_id()

    student = None

    for item in students:
        if item["id"] == student_id:
            student = item
            break

    if student is None:
        print(f"{Colors.RED}Student not found.{Colors.RESET}")
        return

    print("\nCurrent Student Information:")
    print(f"Name   : {student['name']}")
    print(f"Age    : {student['age']}")
    print(f"Gender : {student['gender']}")
    print(f"Course : {student['course']}")
    print(f"Marks  : {student['marks']}")

    print("\nEnter new information:")

    student["name"] = get_name()
    student["age"] = get_age()
    student["gender"] = get_gender()
    student["course"] = get_course()
    student["marks"] = get_marks()

    student["grade"] = calculate_grade(student["marks"])

    save_students(students)

    print(f"\n{Colors.GREEN}Student updated successfully!{Colors.RESET}")


# ============================================================
#                    DELETE STUDENT
# ============================================================

def delete_student(students):

    section("DELETE STUDENT")

    student_id = get_student_id()

    for student in students:

        if student["id"] == student_id:

            print("\nStudent Found:")
            print(f"Name: {student['name']}")
            print(f"Course: {student['course']}")

            confirmation = input(
                "\nAre you sure you want to delete? (Y/N): "
            ).strip().upper()

            if confirmation == "Y":

                students.remove(student)
                save_students(students)

                print(
                    f"{Colors.GREEN}"
                    f"Student deleted successfully!"
                    f"{Colors.RESET}"
                )

            else:
                print("Deletion cancelled.")

            return

    print(f"{Colors.RED}Student not found.{Colors.RESET}")


# ============================================================
#                    SORT STUDENTS
# ============================================================

def sort_students(students):

    section("SORT STUDENTS")

    if not students:
        print("No records available.")
        return

    print("1. Sort by Name")
    print("2. Sort by Marks")
    print("3. Sort by Age")
    print("4. Sort by Student ID")

    choice = input("\nEnter choice: ").strip()

    if choice == "1":

        sorted_students = sorted(
            students,
            key=lambda x: x["name"]
        )

    elif choice == "2":

        sorted_students = sorted(
            students,
            key=lambda x: x["marks"],
            reverse=True
        )

    elif choice == "3":

        sorted_students = sorted(
            students,
            key=lambda x: x["age"]
        )

    elif choice == "4":

        sorted_students = sorted(
            students,
            key=lambda x: x["id"]
        )

    else:
        print(f"{Colors.RED}Invalid choice.{Colors.RESET}")
        return

    display_students(sorted_students)


# ============================================================
#                    STATISTICS
# ============================================================

def statistics(students):

    section("STUDENT STATISTICS")

    if not students:
        print("No student records available.")
        return

    total = len(students)

    total_marks = sum(
        student["marks"] for student in students
    )

    average = total_marks / total

    highest = max(
        students,
        key=lambda x: x["marks"]
    )

    lowest = min(
        students,
        key=lambda x: x["marks"]
    )

    passed = sum(
        1 for student in students
        if student["marks"] >= 50
    )

    failed = total - passed

    print(f"Total Students : {total}")
    print(f"Average Marks  : {average:.2f}")
    print(f"Highest Marks  : {highest['marks']}")
    print(f"Top Student    : {highest['name']}")
    print(f"Lowest Marks   : {lowest['marks']}")
    print(f"Lowest Student : {lowest['name']}")
    print(f"Passed         : {passed}")
    print(f"Failed         : {failed}")


# ============================================================
#                    MENU
# ============================================================

def menu():

    print()
    print(f"{Colors.BLUE}{Colors.BOLD}")

    line("╔", 70)
    print("║              STUDENT MANAGEMENT SYSTEM                  ║")
    line("╚", 70)

    print(Colors.RESET)

    print(f"{Colors.GREEN}1.{Colors.RESET} Add Student")
    print(f"{Colors.GREEN}2.{Colors.RESET} Display Students")
    print(f"{Colors.GREEN}3.{Colors.RESET} Search Student")
    print(f"{Colors.GREEN}4.{Colors.RESET} Update Student")
    print(f"{Colors.GREEN}5.{Colors.RESET} Delete Student")
    print(f"{Colors.GREEN}6.{Colors.RESET} Sort Students")
    print(f"{Colors.GREEN}7.{Colors.RESET} Student Statistics")
    print(f"{Colors.RED}8.{Colors.RESET} Exit")

    line("─")


# ============================================================
#                    MAIN PROGRAM
# ============================================================

def main():

    students = load_students()

    while True:

        menu()

        choice = input(
            f"{Colors.CYAN}Enter your choice (1-8): {Colors.RESET}"
        ).strip()

        if choice == "1":

            add_student(students)
            pause()

        elif choice == "2":

            display_students(students)
            pause()

        elif choice == "3":

            search_student(students)
            pause()

        elif choice == "4":

            update_student(students)
            pause()

        elif choice == "5":

            delete_student(students)
            pause()

        elif choice == "6":

            sort_students(students)
            pause()

        elif choice == "7":

            statistics(students)
            pause()

        elif choice == "8":

            print()
            line("═")
            print(
                f"{Colors.GREEN}{Colors.BOLD}"
                "Thank you for using Student Management System!"
                f"{Colors.RESET}"
            )
            line("═")
            break

        else:

            print(
                f"{Colors.RED}"
                "Invalid choice! Please select 1-8."
                f"{Colors.RESET}"
            )


# ============================================================
#                    PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()