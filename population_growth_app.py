# -*- coding: utf-8 -*-
"""Population Growth App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19l6kdsaavj3RqorP9_AAzcKfmlUHs-wH

# POPULATION GROUWTH - UK CENSUS ANALYSIS

## Data Cleaning
First of all, the required python libraries are imported to read in the census data provided for analysis. Then, we proceed with checking for errors or abnormalities in the data before cleaning it.
"""

# Commented out IPython magic to ensure Python compatibility.
# Importing required libraries
import pandas as pd
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

# Try to read the csv file and handle the error if it happens
try:
    # Raw CSV URL
    raw_csv_url = "https://raw.githubusercontent.com/xbabs/Population-Growth-App/main/census_data.csv"

    # Read the census data using the raw URL
    census_data = pd.read_csv(raw_csv_url)

    # Display the first few rows of the data to verify
    print(census_data.head())

    # You can now proceed with data cleaning and analysis
    print("CSV file loaded successfully!")

except pd.errors.ParserError as e:
    print(f"Error reading CSV file: {e}")
    print("Please ensure the CSV file is properly formatted.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

census_data

census_data.info() # checks for the entries, columns, null values and datatypes

"""### Problems with the imported dataset

From the imformation displayed above:

1. The "unnamed: 0" column is not needed because it has nothing to do with cleaning of the given data.

2. There are null values in:
    1. Marital Status
    2. Religion

3. Also, we need to check the datatype for each attribute (column). Age is meant to be an integer, not float

4. The 11 columns must be thoroughly cleaned in cases of age with minors, null values and  NA values for entries. e.g. minors should have no religion and marital status, etc.
"""

census = census_data.drop(["Unnamed: 0"], axis = 1) # This removes the unnamed: 0 column from the dataframe

census # The refined dataframe

census["Age"] = census["Age"].astype("int64") # Converts the age datatype from float to int

census.describe(include = "all") # Shows the details of the whole dataset

"""Here, the data features have is to be checked starting from the first column to ensure clarity and for proper processing. Since the unneeded column has been removed, we need to identify unique values, missing values and empty entries. Then, any errors found needs to be cleaned appropriately.

#### 1. House Number
"""

census["House Number"].unique() # Checks for the house number possible elements in the census data

census[census["House Number"] == " "] # Checks for any empty value available

countError = census["House Number"].value_counts()["Five"] # The assigned variable checks for inappropriate house number(s).
countError

# The replace function is used to change the house number in words to figure
census["House Number"] = census["House Number"].replace("Five", "5")

# Checks and shows any null value present in each column
census.isnull().any()

census["House Number"].unique() # To verify the entry is correct

"""#### 2. Street"""

census["Street"].unique() # Unique values in street is diplayed and errors can be spotted and corrected

# Check for any null value in street
census["Street"].isnull().any()

census[census["Street"] == " "] # Checks for empty entries in street but none was found

census['Street'].value_counts()

"""#### 3. First Name"""

census["First Name"].unique() # Checks for the first name data series

census[census["First Name"] == " "] # Verifies if there are missing values in the first name entry

census["First Name"].isnull().any() # Checks for null values

# The replace function is used to replace any  in the error with an appropriate one
# In this case, the empty space after the name 'Marion' is corrected
census["First Name"] = census["First Name"].replace(['Marion ', 'Marion'])

census["First Name"].unique()

census["First Name"] == 'Marion'

"""#### SURNAME"""

census["Surname"].unique() # Show the Surnames in the data given

census["Surname"].isnull().any() # Checks for any null values in the surname entry

census[census["Surname"] == " "] # Checks for people with no surname filled in

"""The people in the cell above with no given surname needs to be checked and corrected. To do this, the House number and Street could be checked to see if they share thesame surname with everyone in the household."""

# Kelly's house address
census.loc[(census['Street'] == 'White Avenue') & (census['House Number'] == '27')]

# Naomi's house address
census.loc[(census['Street'] == 'White Avenue') & (census['House Number'] == '50')]

# Elaine's house address
census.loc[(census['Street'] == 'Newcastle Trail') & (census['House Number'] == '2')]

# All three with no given surname will take thesame surname with their corresponding
# household because other occupants share thesame surname as well. Also, the
# is based on their respective relationship to head of house.
census.loc[8888, "Surname"] = "Mellor"
census.loc[8965, "Surname"] = "Begum"
census.loc[10140, "Surname"] = "West"

census[census["Surname"] == " "] # The output shows there are no more empty fields in surname

"""#### AGE"""

census["Age"].unique() # checks for the age data series

census["Age"] = census["Age"].astype("int64") # The astype() function converts the age data type to integer

census["Age"].unique()

census[census["Age"] == " "] # Verifies for an empty field in age

census["Age"].isna().any() # To make sure there are no N/A fields in age

sns.displot(census["Age"], binwidth = 10) # This plot shows the age with the number of people in the group respectively

"""#### RELATIONSHIP TO HEAD OF HOUSE"""

census["Relationship to Head of House"].unique() # Shows the different relationship to head of house

# Firstly, the typographical error is checked and 'Niece' is replace with 'Niece'
census["Relationship to Head of House"] = census["Relationship to Head of House"].replace(["Neice", "Niece"])

census[census["Relationship to Head of House"] == " "] # Empty field are checked, and none was found here

# Checking through the house address
census.loc[(census['Street'] == 'Evans Mission') & (census['House Number'] == '40')]

# The output here shows the people with no relationship with head of house
census[(census["Relationship to Head of House"] == "None") & (census['Marital Status'] == 'Married')]

census["Relationship to Head of House"].isna().any() # To show any N/A values

"""### MARITAL STATUS"""

census["Marital Status"].unique() # Shows marital status of the data series and  check for errors

# The marital should be replaced appropriately and people under 18 has no marital status
census["Marital Status"] = census["Marital Status"].replace(["M", "S", "D", "W", np.nan], ["Married", "Single", "Divorced", "Widowed", "NA"])

census["Marital Status"].unique() # Corrected marital status values

census["Marital Status"].isnull().any() # shows null values, but no null value was found

# Iterating using people aged 18 and above and marital status to check and correct
# if anyone in that group is not married, divorced, widowed or single
census[(census["Age"] >= 18) & (census["Marital Status"] == 'NA')]

# No one is underage and windowed, the code output below confirms that
census[(census["Age"] < 18) & (census["Marital Status"] == 'Widowed')]

# This checks for people under 18 and are married. The acceptable marriage age is 18 and over
census[(census["Age"] < 18) & (census["Marital Status"] == 'Married')]

# To rectify this, the house address (for each person) will be checked to see how
# they're related to their respective household members

# For Lindsey Philips
census.loc[(census['Street'] == 'Allen Crossroad') & (census['House Number'] == '55')]

# For Michelle Bevan
census.loc[(census['Street'] == 'Fraser Avenue') & (census['House Number'] == '45')]

# For Barbara Chamberlain
census.loc[(census['Street'] == 'Tegid Road') & (census['House Number'] == '47')]

"""It was discovered that these 3 people are married as shown in the previous output cells. They are also the head of House. But they share surname with the husbands in each case. It is then assumed that it was a numerical typo error in the fields. However, the assumed age for all 3 females is 18 which is also the accepted age for the head of house."""

# The .loc[] function replaces the age entries with 18 years
census.loc[2141, "Age"] = 18
census.loc[2537, "Age"] = 18
census.loc[7755, "Age"] = 18

# This comfirms that the proper corrections were made using the street and house number
census.loc[(census['Street'] == 'Allen Crossroad') & (census['House Number'] == '55')]

#
census.loc[(census['Street'] == 'Fraser Avenue') & (census['House Number'] == '45')]

census.loc[(census['Street'] == 'Tegid Road') & (census['House Number'] == '47')]

# The output below explains that 2 people have thesame similarities in
# their marital status and relationship to head of house. They are daughters
# to the respective head of house. Hence, the need to check for their household
census.loc[(census['Age'] <= 18) & (census['Marital Status'] == 'Widowed')]

# For Gillian Carter
census.loc[(census['Street'] == "Laurel Parks") & (census['House Number'] == '7')]

# Rosemary Sullivan
census.loc[(census['Street'] == "Edwards Vista") & (census['House Number'] == '31')]

# It could be concluded that both are single as
# they just got married and can't be widowed at that age

census.loc[1704, "Marital Status"] = "Single"
census.loc[9718, "Marital Status"] = "Single"

sns.boxplot(data = census, x = "Age", y = "Marital Status")

# The plot belows displays the census data age series and
# relationship to head of house with respect to their
# marital status
plt.figure(figsize = (11,7))
sns.scatterplot(data = census, x = "Age", y = "Relationship to Head of House", hue = "Marital Status")
plt.title("Age against relationship to Head of House")

"""#### GENDER"""

census["Gender"].unique() # unique values under gender and errors are found

census[census["Gender"] == " "] # checks for empty field(s) in gender

# The house address is used to check where the person stays and
# figure out the gender
census.loc[(census['Street'] == 'Allen Crossroad') & (census['House Number'] == '43')]

# The code above didn't quite solve that, so the surname and marital status are checked
# and only the person comes up in the output
census.loc[(census['Surname'] == 'Quinn') & (census['Marital Status'] == 'Divorced')]

# The previous step didn't work as well,
# The first name data series is checked to be certain
# which gender, which is female as displayed in the next output
census[census["First Name"] == "Victoria"]

census.loc[2101, "Gender"] = "Female"

census[census["Gender"] == " "] # To comfirm the previous output

# There are only 2 known genders , which is Male and Female
# The replace function is used tpo correct these errors
census["Gender"] = census["Gender"].replace(["M", "F", "m", "f", "male", "female"], ["Male", "Female", "Male", "Female", "Male", "Female"])

census["Gender"].unique()

sns.histplot(census["Gender"]) # A plot to show the gender with most population

# The plot to show the genders and their respective marital status
sns.countplot(x = census["Gender"], data = census, hue = "Marital Status")
plt.title("Gender against marital status")

"""### OCCUPATION"""

# Verify and display the unique values in occupation
census["Occupation"].unique()

census[census["Occupation"] == " "] # It shows there are no empty values in occupation

census["Occupation"].isnull().any() # No null value(s) was found

# People aged over 15 years and less than 18 years are checked and they can be on student jobs as PAYE
# but they can't commute out of the town
census.loc[(census["Age"] > 15) & (census["Age"] < 18)]

# No one under 18 years and with the conditions(s) is found
census.loc[(census["Age"] < 18 ) & (census["Occupation"] != 'Child') & (census["Occupation"] != "University Student") & (census["Occupation"] != "Student")]

# It was found out that there were several people aged over 65 years and
# are unemployed. It's assumed that people aged over 65 years should be retired
census.loc[(census["Occupation"] == "Unemployed") & (census["Age"] > 65)]

# To replace the occupation status for people aged over 65 years with retired
census.loc[census[(census["Occupation"] == "Unemployed") & (census["Age"] > 65)].index, "Occupation"] = "Retired"

census.loc[(census["Occupation"] == "Unemployed") & (census["Age"] > 65)]

employment_status = [] # This list is a column added to contain the employment status

for i in census["Occupation"]:
    if i == "Child":
        employment_status.append("Child")
    elif i == "Student":
        employment_status.append("Student")
    elif i == "University Student":
        employment_status.append("University Student")
    elif "Retired" in i:
        employment_status.append("Retired")
    elif i == "Unemployed":
        employment_status.append("Unemployed")
    else:
        employment_status.append("Employed")

census["Employment Status"] = employment_status

census["Employment Status"]

census.head(10) # Shows the employment status column

sns.boxplot(data = census, x = "Age", y = "Employment Status")
plt.title("Age distribution by Occupation")

"""### INFIRMITY"""

census["Infirmity"].unique() # Uniques values of infirmity

census[census["Infirmity"] == " "] # Shows empty fields in infirmity

census['Infirmity'].value_counts()

# The empty fields are replaced with "None"
census['Infirmity'] = census['Infirmity'].replace(" ", "None")

census["Infirmity"].unique()

census[census["Infirmity"] == " "]

census['Infirmity'].value_counts()

"""#### RELIGION"""

# The different religions present in the given data
census["Religion"].unique()

census["Religion"].value_counts() # shows the number of people in a particular religion

census["Religion"].count() # Number of people with a known religion

# Checks for religion of people below age 18
census[census['Age'] < 18]['Religion'].unique()

census["Religion"] = census["Religion"].replace([np.nan, "Nope", "Housekeeper", "Quaker", "Agnostic"], ["N/A", "None", "None","None", "None"])

census[census["Religion"] == " "] # only 2 people don't empty values in their religions

census[census["Age"] > 18]['Religion'].unique()

# Indexing underaged people to have no religion which is N/A
census.loc[census[(census["Age"] < 18)].index, "Religion"] = "N/A"

# Leanne's household (family) practices christianity therefore it can be assumed that hers is christian as well
census.loc[(census["Street"] == "Cunningham Bypass") & (census["House Number"] == "42")]

# list of people over 18 years with religion of N/A (Not Applicable)
census.loc[(census["Religion"] == "N/A") & (census["Age"] > 18)]

census.loc[1387, "Religion"] = "N/A" # She is a child (minor), her religion is Not Applicable (N/A)
census.loc[5816, "Religion"] = "Christian" # She can assume her family's religion

census.loc[census[(census["Religion"] == "N/A") & (census["Age"] > 18)].index, "Religion"] = "None"

# to verify our entries are cleaned
census["Religion"].count()

census["Religion"].value_counts()

sns.boxplot(data = census, x = "Age", y = "Religion")
plt.title("Religion distribution with age")

census.info()

"""## ANALYSIS AND VISUALIZATION

### AGE DISTRIBUTION
The measure of central tendency such as age mean, median and mode could be described and used to determine the age groups
"""

average_age = round(census["Age"].mean()) # Mean age of the data series
modal_age = census["Age"].mode()[0] # Modal age of the data series
median_age = round(census["Age"].median()) # Median age of the data series

# The print function below outputs the mean, mode and median ages respectively (in years)
print(f"The average age of the census data is {average_age} years")
print(f"The modal age of the census data is {modal_age} years")
print(f"The median age of the census data is {median_age} years")

"""A population age pyramid is created below to show the number of people (for the female and male genders) that falls in a particular age group."""

male_gender = census.loc[lambda x:x.Gender == "Male"] # Male gender
female_gender = census.loc[lambda x:x.Gender == "Female"] # female gender

male_age_list = []

count0 = 0
count5 = 0
count10 = 0
count15 = 0
count20 = 0
count25 = 0
count30 = 0
count35 = 0
count40 = 0
count45 = 0
count50 = 0
count55 = 0
count60 = 0
count65 = 0
count70 = 0
count75 = 0
count80 = 0
count85 = 0
count90 = 0
count95 = 0
count99 = 0

for m in male_gender["Age"]:
    if m > 99:
        count99 += 1
    elif m >= 95 and m < 100:
        count95 += 1
    elif m >= 90 and m < 94:
        count90 += 1
    elif m >= 85 and m < 89:
        count85 += 1
    elif m >= 80 and m < 84:
        count80 += 1
    elif m >= 75 and m < 79:
        count75 += 1
    elif m >= 70 and m < 74:
        count70 += 1
    elif m >= 65 and m < 69:
        count65 += 1
    elif m >= 60 and m < 64:
        count60 += 1
    elif m >= 55 and m < 59:
        count55 += 1
    elif m >= 50 and m < 54:
        count50 += 1
    elif m >= 45 and m < 49:
        count45 += 1
    elif m >= 40 and m < 44:
        count40 += 1
    elif m >= 35 and m < 39:
        count35 += 1
    elif m >= 30 and m < 34:
        count30 += 1
    elif m >= 25 and m < 29:
        count25 += 1
    elif m >= 20 and m < 24:
        count20 += 1
    elif m >= 15 and m < 19:
        count15 += 1
    elif m >= 10 and m < 14:
        count10 += 1
    elif m >= 5 and m < 9:
        count5 += 1
    elif m >= 0 and m < 5:
        count0 += 1

count_list = [count99,count95,count90,count85,count80,count75,count70,count65,count60,count55,count50, count45, count40, count35, count30, count25, count20, count15, count10, count5, count0]

for data in count_list:
    male_age_list.append(data)

print(male_age_list)

female_age_list = []

count0 = 0
count5 = 0
count10 = 0
count15 = 0
count20 = 0
count25 = 0
count30 = 0
count35 = 0
count40 = 0
count45 = 0
count50 = 0
count55 = 0
count60 = 0
count65 = 0
count70 = 0
count75 = 0
count80 = 0
count85 = 0
count90 = 0
count95 = 0
count99 = 0

for f in female_gender["Age"]:
    if f > 99:
        count99 += 1
    elif f >= 95 and f < 100:
        count95 += 1
    elif f >= 90 and f < 94:
        count90 += 1
    elif f >= 85 and f < 89:
        count85 += 1
    elif f >= 80 and f < 84:
        count80 += 1
    elif f >= 75 and f < 79:
        count75 += 1
    elif f >= 70 and f < 74:
        count70 += 1
    elif f >= 65 and f < 69:
        count65 += 1
    elif f >= 60 and f < 64:
        count60 += 1
    elif f >= 55 and f < 59:
        count55 += 1
    elif f >= 50 and f < 54:
        count50 += 1
    elif f >= 45 and f < 49:
        count45 += 1
    elif f >= 40 and f < 44:
        count40 += 1
    elif f >= 35 and f < 39:
        count35 += 1
    elif f >= 30 and f < 34:
        count30 += 1
    elif f >= 25 and f < 29:
        count25 += 1
    elif f >= 20 and f < 24:
        count20 += 1
    elif f >= 15 and f < 19:
        count15 += 1
    elif f >= 10 and f < 14:
        count10 += 1
    elif f >= 5 and f < 9:
        count5 += 1
    elif f >= 0 and f < 5:
        count0 += 1

count_list = [count99,count95,count90,count85,count80,count75,count70,count65,count60,count55,count50, count45, count40, count35, count30, count25, count20, count15, count10, count5, count0]

for data in count_list:
    female_age_list.append(data)

print(female_age_list)

new_male_ages = []
for i in male_age_list:
    data = (-1*i)
    new_male_ages.append(data)

# These lines of code implements the grouping of the given data based on gender and their ages to
# plot an age pyramid for the whole population
age_p = pd.DataFrame({'Age': ['100+', '95-99', '90-94', '85-89', '80-84', '75-79', '70-74', '65-69', '60-64', '55-59', '50-54', '45-49', '40-44', '35-39','30-34', '25-29', '20-24', '15-19', '10-14', '5-9', '0-4'], 'Male': new_male_ages, 'Female': female_age_list})

age_group = ['100+', '95-99', '90-94', '85-89', '80-84', '75-79', '70-74', '65-69', '60-64', '55-59', '50-54', '45-49', '40-44', '35-39','30-34', '25-29', '20-24', '15-19', '10-14', '5-9', '0-4']
bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
age_pyramid_first = plt.figure(figsize = (15,7.5), dpi = 100 )
age_pyramid = sns.barplot(x = 'Male', y = 'Age', data = age_p, order = age_group, color = ('blue'), label = 'Male')
age_pyramid = sns.barplot(x ='Female', y = 'Age', data = age_p, order = age_group, color = ('red'), label = 'Female')
age_pyramid.legend()
plt.title("Age Population Pyramid")
age_pyramid.set(xlabel = "Population Count", ylabel = "Age Group")

plt.show()

bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100, 105]

order_class = ['100+', '95-99', '90-94', '85-89','80-84','75-79','70-74','65-69','60-64','55-59','50-54','45-49',
               '40-44','35-39','30-34','25-29','20-24','15-19','10-14','5-9','0-4']
age_group = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64',
         '65-69', '70-74', '75-79', '80-84', '85-89', '90-95','95-99', '100+']
census['Age Group'] = pd.cut(census['Age'],  bins, labels = age_group, include_lowest = True, ordered = False)

age_population = census.groupby(['Age Group', 'Gender']).size().reset_index(name='Population')

"""### Employment"""

employed = census.loc[(census["Employment Status"] == "Employed")]
unemployed = census.loc[(census["Employment Status"] == "Unemployed")]
retired = census.loc[(census["Employment Status"] == "Retired") | (census["Age"] >= 65)]

employed

unemployed

retired # Number of people aged 65 are considered to be retired

"""![image.png](attachment:image.png)"""

# Counts the number of employed, unemployed workers and retired (aging) people
employed_workers = employed.value_counts().sum()
unemployed_workers = unemployed.value_counts().sum()
retired_people = retired.value_counts().sum()

# Shows the number of employed, unemployed people and retirees
print(f"{employed_workers} people are employed")
print(f"{unemployed_workers} people are unemployed")
print(f"{retired_people} people are retired")

# Calculates the unemployement rate in the town
total_labour_force = employed_workers + unemployed_workers
unemployement_rate = (unemployed_workers / total_labour_force) * 100

print(f"The Unemployement rate of the town is {round(unemployement_rate, 1)} %")

sns.histplot(data = unemployed, x = 'Age', hue = 'Gender', multiple = 'stack')
plt.title('Unemployed Count by Age')

"""### Religious Affiliations"""

census["Religion"].value_counts()

# The plot shows how many people practise each religion
plt.figure(figsize = (11,7), dpi = 100)
sns.countplot(data = census, x = "Religion").set_title("Religious Affliliations and number of people that practice them")

# Christian religion has the highest number of people in the proposed town
christian_mode = census[census["Religion"] == "Christian"]["Age"].mode()
christian_avg = census[census["Religion"] == "Christian"]["Age"].mean()

print(f"The most modal age that practice christianity is {christian_mode} ")

print(f"The average age that practice christianity is {round(christian_avg)} years")

christians_aged_50 = census[(census["Religion"] == "Christian") & (census["Age"] > 50)].value_counts().sum()

print(f"The number of Christians aged more than 50 years is {christians_aged_50}")

christians_under_50 = census[(census["Religion"] == "Christian") & (census["Age"] <= 50)].value_counts().sum()

print(f"The number of Christians 50 years and less is {christians_under_50}")

"""### Marriage and Divorce Rate"""

# Plot below shows how Age relates to marital status with respect to corresponding gender
plt.figure(figsize=(11,8))
sns.scatterplot(data = census, x = "Age", y = "Marital Status", hue = "Gender")

married = census.loc[(census["Marital Status"] == "Married")] # List of married people
divorced = census.loc[(census["Marital Status"] == "Divorced")] # List of divorced people

married # Married people

divorced # divorced people

print(f" {(married).value_counts().sum()} people are married")

print(f"{(divorced).value_counts().sum()} people are divorced")

"""The marriage and divorce rates will be calculated to make reasonable analysis and recommendations

![image.png](attachment:image.png)
"""

marriages = (((married).value_counts().sum()) / 2) # The number of marriages because it has to be a pair
marriage_rate = ((marriages) / len(census)) * 1000 # Marriage rate
divorce_rate = (len(divorced) / len(census)) * 1000 # Divorce rate

print(f"The marriage rate is {round(marriage_rate)} per 1000 population (aged 18 and older)")
print(f"The divorce rate is {round(divorce_rate)} per 1000 population (aged 18 and older)")

"""### Occupancy Level

This is the number of people per household
"""

# Household occupancy
occupancy = census.groupby(["House Number", "Street"]).size()

# The house with the highest number of occupants
occupants = occupancy.to_frame(name = "Occupant(s)").reset_index()
occupants

"""There are 3,541 houses in the town, of which some houses are over-occupied. The over-occupied house(s) will be checked to see how it affects the proposed task outcome."""

occupants["Occupant(s)"].value_counts()

# shows that a house with 21 occupants is not reasonable and causes congestion
print(f"The details of the house with highest number of occupants: \n\n {occupants.max()}")

occupants.describe()

"""### Cummuters

They are total number of University Students, Employed workers and other professions that are likely to commute to and from places of work
"""

commuters = census[census["Employment Status"].isin(["Employed", "University Student"])]
commuters

print(f" {commuters.value_counts().sum()} people are likely to be commuters")

"""#### Migration
Also, migration contributes to the growth of the popluation
"""

# List of household lodgers and visitors are regarded as immigrants
immigrants = census[(census["Relationship to Head of House"] == "Lodger") | (census["Relationship to Head of House"] == "Visitor")].value_counts().sum()
print(f"There are {immigrants} immigrants in the town")

# List of divorcees aged 18 and older are regarded as emigrants considering their employement status
male = census[(census['Marital Status'] == 'Divorced') & (census['Occupation'] != 'Student') & (census["Gender"] == "Male")].value_counts().sum()
female = census[(census['Marital Status'] == 'Divorced') & (census['Occupation'] != 'Student') & (census["Gender"] == "Female")].value_counts().sum()

emigrants = female - male
print(f"There are likely {emigrants} emigrants in the town")

"""Migration Rate = ![migration.PNG](attachment:migration.PNG)"""

total_population = census.value_counts().sum()
migration_rate = ((immigrants - emigrants) / (total_population)) * 1000

print(f"The Net Migration Rate per thousand is: {round(migration_rate, 1)}" )

"""### Birth Rate and Death Rate
The birth rate is the number of births in a particular year per thousand people in the population while death rate is the number of deaths in that particular year per thousand people. The evaluation for this is shown in the next cells
"""

census[census["Age"] == 0] # List of babies/ births in this present year

census[census["Age"] == 4] # List of babies/ births 4 years ago

"""Ages between 18 years and 45 years will be analysed to give a more concise overview of crude birth and death rates"""

previous_births = census[census["Age"] == 4].value_counts().sum()
print(f"4 years ago, there were {previous_births} births in the town")

number_of_births = census[census["Age"] == 0].value_counts().sum()
print(f"Presently, there are {number_of_births} births in the town")

"""#### Birth Rate:
![birth.PNG](attachment:birth.PNG)
"""

total_population = census.value_counts().sum() # The town's total population

previous_birth_rate = (previous_births / total_population) * 1000
birth_rate = (number_of_births / total_population) * 1000 # Evaluating the birth rate

print(f"The Birth Rate for the town per thousand is {round(previous_birth_rate)} four years ago")
print(f"The Birth Rate for the town per thousand is {round(birth_rate)} for this year")

"""#### Death Rate:
![deathr.PNG](attachment:deathr.PNG)
"""

previous_deaths =  (census[(census["Age"] > 76) & (census["Age"] <= 102)]).value_counts().sum()
possible_deaths = (census[census["Age"] > 80]).value_counts().sum()

print(f"There were {previous_deaths} deaths Four years ago")
print(f"There could be possibly {possible_deaths} deaths in the coming years")

previous_death_rate = (previous_deaths / total_population) * 1000
death_rate = (possible_deaths / total_population) * 1000

print(f"The Death Rate for the town per thousand was {round(previous_death_rate)} four years ago")
print(f"The Death Rate for the town per thousand is {round(death_rate)} for this year")

"""![growth.PNG](attachment:growth.PNG)"""

natural_increase = (birth_rate - death_rate) / 10 # Deduced from the expression above

print(f" There is a natural population increase rate of {round(natural_increase, 1)}")

"""#### Population Growth
This is know if the population growth is increasing or decreasing

![image.png](attachment:image.png)
"""

# Using the expression above, the population growth
# will be decided if it is increasing or declining

growth_rate = (((number_of_births - possible_deaths) + (immigrants - emigrants)) / total_population) * 100

print(f" There's a probable population growth increase  of {growth_rate:.2f} %")

pip install streamlit

import streamlit as st

# Title
st.title("Population Growth Analysis")

# Input Fields
st.header("Input Parameters")
number_of_births = st.number_input("Number of Births", min_value=0, step=1, value=1000)
possible_deaths = st.number_input("Number of Deaths", min_value=0, step=1, value=500)
immigrants = st.number_input("Number of Immigrants", min_value=0, step=1, value=300)
emigrants = st.number_input("Number of Emigrants", min_value=0, step=1, value=100)
total_population = st.number_input("Total Population", min_value=1, step=1, value=10000)

# Calculate Growth Rate
growth_rate = (((number_of_births - possible_deaths) + (immigrants - emigrants)) / total_population) * 100

# Display Growth Rate
st.subheader("Population Growth Rate")
st.write(f"The calculated growth rate is **{growth_rate:.2f}%**")

# Insights
st.subheader("Insights")
if growth_rate > 0:
    st.success("The population is increasing. This can positively contribute to development and investment opportunities.")
else:
    st.warning("The population is decreasing. This might indicate potential challenges in growth and sustainability.")

"""The is a slight increase in population growth. However, the report for this analysis will describe how it contributes to the town's growth, development and investment considering other essential factors."""