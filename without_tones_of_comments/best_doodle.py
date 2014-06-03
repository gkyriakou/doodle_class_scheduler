#!/usr/bin/python

import csv
import copy
import operator
import sys

d = {}
fraidy_list = []
with open('doodle.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='"')
    for row in spamreader:
        bef_split = ','.join(row)
        after_split = bef_split.split(',')
        fraidy_list.append(after_split[1:])     # strip the name
        n = row.pop(0)

    fraidy_list.pop()                           # remove the count
    # translate into '1':OK and '0'
    for v in range(len(fraidy_list)):
        for m in range(len(fraidy_list[v])):
            if fraidy_list[v][m] == '':
                fraidy_list[v][m] = 0
            else:
                fraidy_list[v][m] = 1

# lets assume that we get a list of list. each encapsulated list contains a 0 if the student is not available and a '1' if the student is available

def find_max(full_list, av_slots, settled_students, beginning = 0, candidates = {}, cur_score = 0, combination = ()):
    """
    returns the av_slots slots that contain the maximum number of available students

    full_list           --- the list with the students availability for all slots: '1'=> students is availabe, '0'=> not available
    av_slots            --- how many different time slots can we use
    settled_students    --- a list containing which of the students already have a slot that they can use and which dont [1,0]
    beginning           --- the slot at after which we will begin searching
    candidates          --- dictionary containing the combination of slots and the number of students that satisfy that can potentially be our solution
    cur_score           --- the amount of students we have satisfied with the slots selected up to now
    combination         --- the indeces of the slots selected so far in a tuple form
    """
    # extract all the "usefull" information
    num_of_students = len(full_list)               # the number of different possible time slots, that students vote over
    num_of_slots = len(full_list[0])         # all the slots have the same number of students, we just pick the first one, cause worst case scenario there is at least one student

    if av_slots > num_of_slots:
        sys.exit("you cannot provide more slots than the number of slots! TERMINATING")

    # we will follow a simple exhaustive solution, without repetetions
    if beginning < num_of_slots-(av_slots-1):   # we should leave enough searching space for the rest of the av_slots
        max_avd = 0                             # maximum number of available students in one day
        max_ss = copy.copy(settled_students)    # availability including the most profitable day of the current av_slot
        tmp = 0
        slot = -1                               # an index to the slot we are examining
        ss = []                                 # the local(the current av_slot's) copy of settled_students that we play with
        for j in range(beginning, num_of_slots-(av_slots-1)):
            ss = copy.copy(settled_students)
            for k in range(num_of_students):
                if full_list[k][j] == 1 and settled_students[k]!=1:     # this students has not be settled yet
                    tmp += 1
                    ss[k] = 1
                else:
                    ss[k] = settled_students[k]

            # there is a chance of never entering that if and leaving the slot at -1. Is there theoretically improvement after that?
            if tmp > max_avd:
                    max_avd = tmp
                    slot = j                                            # note down the most 'profitable' day of the current av_slot
                    max_ss = copy.copy(ss)

            tmp = 0

            if av_slots > 1 and (j+av_slots) <= num_of_slots :  # we have more av_slots to use
                if slot == -1:
                    slot = beginning
                candidates = find_max(full_list, av_slots-1, copy.copy(max_ss), j+1, candidates, cur_score+max_avd, combination+(slot,))

        # execute that only if you are the last av_slot    
        if av_slots == 1:
            if slot == -1:
                print "cannot see how it may reach here"
            candidates[combination+(slot,)] = cur_score + max_avd       # register the score in a dictionary

    return candidates

num_slots = int(raw_input("Enter how many slots do you want to have: "))
print "slot-combination : score"
choices_dictionary = find_max(fraidy_list, num_slots, [0]*len(fraidy_list), beginning = 0, candidates = {}, cur_score = 0, combination = ())
maxes = {}
for i in choices_dictionary:
    if choices_dictionary[i] == max(choices_dictionary.iteritems(), key=operator.itemgetter(1))[1]:
        maxes[i] = max(choices_dictionary.iteritems(), key=operator.itemgetter(1))[1]

print maxes




















