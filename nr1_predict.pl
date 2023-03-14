
% - A team consists out of the 11 best players based on OVR
% team(N1,X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,X11) (X_ = Integer = OVR)
% - Table is a list of teams

maplist(_,[],[]).
maplist(P,[A|As],[B|Bs]) :- call(P,A,B),maplist(P,As,Bs).

% (Points,Team)
zipToZero(Team,(0,Team)).
unzip((P,T),T).

predict_table(Teams,NR1) :-
    maplist(zipToZero,Teams,ZippedTeams),
    predictHelper(ZippedTeams,[],[NR1P|Others]),
    unzip(NR1P,NR1).

predictHelper([],IntermedTable,Table) :-
    sort(IntermedTable,Table).
predictHelper([(P1,T1)|PTs],IntermedTable,Table) :-
    play_others((P1,T1),PTs,P1New,PTsNew),
    predictHelper(PTsNew,[(P1New,T1)|IntermedTable],Table).

play_others((P,T),[],P,[]).
play_others((P,T), [(P2,T2)|PTs], FinalP1, [(NewP2,T2)|Rest]) :-
    T \= T2,
    (ResultH = win,
    ResultA = win,
    NewP is P - 3, % Minus so sort works in right order
    NewP2 is P2 - 3
    ;
    ResultH = win,
    ResultA = loss,
    NewP is P - 6,
    NewP2 is P2
    ;
    ResultH = loss,
    ResultA = win,
    NewP is P,
    NewP2 is P2 - 6
    ;
    ResultH = loss,
    ResultA = loss, 
    NewP is P - 3,
    NewP2 is P2 - 3
    ),
    play(T,T2,ResultH), % At home
    play(T2,T,ResultA), % Away 
    play_others((NewP,T),PTs,FinalP1,Rest).

nn(game_result,[P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11],Y,[win,loss]) :: play(team(N1,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11),team(N2,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11),Y).