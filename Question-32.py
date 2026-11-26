% --- FACTS (Known Truths) ---
american(west).
missile(m1).
owns(nono, m1).
enemy(nono, america).

% --- RULES (Inference Logic) ---

% Rule 1: If X is a missile, then X is a weapon.
weapon(X) :- 
    missile(X).

% Rule 2: If X is an enemy of America, then X is hostile.
hostile(X) :- 
    enemy(X, america).

% Rule 3: If X is a missile and Nono owns X, then West sells X to Nono.
sells(west, X, nono) :- 
    missile(X), 
    owns(nono, X).

% Rule 4 (Main Goal Rule): It is a crime for an American (X) to sell 
% weapons (Y) to a hostile nation (Z).
criminal(X) :- 
    american(X), 
    weapon(Y), 
    sells(X, Y, Z), 
    hostile(Z).
