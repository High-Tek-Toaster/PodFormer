"""Methods to determine the priority of a user to a group after answering
specific questions"""

import random
import math
from dbtools.models import *

MAX_PRIO = 5
MIN_PRIO = 0
#calculate the priority for a group
def calc_project_priority(project, participant_list, attribute_list):
    """Calculates a projects priority.
    @Params: attribute_list is a list of attribute_selection
             participant_list is a list of Participant
             project is of type Project"""
    # multi-step process
    # participant project attributes summed together
    # particpant attributes have the same id
    #   - Homogenous:
    #       -   get the range between the current value and
    #       -   the greatest outlier, then subtract
    #   - Hetergenous:
    #       -   get the range between the current value and
    #       -   the greatest outlier, then add
    tot_score = 0
    # get project score for each participant in the group
    for part in participant_list:
        try:
            tot_score += part.getProjectChoice(project).value
        except (AttributeError):
            tot_score += MAX_PRIO+MIN_PRIO/2

    for att in attribute_list:
        # to get the outliers of the answers
        max_num = 0
        min_num = 5
        val = 0
        #find if we need to change the max/min values
        for part in participant_list:
            try:
                val = part.getAttributeChoice(att).value
                if val < min_num:
                    min_num = val
                if val > max_num:
                    max_num = val
            except (AttributeError): #if the user didn't answer a question
                val = 0
            
        
        #get the furthest range for each attribute among each participant and 
        #add to the total score
        for part in participant_list:

            try:
                val = part.getAttributeChoice(att).value

                if abs(max_num-val) > abs(min_num-val):
                    val = abs(max_num-val)
                else:
                    val = abs(min_num-val)

                if att.attribute.is_homogenous:
                    val = val * -1
            except (AttributeError):
                val = 0

            tot_score += val
        
        return tot_score
def calc_individual_priority(input_list):
    pass

# for this function, we need to handle keeping track of the minimum score
# in each of the projects and add to the master_score
def calc_global_score(project_list, attribute_list):
    master_score = 0
    min_proj = 99999
    for i in range(len(project_list)):
        val = calc_project_priority(project_list[i][0], project_list[i][1], attribute_list)
        if val < min_proj:
            min_proj = val
        master_score += val

    master_score += min_proj
    return master_score

def shuffle_particpants(gf):
    roster = list(gf.getRoster()).copy()
    random.shuffle(roster)
    return roster

def calc_optimal_groups(gf, epoch=50, max_parts=4):
    """Uses random hill climbing algorithm to determine
    the "best" grouping of participants"""
    best_group_value = 0
    best_group_list = []
    #amount of people able to go into projects for evenness
    similar_group_number = int(len(gf.getProjectList()) / len(gf.getRoster()))
    total_combinations = combination_num(max_parts, len(gf.getRoster()))

    # do shuffle for amount of epochs or if we reached
    # the maximum total combinations possible
    for i in range(epoch):
        if i >= total_combinations:
            break
        roster = shuffle_particpants(gf)
        #lists of lists of candidates
        candidate_lists = []

        #creates lists of max_part or optimal sized groups
        while len(roster) > 0:
            temp_list = []
            for j in range(similar_group_number):
                if j >= max_parts:
                    break
                candidate_lists.append(roster.pop())
            
            candidate_lists.append(temp_list.copy())


            #if for some reason we have more people than allowable participants
            if len(candidate_lists) >= len(gf.getProjectList()):
                people_remaining = len(roster)
                #pop evenly into the candidate_lists until we run out of people
                #no on will not get put into a group
                while len(roster) > 0:
                    for i in range(people_remaining):
                        index = i%len(candidate_lists)
                        part = roster.pop()
                        alist = candidate_lists[index]
                        alist.append(part)
                        #candidate_lists[index].append[part]
                
            

        group_list = create_random_candidate(gf.getProjectList(), candidate_lists)
            
        temp = calc_global_score(group_list, gf.getAttributeList())

        if temp > best_group_value:
            best_group_list = group_list.copy()
            best_group_value = temp

    # returns a list of tupled project, with the participant roster
    return best_group_list, best_group_value

def save_group(project, candidate_list):
    return (project, candidate_list)

def combination_num(n, r):
    return math.factorial(n) / (math.factorial(r) * math.factorial(n-r))

def create_random_candidate(project_list, candidate_lists):
    group_list = []
    total = min(len(candidate_lists), len(project_list))
    for i in range(total):
            project = project_list[i]
            candidates = candidate_lists[i]
            group_list.append(save_group(project, candidates))
    
    return group_list