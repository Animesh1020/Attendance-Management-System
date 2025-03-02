import os
import csv

studentName = []
id = []
email = []

while True:
    name = input("Enter student name (or type 'done' to exit): ").strip()
    if name.lower() == "done":
        print("Exited successfully and data is saved.")
        break
    if not name:
        print("Student name cannot be empty!")
        continue
    studentName.append(name)

    studentID = input("Enter student ID: ").strip()
    if not studentID:
        print("Student ID cannot be empty!")
        continue
    id.append(studentID)

    # Automatically generate email based on the student ID
    studentEmail = f"{studentID}@iiitkota.ac.in"
    email.append(studentEmail)

    print(f"Generated email for {name}: {studentEmail}")

# Check if file exists, so we only write the header once.
txt_file_exists = os.path.isfile("studentData.txt")
csv_file_exists = os.path.isfile("studentData.csv")

# Write data in tabular form to a text file
with open("studentData.txt", "a") as txt_file:
    # Write the header if the file doesn't already exist
    if not txt_file_exists:
        txt_file.write(f"{'Name':<20}{'ID':<20}{'Email'}\n")  # Headers with proper alignment

    # Append new data in tabular form
    for i in range(len(id)):
        txt_file.write(f"{studentName[i]:<20}{id[i]:<20}{email[i]}\n")

# Write data in CSV format
with open("studentData.csv", "a", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header if the file doesn't already exist
    if not csv_file_exists:
        csv_writer.writerow(["Name", "ID", "Email"])  # CSV Headers
    
    # Append new data
    for i in range(len(id)):
        csv_writer.writerow([studentName[i], id[i], email[i]])

print("Data appended successfully in 'studentData.txt' and 'studentData.csv'.")
