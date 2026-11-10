fruit_colour(apple, red).
fruit_colour(apple, green).
fruit_colour(banana, yellow).
fruit_colour(orange, orange).
fruit_colour(grapes, purple).
fruit_colour(mango, yellow).
fruit_colour(guava, green).

fruit(Fruit, Colour) :-
    fruit_colour(Fruit, Colour).




Output:
?- fruit(apple, Colour).
Colour = red ;
Colour = green.

?- fruit(Fruit, yellow).
Fruit = banana ;
Fruit = mango.

?- fruit(grapes, Colour).
Colour = purple.
