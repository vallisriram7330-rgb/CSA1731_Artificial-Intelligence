bird(sparrow).
bird(parrot).
bird(pigeon).
bird(eagle).
bird(penguin).
bird(ostrich).

can_fly(sparrow).
can_fly(parrot).
can_fly(pigeon).
can_fly(eagle).

cannot_fly(penguin).
cannot_fly(ostrich).

bird_status(Bird, 'can fly') :-
    can_fly(Bird).
bird_status(Bird, 'cannot fly') :-
    cannot_fly(Bird).


Output:
?- bird_status(sparrow, Status).
Status = 'can fly'.

?- bird_status(penguin, Status).
Status = 'cannot fly'.

?- bird_status(ostrich, Status).
Status = 'cannot fly'.

?- bird_status(tiger, Status).
false.
