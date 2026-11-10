male(ram).
male(arjun).
male(kumar).
female(sita).
female(priya).
female(radhu).

parent(ram, arjun).
parent(sita, arjun).
parent(ram, priya).
parent(sita, priya).
parent(arjun, kumar).
parent(radhu, kumar).

father(X, Y) :-
    parent(X, Y),
    male(X).

mother(X, Y) :-
    parent(X, Y),
    female(X).

sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

brother(X, Y) :-
    sibling(X, Y),
    male(X).

sister(X, Y) :-
    sibling(X, Y),
    female(X).

grandparent(X, Z) :-
    parent(X, Y),
    parent(Y, Z).








Output:
?- father(ram, arjun).
true.

?- mother(sita, priya).
true.

?- sibling(arjun, priya).
true.

?- grandparent(ram, kumar).
true.
