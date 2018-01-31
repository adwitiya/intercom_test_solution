#/**************************************************************/
#       solution.py -- Distance between two locations           *
#       Author:  Adwitiya Chakraborty                           *
#                chakraad@tcd.ie                                *
#                github.com/adwitiya                            *
#/**************************************************************/

import pandas as pd
from math import sin, cos, sqrt, atan2, radians
from tabulate import tabulate

# Global Constants
INTERCOM_LONG =  -6.257664
INTERCOM_LAT = 53.339428
RADIUS_EARTH = 6373.0 #Approx Radius of earth in KMs

# Reads the file using Pandas,
def read_file(file_name,lines):
    doc__ = """
    -- Filename can be txt json or any json file or any web url with json format files
    -- If there are multiple json lines pass lines as True
    """
    file_contents = pd.read_json(file_name, lines=lines)
    return file_contents

# Calculate the Distance between points
def calculate_distance(file_contents):
    invite = []
    for index, row in file_contents.iterrows():
        # Needs to be converted into radians
        diff_long = radians(INTERCOM_LONG) - radians(row['longitude'])
        diff_lat = radians(INTERCOM_LAT) - radians(row['latitude'])

        # Great Circle Distance Formula
        a = sin(diff_lat / 2) ** 2 + cos(row['latitude']) * cos(INTERCOM_LAT) * sin(diff_long / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        # Final distance in kms
        distance = RADIUS_EARTH * c
        # Creating a new feature based on invite selection criteria
        if distance <= 100:
            invite.append('yes')
        else:
            invite.append('no')

    # Appending the newly created feature to the dataframe
    file_contents['invite'] = invite

def main():
    url = 'https://gist.githubusercontent.com/brianw/19896c50afa89ad4dec3/raw/6c11047887a03483c50017c1d451667fd62a53ca/gistfile1.txt'
    df = read_file(url, True)
    calculate_distance(df)
    # Show only users who can be invited
    df = df[df.invite == 'yes']
    # Sort the dataframe using user_id
    df = df.sort_values(['user_id'], ascending=True)
    # Print only name and user_id
    df = df.loc[:, 'name':'user_id']
    # Pretty-print Output using Tabulate
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

if __name__== "__main__":
    main()
