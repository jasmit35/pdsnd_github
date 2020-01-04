"""
Bike Share - An interactive method of reporting share bike data for three select cities.
"""

import time
import pandas as pd
import numpy as np

"""
Constant global data used for selection and validation.
"""

VALID_DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

VALID_MONTHS = ["january", "february", "march", "april", "may", "june"]

VALID_CITIES = ["chicago", "new york city", "washington"]

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\n" + "-" * 60 + "\n")
    print("\nHello! Let's explore some US bikeshare data!\n")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in VALID_CITIES:
        print("Please enter one of the following city names or 'exit'...\n")
        print(str(VALID_CITIES) + " or 'exit'\n")
        city = str(input("===> "))
        city = city.lower()
        if city == "exit":
            return None, None, None

    # get user input for month (all, january, february, ... , june)
    month = ""
    while month not in VALID_MONTHS and month not in ("all", "exit"):
        print("\nPlease enter one of the following ...\n")
        print(str(VALID_MONTHS) + " or 'all' or 'exit'\n")
        month = input("===> ")
        month = month.lower()
        if month == "exit":
            return None, None, None

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day not in VALID_DAYS and day not in ("all", "exit"):
        print("Please enter one of the following...\n")
        print(str(VALID_DAYS) + " or 'all' or 'exit'\n")
        day = input("===> ")
        day = day.lower()
        if day == "exit":
            return None, None, None

    print("\n" + "-" * 60)
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
    input_file_name = CITY_DATA.get(city)

    #  Load the CSV file into a Pandas data frame
    df = pd.read_csv(input_file_name)

    #  Convert the format of the existing date field to a python DateTime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    #  Create new columns to filter on
    df["month"] = df["Start Time"].dt.month
    df["alpha_day"] = df["Start Time"].dt.weekday_name

    #  If a month was provided, filter on it
    if month != "all":
        month_num = VALID_MONTHS.index(month) + 1
        df = df[df["month"] == month_num]

    #  If a day was provided, filter on it
    if day != "all":
        df = df[df["alpha_day"] == day.title()]

    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()

    print(f"\nCalculating the most frequent times of travel in {city}.\n")

    #  Determine the month number with the most rides
    print("\nThe month with the largest number of rides...")
    if month == "all":
        month_index = df["month"].value_counts().idxmax()
        print(f"  {VALID_MONTHS[month_index - 1]}")
    else:
        print(
            f"  You restricted your data to {month} so that is the month with the most rides."
        )

    ride_count = df["month"].value_counts().max()
    print(f"    With a total of {ride_count} rides.\n")

    #  Determine the day of the week with the most rides
    print("The day of the week with the most number of rides...")
    if day == "all":
        weekday_index = df["alpha_day"].value_counts().idxmax()
        print(f"  {weekday_index}")
    else:
        print(f"You restriced your data to {day.title()} so it has the most rides")

    ride_count = df["alpha_day"].value_counts().max()
    print(f"    With a total of {ride_count} rides.")

    #  Determine the hour when most rides start
    hour_index = df["Start Time"].dt.hour.value_counts().idxmax()
    hour_count = df["Start Time"].dt.hour.value_counts().max()
    #  jasmit
    print("\nThe hour of the day when the most rides started...")
    print(f"  {hour_index} with a total of {hour_count} rides.")

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print("-" * 52)
    input("\nPress 'return' to contine")


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print(f"\nCalculating The Most Popular Stations and Trips in {city}.")
    start_time = time.time()

    # display most commonly used start station
    start_index = df["Start Station"].value_counts().idxmax()
    start_count = df["Start Station"].value_counts().max()
    print(f"The most popular station to start a ride - {start_index}")
    print(f"With a total of {start_count} rides.\n")

    # display most commonly used end station
    end_index = df["End Station"].value_counts().idxmax()
    end_count = df["End Station"].value_counts().max()
    print(f"The most popular station where rides end - {end_index}")
    print(f"With a total of {end_count} rides.\n")

    #  jasmit
    # display most frequent combination of start station and end station trip
    #    end_index = df['Start Station', 'End Station'].value_counts().idxmax()

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print("-" * 52)
    input("\nPress 'return' to contine")


def trip_duration_stats(df, city):
    # ---------------------------------------------------------------
    """Displays statistics on the total and average trip duration."""

    print(f"\nCalculating Trip Durations in the city of {city}.")

    start_time = time.time()

    # display total travel time
    df["Travel Time"] = pd.to_datetime(df["End Time"]) - pd.to_datetime(
        df["Start Time"]
    )
    print("Total travel time - " + str(df["Travel Time"].sum()))

    # display mean travel time
    print("Average travel time - " + str(df["Travel Time"].mean()))

    print("\nThese calculations took %s seconds." % (time.time() - start_time))
    print("-" * 52)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    start_time = time.time()

    print(f"\nCalculating user stats for travel in {city}.")
    print(f"\nHere is a summery of the type of users:")

    #  Display counts of gender
    print("\nThe breakdown of the riders based on gender:")
    counts = df["Gender"].value_counts()
    print(f"  Male riders   - {int(counts['Male'])}")
    print(f"  Female riders - {int(counts['Female'])}\n")

    # Display earliest, most recent, and most common year of birth
    earliest_birth = int(df["Birth Year"].min())
    print(f"The earliest year of birth among riders    - {earliest_birth}\n")

    recent_birth = int(df["Birth Year"].max())
    print(f"The most recent year of birth among riders - {recent_birth}\n")

    #     most_common_birth = df["Birth Year"].mode()
    most_common_birth = int(df["Birth Year"].mode())
    print(f"The most common year of birth among riders - {most_common_birth}\n")

    print("\nThese calculations took %s seconds.\n" % (time.time() - start_time))
    print("-" * 52)


def review_data(df):
    loop_counter = 1 #  this counter is used to determine which set of rows to display 
    done = None #  used to stop the loop
    while done != 'exit':
        print(f"{df.head(5 * loop_counter).tail(5)}")
        loop_counter += 1
        done = input(
            "\nPress 'Return' to continue or enter 'exit' to exit ===> "
        )

def main():
    """
    Get the values used to filer the data from the user.
    Filer the data from the input file.
    Call functions to calculate statistics based on dates, locations, trip times and users.
    """
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city)
        trip_duration_stats(df, city)
        #  The city of washington does not provide user statistics
        if city != "washington":
            user_stats(df, city)

        sample = input(
            "\nIf you would like a sample of the raw date, enter 'yes' ===> "
        )
        if sample.lower() == "yes":
            review_data(df)

        restart = input("\nEnter 'yes' if you would like to restart ===> ")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
