# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:56:39 2018

@author: SANDHYAA
"""
import time
import calendar
import pandas as pd
import json as js

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


days=dict(enumerate(calendar.day_name))
months=dict(enumerate(calendar.month_name))

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    month='no'
    day='no'
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Choose city for  analysis : " + str(list(CITY_DATA.keys())) + ":\n ")
        #print(len(city))
        
        if len(city) > 0:
            #if city.upper() == 'NO':
             #   break
            if city.lower() not in list(CITY_DATA.keys()):
                print("Not an appropriate choice." + city)
                continue
            else:
                print("computing for city :" + city.lower())
                break        
        else:
           print("No value entered  :" )
           continue

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Choose any Month or ALL for all analysis : " + str(list(months.values())) + ":\n " )
        #print(len(month))
        
        if len(month) > 0:
            if month.upper() == 'NO':
                break
            if month.upper() == 'ALL':
                print("computing for all months :" + month)
                month='all'
                break
            if month.title() not in  list(months.values()):
                print("Not an appropriate choice." + month)
                continue
            else:
                print("computing for month :" + month.title())
                break        
        else:
           print("No value entered computing for ALL month :" )
           month='all'
           break
        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Choose Day or ALL for all analysis : " + str(list(days.values())) + ":\n ")
        #print(len(day))
        
        if len(day) > 0:
            if day.upper() == 'NO':
                break
            if day.upper() == 'ALL':
                print("computing for all months :" + day)
                day='all'
                break
            if day.title()  not in list(days.values()):
                print("Not an appropriate choice." + day)
                continue
            else:
                print("computing for month :" + day.title())
                break        
        else:
           print("No value entered computing for ALL days :" )
           day='all'
           break

    print('-'*40)
    return city.lower(), month.title(), day.title()

def load_data(city, month, day):
    
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
   # df['month'] = df['Start Time'].dt.month_name()
    #df['month'] = df['Start Time'].dt.month_name()
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        #month = months.index(month) + 1
        #month=months.keys()
        for k,v in enumerate(calendar.month_name):
            #print(month)
            #print(k,v)
            if v==month:
                mthkey=k
   
        # filter by month to create the new dataframe
        df = df[df['month'] == mthkey]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #print( pd.to_datetime(df['Start Time']))
    # display the most common month
    #df['month']=df['Start Time'].dt.month_name()
    df['month']=df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start month:', months[popular_month])
    print('Most Popular Start month:', df['Start Time'].dt.month_name().mode()[0])
    # display the most common day of week
    #df['day']=df['Start Time'].dt.day_name()
    df['day']=df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('Most Popular Start day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('Most Popular Start Station:', df['Start Station'].value_counts().head(1).to_string(header=None))
    print('Most Popular End Station:', df['End Station'].value_counts().head(1).to_string(header=None))
    #print('Most Popular Trip:', df['Start Station','End Station'].value_counts().idxmax())
    print()
    ptrips_start=df[['Start Station','End Station']].groupby(['Start Station','End Station'])['Start Station'].count()
    ptrips_end=df[['Start Station','End Station']].groupby(['Start Station','End Station'])['End Station'].count()
    print("Popular route: \n   Total Trips :" , ptrips_end.max()," start station: " , ptrips_start.idxmax()[0], " end station :" , ptrips_end.idxmax()[1] )
    print()
   # print("trips \n", ptrips.idxmax())
     #pop_trip=df.groupby(['Start Station','End Station']).count())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # display total travel time
    print('Total Travel Time :' ,(df['End Time']-df['Start Time']).sum())

    # display mean travel time
    print('Average Travel Time : ', (df['End Time'] -df['Start Time'] ).mean())    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    # Display counts of user types
        
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_data=df[['User Type']].groupby(['User Type'])['User Type'].count()
    print('user type classification:  \n',user_data.to_string(header=None))
    print()

    if 'Gender' not in df.columns:
        print("Gender Classification Data not Available")
    else:
        Gender=df[['Gender']].groupby(['Gender'])['Gender'].count()
        df['year']=df['Birth Year']
    
        # Display counts of gender
        print('\nGender Distribution : \n',Gender.to_string(header=None))
        print('\nBirth Date Distribution :')
        print('Oldest year :'  , int((df['year'].min())))
        print('Younger year :' ,int((df['year'].max())))
        print('Most in Year :' ,int((df['year'].value_counts().idxmax())))
       # print('Most in Year :' ,int((df['year'].mode())))
    # Display earliest, most recent, and most common year of birth
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    

def display_data(df):
    i=0
    display=''
    while display.lower() not in {'yes','no'}:
        display = input('\nWould you like to view data? Enter yes or no.\n')
        

        
        while display.lower()=='yes': 
            # print('start',i)
            #print(df.shape[0],i)
            if (df.shape[0])<i:
                 print("No further data available reached end")
                 break
            else:
                 print("\nDisplaying five trips data:\n")
                 jr=df.iloc[i:i+5,1:].to_json(orient='records',date_format='iso')
                 print(js.dumps(js.loads(jr), indent=2))
                 #print(df.iloc[i:i+5,1:].to_dict('records'))
                 #print(df.iloc[i:i+5,1:].to_records())
                 #print(df.iloc[i:i+5,1:].to_latex())
                 #print( df.iloc[i:i+5,1:].to_json(orient='records',date_format='iso'))
                 display = input('\nWould you like to view data? Enter yes or no.\n')
                 i=i+5
       #print('end',i)
    return          
    
def main():
    while True:
        city, month, day = get_filters()
        print("Report for city ", city, " Filters used for Month, day :", month , " ," ,day )
        df = load_data(city, month, day)
        if df.empty:
             print("no data availabel for filters selected")
             break
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()    
