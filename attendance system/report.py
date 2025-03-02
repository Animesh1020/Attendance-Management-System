import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, init

# Initialize colorama for console colors
init(autoreset=True)

# Function to load student data with emails
def load_student_data(file_name):
    student_data = {}
    try:
        with open(file_name, "r") as file:
            next(file)  # Skip header line
            for line in file:
                data = line.strip().split("\t")
                if len(data) == 3:
                    name, student_id, email = data
                    last_four_digits = student_id[-4:]
                    student_data[last_four_digits] = (student_id, name, email)
    except FileNotFoundError:
        print(Fore.RED + f"{file_name} not found.")
    return student_data

# Function to generate attendance report
def generate_attendance_report(class_name, student_data):
    class_folder = f"./{class_name}_attendance"
    attendance_data = {}

    if not os.path.exists(class_folder):
        print(Fore.RED + "Class folder does not exist.")
        return

    for filename in os.listdir(class_folder):
        if filename.endswith(".txt"):
            day_file = os.path.join(class_folder, filename)
            with open(day_file, "r") as file:
                next(file)
                for line in file:
                    data = line.strip().split("\t")
                    if len(data) == 4:
                        student_id, student_name, status, _ = data
                        if student_id not in attendance_data:
                            attendance_data[student_id] = {
                                'name': student_name,
                                'present_days': 0,
                                'total_days': 0
                            }
                        attendance_data[student_id]['total_days'] += 1
                        if status.lower() == "present":
                            attendance_data[student_id]['present_days'] += 1

    report = []
    for student_id, data in attendance_data.items():
        attendance_percentage = (data['present_days'] / data['total_days']) * 100
        report.append((student_id, data['name'], attendance_percentage))

    report_file = os.path.join(class_folder, "attendance_report.txt")
    with open(report_file, "w") as file:
        file.write("ID\tName\tAttendance Percentage\n")
        for student_id, name, percentage in report:
            file.write(f"{student_id}\t{name}\t{percentage:.2f}%\n")

    print(Fore.YELLOW + f"Attendance report saved to {report_file}.")

    low_attendance_students = [record for record in report if record[2] < 75]
    if low_attendance_students:
        print(Fore.RED + "Students with less than 75% attendance:")
        for student_id, name, percentage in low_attendance_students:
            print(f"{name} (ID: {student_id}) - {percentage:.2f}%")

        send_email = input("Do you want to send an email to these students? (yes/no): ").strip().lower()
        if send_email == 'yes':
            for student_id, name, percentage in low_attendance_students:
                last_four_digits = student_id[-4:]
                if last_four_digits in student_data:
                    email = student_data[last_four_digits][2]
                    send_warning_email(name, student_id, percentage, email)
                else:
                    print(Fore.RED + f"No email found for {name} (ID: {student_id}).")

# Function to send a warning email
def send_warning_email(name, student_id, attendance_percentage, recipient_email):
    sender_email = "annsh2003@gmail.com"
    sender_password = "onucetmyvbhzmgks"

    subject = "Attendance Warning"
    body = (f"Dear {name},\n\n"
            f"Your attendance has fallen below 75%. "
            f"Your current attendance percentage is {attendance_percentage:.2f}%. "
            "Please make sure to attend your classes regularly.\n\n"
            "Best regards,\nYour School")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(Fore.GREEN + f"Email sent to {name} ({student_id}) at {recipient_email}.")
    except Exception as e:
        print(Fore.RED + f"Failed to send email to {name}: {str(e)}")

# Main function
def main():
    class_name = input("Enter the class name for attendance report: ").strip()
    student_data_file = "studentData.txt"
    student_data = load_student_data(student_data_file)

    if student_data:
        generate_attendance_report(class_name, student_data)
    else:
        print(Fore.RED + "No student data found to generate report.")

if __name__ == "__main__":
    main()
