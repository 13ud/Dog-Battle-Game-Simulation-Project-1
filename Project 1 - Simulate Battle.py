def listconversion(pack):
    """ Helper function that rewrites each dog in the packs from a tuple to a
    list, so DP and HP can be adjusted without assigning external variables
    Input:
    - pack, a list of dog candidate tuples """

    doginfo = []
    dogs = []

    for info in pack:
        doginfo.append(list(info))
        dogs.append(info[0])

    return doginfo, dogs


def sim_battle(lpack, rpack):
    """ Returns a tuple of the battle outcome (the winning side, or a tie)
    and the winning pack's remaining alive dogs. Simulates a battle
    between the pack leaders until a team (or both) is all knocked out.
    This function does not consider the breed's special effects.
    Input:
    - lpack, a list of dog candidate tuples part of the left dog pack
    - rpack, a list of dog candidate tuples part of the right dog pack """

    # Uses helper function to rewrite dog info from tuple to list, so DP and
    # HP values can be adjusted directly without assigning to another variable
    doginfoleft, dogsleft = listconversion(lpack)
    doginforight, dogsright = listconversion(rpack)

    # Makes sure that when all the pack is knocked out (i.e. removed
    # from the list), the function stops the battle, and returns the results
    while doginfoleft != [] and doginforight != []:
        doginfoleft[0][2] -= doginforight[0][1]
        doginforight[0][2] -= doginfoleft[0][1]

        # this condition is satisfied if both pack leaders are knocked out
        # simultaneously in a duel, and so removes both from their pack lists
        if doginfoleft[0][2] <= 0 and doginforight[0][2] <= 0:
            doginfoleft.pop(0)
            doginforight.pop(0)


        # When ONLY the left pack leader is knocked out in the duel, this
        # condition is satisfied, so the dog is removed from the left pack
        elif doginfoleft[0][2] <= 0:
            doginfoleft.pop(0)


        # When ONLY the right pack leader is knocked out in the duel, this
        # condition is satisfied, so the dog is removed from the right pack
        elif doginforight[0][2] <= 0:
            doginforight.pop(0)

    # Tests if either the left or right pack team has any dogs present after
    # the battle is done, If so, it is the winning team and will return
    # a tuple of the winning side and the remaining dogs awake in the pack
    doglist = []
    if doginfoleft != []:
        for dogs in doginfoleft:
            doglist.append(tuple(dogs))
        return 'L', doglist

    elif doginforight != []:
        for dogs in doginforight:
            doglist.append(tuple(dogs))
        return 'R', doglist

    return 'T', []





