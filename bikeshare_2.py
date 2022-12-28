import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

DAY_LIST = [
    "all",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

MONTH_LIST = ["all", "january", "february", "march", "april" "may", "june"]


def check_user_input(inp, type):
    """
    Checks user's input"

     inp : The input from the user (city, month, day)
     type: The type of input: 1 = city, 2 = month, 3 = day
    """

    while True:
        read = input(inp)
        try:
            if read.lower() in CITY_DATA.keys() and type == 1:
                break
            elif read.lower() in MONTH_LIST and type == 2:
                break
            elif read.lower() in DAY_LIST and type == 3:
                break
            else:
                if type == 1:
                    print(
                        "Error, your city must be in: chicago new york city or washington"
                    )
                if type == 2:
                    print(
                        "Error, your month must be in: january, february, march, april, may, june or all"
                    )
                if type == 3:
                    print(
                        "Error, your day must be in: sunday, ... friday, saturday or all"
                    )
        except ValueError:
            print("Error, wrong input!")

    return read.lower()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_user_input("Enter city, (chicago, new york city, washington): ", 1)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = check_user_input("Enter month, (all, january, february, ... , june): ", 2)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_user_input("Enter day, (all, monday, tuesday, ... sunday): ", 3)

    print("-" * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month, day of week, hour from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df["month"].mode()[0]
    print("The most common month is:", common_month)

    # TO DO: display the most common day of week
    common_day = df["day_of_week"].mode()[0]
    print("The most common day of week is:", common_day)

    # TO DO: display the most common start hour
    common_start_hour = df["hour"].mode()[0]
    print("The most common start hour is:", common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print("The most commonly used start station is:", common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print("The most commonly used end station is:", common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    group = df.groupby(["Start Station", "End Station"])
    most_frequent_combination_station = (
        group.size().sort_values(ascending=False).head(1)
    )
    print(
        "The most frequent combination of start station and end station trip is:\n",
        most_frequent_combination_station,
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total Travel Time:", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("Mean Travel Time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User type stats:")
    print(df["User Type"].value_counts())
    if city != "washington":
        # TO DO: Display counts of gender
        print("Gender stats:")
        print(df["Gender"].value_counts())

        # TO DO: Display earliest, most recent, and most common year of birth
        print("Birth year stats:")
        most_common_year_of_birth = df["Birth Year"].mode()[0]
        print("Most Common Year:", most_common_year_of_birth)
        most_recent_year_of_birth = df["Birth Year"].max()
        print("Most Recent Year:", most_recent_year_of_birth)
        earliest_year_of_birth = df["Birth Year"].min()
        print("Earliest Year:", earliest_year_of_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def display_raw_data(df):
    """Displays 5 rows of data from the csv file for the selected city.

    df: Data frame.

    """
    RESPONSE = ["yes", "no"]
    raw_data = ""

    counter = 0
    while raw_data not in RESPONSE:
        print("\nDo you want to see the raw data?")
        print("\nPlease answer (Yes or No): ")
        raw_data = input().lower()
        # the raw data from the df is displayed if user opts for it
        if raw_data == "yes":
            print(df.head())
        elif rdata not in RESPONSE:
            print("\Error, answer only with (yes or no)!")
            print("\nRestarting..\n")

    # Extra while loop here to ask user if they want to continue viewing data
    while raw_data == "yes":
        print("Do you want to see the raw data?")
        counter += 5
        raw_data = input().lower()
        # If user opts for it, this displays next 5 rows of data
        if raw_data == "yes":
            print(df[counter : counter + 5])
        elif raw_data != "yes":
            break

    print("-" * 40)

def print_error():
    print("Error!")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
