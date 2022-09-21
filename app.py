import streamlit as st
import pandas as pd

import preprocessing, functions

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


st.set_page_config(page_title="Olympic Analysis",
                   layout = 'wide',
                   page_icon='https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png',
                   initial_sidebar_state='collapsed')

sns.set_style("darkgrid", {"grid.color": ".6"})


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessing.preprocessing(df, region_df)
st.sidebar.markdown("<h1 style='text-align: center'>Olympics Analysis</h1>", unsafe_allow_html=True)
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

st.sidebar.write('\n')
user_selection = st.sidebar.radio("Choose an option",
                 ('Medal Tally', 'Overall Analysis', 'Country wise', 'Athlete wise'))


st.sidebar.write('\n')
if user_selection == 'Medal Tally':
    st.markdown("<h1 style='text-align: center'>Medal Statistics</h1>", unsafe_allow_html=True)

    years = functions.fetchYear(df)

    countries = functions.fetchCountry(df)

    year = st.sidebar.selectbox("Select Year", years)

    country = st.sidebar.selectbox("Select Country", countries)

    medals = functions.country_year_medal_statistics(df, year, country)

    if(year == "All Years" and country == "All Countries"):

        st.markdown("<h2 style='text-align: center'>Participating countries in Olympics</h2>", unsafe_allow_html=True)

    elif(year!= "All Years" and country == "All Countries"):

        st.title("Performance of countries in " + str(year))

    elif(year== "All Years" and country != "All Countries"):

        st.title("Performance of " + country+ " across olympics")

    else:

        st.title("Performance of " + country + " in " + str(year))

    st.table(medals)

if user_selection == "Overall Analysis":
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['Region'].unique().shape[0]


    st.markdown("<h1 style='text-align: center'>Top Statistics</h1>", unsafe_allow_html=True)
    st.write('\n')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='text-align: left'>Olympics so far</h4>", unsafe_allow_html=True)

        st.title(editions)
    with col2:
        st.markdown("<h4 style='text-align: left'>Host Cities</h4>", unsafe_allow_html=True)
        st.title(cities)
    with col3:
        st.markdown("<h4 style='text-align: left'>Sports played</h4>", unsafe_allow_html=True)
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='text-align: left'>Events hosted</h4>", unsafe_allow_html=True)
        st.title(events)
    with col2:
        st.markdown("<h4 style='text-align: left'>Participating Countries</h4>", unsafe_allow_html=True)
        st.title(nations)
    with col3:
        st.markdown("<h4 style='text-align: left'>Athletes Participated</h4>", unsafe_allow_html=True)
        st.title(athletes)

    st.write('\n')

    #top perfromers of all time
    topPerformers = functions.topPerformers(df).head(10).sort_values(by  = 'Total', ascending = True)
    st.markdown("<h3 style='text-align: center'>Top 10 countries with most medals</h3>", unsafe_allow_html=True)
    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor('#0E1117')
    sns.barplot(x = topPerformers['Region'], y = topPerformers['Total'])

    plt.ylabel("Total", color='white')

    plt.xlabel('Countries', color='white')

    plt.yticks(color='white')

    plt.xticks(color='white')

    fig.tight_layout()
    st.pyplot(fig)
    st.write('\n')

    #Performance of particular country
    nations_over_time, column = functions.trend_with_time(df, 'Region')
    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor('#0E1117')
    sns.lineplot(nations_over_time, x="Year", y=column, marker= 'o')
    #st.title("Participating Nations over the years")
    st.markdown("<h3 style='text-align: center'>Participating Nations over the years</h3>", unsafe_allow_html=True)
    fig.tight_layout()
    plt.ylabel("Nations", color='white')

    plt.xlabel('Year', color='white')

    plt.yticks(color='white')

    plt.xticks(color='white')
    st.pyplot(fig)
    st.write('\n')

    events_over_time, column = functions.trend_with_time(df, 'Event')
    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor('#0E1117')
    sns.lineplot(events_over_time, x="Year", y=column, marker='o')
    st.markdown("<h3 style='text-align: center'>Events over the years</h3>", unsafe_allow_html=True)
    fig.tight_layout()
    plt.ylabel("Event", color='white')

    plt.xlabel('Year', color='white')

    plt.yticks(color='white')

    plt.xticks(color='white')
    st.pyplot(fig)
    st.write('\n')

    athlete_over_time,column = functions.trend_with_time(df, 'Name')
    fig = plt.figure(figsize=(10, 5))
    fig.patch.set_facecolor('#0E1117')
    sns.lineplot(athlete_over_time, x="Year", y=column, marker='o')
    st.markdown("<h3 style='text-align: center'>Athletes over the years</h3>", unsafe_allow_html=True)
    fig.tight_layout()
    plt.ylabel("Athletes", color='white')

    plt.xlabel('Year', color='white')

    plt.yticks(color='white')

    plt.xticks(color='white')
    st.pyplot(fig)
    st.write('\n')

if user_selection == 'Country wise':

    st.sidebar.title('Country wise')

    countries = sorted(df['Region'].dropna().unique().tolist())

    country = st.sidebar.selectbox('Select a Country', countries)

    stats = functions.countryStats(df, country)
    st.markdown(f"""<h3 style='text-align: center'>{country}'s  medal tally over the years</h3>""", unsafe_allow_html=True)
    st.bar_chart(stats)


    st.write('\n')

    pt = functions.sportHeatmap(df, country)

    if(not pt.empty):
        st.markdown(f"""<h3 style='text-align: center'>{country}'s medal distribution across top 5 sports</h3>""", unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize = (10,6))

        fig1.patch.set_facecolor('#0E1117')
        plt.rcParams['text.color'] = 'white'

        if(len(pt) >= 5):


            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            explode = (0.05, 0.05, 0.05, 0.05, 0.05)
            ax1.pie(pt.head()['Medal'], colors = colors, labels=pt.head()['Sport'], autopct='%1.1f%%', startangle=90
                    , pctdistance=0.85, explode=explode)



        elif (len(pt) >= 1 and len(pt) < 5):

            ax1.pie(pt.head()['Medal'], labels=pt.head()['Sport'], autopct='%1.1f%%', startangle=90
                    , pctdistance=0.85)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        ax1.axis('equal')
        plt.tight_layout()

        st.pyplot(fig1)


    topAtheletes = functions.topAthletes(df, country)
    st.write('\n')

    if (not topAtheletes.empty):
        st.markdown(f"""<h3 style='text-align: center'>Top 10 athletes of {country}</h3>""",unsafe_allow_html=True)
        topAtheletes.index = np.arange(1, topAtheletes.shape[0] + 1)
        st.table(topAtheletes)


if user_selection == "Athlete wise":

    age = functions.ageDistribution(df)
    st.markdown("<h3 style='text-align: center'>Age distribution of artists</h3>", unsafe_allow_html=True)

    fig = plt.figure(figsize=(10, 5))

    fig.patch.set_facecolor('#0E1117')

    plt.hist(age['Age'], bins=np.arange(10, 80, 2), color='purple')

    plt.ylabel("Number of participants", color = 'white')

    plt.yticks(color = 'white')

    plt.xlabel('Age', color = 'white')

    plt.xticks(color = 'white')

    fig.tight_layout()

    st.pyplot(fig)


    medalDistribution  = functions.medaldistributionAge(df)
    st.markdown("<h3 style='text-align: center'>Medal distribution with Age & Height</h3>", unsafe_allow_html=True)

    fig = plt.figure(figsize=(10, 5))

    fig.patch.set_facecolor('#0E1117')

    sns.scatterplot(x= medalDistribution['Age'], y=medalDistribution['Height'], hue = df['Sex'])

    plt.ylabel("Height", color = 'white')

    plt.xlabel('Age', color = 'white')

    plt.yticks(color='white')

    plt.xticks(color='white')

    fig.tight_layout()

    st.pyplot(fig)


    womenParticipation = functions.womenParticipation(df)
    st.markdown("<h3 style='text-align: center'>Women participation over the years</h3>", unsafe_allow_html=True)

    fig = plt.figure(figsize=(10, 5))

    fig.patch.set_facecolor('#0E1117')

    sns.barplot(x=womenParticipation['Year'], y=womenParticipation['Sex'])

    plt.ylabel("Count", color = 'white')

    plt.xlabel('Year', color = 'white')

    plt.yticks(color='white')

    plt.xticks(color='white')

    plt.xticks(rotation = 90)

    fig.tight_layout()

    st.pyplot(fig)















