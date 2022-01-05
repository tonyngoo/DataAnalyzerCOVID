#!/usr/bin/env python
'''

    THIS IS A RECORD OF THE PREPROCESSING BEFORE IT WAS REFACTORED 

  ////////////////////////////////////////////////
  Author(s): Anthony Vidovic (1130891), John Denbutter (1056466), Or Brener (1140102), Tony Ngo (1142414)

  Project: COVID-19 data Milestone 2
  Date of Last Update: Friday, March 19th, 2021
  ////////////////////////////////////////////////
  Functional Summary:
    - This file preproccesses selected data into csv files
    - Each question has their data points they use so we will seperate the data into smaller .csv's for each respective question
    
  Commandline Parameters: 1
    argv[1] = raw data file

  Run with:
    python preproccessing.py data/raw_dataset1.csv
  ////////////////////////////////////////////////
'''

# --------------------#
#      Libraries      #
# --------------------#
import sys
import csv

# --------------------#
#       Methods       #
# --------------------#
def write_to_csv(filename, data):
    '''creates a csv writer then writes rows to csv file

    param - filename: name of the file to write to
    param - data: data to write with

    return: A list with the file contents
    '''
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# --------------------#
#     Main program    #
# --------------------#
def main(argv):
    #only allow 1 command line argument (not including .py file)
    if len(argv) != 2:
        print("Usage: preproccessing.py <<raw data file>>")

        sys.exit(1)

    #name and path of file in user's filesystem
    data_filename = argv[1]
     
    #try to open file, if cant open throw error
    try:
        fh = open(data_filename, encoding="utf-8-sig")
    except IOError as err:
        print("Unable to open file '{}' : {}".format(data_filename, err),
              file=sys.stderr)
        sys.exit(1)

    data_reader = csv.reader(fh)

    #initialization of a list for each catagory of indices (as required per questions)
    data_array_Q1 = []
    data_array_Q1_processed = []
    data_array_Q2 = []
    data_array_Q2_processed = []
    data_array_Q3and4 = []
    data_array_Q3and4_processed = []

    #for all the lines in data_reader which is the user defined raw data dile
    for data in data_reader:
          #if it is outbreak related:
          if (data[9].lower() == "yes"):
            #data for the first question
            #[PHU, Gender]
            q1_list = [data[10], data[6]]
            data_array_Q1.append(q1_list)

          #data for the second question
          #[PHU, age]  
          q2_list = [data[10], data[5]]
          data_array_Q2.append(q2_list)

          #data for the third and fourth question
          #[accurate_episode_date]
          q3and4_list = [data[1]]
          data_array_Q3and4.append(q3and4_list)
   
    
    #sorted by PHUs
    data_array_Q1.sort()
    data_array_Q2.sort()
    #sorted by date
    data_array_Q3and4.sort()

    #----------------processed Q1---------------#
    #instead of having each line represent one case of an outbreak related covid case. Each PHU will have the total number of cases related to an outbreak

    female_count = 0
    male_count = 0
    genderDiverse_count = 0
    unspecified_count = 0

    total = 0
    
    #for first line of data
    if data_array_Q1[0][1].lower() == "female":
      female_count += 1
      total += 1
    elif data_array_Q1[0][1].lower() == "male":
      male_count += 1
      total += 1
    elif data_array_Q1[0][1].lower() == "gender diverse":
      genderDiverse_count += 1
      total += 1
    elif data_array_Q1[0][1].lower() == "unspecified":
      unspecified_count += 1
      total += 1
      
      
    for i in range(1, len(data_array_Q1)):
      #if current line is the same PHU as the last line
      if data_array_Q1[i][0] == data_array_Q1[i-1][0]:
        if data_array_Q1[i][1].lower() == "female":
          female_count += 1
          total += 1
        elif data_array_Q1[i][1].lower() == "male":
          male_count += 1
          total += 1
        elif data_array_Q1[i][1].lower() == "gender diverse":
          genderDiverse_count += 1
          total += 1
        elif data_array_Q1[i][1].lower() == "unspecified":
          unspecified_count += 1
          total += 1
      #if different PHU as last line
      else:
        #append the PHU, Gender, gender_count 
        q1_list = [data_array_Q1[i-1][0],  "FEMALE", female_count]
        data_array_Q1_processed.append(q1_list)
        q1_list = [data_array_Q1[i-1][0],  "MALE", male_count]
        data_array_Q1_processed.append(q1_list)
        q1_list = [data_array_Q1[i-1][0],  "GENDER DIVERSE", genderDiverse_count]
        data_array_Q1_processed.append(q1_list)
        q1_list = [data_array_Q1[i-1][0],  "UNSPECIFIED", unspecified_count]
        data_array_Q1_processed.append(q1_list)

        #set counters back to zero
        female_count = 0
        male_count = 0
        genderDiverse_count = 0
        unspecified_count = 0
        
        #check the current line for the count
        if data_array_Q1[i][1].lower() == "female":
          female_count += 1
          total += 1
        elif data_array_Q1[i][1].lower() == "male":
          male_count += 1
          total += 1
        elif data_array_Q1[i][1].lower() == "gender diverse":
          genderDiverse_count += 1
          total += 1
        elif data_array_Q1[i][1].lower() == "unspecified":
          unspecified_count += 1
          total += 1

      #for the last line of the data
      if i == len(data_array_Q1)-1:
        #append the PHU, Gender, gender_count
        q1_list = [data_array_Q1[i-1][0],  "FEMALE", female_count]
        data_array_Q1_processed.append(q1_list)
        q1_list = [data_array_Q1[i-1][0],  "MALE", male_count]
        data_array_Q1_processed.append(q1_list)
        q1_list = [data_array_Q1[i-1][0],  "GENDER DIVERSE", genderDiverse_count]
        data_array_Q1_processed.append(q1_list)
        q1_list = [data_array_Q1[i-1][0],  "UNSPECIFIED", unspecified_count]
        data_array_Q1_processed.append(q1_list)

    #--for testing-- prints total # of casses related to an outbreak  
    print(total)
    
    #----------------processed Q1---------------#

    #----------------processed Q2---------------#
    #instead of having each line represent one covid case per age range, Each PHU will have the total number of cases per age range 

    less20_count = 0
    twenties_count = 0
    thirties_count = 0
    fourties_count = 0
    fifties_count = 0
    sixties_count = 0
    seventies_count = 0
    eighties_count = 0
    more90_count = 0
    unknown_count = 0
    ages_count = [twenties_count, thirties_count, fourties_count, fifties_count, sixties_count, seventies_count, eighties_count, more90_count, less20_count, unknown_count]
    ages = ["20s", "30s", "40s", "50s", "60s", "70s", "80s", "90+", "<20", "UNKNOWN"]
      
    total = 0
    
    #for first line of data
    for i in range(0, len(ages)):
      if data_array_Q2[0][1] == ages[i]:
        ages_count[i] += 1
        total += 1
  
      
      
    for i in range(1, len(data_array_Q2)):
      #if current line is the same PHU as the last line
      if data_array_Q2[i][0] == data_array_Q2[i-1][0]:
        for j in range(0, len(ages)):
          if data_array_Q2[i][1] == ages[j]:
            ages_count[j] += 1
            total += 1
    
      #if diffrent PHU as last line
      else:
        #append the PHU, age range, age_count
        for j in range(0, len(ages)):
          q2_list = [data_array_Q2[i-1][0],  ages[j], ages_count[j]]
          data_array_Q2_processed.append(q2_list)
        

        #set counters back to zero
        for j in range(0, len(ages)):
            ages_count[j] = 0
        
        #check the current line for the count
        for j in range(0, len(ages)):
          if data_array_Q2[i][1] == ages[j]:
            ages_count[j] += 1
            total += 1

      # last line is "Reporting_PHU_ID,Age_Group"...no need for the following:
      #for the last line of the data
      # if i == len(data_array_Q2)-1:
      #    #append the PHU, age range, age_count
      #     for j in range(0, len(ages)):
      #       q2_list = [data_array_Q2[i-1][0],  ages[j], ages_count[j]]
      #       data_array_Q2_processed.append(q2_list)

    #--for testing-- prints total # of cases related to an outbreak  
    print(total)

    #----------------processed Q2---------------#

    #----------------processed Q3and4---------------#
    #instead of having each line represent one covid case per date, Each date will have the total number of cases in that date 

    date_count = 0
    total = 0
    
    #for first line of data
    date_count += 1
    total += 1
  
      
      
    for i in range(1, len(data_array_Q3and4)):
      #if current line is the same date as the last line
      if data_array_Q3and4[i][0] == data_array_Q3and4[i-1][0]:
        date_count += 1
        total += 1
    
      #if different date as last line
      else:
        #append the date, date_count
        q3and4_list = [data_array_Q3and4[i-1][0], date_count]
        data_array_Q3and4_processed.append(q3and4_list)
        

        #set counter back to zero
        date_count = 0
        
        #if it is not the last line
        #no double counting for the last line
        if not (i == len(data_array_Q3and4)-1):
          date_count += 1
          total += 1

      # last line is "Accurate_Episode_Date"...no need for the following:
      #for the last line of the data
      # if i == len(data_array_Q3and4)-1:
      #   #append the date, date_count
      #   q3and4_list = [data_array_Q3and4[i-1][0], date_count]
      #   data_array_Q3and4_processed.append(q3and4_list)

    #--for testing-- prints total # of casses related to an outbreak  
    print(total)

    #----------------processed Q3and4---------------#

    #call on functions to create csv files
    write_to_csv('data/testing_data/dataQ1Compare.csv', data_array_Q1_processed)
    #write_to_csv('data/dataQ1Proccessed.csv', data_array_Q1_processed)
    write_to_csv('data/testing_data/dataQ2Compare.csv', data_array_Q2_processed)
    #write_to_csv('data/dataQ2Proccessed.csv', data_array_Q2_processed)
    write_to_csv('data/testing_data/dataQ3and4Compare.csv', data_array_Q3and4_processed)
    #write_to_csv('data/dataQ3and4Proccessed.csv', data_array_Q3and4_processed)
    #write_to_csv('data/datasetQ4.csv', data_array_set2)


## Call our main function, passing the system argv as the parameter
main(sys.argv)

#
#   End of Script
#