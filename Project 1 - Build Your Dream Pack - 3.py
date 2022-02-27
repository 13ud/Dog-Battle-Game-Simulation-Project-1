from itertools import permutations
# from reference import sim_enhanced_battle

def listconversion(pack):
    """ Helper function that rewrites each dog in the packs from a tuple to a
    list, so DP and HP can be adjusted directly without assigning externally"""
    doginfo = []
    dogs = []

    for info in pack:
        doginfo.append(list(info))
        dogs.append(info[0])

    return doginfo, dogs


def sim_enhanced_battle(lpack, rpack):
    """ Returns a tuple of the battle outcome (the winning side, or a tie)
        and the winning pack's remaining alive dogs. This function accomodates
        for the special effects of different breeds, where each pack leader
        simultaneously attacks until one team has all been knocked out. """

    # Uses helper function to rewrite dog info from tuple to list, so DP and
    # HP values can be adjusted directly without assigning to another variable
    doginfoleft, dogsleft = listconversion(lpack)
    doginforight, dogsright = listconversion(rpack)

    # initialising counter to control the 'golden' special effect per duel
    repeat = 0

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
            if dogs == 'golden' and repeat < 1:
                doginfoleft[0][2] += 4

        for dogs in dogsright:
            if dogs == 'golden' and repeat < 1:
                doginforight[0][2] += 4

        repeat += 1

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
        if doginfoleft[0][2] <= 0 and doginforight[0][2] <= 0:

            # Checks whether the knocked out pack leader is a 'corgi' breed,
            # and also IF there are other AWAKE dogs than just the pack leader.
            # When both conditions are satisfied, the corgi's special effect
            # will take place, giving the next dog in line the leader's DP
            if dogsleft[0] == 'corgi' and len(doginfoleft) > 1:
                doginfoleft[1][1] += doginfoleft[0][1]

            if dogsright[0] == 'corgi' and len(doginforight) > 1:
                doginforight[1][1] += doginforight[0][1]

                # removes both pack leaders from their respective side's lists
            # and the list of awake dogs in each side
            dogsleft.pop(0)
            dogsright.pop(0)
            doginfoleft.pop(0)
            doginforight.pop(0)

            # Resets the repeat counter after EVERY DUEL, NOT EVERY ATTACK
            repeat = 0

            # When ONLY the left pack leader is knocked out in the duel, this
        # condition is satisfied, so the dog is removed from the left pack
        elif doginfoleft[0][2] <= 0:

            if dogsleft[0] == 'corgi' and len(doginfoleft) > 1:
                doginfoleft[1][1] += doginfoleft[0][1]

            # removes knocked out left pack leader from the left side's list
            dogsleft.pop(0)
            doginfoleft.pop(0)

            repeat = 0

            # When ONLY the right pack leader is knocked out in the duel, this
        # condition is satisfied, so the dog is removed from the right pack
        elif doginforight[0][2] <= 0:

            if dogsright[0] == 'corgi' and len(doginforight) > 1:
                doginforight[1][1] += doginforight[0][1]

            dogsright.pop(0)
            doginforight.pop(0)

            repeat = 0

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


def get_permutations(candidates, pack_size):
    ''' Returns a list of lists containing every possible permutation
    (of size 'permutation_size') of candidates.
    Input:
    - candidates, a non-empty list of dog candidate tuples (in arbitrary order)
    - permutation_size, the size of each permutation '''

    # Generates all pack permutations of the candidates, restricted to the
    # minimum value between the pack_size and number of candidates.
    lst = []
    min_len = min(pack_size, len(candidates))

    for pack in permutations(candidates, min_len):
        lst.append(pack)
    return lst


def build_dream_pack(candidates, pack_size, opponent_pack):
    """ Returns a tuple of the best performing team (of size 'pack_size')
    and its hp score, by creating every team permutation possible
    (using the get_permutations function), and sorting by the highest hp score.
    Input:
    - candidates, a non-empty list of dog candidate tuples (in arbitrary order)
    - pack_size, the maximum number of dogs in a pack (ranging from 1 to 5)
    - opponent_pack, a list of dog tuples describing your opponent's pack """

    # Generates every permutation of candidates within the pack size constraint
    listofperms = get_permutations(candidates, pack_size)

    # Initialising the values and lists used later in the function
    # hpmax MUST BE assigned a value that is LESS then the sum of the opponent
    # pack's HP, so this DEFINITIVELY works in ALL cases of: hp > hpmax
    idealindex = 0
    bestlist = []
    hpmax = 0

    for dogs in opponent_pack:
        hpmax -= dogs[2]

    # Runs through each permutation of the candidate pack
    # After every iteration of a permutation, the HP score counter is reset
    # and stores the position of the specific permutation in the list
    for permutation in listofperms:
        hp = 0
        index = listofperms.index(permutation)

        # Uses pre-made function to assign score with the tuple of the
        # winning side and the remaining AWAKE dogs in the winning pack
        score = sim_enhanced_battle(list(permutation), opponent_pack)

        # Calculates the HP score for each permutation battle result by
        # adjusting the HP counter differently, depending on which side won.
        # (+ HP if Left Pack Wins, - HP if Right {Opponent} Pack WINS)
        for dogs in score[1]:

            if score[0] == 'L':
                hp += dogs[2]

            elif score[0] == 'R':
                hp -= dogs[2]

        # Checks whether the current permutation's battle HP score is greater
        # than the current highest HP score.
        # If so, the highest HP score is updated, the permutation overwrites a
        # list, and the index of this 'DREAM PACK' permutation is stored
        if hp > hpmax:
            idealindex = index
            hpmax = hp
            bestlist = [list(permutation)]


        # If the HP score of the current permutation iterated is EQUAL to the
        # current highest HP score, then it is appended to the list of
        # previous pack permutations with the shared top HP score
        elif hp == hpmax:
            bestlist.append(list(permutation))

    # Checks whether the list is shared with other permutations
    # OR is a standalone of highest HP score
    # IF THE FORMER, the pack is sorted in lexicographical order,
    # and a tuple of the top permutation and the HP score is returned!
    if len(bestlist) > 1:
        return sorted(bestlist)[0], hpmax

    # IF THE LATTER, the index stored of the best-performing permutation
    # is utilised to return a tuple of the top permutation and the HP score
    return list(listofperms[idealindex]), hpmax


print(build_dream_pack([("corgi", 6, 5), ("husky", 3, 4), ("husky", 1, 2)], 3, [("golden", 2, 2), ("golden", 3, 9)]))
