#  typage clauses : abcisse_ordonnée_élément
#  ex : 0_0_1
class Nb_elt (Enum):
    EMPTY = 1
    WALL = 2
    GUARD_N = 3
    GUARD_E = 4
    GUARD_S = 5
    GUARD_W = 6
    CIVIL_N = 7
    CIVIL_E = 8
    CIVIL_S = 9
    CIVIL_W = 10
    TARGET = 11
    SUIT = 12
    PIANO_WIRE = 13

m = 3 #taille abcisse
n = 2 #taille ordonnée
nb_elt = 13
clause = []
clause_neg = []
kb = []
#################### Encodage des règles ####################


######### Rule 1 : chaque case possède un unique élément (enum Elt) (on compte empty comme un élément)
 # R1.a : there are at least one element per case
 # clauses de type : 0_0_1 ou 0_0_2 ou ... ou 0_0_13, et ce, pour chaque case 
at_least_one_R1 = []
at_least_one_R1_neg = [] # sera utilisée pour la création de la clause au plus un

for i in range (0, m) :
    for j in range (0, n) :
        for k in Elt :
            clause.append(f"{i}_{j}_{k.value}")
            clause_neg.append(f"-{i}_{j}_{k.value}")
        at_least_one_R1.append(clause)
        at_least_one_R1_neg.append(clause_neg)
        clause = []
        clause_neg = []
print(f"at_least_one_R1 = {at_least_one_R1}\n")
print(f"at_least_one_R1_neg = {at_least_one_R1_neg}\n")
    
        
# R1.b : there is at most one element per case 
# clauses de type : ["-0_0_1", "-0_0_1", ... , "-0_0_k" ]
at_most_one_R1 = []
for l in at_least_one_R1_neg :
    for c in combinations(l,2) : # permet d'ajouter les tuples un par un dans at_most_one_R1
        at_most_one_R1.append(c)
print(f"at_most_one_R1 = {at_most_one_R1}\n")






######### Rule 2 : there are exactly one piano wire, one suit and one target on the map

#R2.a there are at least one piano wire, one suit and one target on the map
# clause de type : ["0_0_11", "0_1_11", ..., "n_m_11"] (exemple pour la target)

at_least_one_pw = []
at_least_one_suit = []
at_least_one_target = []
at_least_one_pw_neg = []
at_least_one_suit_neg = []
at_least_one_target_neg = []

for i in range (0, m) :
    for j in range (0, n) :
        at_least_one_pw.append(f"{i}_{j}_{Elt.PIANO_WIRE.value}")
        at_least_one_pw_neg.append(f"-{i}_{j}_{Elt.PIANO_WIRE.value}")

        at_least_one_suit.append(f"{i}_{j}_{Elt.SUIT.value}")
        at_least_one_suit_neg.append(f"-{i}_{j}_{Elt.SUIT.value}")

        at_least_one_target.append(f"{i}_{j}_{Elt.TARGET.value}")
        at_least_one_target_neg.append(f"-{i}_{j}_{Elt.TARGET.value}")

print(f"at_least_one_pw = {at_least_one_pw}\n")
print(f"at_least_one_pw_neg = {at_least_one_pw_neg}\n")
print(f"at_least_one_suit = {at_least_one_suit}\n")
print(f"at_least_one_suit_neg = {at_least_one_suit_neg}\n")
print(f"at_least_one_target = {at_least_one_target}\n")
print(f"at_least_one_target_neg = {at_least_one_target_neg}\n")




# R2.b : there are at most one piano wire, one suit and one target on the map
#  clauses de type [('-0_0_13', '-0_1_13'), ('-0_0_13', '-1_0_13'), ('-0_0_13', '-1_1_13')...
at_most_one_R2 = []
for l in [at_least_one_pw_neg, at_least_one_suit_neg, at_least_one_target_neg] :
    print(f"l : {l}\n")
    for c in combinations(l,2) : # permet d'ajouter les tuples un par un dans regle1b
        at_most_one_R2.append(c)
print(f"at_most_one_R2 = {at_most_one_R2}\n")





######### Rule 3 : there are exactly nb_guards guards and nb_civils civils on the map 
# /!\ We have to take into account the direction of the guards and civils : we have 8 elements 

#R3.a there are at least nb_guards guards and nb_civils civils on the map 
at_least_nb_guards = []
at_least_nb_civils = []
for i in range (0, m) :
    for j in range (0, n) :
        at_least_nb_civils.append(f"{i}_{j}_{Elt.PIANO_WIRE.value}")
        at_least_one_pw_neg.append(f"-{i}_{j}_{Elt.PIANO_WIRE.value}")

        at_least_one_suit.append(f"{i}_{j}_{Elt.SUIT.value}")
        at_least_one_suit_neg.append(f"-{i}_{j}_{Elt.SUIT.value}")

        at_least_one_target.append(f"{i}_{j}_{Elt.TARGET.value}")
        at_least_one_target_neg.append(f"-{i}_{j}_{Elt.TARGET.value}")

print(f"at_least_one_pw = {at_least_one_pw}\n")
print(f"at_least_one_pw_neg = {at_least_one_pw_neg}\n")
print(f"at_least_one_suit = {at_least_one_suit}\n")
print(f"at_least_one_suit_neg = {at_least_one_suit_neg}\n")
print(f"at_least_one_target = {at_least_one_target}\n")
print(f"at_least_one_target_neg = {at_least_one_target_neg}\n")









#regle .. : quand je vois le contenu d'une case, je l'ajoute à ma KB
#  exemple : je vois du clear en (2,2) : on ajoute la clause ["2_2_1"] à la KB