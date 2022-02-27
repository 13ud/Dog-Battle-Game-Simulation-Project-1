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


def hpscore_calculator(pack, opponent_pack):
    """ HELPER FUNCTION, Calculates & returns the remaining total hp of the
    pack MINUS the remaining total hp of the opponent's pack.
    Input:
    - pack, a list of dog tuples describing YOUR pack
    - opponent_pack, a list of dog tuples describing your opponent's pack """

    # Initialises the HP value and calculates the score outcome of the battle
    hp = 0
    score = sim_enhanced_battle(pack, opponent_pack)

    # Calculates the HP score for each permutation battle result by
    # adjusting the HP counter differently, depending on which side won.
    # (+ HP if Left Pack Wins, - HP if Right {Opponent} Pack WINS)
    for dogs in score[1]:

        if score[0] == 'L':
            hp += dogs[2]

        elif score[0] == 'R':
            hp -= dogs[2]

    return hp


def build_pack_quick(candidates, pack_size, opponent_pack, pool_size):
    """ Builds and returns the dream team of size 'pack_size' along with the
    HP score, by using a Greedy algorithm which quickly takes the top
    'pool_size' teams in each change of index, sorting by highest hp scores.
    Input:
    - candidates, a non-empty list of dog candidate tuples (in arbitrary order)
    - pack_size, the maximum number of dogs in a pack (ranging from 1 to 5)
    - opponent_pack, a list of dog tuples describing your opponent's pack
    - pool_size, the maximum count of alternative variants stored and
      considered in each stage. (is a non-zero positive int) """

    # initialises 3 lists which are updated after the end of every iteration
    toppacks = [candidates]
    scores = []
    setofpacks = []

    # Runs through each element of the pack list, and creates permutations.
    # Restarts the setofpacks list after moving on to next element of list
    # in order to not mix with previous packs not within the pool size
    for element in range(pack_size):
        setofpacks = []
        scores = []

        # Runs through the list of size 'pool_size', consisting of the
        # packs with the top performing HP scores.
        # Initially, toppacks is assigned the initial candidate list as no
        # permutations have been made BEFORE the first iteration of adjustments
        for index in range(len(toppacks)):

            # Runs through each of the candidates in the list and IF the
            # dog is NOT already in the list, the element in the list is
            # reassigned as the dog currently being iterated through.
            for dog in candidates:
                pack = toppacks[index][0:element + 1].copy()
                candidatelist = candidates.copy()

                if dog not in pack:
                    pack[element] = dog

                # After adjusting the specific element of the pack list,
                # The rest of the pack is deleted and the remaining candidates,
                # NOT already in the pack, are appended in their original order
                # Then the pack list is cut down to size constraint 'pack_size'
                del pack[(element + 1):]
                for c in candidatelist:

                    if c not in pack:
                        pack.append(c)
                pack = pack[0:pack_size]

                # After the pack is adjusted to fit the size constraint,
                # It calculates the hp score of this pack permutation
                # THAT HAS NOT BEEN TESTED YET (i.e. not in setofpacks)
                if pack not in setofpacks:
                    hp = hpscore_calculator(pack, opponent_pack)

                    # The HP is set to NEGATIVE in order to sort numbers by
                    # largest ABSOLUTE value AND at the same time,
                    # allowing the sorting of dogs in lexicographic order
                    scores.append((-hp, pack))
                    setofpacks.append(pack)

        # AFTER every toppack permutation (where the element is changed)
        # has appended a tuple of itself and its HP score to the list 'scores',
        # it is sorted in decreasing HP order, and the top performing packs
        # of size 'pack_size' is assigned to 'toppacks', to be iterated again
        toppacks = sorted(scores)[0:pool_size]
        toppacks = [scores[1] for scores in toppacks]

    # After the permutations of the final element of the pack have been
    # scored and assigned to toppacks, a tuple consisting of the
    # TOP performing pack and its final HP score is calculated and returned
    final_hp = hpscore_calculator(toppacks[0], opponent_pack)

    return toppacks[0], final_hp


TEST_CANDIDATES = [("golden", 3, 2), ("husky", 4, 2), ("corgi", 2, 3), ("golden", 2, 4), ("husky", 2, 4)]
TEST_OPP_PACK = [("husky", 2, 6), ("golden", 3, 6)]

print(build_pack_quick(TEST_CANDIDATES, 3, TEST_OPP_PACK, 3))