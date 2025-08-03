"""

author : Sam Mukherjee

"""

"""
=====================================MetaData=====================================
Field_Name	Description			
stusps	State Postal Code			
state	2 Digit State FIPS Code			
hud_area_code	HUD Specific Area Code			
County_Name	County Name			
county_town_name	Town Name for areas in New England (Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont)- Otherwise, County Name			
metro	1 if area is in a Metropolitan Statistical Area- 0 if not			
HUD_Area_Name	HUD Area Name			
fips	Concatenated 2 Digit State FIPS Code, 3 Digit County FIPS Code, and 5 Digit County Subdivision FIPS Code			
pop2022	Population in 2022		
	
fmr_0	FY 2025 0-Bedroom Fair Market Rent			
fmr_1	FY 2025 1-Bedroom Fair Market Rent			
fmr_2	FY 2025 2-Bedroom Fair Market Rent			
fmr_3	FY 2025 3-Bedroom Fair Market Rent			
fmr_4	FY 2025 4-Bedroom Fair Market Rent			

"""
import sys, os
import pandas as pd



def parse_2025_data():
    base_dir = os.path.dirname(__file__)  # where this script lives
    csv_path = os.path.join(base_dir, "..", "data", "FY2025_FMRs_by_County", "FY25_FMRs_revised.csv")
    return pd.read_csv(csv_path)

def parse_rent_data (state='FL',county = 'Marion County'):
    base_dir = os.path.dirname(__file__)  # where this script lives
    csv_path = os.path.join(base_dir, "..", "data", "FY2025_FMRs_by_County", "FY25_FMRs_revised.csv")
    df = pd.read_csv(csv_path)


    # Example: Filter for a specific state and county
    #state = 'FL'
    #county = 'Marion County'
    filtered_df = df[(df['stusps'] == state) & (df['countyname'] == county)]

    print(filtered_df)
    print(filtered_df)

    print("Current market data for a 1 bed is ",filtered_df['fmr_1'].values[0])
    print("Current market data for a 2 bed is ",filtered_df['fmr_2'].values[0])
    print("Current market data for a 3 bed is ",filtered_df['fmr_3'].values[0])
    print("Current market data for a 4 bed is ",filtered_df['fmr_4'].values[0])
    return filtered_df