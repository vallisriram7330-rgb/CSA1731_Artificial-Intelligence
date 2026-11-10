% Educational examples only
diet(diabetes, vegetables).
diet(diabetes, whole_grains).
diet(diabetes, fruits_in_moderation).

diet(hypertension, low_salt_food).
diet(hypertension, fruits).
diet(hypertension, vegetables).

diet(anemia, iron_rich_food).
diet(anemia, spinach).
diet(anemia, beans).

suggest_diet(Disease, Food) :-
    diet(Disease, Food).



Output:
?- suggest_diet(diabetes, Food).
Food = vegetables ;
Food = whole_grains ;
Food = fruits_in_moderation.

?- suggest_diet(hypertension, Food).
Food = low_salt_food ;
Food = fruits ;
Food = vegetables.

?- suggest_diet(anemia, Food).
Food = iron_rich_food ;
Food = spinach ;
Food = beans.

?- suggest_diet(malaria, Food).
false.
