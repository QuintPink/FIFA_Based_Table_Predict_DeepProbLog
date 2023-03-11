
% - A team consists out of the 11 best players based on OVR
% team(X1,X2,X3,X4,X5,X6,X7,X8,X9,X10,X11) (X_ = Integer = OVR)
% - Table is a list of teams
maplist(_,[],[]).
maplist(P,[A|As],[B|Bs]) :- call(P,A,B),maplist(P,As,Bs).

% (Points,Team)
zipToZero(Team,(0,Team)).
unzip((P,T),T).

predict_table(Teams,Table) :-
    maplist(zipToZero,Teams,ZippedTeams),
    predictHelper(Teams,ZippedTeams,RTable),
    maplist(unzip,RTable,Table).

predictHelper([],IntermedTable,Table) :-
    sort(IntermedTable,RTable),
    reverse(RTable,Table).
predictHelper([T1|Ts],IntermedTable,Table) :-
    member((P1,T1),IntermedTable),
    play_others((P1,T1),IntermedTable,ResultTable),
    predictHelper(Ts,ResultTable,Table).

play_others((P,T),[],[(P,T)]).
play_others((P,T),[(_,T)|Ts],Rest) :-
    play_others((P,T),Ts,Rest).
play_others((P,T), [(P2,T2)|Ts], [(NewP2,T2)|Rest]) :-
    T \== T2,
    play(T,T2,Result),
    (Result == win,
    NewP is P + 3,
    NewP2 is P2
    ;
    Result == draw,
    NewP is P + 1,
    NewP2 is P2 + 1
    ;
    Result == loss,
    NewP is P,
    NewP2 is P + 3
    ),
    play_others((NewP,T),Ts,Rest).

nn(game_result,[X],Y,[win,draw,loss]) :: play(team(N1,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11),team(N2,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,B11),Y).