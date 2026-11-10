% Initial facts
fact(a).
fact(b).

% Rules deriving new conclusions
rule(c) :-
    fact(a),
    fact(b).

rule(d) :-
    rule(c).

rule(e) :-
    rule(d).



Output:
?- rule(c).
true.

?- rule(d).
true.

?- rule(e).
true.
