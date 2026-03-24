import time
import pandas as pd
import numpy as np

# Map of city names to their data files
CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """Asks the user for city, month and day to analyze."""

    print("\nWelcome! Let's analyze some US bikeshare data.\n")

    # Allowed inputs
    cities = {
        'chicago': 'chicago',
        'new york': 'new york city',
        'new york city': 'new york city',
        'nyc': 'new york city',
        'washington': 'washington'
    }

    while True:
        city = input("Choose a city (Chicago, New York City, Washington): ").strip().lower()
        if city in cities:
            city = cities[city]
            break
        print("That's not a valid option, try again.\n")

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Choose a month (January–June) or 'all': ").strip().lower()
        if month in months:
            break
        print("Invalid month. Please try again.\n")

    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    while True:
        day = input("Choose a day of the week or 'all': ").strip().lower()
        if day in days:
            break
        print("Invalid day. Try again.\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Loads the data for the selected city and applies filters."""

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics related to most common travel times."""

    print('\nCalculating frequent travel times...\n')
    start_time = time.time()

    print("Most common month:", df['month'].mode()[0].title())
    print("Most common day:", df['day_of_week'].mode()[0].title())
    print("Most common start hour:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics related to stations and trips."""

    print('\nCalculating station statistics...\n')
    start_time = time.time()

    print("Most common start station:", df['Start Station'].mode()[0])
    print("Most common end station:", df['End Station'].mode()[0])

    df['trip_route'] = df['Start Station'] + " -> " + df['End Station']
    print("Most frequent trip:", df['trip_route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    print("Total travel time:", df['Trip Duration'].sum())
    print("Average travel time:", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays user demographic statistics."""

    print('\nCalculating user statistics...\n')
    start_time = time.time()

    print("User types:\n", df['User Type'].value_counts().to_string(), "\n")

    if 'Gender' in df.columns:
        print("Gender breakdown:\n", df['Gender'].value_counts().to_string(), "\n")
    else:
        print("No gender data for this city.\n")

    if 'Birth Year' in df.columns:
        print("Earliest year:", int(df['Birth Year'].min()))
        print("Most recent year:", int(df['Birth Year'].max()))
        print("Most common year:", int(df['Birth Year'].mode()[0]), "\n")
    else:
        print("No birth year data for this city.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw = input('\nSee raw data? (yes/no): ').strip().lower()
        row_start = 0

        while show_raw == 'yes':
            print(df.iloc[row_start:row_start + 5])
            row_start += 5

            if row_start >= len(df):
                print("\nNo more data available.")
                break

            show_raw = input("\nSee 5 more rows? (yes/no): ").strip().lower()

        restart = input('\nRestart program? (yes/no): ').strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()