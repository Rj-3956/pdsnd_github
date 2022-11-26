import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #get user input for city
    
    city_list= ['chicago', 'new york city', 'washington']
    
    while True:
        
        try:
            city = input("Enter city you want to explore - Chicago, New York City, Washington: ").lower().strip()
            
            if city in city_list:
                break
            else:
                print("\nThe city name is not valid, please try again: ")
            
        except:
            print('Invalid Input, please try again')
            
        
    # get user input for month (all, january, february, ... , june)
    
    
    month_list=['january', 'february','march','april','may','june']
    
    while True:
        try:
            
            month = input("\nname of the month to filter {}, or \"all\" to apply no month filter: ".format(month_list).title()).lower().strip()

            if month in month_list or month =='all':
                break
            else:
                print("Not a valid input, please try again: ")
        except:
                print("invalid input please try again")
                
                


    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    days_of_week=['monday', 'tuesday','wednesday','thursday','friday','saturday','sunday']

    while True:
        
        try:
            day = input('\nname of the day of week to filter {}, or "all" to apply no day filter: '.format(days_of_week).title()).lower().strip()
        
            if day in days_of_week or day =='all':
                break
            else:
                print("Not a valid input, please try again: ")
        except:
                print("invalid input please try again")     
                
                
    print('-'*40)
    return city, month, day


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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
   
    #extract most common month using month list to revert the number to month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df['month'].mode()[0]
    print("Most Common Month: ",months[common_month - 1].title())
    
    # extract most common day of the week
    common_day = df['day_of_week'].mode()[0]
    print("Most Common Day: ",common_day.title())
    
    # extract most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most Popular start hour is ",popular_hour)

        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station and trips
   
    popular_start_station = df['Start Station'].value_counts(sort=True)

    print('Most popular Start station is: ',popular_start_station.index[0])
    print('Total number of trips: ',popular_start_station.values[0])
    
    #display most commonly used end station and trips

    popular_end_station = df['End Station'].value_counts(sort=True)

    print('\nMost popular End station is: ',popular_end_station.index[0])
    print('Total number of trips: ',popular_end_station.values[0])
    
    
    #display most frequent combination of start station and end station trip
    
    #capture the start and end station using index position
    start_S, End_S = df.groupby(['Start Station','End Station']).size().idxmax()
    print("\nMost Frequent combination is Starting from station: {} \nand going to station: {}".format(start_S, End_S) )
    
    counts = df.groupby(['Start Station','End Station']).size().max()
    print("Frequenct: ",counts)
       

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_duration = df['Trip Duration'].sum()
    print("Totatl duration (in seconds): ", total_duration)
    
    average_duration = df['Trip Duration'].mean()
    print("Average Duration (in seconds): ", average_duration)


    # display mean travel time

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts(sort=True)
    
    df_user = pd.DataFrame(user_types)
    df_user.columns = ['Count']
    
    print(df_user)
    print('\n')
    
    
    #Display counts of gender
    #check if gender is present in dataset
    if 'Gender' in df:
        gender = df['Gender'].value_counts(sort=True)
        df_gender = pd.DataFrame(gender)
        df_gender.columns = ['Count']
    
        print(df_gender)
    else:
        print('Gender Data not available')
    print('\n')
    
    #Display earliest, most recent, and most common year of birth
    #check if year of birth is present
    
    if 'Birth Year' in df:
        print("Earliest year of birth: ", int(df['Birth Year'].min()))
        print("Most recent year of birth: ", int(df['Birth Year'].max()))
        print("Most common year of birth: ", int(df['Birth Year'].mode()[0]))
    else:
        print('Year of Birth Data not available')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def check_raw_data(df):
      
  
    """
    Asks user if they want to see raw data.

    Displays:
        5 rows at a time, if user accepts to see more data it keep printing next 5 rows in the data frame
    """
    
    #Checing raw data

    row_index=0
    while True:
        
        #get user input to check raw data
        try:
            check_raw_data = input('would you like to see some raw data \nEnter yes or y to continue or any other charector to exit: ').lower().strip()
            
            if check_raw_data not in ['y', 'yes']:
                break
            
        except:
            print('please enter proper value')
            
                

         
        print(df.iloc[row_index: row_index+5])
        row_index += 5
            
    

def main():
    
    while True:
        
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print('\nGetting details of {} for {} month(s) and {} day(s) '.format(city.title(), month.title(), day.title()))
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        check_raw_data(df)

        restart = input('\nWould you like to restart?\nEnter yes or y to continue. Press any other charector to exit. ')
        
        if restart.lower() not in ['y', 'yes']:
            break
           

if __name__ == "__main__":
	main()


