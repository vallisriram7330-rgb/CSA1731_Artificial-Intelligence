person(ram, date(10, 5, 2004)).
person(sita, date(15, 8, 2003)).
person(raj, date(20, 12, 2004)).
person(kumar, date(25, 3, 2005)).

display(Name, DOB) :-
    person(Name, DOB).

Output:
?- display(ram, DOB).
DOB = date(10, 5, 2004).
