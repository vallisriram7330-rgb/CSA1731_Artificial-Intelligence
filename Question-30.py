% Entry point
start :-
    retractall(known(_, _)),
    write('Enter patient name (in quotes, e.g., ravi): '),
    read(Patient),
    (   hypothesis(Patient, Disease) ->
        format('~w probably has ~w.~n', [Patient, Disease])
    ;   write('Sorry, a diagnosis could not be determined from the given symptoms.'), nl
    ).

% Diagnostic rules (hypotheses)
hypothesis(Patient, flu) :-
    symptom(Patient, fever),
    symptom(Patient, body_ache),
    symptom(Patient, cough).

hypothesis(Patient, common_cold) :-
    symptom(Patient, runny_nose),
    symptom(Patient, sneezing),
    symptom(Patient, sore_throat).

hypothesis(Patient, migraine) :-
    symptom(Patient, headache),
    symptom(Patient, nausea).

% Symptom definitions
symptom(Patient, fever)      :- ask(Patient, 'have a fever').
symptom(Patient, body_ache)  :- ask(Patient, 'have body aches').
symptom(Patient, cough)      :- ask(Patient, 'have a cough').
symptom(Patient, runny_nose) :- ask(Patient, 'have a runny nose').
symptom(Patient, sneezing)   :- ask(Patient, 'have sneezing').
symptom(Patient, sore_throat):- ask(Patient, 'have a sore throat').
symptom(Patient, headache)   :- ask(Patient, 'have a headache').
symptom(Patient, nausea)     :- ask(Patient, 'have nausea').

% Dynamic memory to avoid asking the same symptom twice
:- dynamic known/2.

ask(Patient, Question) :-
    known(Symptom, Reply), !,
    Reply == y.

ask(Patient, Question) :-
    format('Does ~w ~w (y/n)? ', [Patient, Question]),
    read(Reply),
    assert(known(Question, Reply)),
    Reply == y.
