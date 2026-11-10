symptom(ram, fever).
symptom(ram, cough).
symptom(ram, body_pain).

symptom(sita, sneezing).
symptom(sita, runny_nose).

symptom(raj, fever).
symptom(raj, headache).

% Simplified educational rules
diagnosis(Person, possible_flu) :-
    symptom(Person, fever),
    symptom(Person, cough),
    symptom(Person, body_pain).

diagnosis(Person, possible_common_cold) :-
    symptom(Person, sneezing),
    symptom(Person, runny_nose).

diagnosis(Person, requires_medical_review) :-
    symptom(Person, fever),
    symptom(Person, headache).




Output:
?- diagnosis(ram, Disease).
Disease = possible_flu.

?- diagnosis(sita, Disease).
Disease = possible_common_cold.

?- diagnosis(raj, Disease).
Disease = requires_medical_review.

?- diagnosis(unknown, Disease).
false.
