# IA02 : Rapport de projet
DUPRE Manon - WACHNICKI Anoukhan

<br><br><br>  
# Sommaire : 
- Modélisation STRIPS 
- Fonctionnement de notre projet 
  - Phase 1
    - Fonctionnement de la phase
    - Forces et faiblesses
  - Phase 2
    - Fonctionnement de la phase
    - Forces et faiblesses

<br><br><br> 

# Modélisation STRIPS 

## Précisions des choix de modélisation, validées par Mr Lagrue : 
    - Nous n'écrirons pas tous les prédicats et fluents. En effet, différentes possibilités les concernant sont si nombreuses que nous n’en détaillerons que quelques-unes.
    - Nous ne nous occupons pas de la gestion des points pour le Strips, ainsi, nous ne gérons pas non plus la vue des gardes, de Hitman, ainsi que l’ouïe de Hitman.

<br>

## Prédicats : 
    guard(d, x, y)
    civil(d, x, y)
    pw(x, y)
    suit(x, y)
    walkable(x, y)
    next_clockwise(d1, d2)
    next_anti_clockwise(d1, d2)
    relative_pos1(d1, x1, y1, x2, y2)
    hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(d1, x1, y1, d2, x2, y2) 

<br> 

## Explications supplémentaires concernant certains prédicats : 

    - next_clockwise(d1, d2) et next_anti_clockwise(d1, d2) 
    Ces prédicats donnent, à partir d’une direction de base (d1), la prochaine direction dans le sens indiqué par le nom du prédicat (d2).

    - walkable(x, y) 
    walkable() correspond aux cases du jeu sur lesquelles hitman peut passer : c’est à dire toutes les cases sauf les murs et les gardes.

    - relative_pos1(d, x1, y1, x2, y2)
    Ce prédicat permet de savoir quand la case (x1, y1) est voisine d’une autre case (x2, y2), dans la direction d. Exemple : nous avons relative_pos(E, 0, 0, 1, 0) car la case (0, 0) est voisine avec la case (0, 0) qui est plus à l'Est.


    - hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(d1, x1, y1, d2, x2, y2)
    Nous avons  d1, x1, y1 qui correspondent à la direction et la position de hitman, et d2, x2, y2 qui correspondent à celles d’un garde ou d’un civil.
    Ce prédicat se base, pour chaque case possible, sur le raisonnement suivant : p correspond à une personne étant un garde ou un civil. Hitman et p sont sur des cases adjacentes. Nous nous intéressons aux cas où hitman voit p mais p ne le voit pas, via des couples (d1, d2) : 
    - si hitman est au dessus de p, nous avons : (S, non N) → (S, S), (S, W), (S, E)
    - si hitman est au dessous de p, nous avons : (N, non S) → (N, W), (N, N), (N, E)
    - si hitman est à gauche de p, nous avons : (E, non W) → (E, S), (E, N), (E, E)
    - si hitman est à droite de p, nous avons : (W, non E) → (W, N), (W, S), (W, W)
    Ici, l’idéal aurait été de ne pas faire cette modélisation en strips. En prolog, par exemple, nous aurions pu réutiliser le prédicat relative_pos1(d, x1, y1, x2, y2) pour définir person_close_but_don_t_see_hitman(d1, x1, y1, d2, x2, y2). Cela aurait permis de fortement gagner en efficacité. 

<br>  

## Fluents : 
    - hitman(d, x, y, p, s, so) : avec d pour direction (parmis N, E, S, W), p pour piano wire (True or False) (True si hitman possède l’objet sur lui), s pour suit (True or False), so pour “suit on” (hitman a passé le costume : True or False)

    - target(x, y, alive) : (x, y, alive), avec x et y pour les coordonnées, et alive un booléen exprimant si la cible est morte (False) ou vivante (True)

<br> 

## Constantes : 
    N, E, S, W : pour North, East, South, West

<br> 

## Init : 
    hitman(d, 1, 0, False, False, False) 
    ∧ target(0, 3, True) ∧ pw(5, 0) ∧ suit(3, 5) ∧ gard(N, 4, 5) ∧ civil(E, 3, 2)...  
    ∧ walkable(0, 0) ∧ walkable(0, 1) ∧ walkable(1, 0) ∧ walkable(1, 1) ∧ walkable(2, 1) ∧ ...  

    ∧ next_clockwise(N, E) ∧ next_clockwise(E, S) ∧ next_clockwise(S,  W) ∧ next_clockwise(W, N) ∧ next_anti_clockwise(N, W) ∧ next_anti_clockwise(W, S) ∧ next_anti_clockwise(S, E) ∧ next_anti_clockwise(E, N)

    ∧ relative_pos1(N, 0, 0, 0, 1) ∧ relative_pos1(E, 0, 0, 1, 0) ∧ relative_pos1(S, 0, 1, 0, 0) ∧ relative_pos1(S, 0, 1, 0, 2) ∧ ...

    ∧ hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(N, 4, 5, N, 4, 4) ∧ hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(N, 4, 5, S, 4, 4) ∧ hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(N, 4, 5, E, 4, 4) ∧ 
    hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(N, 4, 5, O, 4, 4) ∧ 
    hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(N, 4, 5, S, 5, 5) ∧ hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(N, 4, 5, E, 5, 5) ∧ 
    hitman_close_to_person_and_see_him_but_person_don_t_see_hitman(N, 4, 5, O, 5, 5) ∧ …

<br> 

## Goal : 
    hitman(d, 1, 0, True, s, so) ∧ target(0, 3, False) 

    En effet, hitman doit être revenu à la case de départ, et target doit être mort (alive = False).

<br> 

## Actions : 
    Action( turn_clockwise()
        Precond : hitman(d, x, y, p, s, so), next_clockwise(d, d2)
        Effect : hitman(d2, x, y, p, s, so) ∧ ¬hitman(d, x, y, p, s, so) )


    Action( turn_anti_clockwise()
        Precond : hitman(d, x, y, p, s, so), next_anti_clockwise(d, d2)
        Effect : hitman(d2, x, y, p, s, so) ∧ ¬hitman(d, x, y, p, s, so) )


    Action( advance(d)
        Precond : hitman(d, x, y, p, s, so) ∧ walkable(x1, y1)  ∧ Pos_relative_1(d, x, y, x1, y1)
        Effect : hitman(d, x1, y1, p, s, so) ∧ ¬hitman(d, x, y, p, s, so) )


    Action( take_piano_wire()
        Precond : hitman(d, x, y, False, s, so) ∧ pw(x, y)
        Effect : hitman(d, x, y, True, s, so) ∧ ¬pw(x, y) ∧ ¬hitman(d, x, y, False, s, so) )


    Action( take_suit()
        Precond : hitman(d, x, y, p, False, False) ∧ suit(x, y)
        Effect : hitman(d, x, y, p, True, False) ∧ ¬suit(x, y) ∧ ¬hitman(d, x, y, p, False, False)  )



    Action( put_suit_on()
        Precond : hitman(d, x, y, p, True, False)
        Effect : hitman(d, x, y, p, True, True) ∧ ¬hitman(d, x, y, p, True, False)  )

   
    Action( neutralise_guard()
        Precond : hitman(d, x, y, p, s, so) ∧ guard(d2, x2, y2) ∧ hitman_close_to_people_and_see_him_but_people_don_t_see_hitman(d, x, y, d2, x2, y2)
        Effect : ¬guard(d2, x2, y2) ∧ ¬hitman_close_to_people_and_see_him_but_people_don_t_see_hitman(d, x, y, d2, x2, y2) )


    Action( neutralise_civil()
        Precond : hitman(d, x, y, p, s, so) ∧ civil(d2, x2, y2) ∧ hitman_close_to_people_and_see_him_but_people_don_t_see_hitman(d, x, y, d2, x2, y2)
        Effect : ¬civil(d2, x2, y2) ∧ ¬hitman_close_to_people_and_see_him_but_people_don_t_see_hitman(d, x, y, d2, x2, y2) )


    Action( kill_target()
        Precond : hitman(d, x, y, True, s, so) ∧ target(x, y, True) 
        Effect : target(x, y, False) ∧ ¬target(x, y, True) )


<br> <br> <br>

# Fonctionnement de notre projet

## Phase 1
    
### Fonctionnement de la phase
    ...

<br>

### Forces et faiblesses
    ...

<br> <br>

## Phase 2

### Fonctionnement de la phase
    ...

<br>

### Forces et faiblesses
    ...


