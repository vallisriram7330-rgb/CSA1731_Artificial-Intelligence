% State: state(MonkeyPosition, BoxPosition, MonkeyStatus, HasBanana)

move(state(P, B, on_floor, no),
     state(Q, B, on_floor, no)) :-
    adjacent(P, Q).

push_box(state(P, P, on_floor, no),
         state(middle, middle, on_floor, no)) :-
    P \= middle.

climb_box(state(middle, middle, on_floor, no),
          state(middle, middle, on_box, no)).

grasp_banana(state(middle, middle, on_box, no),
             state(middle, middle, on_box, yes)).

adjacent(door, window).
adjacent(window, middle).
adjacent(middle, door).
adjacent(window, door).
adjacent(door, middle).

can_get_banana :-
    Initial = state(door, window, on_floor, no),
    move(Initial, S1),
    push_box(S1, S2),
    climb_box(S2, S3),
    grasp_banana(S3, Final),
    Final = state(_, _, _, yes),
    writeln('Monkey gets the banana successfully.').






Output:
?- can_get_banana.
Monkey gets the banana successfully.
true.
