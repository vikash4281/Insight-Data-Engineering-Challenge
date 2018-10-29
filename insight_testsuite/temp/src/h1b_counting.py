import csv
import sys


# this is the function to read the input file

def load_data(input_file_location):
    # read in input file
    with open(input_file_location) as input:
        # load the csv with ; delimiter
        reader = csv.reader(input, delimiter=';')
        # load the first row as columns
        columns = next(reader)
        # load the remaining data
        actual_data = list(reader)
        # check if number of columns and the data are same
        if (len(actual_data[0]) == len(columns)):
            return columns, actual_data


# this is the function to count the number of certified applications

def certified_applications_count(columns, data):
    # initialise a dictionary to store occupation as key and count as value
    occupations_number = dict()
    # initialise a dictionary to store state as key and count as value
    states_number = dict()

    # check column index for all the three cases observed in the input. if it does not match revert
    # back to the 2014 version of the input
    try:
        socname = columns.index('SOC_NAME')
    except:
        socname = columns.index('LCA_CASE_SOC_NAME')

    try:
        state_col = columns.index('WORKSITE_STATE')
    except:
        state_col = columns.index('LCA_CASE_WORKLOC1_STATE')

    try:
        status = columns.index('CASE_STATUS')
    except:
        status = columns.index('STATUS')

    # counter to count certified number of applications
    certified_applications_counter = 0
    # iterate for each line in data
    for line in data:
        # check if certified
        if line[status] == 'CERTIFIED':
            # clean the occupation
            occupation = line[socname].strip('"')
            # add to occupation dictionary and increase count
            occupations_number[occupation] = occupations_number.get(occupation, 0) + 1
            # get the state information
            state = line[state_col]
            # add the state to state dictionary and increase count
            states_number[state] = states_number.get(state, 0) + 1
            # increase total certfied application counter
            certified_applications_counter += 1
    return certified_applications_counter, occupations_number, states_number


# this is the function to sort certified applications based on descending order and then job title

def certified_sorter(certified_applications_count, total):
    # convert the dictionary to list
    certified_applications_list = [[key, value, '{:.1%}'.format(value / total)] \
                                   for (key, value) in certified_applications_count.items()]
    # sort the list using lambda functions
    certified_applications_list.sort(key=lambda x: (-x[1], x[0]))
    return certified_applications_list

# this is the function to write the result to a text file

def write_result(occupations_sorted, states_sorted, output_file_occupation, output_file_state):
    with open(output_file_occupation, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])
        writer.writerows(occupations_sorted[:10])

    with open(output_file_state, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])
        writer.writerows(states_sorted[:10])



def main():
    input_file_location = sys.argv[1]
    occupation_outfile = sys.argv[2]
    state_outfile = sys.argv[3]
    columns, data = load_data(input_file_location)
    total, occupations_number, states_number = certified_applications_count(columns, data)
    sorted_occupation = certified_sorter(occupations_number, total)
    sorted_state = certified_sorter(states_number, total)
    write_result(sorted_occupation, sorted_state, occupation_outfile, state_outfile)

if __name__ == '__main__':
    main()





