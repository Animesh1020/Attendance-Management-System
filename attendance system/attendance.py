import os
from colorama import Fore, init

# Initialize colorama to work with color in console
init(autoreset=True)

# Function to read student data from the studentData.txt file
def load_student_data(file_name):
    student_data = {}
    try:
        with open(file_name, "r") as file:
            next(file)  # Skip the header line
            for line in file:
                data = line.strip().split()
                if len(data) == 3:  # Ensure there are three entries (Name, ID, Email)
                    name, student_id, email = data
                    last_four_digits = student_id[-4:]  # Extract the last 4 digits of the student ID
                    student_data[last_four_digits] = (student_id, name)
    except FileNotFoundError:
        print(f"{file_name} not found. Please ensure the file exists.")
    return student_data

# Function to get the next available day number by counting existing files
def get_next_day(class_folder):
    day_counter = 1
    while os.path.exists(f"{class_folder}/Day_{day_counter}.txt"):
        day_counter += 1
    return day_counter

# Function to take attendance for multiple days and save it day-wise in a class folder
def take_attendance(student_data):
    class_name = input("Enter class name: ").strip()
    class_folder = f"./{class_name}_attendance"
    
    # Create the class folder if it doesn't exist
    if not os.path.exists(class_folder):
        os.makedirs(class_folder)

    # Find the next available day
    day_counter = get_next_day(class_folder)

    while True:
        print(f"Taking attendance for Day {day_counter}.")

        day_file = f"{class_folder}/Day_{day_counter}.txt"
        attendance_data = []  # To store the attendance records for the day
        absent_students = []   # To track absent students

        # Collect all student IDs for marking attendance
        student_ids = list(student_data.keys())

        # Taking attendance for multiple students
        while True:
            studentID_last4 = input(f"Enter last 4 digits of student ID (or type 'done' to finish attendance for Day {day_counter}): ").strip()

            if studentID_last4.lower() == "done":
                print(f"Attendance for Day {day_counter} completed.")
                break

            if studentID_last4 in student_data:
                student_id, student_name = student_data[studentID_last4]
                attendance_data.append(f"{student_id}\t{student_name}\tPresent\tDay {day_counter}")
                print(Fore.GREEN + f"Attendance marked for {student_name} (ID: {student_id}) on Day {day_counter}.")
            else:
                print(Fore.RED + "Student not found. Please enter a valid last 4 digits of the ID.")

        # Mark absent students
        for last_four_digits, (student_id, student_name) in student_data.items():
            if f"{student_id}\t{student_name}\tPresent\tDay {day_counter}" not in attendance_data:
                absent_students.append(f"{student_id}\t{student_name}\tAbsent\tDay {day_counter}")

        # Combine present and absent data
        complete_attendance = attendance_data + absent_students

        # Saving the attendance data to a file after all entries are made
        with open(day_file, "w") as file:
            file.write("ID\tName\tStatus\tDay\n")  # Write the header for the file
            for record in complete_attendance:
                file.write(f"{record}\n")

        print(f"Attendance for Day {day_counter} saved in {day_file}.")
        
        # Ask the user if they want to take attendance for the next day
        next_day = input("Would you like to proceed to the next day? (yes/no): ").strip().lower()
        if next_day == 'no':
            print("Attendance process completed.")
            break
        else:
            day_counter += 1

# Load student data from the studentData.txt file
file_name = "studentData.txt"
student_data = load_student_data(file_name)

if student_data:
    take_attendance(student_data)
else:
    print("No student data found to take attendance.")
