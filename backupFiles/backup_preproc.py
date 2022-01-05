#!/usr/bin/env python
'''
------------------------------------------------------------------------------
| __FILE__:            preprocessing_optimized.py                                   |  
| __AUTHORS__:         Anthony Vidovic (1130891), John Denbutter 
|                      (1056466) Or Brener (1140102), Tony Ngo        |                      (1142414)
|                                                                     |
| __PROJECT__:         COVID-19 Data Analysis and Visualization       |
| __LAST UPDATED__:    Monday, March 29th, 2021                       |
------------------------------------------------------------------------------
| __SUMMARY__:         This file is a refactored version of preprocessing.py. It preproccesses selected data into csv |                      files.
|                      Each question has their data points they use   |                      so we
|                      will seperate the data into smaller csv files and aggregate the information we are concered with.        |
|                                                                            |
| __DATA__:            Data used from raw dataset 1 (the data set of all confried COVID cases in Ontartio) "raw_dataset1.csv"        |
|                                                                            |
| __RUN WITH__:        python preprocessing_optimized.py data/raw_dataset1.csv             |                  
|                                                                            | 
| __COMMAND LINE__:    argv[1] = raw data file                               |
------------------------------------------------------------------------------
'''

#
# Start of script
#

# Packages and modules
import sys
import csv


def write_to_csv(filename, data):
    '''creates a csv writer then writes rows to csv file

    param - filename: name of the file to write to
    param - data: data to write with

    return: A list with the file contents
    '''
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def open_file(filename):
    '''Opens and creates a file handle for a file

    param - filename: name of the file

    return: file handle
    '''
    try:
        fh = open(filename, encoding="utf-8-sig")
        return fh
    except IOError as err:
        print("Unable to open file '{}' : {}".format(filename, err),
              file=sys.stderr)
        sys.exit(1)


def process_data_1(data_list, counts, list_being_counted):
    '''Process data for genderPercentage.py and ageRange.py This function counts the sum of values to aggregate the data in data_list

    param - data_list: a sorted list of the dataset being aggragated
    param - list_being_counted: list of all the objects that needed to be counted
    param - counts: a list of variables that hold the counts for each object in list_being_counted

    return: a subset of data_list where the data is aggregated based on the parameter counts
    '''

    aggregated = []
    # Total is used for testing purposes to check that each line is being counted properly
    total = 0

    # Checks first line in the file
    for i in range(0, len(list_being_counted)):
        if data_list[0][1] == list_being_counted[i]:
            counts[i] += 1
            total += 1

    # From second line to the end of the file
    for i in range(1, len(data_list)):
        # If current line is the same PHU as the last line
        if data_list[i][0] == data_list[i - 1][0]:
            for j in range(0, len(list_being_counted)):
                if data_list[i][1] == list_being_counted[j]:
                    counts[j] += 1
                    total += 1

        # If different PHU as last line
        else:
            # Append the PHU, the count name, and the count itself
            for j in range(0, len(list_being_counted)):
                aggregated.append(
                    [data_list[i - 1][0], list_being_counted[j], counts[j]])

            # Set counters back to zero
            for j in range(0, len(list_being_counted)):
                counts[j] = 0

            # Check the current line for the count
            for j in range(0, len(list_being_counted)):
                if data_list[i][1] == list_being_counted[j]:
                    counts[j] += 1
                    total += 1

        # For the last line of the data
        if i == len(data_list) - 1 and (data_list[i][0]).isdigit():
            # Append the PHU, the count name, and the count itself
        	for j in range(0, len(list_being_counted)):
	            aggregated.append([data_list[i - 1][0], list_being_counted[j], counts[j]])

    # Uncomment if you want to test
    #print(total)

    return aggregated


def process_data_dates(data_list, count):
    '''Process data for caseTrendInRnage.py and LTCHRatio.py This function counts the sum of cases for each data in data_list

    param - data_list: a sorted list of all the dates in the dataset being aggragated
    param - count: the number of cases for each date

    return: a subset of data_list where the data is aggregated based on the number of cases in each date
    '''

    aggregated = []
    # Total is used for testing purposes to check that each line is being counted properly
    total = 0

    # First line in the file
    count += 1
    total += 1

    # From second line to the end of the file
    for i in range(1, len(data_list)):
        # If current line is the same date as the last line
        if data_list[i][0] == data_list[i - 1][0]:
            count += 1
            total += 1

        # If different date as last line
        else:
            # Append the date and count
            aggregated.append([data_list[i - 1][0], count])

            # Set counter back to zero
            count = 0

            # The last line in the data_list will not need to be counted
            # Check the current line for the count
            if not (i == len(data_list) - 1):
                count += 1
                total += 1

    # Uncomment if you want to test
    #print(total)

    return aggregated


def main(argv):

    # Only allow 1 command line argument (not including .py file)
    if len(argv) != 2:
        print("Usage: preprocessing_optimized.py <<raw data file>>")
        sys.exit(1)

    # Try to open file, if cant open throw error
    fh = open_file(argv[1])
    data_reader = csv.reader(fh)

    # Initialization of a list for each category of indices (as required per questions)
    data_list_q1 = []
    # data_list_q1_processed = []
    data_list_q2 = []
    # data_list_q2_processed = []
    data_list_q3_and_q4 = []
    # data_list_q3_and_q4_processed = []

    # For all the lines in data_reader which is the user defined raw data file
    for data in data_reader:
        # If it is outbreak related:
        if (data[9].lower() == "yes"):
            # Data for the first question
            # [PHU, Gender]
            q1_list = [data[10], data[6]]
            data_list_q1.append(q1_list)

        # Data for the second question
        # [PHU, age]
        q2_list = [data[10], data[5]]
        data_list_q2.append(q2_list)

        # Data for the third and fourth question
        # [accurate_episode_date]
        q3and4_list = [data[1]]
        data_list_q3_and_q4.append(q3and4_list)

    # Sorted by PHUs
    data_list_q1.sort()
    data_list_q2.sort()
    # Sorted by date
    data_list_q3_and_q4.sort()

    #----------------processed Q1---------------#

    #data_list_q1_processed = process_Q1_data(data_list_q1) DO WE NEED THIS?

    gender_count = [0, 0, 0, 0]
    gender_list = ["FEMALE", "MALE", "GENDER DIVERSE", "UNSPECIFIED"]
    data_list_q1_processed = process_data_1(data_list_q1, gender_count,
                                            gender_list)
    write_to_csv('data/testing_data/test.csv', data_list_q1_processed)

    ages_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ages_list = [
        "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90+", "<20",
        "UNKNOWN"
    ]
    data_list_q2_processed = process_data_1(data_list_q2, ages_count,
                                            ages_list)
    write_to_csv('data/testing_data/test2.csv', data_list_q2_processed)

    date_count = 0
    data_list_q3_and_q4_processed = process_data_dates(data_list_q3_and_q4,
                                                       date_count)
    write_to_csv('data/testing_data/test3and4.csv',
                 data_list_q3_and_q4_processed)


#to test it on the shell:
#cmp --silent data/testing_data/test.csv data/dataQ1.csv && echo 'Success'

## Call our main function, passing the system argv as the parameter
main(sys.argv)

#
#   End of Script
#
