
print("===== Student Result Management System =====")

name = input("Enter student name: ")


def get_mark(subject):
    while True:
        try:
            mark = float(input(f"Enter mark for {subject}: "))

            if 0 <= mark <= 100:
                return mark
            else:
                print("Invalid marks! Enter a value between 0 and 100.")

        except ValueError:
            print("Invalid input! Please enter a number.")


mark1 = get_mark("subject 1")
mark2 = get_mark("subject 2")
mark3 = get_mark("subject 3")

total = mark1 + mark2 + mark3
average = total / 3

if average >= 90:
    grade = "A"
elif average >= 75:
    grade = "B"
elif average >= 50:
    grade = "C"
else:
    grade = "Needs Improvement"

print("\n===== Student Result =====")
print("Student Name:", name)
print("Subject 1:", mark1)
print("Subject 2:", mark2)
print("Subject 3:", mark3)
print("Total Marks:", total, "/ 300")
print("Average Marks:", round(average, 2))
print("Grade:", grade)

if mark1 >= 35 and mark2 >= 35 and mark3 >= 35:
    print("Result: PASS")
else:
    print("Result: FAIL")
