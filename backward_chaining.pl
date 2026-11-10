parent(ram, arjun).
parent(arjun, kumar).
parent(kumar, priya).

grandparent(X, Z) :-
    parent(X, Y),
    parent(Y, Z).

ancestor(X, Y) :-
    parent(X, Y).

ancestor(X, Y) :-
    parent(X, Z),
    ancestor(Z, Y).


Output:

?- grandparent(ram, kumar).
true.

?- ancestor(ram, kumar).
true.

?- ancestor(ram, X).
X = arjun ;
X = kumar ;
X = priya.
