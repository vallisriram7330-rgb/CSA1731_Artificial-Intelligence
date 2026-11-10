hanoi(1, A, B, _) :-
    format('Move disk from ~w to ~w~n', [A, B]).
hanoi(N, A, B, C) :-
    N > 1,
    M is N - 1,
    hanoi(M, A, C, B),
    hanoi(1, A, B, C),
    hanoi(M, C, B, A).


Output:

?- hanoi(3, a, c, b).
Move disk from a to c
Move disk from a to b
Move disk from c to b
Move disk from a to c
Move disk from b to a
Move disk from b to c
Move disk from a to c
true.
