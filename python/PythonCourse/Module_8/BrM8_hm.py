# С помощью библиотеки sqlite3 создайте базу данных и подключитесь к ней.
# Создайте в ней таблицы:
#
# Students
# Поля: (id, name, surname, age, city)
#
# Courses
# Поля: (id, name, time_start, time_end)
# Student_courses
# Поля: (student_id, course_id)
# course_id - id курса, который проходит студет (Foreign key)
# student_id - id студента, который проходит курс (Foreign key)

import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.sqlite')

cursor = conn.cursor()
# cursor.execute("CREATE TABLE Students (id int, name Varchar(32), surname Varchar(32), age int, city Varchar(32))")
# cursor.execute("CREATE TABLE Courses (id int, name Varchar(32), time_start timestamp, time_end timestamp)") #time_end timestamp
# cursor.execute("CREATE TABLE Student_courses (student_id int, course_id int)")

# Добавьте в таблицы объекты:
# Courses:
# (1, 'python', 21.07.21, 21.08.21)
# (2, 'java', 13.07.21, 16.08.21)
#
# Students:
# (1, 'Max', 'Brooks', 24, 'Spb')
# (2, 'John', 'Stones', 15, 'Spb')
# (3, 'Andy', 'Wings', 45, 'Manchester')
# (4, 'Kate', 'Brooks', 34, 'Spb')
# Student_courses:
# (1, 1)
# (2, 1)
# (3, 1)
# (4, 2)

# cursor.executemany("INSERT INTO Courses VALUES (?, ?, ?, ?)", [(1, 'python', '21.07.21', '21.08.21'),(2, 'java', '13.07.21', '16.08.21')])
# cursor.executemany("INSERT INTO Students VALUES (?, ?, ?, ?, ?)",[(1, 'Max', 'Brooks', 24, 'Spb'),(2, 'John', 'Stones', 15, 'Spb'),(3, 'Andy', 'Wings', 45, 'Manhester'),(4, 'Kate', 'Brooks', 34, 'Spb')])
# cursor.executemany("INSERT INTO Student_courses VALUES (?, ?)",[(1, 1),(2, 1),(3, 1),(4, 2)])

conn.commit()
# Напишите запросы, чтобы получить:
# 1. Всех студентов старше 30 лет.
# 2. Всех студентов, которые проходят курс по python.
# 3. Всех студентов, которые проходят курс по python и из Spb.
cursor.execute("SELECT name FROM Students WHERE age > 30")
print(cursor.fetchall())

#cursor.execute("SELECT name FROM Students JOIN Student_courses ON Students.id = Student_courses.student_id WHERE age > 30")
cursor.execute("SELECT id FROM Student_courses WHERE course_id == 1 AND INNER JOIN Students ON Student_courses.student_id = Students.id")
print(cursor.fetchall())

#cursor.execute("SELECT id FROM Student_courses WHERE course_id == 1 AND INNER JOIN Students ON Student_courses.student_id = Students.id WHERE city == Spb")
#print(cursor.fetchall())

conn.close()