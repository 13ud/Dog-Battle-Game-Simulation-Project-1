def listconversion(pack):
    """ HELPER FUNCTION, that rewrites each dog in the packs from a tuple to a
    list, so DP and HP can be adjusted without assigning external variables
    Input:
    - pack, a list of dog candidate tuples """

    doginfo = []
    dogs = []

    for info in pack:
        doginfo.append(list(info))
        dogs.append(info[0])

    return doginfo, dogs


def corgi_effect(leftdog, rightdog):
    """ HELPER FUNCTION, Returns tuple of the adjusted dog info lists.
    Checks whether the knocked out pack leader is a 'corgi' breed, and also IF
    there are any other AWAKE dogs besides the pack leader. IF both conditions
    are satisfied for a dog pack, the corgi's special effect will take place,
    giving the next dog in line the leader's DP.
    Input:
    - leftdog, a list of dog candidate tuples part of the left dog pack
    - rightdog, a list of dog candidate tuples part of the right dog pack """

    if leftdog[0][2] <= 0 and leftdog[0][0] == 'corgi' and len(leftdog) > 1:
        leftdog[1][1] += leftdog[0][1]

    if rightdog[0][2] <= 0 and rightdog[0][0] == 'corgi' and len(rightdog) > 1:
        rightdog[1][1] += rightdog[0][1]

    return leftdog, rightdog


def sim_enhanced_battle(lpack, rpack):
    """ Returns a tuple of the battle outcome (the winning side, or a tie)
    and the winning pack's remaining alive dogs. This function accomodates
    for the special effects of different breeds, where each pack leader
    simultaneously attacks until one team has all been knocked out.
    Input:
    - lpack, a list of dog candidate tuples part of the left dog pack
    - rpack, a list of dog candidate tuples part of the right dog pack """

    # Uses helper function to rewrite dog info from tuple to list, so DP and
    # HP values can be adjusted directly without assigning to another variable
    doginfoleft, dogsleft = listconversion(lpack)
    doginforight, dogsright = listconversion(rpack)

    # initialising counter to restrict the 'golden' HP effect to 1 per duel
    repeatduel = 0

    # Makes sure that when all the pack is knocked out (i.e. removed
    # from the list), the function stops the battle, and returns the results
    while doginfoleft != [] and doginforight != []:

        # calculates the number of AWAKE 'husky' dogs in both packs
        huskycounter = dogsleft.count('husky') + dogsright.count('husky')

        # Runs through the list of dogs on each side to check for any golden
        # breeds present. For every one found, the pack leader gains +4 HP
        # NOTE: the condition repeat < 1 makes sure that the golden breed's
        # special effect is only applied ONCE EVERY DUEL, NOT EVERY ATTACK
        for dogs in dogsleft:
            if dogs == 'golden' and repeatduel < 1:
                doginfoleft[0][2] += 4

        for dogs in dogsright:
            if dogs == 'golden' and repeatduel < 1:
                doginforight[0][2] += 4

        repeatduel += 1

        # Checks whether each pack leader is a 'husky' breed, and if so will
        # add 2 to its DP for every AWAKE 'husky' present in both packs
        if dogsleft[0] == 'husky':
            doginfoleft[0][1] += 2 * huskycounter

        if dogsright[0] == 'husky':
            doginforight[0][1] += 2 * huskycounter

            # Simulates the duel by decreasing the HP of each pack leader by their
        # opposing pack leader's DP value
        doginforight[0][2] -= doginfoleft[0][1]
        doginfoleft[0][2] -= doginforight[0][1]

        # this condition is satisfied if both pack leaders are knocked out
        # simultaneously in a duel, and so removes both from their pack lists
        # And applies the helper function 'corgi_effect' when conditions met
        if doginfoleft[0][2] <= 0 and doginforight[0][2] <= 0:
            doginfoleft, doginforight = corgi_effect(doginfoleft, doginforight)

            dogsleft.pop(0)
            dogsright.pop(0)
            doginfoleft.pop(0)
            doginforight.pop(0)

            # Resets the repeat counter after EVERY DUEL, NOT EVERY ATTACK
            repeatduel = 0

            # When ONLY the left pack leader is knocked out in the duel, this
        # condition is satisfied, so the leader is removed from the left pack
        # And the helper function 'corgi_effect' is applied.
        elif doginfoleft[0][2] <= 0:
            doginfoleft = corgi_effect(doginfoleft, doginforight)[0]

            dogsleft.pop(0)
            doginfoleft.pop(0)

            repeatduel = 0

            # When ONLY the right pack leader is knocked out in the duel, this
        # condition is satisfied, so the dog is removed from the right pack
        elif doginforight[0][2] <= 0:
            doginforight = corgi_effect(doginfoleft, doginforight)[1]

            dogsright.pop(0)
            doginforight.pop(0)

            repeatduel = 0

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


print(sim_enhanced_battle([("corgi", 6, 5), ("husky", 3, 4)], [("golden", 2, 2), ("golden", 3, 9)]))

print(sim_enhanced_battle([("corgi", 6, 5), ("husky", 3, 4)], [("corgi", 2, 2), ("golden", 3, 9)]))

print(sim_enhanced_battle([("golden", 4, 4), ("golden", 4, 7), ("golden", 4, 11), ("golden", 6, 12)],
                          [("golden", 21, 4)]))

print(sim_enhanced_battle([("corgi", 1, 1), ("corgi", 1, 1), ("corgi", 1, 1), ("corgi", 1, 1), ("corgi", 1, 1)],
                          [("normal", 1, 10)]))

print(sim_enhanced_battle([("husky", 1, 25)], [("husky", 1, 1), ("husky", 1, 1), ("husky", 1, 1)]))

print(sim_enhanced_battle([], []))



