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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd

def parse_2025_data (state='FL',county = 'Marion County'):
    return pd.read_csv('../data/FY2025_FMRs_by_County/FY25_FMRs_revised.csv')


def parse_rent_data (state='FL',county = 'Marion County'):
    df = pd.read_csv('../data/FY2025_FMRs_by_County/FY25_FMRs_revised.csv')


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