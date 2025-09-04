# Student Report Card Management System

# ---------- FUNCTION DEFINITIONS ----------
def calculate_grade(marks):
    """Function to calculate grade using nested if/else"""
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "A"
    elif marks >= 60:
        return "B"
    elif marks >= 40:
        return "C"
    else:
        return "Fail"


def save_to_file(students):
    """Function to save student data to file"""
    try:
        with open("report_cards.txt", "w") as f:
            for student in students:
                f.write(str(student) + "\n")
        print("✅ Report cards saved to report_cards.txt")
    except Exception as e:
        print("⚠️ Error while saving file:", e)


# ---------- DATA STRUCTURES ----------
students = []  # List of dictionaries (each dict = one student)
unique_ids = set()  # To ensure no duplicate student IDs

# ---------- MAIN PROGRAM ----------
while True:
    try:
        print("\n--- Student Report Card System ---")
        print("1. Add Student")
        print("2. Show All Students")
        print("3. Save & Exit")
        
        choice = int(input("Enter choice: "))

        if choice == 1:
            # Collect student details
            student_id = int(input("Enter Student ID: "))
            
            # Ensure unique IDs using SET
            if student_id in unique_ids:
                print("⚠️ Student ID already exists!")
                continue
            unique_ids.add(student_id)

            name = input("Enter Name: ")
            age = int(input("Enter Age: "))

            # Tuple for fixed seat position (row, column)
            seat = (int(input("Row: ")), int(input("Column: ")))

            # Subjects dictionary
            marks = {}
            for subject in ["Math", "Science", "English"]:
                mark = int(input(f"Enter marks for {subject}: "))
                marks[subject] = mark

            # Average calculation
            avg = sum(marks.values()) / len(marks)
            grade = calculate_grade(avg)

            # Store everything in a dictionary
            student = {
                "id": student_id,
                "name": name,
                "age": age,
                "seat": seat,
                "marks": marks,
                "average": avg,
                "grade": grade
            }

            # Add to students list
            students.append(student)
            print(f"✅ Student {name} added successfully!\n")

        elif choice == 2:
            print("\n--- All Students ---")
            if not students:
                print("No students available.")
            else:
                for s in students:  # Loop through list of dicts
                    print(f"ID: {s['id']} | Name: {s['name']} | Grade: {s['grade']}")

        elif choice == 3:
            save_to_file(students)
            print("👋 Exiting program...")
            break

        else:
            print("Invalid choice. Try again.")

    except ValueError:
        print("⚠️ Invalid input. Please enter numbers where required.")
