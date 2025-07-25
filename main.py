import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/mission_launches.csv")
pd.options.display.max_columns = None
pd.options.display.max_rows = None

date_mission_status_df = df.dropna()
clean_df = date_mission_status_df.drop_duplicates()

clean_df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

def run_challenge(description, func):
    print(f"\nChallenge: {description}")
    input("Press ENTER to see the result...\n")
    func()

## Who launched the most missions in any given year?--------------------------------------------------------------------
def most_missions_per_year():
    organisation_and_dates_df = clean_df[['Organisation', 'Date']].copy()
    organisation_and_dates_df['Date'] = organisation_and_dates_df['Date'].dt.year.astype('Int64')
    organisation_and_dates_df = organisation_and_dates_df.dropna(subset=['Date'])

    org_date_grouped_count_df = organisation_and_dates_df.groupby(['Date', 'Organisation']).size().reset_index(name='LaunchCount')
    print("Who launched the most missions in any given year?\n")
    most_launches_per_year = org_date_grouped_count_df.sort_values(by='LaunchCount', ascending=False).head(10)
    print(most_launches_per_year)

    top_orgs_per_year = org_date_grouped_count_df.loc[org_date_grouped_count_df.groupby('Date')['LaunchCount'].idxmax()].reset_index(drop=True)

    plt.figure(figsize=(14, 7))
    bars = plt.bar(top_orgs_per_year['Date'].astype(str), top_orgs_per_year['LaunchCount'], color='cornflowerblue')

    for bar, org in zip(bars, top_orgs_per_year['Organisation']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, org, ha='center', va='bottom', rotation=90, fontsize=10)

    plt.xlabel('Year')
    plt.ylabel('Number of Launches')
    plt.title('Organisation with Most Launches Per Year')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


##How has the cost of a space mission varied over time?-----------------------------------------------------------------

def analysis_cost_over_time():
    date_price_df = clean_df[['Date', 'Price']].drop_duplicates()
    sorted_date_price_df = date_price_df.sort_values(by='Date', ascending=True)
    sorted_date_price_df['Date'] = sorted_date_price_df['Date'].dt.tz_localize(None)
    sorted_date_price_df['Price'] = pd.to_numeric(sorted_date_price_df['Price'], errors='coerce')

    yearly_price = sorted_date_price_df.groupby(sorted_date_price_df.Date.dt.year)['Price'].mean().reset_index()
    print(yearly_price)

    plt.figure(figsize=(22, 14))
    plt.plot(yearly_price['Date'], yearly_price['Price'], marker='o')
    plt.xticks(rotation=45)
    plt.ylim(bottom=0, top=sorted_date_price_df['Price'].max()*1.2)
    plt.title('Average Cost for Space Missions')
    plt.xlabel('Year')
    plt.ylabel('Average Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

##Which months are the most popular for launches?-----------------------------------------------------------------------

def most_popular_months_for_launches():
    only_date_df = clean_df[['Date']].copy()
    only_date_df['Date'] = only_date_df['Date'].dt.month.astype('Int64')

    count_launches_per_month = only_date_df.groupby(['Date']).size().reset_index(name='LaunchCount')
    months_ranking_df = count_launches_per_month.sort_values(by='LaunchCount', ascending=False)
    print(months_ranking_df)

    plt.figure(figsize=(18, 8))
    bars = plt.bar(months_ranking_df['Date'].astype(str), months_ranking_df['LaunchCount'], color='cornflowerblue')

    plt.xlabel('Month')
    plt.ylabel('Number of Launches')
    plt.title('Month with Most Launches Per Year')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


##Have space missions gotten safer or has the chance of failure remained unchanged?-------------------------------------
def space_missions_safer_over_time():
    date_mission_status_df = clean_df[['Date', 'Mission_Status']].copy()

    date_mission_status_df['Year'] = date_mission_status_df['Date'].dt.year

    date_mission_status_cleaned = date_mission_status_df.dropna(subset=['Year', 'Mission_Status'])

    mission_status_counts = date_mission_status_cleaned.groupby(['Year', 'Mission_Status']).size().unstack(fill_value=0)

    mission_status_counts['Total'] = mission_status_counts.sum(axis=1)
    mission_status_counts['Failure_Rate'] = mission_status_counts.get('Failure', 0) / mission_status_counts['Total']
    print(f"Total mission count: {mission_status_counts['Total']}")
    print(f"Failure Rate: {mission_status_counts['Failure_Rate']}")

    plt.figure(figsize=(16, 10))
    plt.plot(mission_status_counts.index, mission_status_counts['Failure_Rate'])
    plt.xlabel('Year')
    plt.ylabel('Failure Rate')
    plt.title('Failure Rate of Space Missions Over Years')
    plt.xticks(mission_status_counts.index, rotation=45)
    plt.tight_layout()
    plt.show()


# ------------------ Run Challenges ------------------

run_challenge("Who launched the most missions in any given year?", most_missions_per_year)

run_challenge("How has the cost of a space mission varied over time?", analysis_cost_over_time)

run_challenge("Which months are the most popular for launches?", most_popular_months_for_launches)

run_challenge("Have space missions gotten safer or has the chance of failure remained unchanged?", space_missions_safer_over_time)
