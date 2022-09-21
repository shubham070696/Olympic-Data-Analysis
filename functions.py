def medalCount(df):

    medalTally = df.drop_duplicates(subset = ['Team', 'NOC', 'Region',  'Games',  'Year', 'City', 'Sport', 'Event', "Medal"])

    return medalTally


def fetchCountry(df):

    country = df['Region'].dropna().unique().tolist()
    country = sorted(country)
    country.insert(0, "All Countries")

    return country


def fetchYear(df):
    year = df['Year'].unique().tolist()
    year  = sorted(year)
    year.insert(0, "All Years")
    return year

def country_year_medal_statistics(df, year, country):

    temp  = medalCount(df)

    if(year  == "All Years" and country == "All Countries"):

        temp = temp.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values( by=['Gold', 'Silver', 'Bronze'], ascending=False).reset_index()

        #return temp

    elif( year!= "All Years" and country == "All Countries"):

        temp = temp[temp['Year'] == int(year)]

        temp = temp.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(['Gold', 'Silver', 'Bronze'], ascending=False).reset_index()

    elif(year == 'All Years' and country!="All Countries"):

        temp = temp[temp['Region'] == country]

        temp = temp.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(['Gold', 'Silver', 'Bronze'], ascending=False).reset_index()

    else:

        temp = temp[(temp['Region'] == country) & (temp['Year'] == int(year))]

        temp = temp.groupby(['Region', 'Year']).sum()[['Gold', 'Silver', 'Bronze']].sort_values(['Gold', 'Silver', 'Bronze'], ascending=False).reset_index()

    temp['Total'] = temp['Gold'] + temp['Silver'] + temp['Bronze']
    temp[['Gold', 'Silver', 'Bronze', 'Total']] = temp[['Gold', 'Silver', 'Bronze', 'Total']].astype('int64')

    return temp

def trend_with_time(df, col):

   df =  df[['Year', col]].drop_duplicates().groupby('Year').count().reset_index().sort_values('Year', ascending=True)
   temp  =""

   if(col == 'Region'):

       temp ='Nations'

   elif(col =='Event'):

       temp  = "Events"

   else:

       temp = "Artists"

   df = df.rename(columns= { col: temp})

   return df, temp


def countryStats(df, country):


    temp = medalCount(df)
    temp.dropna(subset=['Medal', 'Bronze', 'Gold', 'Silver'])
    temp = temp[temp['Region'] == str(country)].groupby('Year')['Bronze', 'Gold', 'Silver'].sum()
    return temp

def sportHeatmap(df, country):

    temp = medalCount(df)
    temp = temp.dropna(subset=['Medal'])
    temp = temp[['Region', 'Sport', 'Medal']]
    temp = temp[temp['Region'] == country]
    temp = temp.groupby(['Region', 'Sport']).count().reset_index().sort_values(by='Medal', ascending=False)
    #temp.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return temp

def topAthletes(df, country):

    temp = df.dropna(subset=['Medal'])
    temp['Total'] = temp['Gold'] + temp['Silver'] + temp['Bronze']
    temp = temp[temp['Region'] == str(country)]
    temp = temp.groupby(['Name', 'Sport'])['Total'].count().sort_values(ascending=False).reset_index().head(10)

    return temp

def topPerformers(df):

    temp = medalCount(df)
    temp = temp.dropna(subset=['Medal', 'Bronze', 'Gold', 'Silver'])
    temp['Total'] = temp['Gold'] + temp['Silver'] + temp['Bronze']
    temp = temp.groupby(['Region'])['Total'].sum().sort_values(ascending = False).reset_index()
    temp[['Total']] = temp[['Total']].astype('int64')

    return temp


def ageDistribution(df):


    age = df[['Age', 'Height', 'Weight']]
    age = age.fillna(0)
    age['Age'] = age['Age'].astype('int64')

    return age

def medaldistributionAge(df):
    age = df[['Age','Sex' , 'Height', 'Weight', 'Medal']]

    age = age.dropna(subset = ['Medal'])
    age = age.fillna(0)
    age['Age'] = age['Age'].astype('int64')

    return age[(age['Age']!=0) & (age['Height']!=0.0)]

def womenParticipation(df):

    sex = df[['Sex', 'Year']]
    sex = sex[sex['Sex'] == 'F']
    return sex.groupby('Year').count().reset_index()












