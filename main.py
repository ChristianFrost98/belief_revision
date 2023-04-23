"""
1 ) Belief base implementation
- Lav en klasse som kan afbilde en belief base og dets set af beliefs
- Her skal der laves support for the logiske operation OR, AND, NOT, osv.
- Denne model skal også kunne rumme en priortering af disse beliefs
- Det skal være muligt at printe denne belief base
- Det skal være muligt at intere denne belief base
"""



"""
2 ) Resolution base logical entailment
- You can implement the resolution-based method by writing a function that 
  takes in a set of formulas and a single formula and returns True if the set
  logically entails the single formula and False otherwise.
- Der skal implementeres en funktion til resolution for at tjekke entailment
"""



"""
3 ) Implementation of contraction of belief base:
- Her ønsker vi at tilføje et nyt belief til vores belief base, derfor skal
vi tjekke om dette belief bryder med nogle af vores eksisterende. Herved
skal resolution funktion til at tjekke om det nye belief passer ind.
- Her skal der benyttes AGM posulater til at tjekke om contraction var
en success
"""



"""
4 ) Implementation of expansion of belief base:
- Til sidst når man har fundet den bedst mulige revision af belief basen
som vil tillade at vi kan tilføje vores nye belief. Skal det nye belief
tilføres til belief basen. 
"""