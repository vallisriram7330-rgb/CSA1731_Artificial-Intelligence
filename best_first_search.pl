edge(a, b).
edge(a, c).
edge(b, d).
edge(b, e).
edge(c, f).
edge(d, g).
edge(e, g).
edge(f, g).

heuristic(a, 7).
heuristic(b, 6).
heuristic(c, 4).
heuristic(d, 5).
heuristic(e, 3).
heuristic(f, 2).
heuristic(g, 0).

best_first(Start, Goal, Path) :-
    search([[Start]], Goal, ReversePath),
    reverse(ReversePath, Path).

search([[Goal|Rest]|_], Goal, [Goal|Rest]).

search([[Node|Rest]|OtherPaths], Goal, Path) :-
    findall([Next,Node|Rest],
            (edge(Node,Next),
             \+ member(Next,[Node|Rest])),
            NewPaths),
    append(OtherPaths,NewPaths,AllPaths),
    sort_frontier(AllPaths,Sorted),
    search(Sorted,Goal,Path).

sort_frontier(Paths,Sorted) :-
    findall(H-P,
            (member(P,Paths),
             P=[Node|_],
             heuristic(Node,H)),
            Pairs),
    keysort(Pairs,SortedPairs),
    remove_keys(SortedPairs,Sorted).

remove_keys([],[]).
remove_keys([_-P|Rest],[P|Paths]) :-
    remove_keys(Rest,Paths).





Output:
?- best_first(a, g, Path).
Path = [a, c, f, g].
