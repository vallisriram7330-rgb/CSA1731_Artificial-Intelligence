student(ram, teacher1, cs101).
student(sita, teacher2, cs102).
student(raj, teacher1, cs103).
student(kumar, teacher3, cs104).

teacher(teacher1, john).
teacher(teacher2, david).
teacher(teacher3, peter).

subject(cs101, computer_science).
subject(cs102, mathematics).
subject(cs103, physics).
subject(cs104, chemistry).

details(Student, Teacher, Subject) :-
    student(Student, Teacher, Subject).

teacher_name(Student, Name) :-
    student(Student, T, _),
    teacher(T, Name).


Output:
?- details(ram, T, S).
T = teacher1,
S = cs101.

?- teacher_name(sita, Name).
Name = david.
