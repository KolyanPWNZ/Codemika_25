# uml схема - https://drive.google.com/file/d/1ouhlnpN_RRffQcNUTSBC-UOFRgwMoYsj/view?usp=sharing
# github https://github.com/KolyanPWNZ/Codemika_25

import re
import random
from statistics import mean

class User:
    __id = 0  # static field

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self._update_id()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if type(name) == str:
            self._name = name

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, surname):
        if type(surname) == str:
            self._surname = surname

    @property
    def id(self):
        return self._id

    # функция обновления id
    def _update_id(self):
        self._id = User.__id
        User.__id += 1


class Student(User):
    def __init__(self, name, surname, phone_number):
        super(Student, self).__init__(name, surname)
        self.phone_number = phone_number

    def __str__(self):
        return "id:"+str(self.id) + " " + self.name + " " + self.surname + " " + self.phone_number

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone):
        phone = re.findall(r"(?:(?:8|\+7)[\- ]?)?(?:\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}", str(phone))
        if len(phone) != 0:
            self._phone_number = phone[0]
        else:
            self._phone_number = "none"
            print("Не удалось добавить номер телефона!")


class Course:
    __id = 0  # static field

    # максимальные и минимальные значения для оценок:

    def __init__(self, name_course, min_mark, max_mark):
        self.name_course = name_course
        self.__min_mark = 0
        self.__max_mark = 0
        self.min_mark = min_mark
        self.max_mark = max_mark
        self._students = dict()
        self._update_id()

    def __str__(self):
        return "id:" + str(self.id) + " - " + self.name_course

    @property
    def id(self):
        return self.__id

    # функция обновления id
    def _update_id(self):
        self._id = Course.__id
        Course.__id += 1

    @property
    def name_course(self):
        return self.__name_course

    @name_course.setter
    def name_course(self, name_course):
        if type(name_course) == str:
            self.__name_course = name_course
        else:
            print("Название курса должно быть строкой!")

    @property
    def min_mark(self):
        return self.__min_mark

    @min_mark.setter
    def min_mark(self, min_mark):
        if type(min_mark) == int:
            if min_mark <= self.max_mark:
                self.__min_mark = min_mark
            else:
                print("Минимальная оценка должна быть меньше максимальной!")
        else:
            print("Минимальная оценка должна бить числом!")

    @property
    def max_mark(self):
        return self.__max_mark

    @max_mark.setter
    def max_mark(self, max_mark):
        if type(max_mark) == int:
            if max_mark > self.min_mark:
                self.__max_mark = max_mark
            else:
                print("Максимальная оценка должна быть больше минимальной!")
        else:
            print("Максимальная оценка должна бить числом!")

    def print_students(self):
        for student in self._students:
            self.get_mark_student(student)

    # валидация студента
    def _check_type_student(self, student, show_info=False):
        if type(student) == Student:
            return True
        else:
            if show_info:
                print("Объект не относится к классу Student!")
            return False

    # проверка наличия студента на курсе
    def _check_presence_student(self, student, show_info=False):
        if student in self._students.keys():
            return True
        else:
            if show_info:
                print("Студента:", student, "- еще нет накурсе")
            return False

    # возвращает оценки для студента
    def get_mark_student(self, student):
        if self._check_type_student(student) and self._check_type_student(student):
            print('Студент:', student.id, student.name, student.surname)
            print('Оценки:', self._students[student]["marks"])
            print("Финальная оценка:", self._students[student]["final_mark"])
        else:
            print("Не удалось получить оценки для данного студента")

    # функция добавления оценок студенту
    def add_mark(self, student, marks):
        if self._check_type_student(student, True) and self._check_presence_student(student, True):
            if type(marks) == list:
                for mark in marks:
                    if type(mark) == int and self.min_mark <= mark <= self.max_mark:
                        self._students[student]["marks"].append(mark)
                    else:
                        print("Оценку:", mark, "не удалось добавить.")
                        print("Оценка должна быть целым числом в интервале [", self.min_mark, ":", self.max_mark, "]",
                              end='\n\n')
            else:
                print("Оценки должны подаваться на вход в виде списка!")
            print("Завершено добавление оценок студенту:", student, "на курсе", self)

    # выставление студентам финальных оценок
    def calculate_final_mark(self):
        if len(self._students) != 0:
            for student in self._students:
                student_info = self._students[student]
                student_marks = student_info['marks']
                final_mark = mean(student_marks) # средняя оценка
                self._students[student]["final_mark"] = round(final_mark)
            print("Оценки по курсу", self,"были выставлены!", end='\n\n')
        else:
            print("На курсе еще нет студентов!")

    # метод добавления одного студента
    def add_student(self, student):
        # проверяем что объект является студентом и его еще нет на курсе
        if self._check_type_student(student) and not self._check_presence_student(student):
            self._students.update({
                student:{
                    "marks": list(),
                    "final_mark": 0
                }
            })
            print("Студент:", student, "был добавлен на курс -", self, end='\n')
        else:
            print("Не удалось добавить студента на курс!")

    # метод добавления списка студентов на курс
    def add_students(self, students):
        if type(students) == list:
            for student in students:
                self.add_student(student)
        else:
            print("Студенты должны передаваться в списке!")


class CalculateCourse:
    @staticmethod
    def print_results(courses):
        if type(courses) == list:
            print("Результаты курсов:")
            for course in courses:
                print("Курс -",course)
                course.calculate_final_mark()
                print("Результаты студентов:")
                course.print_students()
                print("")
        else:
            print("На вход должен подаваться список!")


def random_mark(quantity = 5, min_mark = 0, max_max = 100):
    marks = list()
    while quantity > 0:
        marks.append(random.randint(min_mark, max_max))
        quantity -= 1
    return  marks


# создаем студентов
student1 = Student("Михаил", "Фиков", "89527894563")
student2 = Student("Александр", "Зеленин", "dfgd89547549513")
student3 = Student("Никита", "Егоров", "89785914596")
student4 = Student("Алена", "Самарина", "89985418525")
student5 = Student("Анастасия", "Дудка", "89526547896")

student_list = [student1, student2, student3, student4, student5]

# создаем курсы
course_prog = Course("Программирование", 0, 100)
course_design = Course("Дизайн", 0, 100)
course_eng = Course("Английский язык", 0, 100)

# зачисляем студентов на курсы
print("Зачисление студентов на курсы:")
course_prog.add_students(student_list)
course_design.add_students(student_list)
course_eng.add_students(student_list)
print("")

couses_list = [course_prog, course_design, course_eng]

# добавляем случайные оценки студентам
print("Добавление оценок студентам:")
for student in student_list:
    for course in couses_list:
        course.add_mark(student, random_mark())
print("")


# выставления финальных оценок по курсам
calc_course = CalculateCourse()
calc_course.print_results(couses_list)