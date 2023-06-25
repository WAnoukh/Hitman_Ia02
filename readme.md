# IA02 : Rapport de projet
DUPRE Manon - WACHNICKI Anoukhan

<br><br><br>  
# Sommaire : 
- Faire fonctionner le projet
- Modélisation STRIPS 
- Fonctionnement de notre projet 
  - Phase 1
    - Fonctionnement de la phase
    - Forces et faiblesses
  - Phase 2
    - Fonctionnement de la phase
    - Forces et faiblesses

<br><br><br> 

# Faire fonctionner le projet

Il est important de :
* **Exécuter** le fichier **main.py**
* Que l'**arbitre** soit localisé dans le fichier **./hitman/hitman.py** relativement a main.py et se nomme **HitmanReferee**. (a moins de changer tout les 'from hitman.hitman import HitmanReferee' par l'importation voulue)
* Que gophersat.exe soit présent dans le même dossier que main.py (En réalité il n'est pas utilisé dans le projet, c'est seulement si vous voulez tester les fonctions présentes du SAT)


# Modélisation STRIPS 

## Précisions des choix de modélisation, validées par M. Lagrue : 
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
La phase 1 fonctionne de la manière suviante:
* On initialise une carte "vide" qui va nous servir de base de connaissance.
* Après chaque déplacement, nous la complétons avec ce qu'Hitman voit.
* Pour le déplacement, nous cherchons une case de la carte dont le contenu est encore inconnu (la plus proche possible). Ensuite nous lançons un A* afin de chercher un chemin efficace jusqu'a cette case (en supposant que les cases encore inconnue sont des cases du type HC.EMPTY). Nous allons ensuite effectuer uniquement la première action du chemin du A* afin de prendre en compte les informations nouvellement dévoilées. 
<br>Une fois les nouvelles informations enregistrées dans notre carte des connaissances, nous relançons un autre A* vers la même case que précédemment. Une fois cette case finalement atteinte, nous en choisissons une autre, ainsi de suite jusqu'à avoir tout découvert.

Le fonctionnement du A* sera expliqué dans la Phase 2

Toutes les fonctions nécessaires à l'ajout de déduction SAT sont quasiment présentes :
* L'ajout de clause lors de l'exploration
* L'initialisation de la base de clause avec les règles du jeu (sauf pour ce qui est de lier les cases où l'on se fait voir par un garde et la présence de garde)

Nous avons pris comme littéraux :
* **Les gardes** (avec un littéral pour chaques position et orientation possible)
* **Un garde simple** (comme avant mais sans prendre en compte l'orientation du garde, des CNF permettent de codes qu'un garde simple équivalent à un unique garde nord, sud, est ou ouest)
* La même chose pour les **civils**
* Une clause **seen** qui permet de renseigner si on s'est fait voir par un guard sur une case particulière (dérivé pour chaque position)
* Une clause **sound** qui permet de renseigner le nombre de personnes entendu sur une case (dérivé aussi pour chaque position)

Nous n'avons pas finalisé l'implémentation du SAT car nous n'avons pas codé la génération des clauses liant les littéraux **seen** des **gardes**. Mais nous comptions faire une déduction avant de lancer un A* pour trouver le chemins vers une case inconnue afin de choisir une autre case si on pouvait déduire le type de la case précédente.
<br>

### Forces et faiblesses
Sytème assez rapide, cependant vers la fin de son exécution, quand les cases inconnues sont peu nombreuses, elles ont tendance à être très éparpillées et hitman aura tendance à faire des allés retours inutiles. C'est ici que le SAT aurait été très utile car ces cases isolées sont donc très probablement déductible.

<br> <br>

## Phase 2

### Fonctionnement de la phase
La phase 2 est entièrement réalisé par un **A***.

Les états sont identifiés par le **"status"** renvoyé par l'HitmanReferee (avec la pénalité mise à 0). En effet, le status permet de définir parfaitement la situation de la phase 2 et le fait d'annuler les pénalités permet de se rendre compte quand deux chemin mènent vers le même "status" et de comparer leurs heuristiques pour décider du meilleur chemin.

Les états de succès ( qui terminent la recherche) sont ceux où hitman est en (0,0) et a tué sa cible (is_target_down est vrai). Pour le A* utilisé dans la phase 1 les états finaux sont ceux où hitman à atteint la case voulue.

Les successeurs des états sont tous les "status" que l'on peut obtenir après avoir effectué une action comme un déplacement ou bien un ramassage d'objet ou l'enfilage de combinaison (et toutes les autres).
<br>.
Nous filtrons cependant les status qui sont invalides (avoir avancé sur un mur ou avoir récupéré un objet qui n'est pas présent) ou les status qui résultent d'actions stupides (tourner 3 fois dans la même direction, tourner dans un sens puis dans l'autre, retourner à un emplacement qu'on a quitté avec une direction différente alors que nous avons effectué aucune action significative)

Pour générer ces **"status"** et les pénalités qui vont avec, nous utilisons un **Oracle** (classe identique à HitmanReferee) sur lequel un execute les actions voulues.

L'Heuristique est calculée comme suit :
* L'heuristique initialisée au nombre de pénalités (en effet on cherche à les minimiser)
* Si Hitman n'a pas pris la corde, on rajoute à l'heuristique la **distance** de Manhattan entre **hitman** et la **corde** ainsi que de la **distance** entre la **corde** et la **cible**.<br>On rajoute aussi **+4**
* Si Hitman n'as pas tué sa cible, on rajoute à l'heuristique la **distance** de Manhattan entre **hitman** et la **cible** ainsi que de la **distance** entre la **cible** et la **position (0,0)**.<br>On rajoute aussi **+2**
* Si aucun des deux, on rajoute à l'heuristique la **distance** de Manhattan entre **hitman** et la **position (0,0)**

Le fait de rajouter les distance entre les objectifs courant et les prochains objectif dans l'heuristique servent à rendre l'heuristique parfaitement **décroissante** au fur et à mesure qu'on se rapproche du but final.
Ainsi, l'heuristique sera toujours plus grande lorsque Hitman n'aura pas pris la corde que quand il l'aura récupérée.<br>
A l'exception du moment où Hitman ait écopé de beacon de pénalité, mais dans ce cas il est intéressant que l'heuristique soit grande afin d'explorer des possibilités avant la récupération de la corde (Comme tuer un garde qui la surveille, cela coutes des points, mais est avantageux finalement).
Ceci est aussi vrai pour l'assassinat de la cible.
<br>
Les **+2** et **+4** sont la pour s'assurer qu'au moment de récupérer la corde ou d'avoir tué la cible, l'heuristique compense les pénalités de ces actions, afin que l'A* continue d'explorer cette voie plutôt que de regarder des voies qui n'ont pas encore effectué cette action.
<br>

### Forces et faiblesses
La force de cette implémentation est qu'elle est très efficace et donne quasiment toujours le meilleur chemin. Elle s'adapte très bien à la subtilité des assassinats de garde pour libérer un chemin en avance.
<br>
Cependant, elle est assez longue pour les grandes cartes.


