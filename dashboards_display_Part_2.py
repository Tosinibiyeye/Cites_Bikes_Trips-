################################################ CHICAGO CITI BIKES DASHABOARD #####################################################
import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image
########################### Initial settings for the dashboard ##################################################################
st.set_page_config(
    page_title="CHICAGO CITI BIKES DASHABOARD",  # Title of the tab in the browser
    page_icon="🚴‍♂️",  # Optional: set a custom emoji/icon
    layout="wide"  # Use wide screen layout for better visibility
)
st.title("Bike Rides and Weather Dashboard")

# Sidebar for navigation
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot_2.gz', index_col = 0)
top_20_stations = pd.read_csv('top_20_stations.csv', index_col = 0)



########################################## DEFINE THE CHARTS #####################################################################

### Page sections

if page == "Intro page":
    st.markdown("""#### This dashboard provides insights into daily bike rides and weather patterns. 
               Explore trips from various stations, observe trends over time, and see how temperature correlates with biking activity.
                Use the interactive charts and visualizations below to dive deeper into the data.""")
    st.markdown("Right now, Chicago citi bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

          # Display the image
    my_image = Image.open("bikes_in_Chicago.jpg")  
    st.image(my_image, caption="Chicago Citi Bikes",width=1000 )

    ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

     # Create subplots with secondary y-axis
    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add the line for daily bike rides (in blue)
    fig_2.add_trace(
    go.Scatter(x=df['date'], y=df['bike_rides_daily'], name='Daily Bike Rides', line=dict(color='blue')),
    secondary_y=False
    )

    # Add the line for daily temperature (in red)
    fig_2.add_trace(
    go.Scatter(x=df['date'], y=df['avgTemp'], name='Daily Temperature', line=dict(color='red')),
    secondary_y=True
    )

    # Update layout with title
    fig_2.update_layout(
    title_text='Daily Bike Rides and Temperature Over Time',  # Set the title
    xaxis_title='Date',
    yaxis_title='Bike Rides',
    legend=dict(x=0.1, y=1.1)  # Position legend above plot
    )

    # Update y-axis titles
    fig_2.update_yaxes(title_text='Daily Bike Rides', secondary_y=False)
    fig_2.update_yaxes(title_text='Daily Temperature', secondary_y=True)

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage thiss insightt indicates that the shortage problem may be prevalent merely in the warmer months,approximately from May to October.")

    ### Most popular stations page

    # Create the season variable

elif page =='Most popular stations':
    
     ## Bar chart

    # Adding blue color to the palette
    fig = go.Figure(go.Bar(x = top_20_stations['start_station_name'], y = top_20_stations['trip_count'], marker =     {'color': top_20_stations['trip_count'],'colorscale': 'Blues'}))
    fig.update_layout(
     title = 'Top 20 most popular bike stations in Chicago',
     xaxis_title = 'Start stations',
     yaxis_title ='Sum of trips',
     width = 900, height = 600)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see Streeter Drive/Grand Avenue, Canal Street/Adams Streat as well Clinton Street/Madison Street. There is a big jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")

elif page == 'Interactive map with aggregated bike trips': 
     
    ### Add the kepler map ###

    path_to_html = "kepler_map.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f:html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in Chicago")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("Streeter Drive/Grand Avenue, Canal Street/Adams Street as well as Clinton Street/Madison Street.While having the aggregated bike trips filter enabled, we can see that even though Clinton Street/Madison Street is a popular start stations, it doesn't account for the most commonly taken trips.")
    st.markdown("The most common routes (>2,000) are between Theater on the Lake, Streeter Dr/Grand Avenue,Millenium Park, Columbus Dr/Randolph Street, Shedd Aquarium, Michigan Avenue/Oak Street, Canal Street/Adams Street, which are predominantly located along the water.")

     ### CONCLUSIONS PAGE: RECOMMENDATIONS

else:
    st.header("Conclusions and recommendations")
    bikes = Image.open("Chicago_citis_bikes .jpg")  #source: Midjourney
    st.image(bikes, width=1000 )
    st.markdown("### Our analysis has shown that Chicago citi bikes should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the water line, such as heater on the Lake, Streeter Dr/Grand Avenue, Millenium Park, Columbus Dr/Randolph Street, Shedd Aquarium, Michigan Avenue/Oak Street,Canal Street/Adams Street")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costss")

