import pandas as pd
from math import sin, cos, sqrt, atan2, radians
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

def calculate_distance(file_contents):
    invite = []
    for index, row in file_contents.iterrows():
        diff_long = radians(INTERCOM_LONG) - radians(row['longitude'])
        diff_lat = radians(INTERCOM_LAT) - radians(row['latitude'])

        a = sin(diff_lat / 2) ** 2 + cos(row['latitude']) * cos(INTERCOM_LAT) * sin(diff_long / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = RADIUS_EARTH * c

        if distance <= 100:
            invite.append('yes')
        else:
            invite.append('no')
    file_contents['invite'] = invite

def main():
    url = 'https://gist.githubusercontent.com/brianw/19896c50afa89ad4dec3/raw/6c11047887a03483c50017c1d451667fd62a53ca/gistfile1.txt'
    df = read_file(url,True)
    calculate_distance(df)
    df = df[df.invite == 'yes']
    df = df.sort_values(['user_id'], ascending=True)
    print(df.loc[:, 'name':'user_id'])

if __name__== "__main__":
    main()
