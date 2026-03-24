import time
import pandas as pd
import numpy as np

# Dictionary mapping each city name to the corresponding CSV data file
CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """Asks the user for city, month and day to analyze."""

    print("\nHello! Let's explore some US bikeshare data.\n")

    # Dictionary of accepted city inputs (with variations in spelling)
    cities = {
        'chicago': 'chicago',
        'new york': 'new york city',
        'new york city': 'new york city',
        'nyc': 'new york city',
        'washington': 'washington'
    }

    # Loop asking for a valid city until a correct one is entered
    while True:
        city = input("Choose a city (Chicago, New York City, Washington): ").strip().lower()
        if city in cities:
            city = cities[city]
            break
        print("That's not a valid option, try again.\n")

    # List of allowed months for filtering
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    # Loop to validate month input from the user
    while True:
        month = input("Choose a month (January–June) or 'all': ").strip().lower()
        if month in months:
            break
        print("Invalid month. Please try again.\n")

    # List of available days for filtering
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

    # Loop to validate day input from the user
    while True:
        day = input("Choose a day of the week or 'all': ").strip().lower()
        if day in days:
            break
        print("Invalid day. Try again.\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Loads the data for the selected city and applies filters."""

    # Read the CSV file for the selected city
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time column into datetime for easier manipulation
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract useful time components (month, weekday, hour)
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filter the DataFrame by month if the user selected one
    if month != 'all':
        df = df[df['month'] == month]

    # Filter the DataFrame by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics related to most common travel times."""

    print('\nCalculating frequent travel times...\n')
    start_time = time.time()

    # Display the most common month, day of week, and hour of travel
    print("Most common month:", df['month'].mode()[0].title())
    print("Most common day:", df['day_of_week'].mode()[0].title())
    print("Most common start hour:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics related to stations and trips."""

    print('\nCalculating station statistics...\n')
    start_time = time.time()

    # Display the most commonly used start and end stations
    print("Most common start station:", df['Start Station'].mode()[0])
    print("Most common end station:", df['End Station'].mode()[0])

    # Create a combined trip string to identify the most frequent route
    df['Trip'] = df['Start Station'] + " -> " + df['End Station']
    print("Most frequent trip:", df['Trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # Show total and average duration values
    print("Total travel time:", df['Trip Duration'].sum())
    print("Average travel time:", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays user demographic statistics."""

    print('\nCalculating user statistics...\n')
    start_time = time.time()

    # Display counts of user types present in the dataset
    print("User types:\n", df['User Type'].value_counts().to_string(), "\n")

    # Display gender breakdown when present (Chicago & NYC)
    if 'Gender' in df.columns:
        print("Gender breakdown:\n", df['Gender'].value_counts().to_string(), "\n")
    else:
        print("No gender data for this city.\n")

    # Display birth year statistics when present
    if 'Birth Year' in df.columns:
        print("Earliest year:", int(df['Birth Year'].min()))
        print("Most recent year:", int(df['Birth Year'].max()))
        print("Most common year:", int(df['Birth Year'].mode()[0]), "\n")
    else:
        print("No birth year data for this city.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    # Main loop allowing the user to restart the program
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask user if they want to see raw data in increments of 5 rows
        show_raw = input('\nSee raw data? (yes/no): ').strip().lower()
        row_start = 0

        # Show raw data in chunks of 5 rows
        while show_raw == 'yes':
            print(df.iloc[row_start:row_start + 5])
            row_start += 5

            # Stop if we reach the end of the dataset
            if row_start >= len(df):
                print("\nNo more data available.")
                break

            show_raw = input("\nSee 5 more rows? (yes/no): ").strip().lower()

        # Ask user whether they want to restart the analysis
        restart = input('\nRestart program? (yes/no): ').strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()