#!/usr/bin/env python
# coding: utf-8

# %load bikeshare.py
import time
from datetime import date
import pandas as pd
import numpy as np
import calendar

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while True:
            city = input("Please enter a city to filter by (Chicago, New York City, Washington):\n").strip().lower()
            try:
                if city in ['chicago', 'new york city', 'washington']:
                    print("You chose: " + city.title())
                    break
            except:
                print(city + " is an invalid input! Please choose between Chicago, New York City, or Washington\n")

            print(city + " is an invalid input! Please choose between Chicago, New York City, or Washington\n")



    #get user input for month (all, january, february, ... , june)
    #used calendar module from https://stackoverflow.com/questions/40076887/convert-python-abbreviated-month-name-to-full-name
    month = ""
    month_abbr_dict = dict(zip(calendar.month_abbr[1:], calendar.month_name[1:]))
    while True:
            month = input("Please enter a month of the year, or choose 'all' (Full month or 3 letter abbreviation accepted):\n").strip().lower()
            try:
                #if month in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all']:
                if month.title() in calendar.month_name:
                    print("You chose: " + month.title())
                    break
                #elif month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'all']:
                elif month.title() in calendar.month_abbr:
                    month = month_abbr_dict[month.title()].lower()
                    print("You chose: " + month.title())
                    break
                elif month == 'all':
                    print("You chose: all months")
                    break
            except Exception as e:
                print(e)
                print(month + " is an invalid input! Please enter a month of the year, or choose 'all'\n")

            print(month + " is an invalid input! Please enter a month of the year, or choose 'all'\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    day_abbr_dict = dict(zip(calendar.day_abbr, calendar.day_name))
    while True:
            day = input("Please enter a day of the week, or choose 'all' (Full day or 3 letter abbreviation accepted):\n").strip().lower()
            try:
                if day.title() in calendar.day_name:
                    print("You chose: " + day.title())
                    break
                elif day.title() in calendar.day_abbr:
                    day = day_abbr_dict[day.title()].lower()
                    print("You chose: " + day.title())
                    break
                elif day == 'all':
                    print("You chose: all days")
                    break
            except Exception as e:
                #print(e)
                print(day + " is an invalid input! Please enter a day of the week, or choose 'all'\n")

            print(day + " is an invalid input! Please enter a day of the week, or choose 'all'\n")

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

    #import csv based on city input
    df = pd.read_csv(CITY_DATA[city])
    df.columns = df.columns.str.replace(' ', '_')

    #convert Start_Time to datetime dtype
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])

    #Check if input was 'all', if not, convert month to int and compare with df to filter
    if month != 'all':
        month = time.strptime(month, "%B").tm_mon
        is_month = df['Start_Time'].dt.month == month
        df = df[is_month]

    #Same as month if block, but compare for weekdays
    if day != 'all':
        day = time.strptime(day, "%A").tm_wday
        is_day = df['Start_Time'].dt.weekday == day
        df = df[is_day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        month_list = list(calendar.month_name)
        common_month = df.groupby(df['Start_Time'].dt.month)['Start_Time'].count().sort_values(ascending=False).head(1)
        print("The most common month to travel is {}, with a count of {}.".format(month_list[common_month.index[0]], common_month.values[0]))
        print(". "*10)


    # display the most common day of week
    if day == 'all':
        day_list = list(calendar.day_name)
        common_day = df.groupby(df['Start_Time'].dt.weekday)['Start_Time'].count().sort_values(ascending=False).head(1)
        print("The most common day to travel is {}, with a count of {}.".format(day_list[common_day.index[0]], common_day.values[0]))
        print(". "*10)

    # display the most common start hour
    if not df.empty:
        common_hour = df.groupby(df['Start_Time'].dt.hour)['Start_Time'].count().sort_values(ascending=False).head(3)
        print("Top 3 hours of travel:")
        print(common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df.groupby(df['Start_Station'])['Start_Station'].count().sort_values(ascending=False).head(10)
    print("The most commonly used start station is {}, with a count of {}.".format(common_start_station.index[0], common_start_station.values[0]))
    print(". "*10)

    # display most commonly used end station
    common_end_station = df.groupby(df['End_Station'])['End_Station'].count().sort_values(ascending=False).head(10)
    print("The most commonly used end station is {}, with a count of {}.".format(common_end_station.index[0], common_end_station.values[0]))
    print(". "*10)

    # display most frequent combination of start station and end station trip
    #df.insert(2, "Month", df.Start_Time.str[5:7])
    df['Combo_Station'] = df['Start_Station'] + ' to ' + df['End_Station']
    common_combo_station = df.groupby(df['Combo_Station'])['Combo_Station'].count().sort_values(ascending=False).head(10)
    print("The most common trip is {}, with a count of {}.".format(common_combo_station.index[0], common_combo_station.values[0]))
    print(". "*10)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_sum = round(df['Trip_Duration'].sum(), 2)
    trip_count = df['Trip_Duration'].count()


    # display mean travel time
    trip_avg = df['Trip_Duration'].mean()


    print("The total travel time for these criteria is {}, with a count of {} trips.".format(trip_sum, trip_count))
    print("The average travel time was {}.".format(round(trip_avg, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df.groupby(df['User_Type'])['User_Type'].count().sort_values(ascending=False)
    print("Count of users by type is as follows:")
    print(user_count)
    print(". "*10)

    # Display counts of gender
    try:
        gender_count = df.groupby(df['Gender'])['Gender'].count().sort_values(ascending=False)
        print("Count of genders is as follows:")
        print(gender_count)
        print(". "*10)
    except:
        print("No data found for Gender!")


    # Display earliest, most recent, and most common year of birth
    try:
        oldest = df['Birth_Year'].min()
        youngest = df['Birth_Year'].max()
        common_birth = df.groupby(df['Birth_Year'])['Birth_Year'].count().sort_values(ascending=False).head(1)
        print("The youngest user recorded was born in {}, the oldest user recorded was born in {}.".format(int(youngest), int(oldest)))
        print("The most common year of birth was {}, with a count of {}.".format(int(common_birth.index[0]), common_birth.values[0]))
    except:
        print("No data found for Birth Year!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_data(df):
    """Displays 5 rows of data until there's none left"""

    print('\nDisplaying 5 rows of data...')

    df_len = len(df.index)
    end_row = 5

    trip_rows = df[(end_row-5):end_row]
    print(trip_rows)


    while True:
        try:
            see_data = input('\nWould you like to see more trip data? Enter yes or no.\n')
            if see_data.lower() == 'yes' and end_row <= df_len:
                end_row += 5
                trip_rows = df[(end_row-5):end_row]
                print(trip_rows)
            elif see_data.lower() == 'no' or end_row > df_len:
                break
            else:
                print("Invalid input! Please try again")
        except:
            print("Invalid input! Please try again")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        try:
            time_stats(df,month,day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            see_data = input('\nWould you like to see some trip data? Enter yes or no.\n')
            if see_data.lower() == 'yes':
                trip_data(df)
        except:
            #print(e)
            print("Search criteria returned no data! Please alter your search and try again.")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
