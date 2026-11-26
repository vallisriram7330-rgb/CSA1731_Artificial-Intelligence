% Allow dynamic modification of facts in the knowledge base during execution
:- dynamic fact/1.

% --- INITIAL FACTS ---
fact(american(west)).
fact(enemy(nono, america)).
fact(owns(nono, m1)).
fact(missile(m1)).

% --- FORWARD CHAINING RULES ---
% Syntax: rule(Premises_List, Conclusion)

% Rule 1: Missiles are weapons
rule([missile(X)], weapon(X)).

% Rule 2: An enemy of America is hostile
rule([enemy(X, america)], hostile(X)).

% Rule 3: If Nono owns a missile, West sold it to Nono
rule([missile(X), owns(nono, X)], sells(west, X, nono)).

% Rule 4: If an American sells a weapon to a hostile nation, they are a criminal
rule([american(X), weapon(Y), hostile(Z), sells(X, Y, Z)], criminal(X)).

% --- INFERENCE ENGINE ---

% Main entry point to start forward chaining
forward_chain :-
    new_fact_derived(NewFact), !,
    write('Derived new fact: '), write(NewFact), nl,
    assertz(fact(NewFact)),
    forward_chain.
forward_chain :-
    write('--- Forward chaining complete. No more new facts can be derived. ---'), nl.

% Finds a rule whose premises are all satisfied, but whose conclusion is not yet known
new_fact_derived(Conclusion) :-
    rule(Premises, Conclusion),
    \+ fact(Conclusion),          % Ensure the conclusion is not already in the database
    all_premises_true(Premises).  % Check if all conditions in the premise list hold

% Recursively verify that every premise exists as a known fact
all_premises_true([]).
all_premises_true([Premise | Rest]) :-
    fact(Premise),
    all_premises_true(Rest).

% Helper predicate to display all facts currently in the knowledge base
show_facts :-
    write('Current Knowledge Base:'), nl,
    forall(fact(F), (write('  - '), write(F), nl)).
