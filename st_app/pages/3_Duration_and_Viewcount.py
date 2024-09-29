import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import pandas as pd
import utilities

st.write("# NorthStar метрики - количество уникальных просмотров и время просмотра")
utilities.dataset_discalaimer()

data = st.session_state['data']


# Convert the event_timestamp to datetime if it's not already
data['event_timestamp'] = pd.to_datetime(data['event_timestamp'])

# Extract just the date (without time) from the timestamp
data['event_date'] = data['event_timestamp'].dt.date

def plot_viewcount_hist(data):
    day_counts = data.groupby('event_date').size().reset_index(name='counts')

    # Create a list of repeating colors
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink', 'cyan']

    # Generate a repeating list of colors that corresponds to the rows in day_counts
    color_sequence = [colors[i % len(colors)] for i in range(len(day_counts))]

    # Create the bar plot with repeating colors
    fig = px.bar(day_counts, x='event_date', y='counts',
                 labels={'event_date': 'Day', 'counts': 'Number of Rows'},
                 title="Number of Unique Views per Day")

    # Update the colors manually in the figure
    fig.update_traces(marker_color=color_sequence)

    # Add vertical lines as dividers every 7 days using actual date labels
    for i in range(7, len(day_counts), 7):
        fig.add_vline(x=day_counts['event_date'][i], line_width=3, line_dash="dash", line_color="black")

    # Update x-axis to show only the dates present in the data
    fig.update_layout(xaxis_type='category')
    return fig


def plot_video_watchtime_per_day(data):
    # Group by date and calculate the sum of video durations for each day
    daily_watchtime = data.groupby('event_date')['total_watchtime'].sum().reset_index()

    # Create a repeating color sequence for the days of the week
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink', 'cyan']
    color_sequence = [colors[i % len(colors)] for i in range(len(daily_watchtime))]

    # Create a bar plot using Plotly Express
    fig = px.bar(daily_watchtime, x='event_date', y='total_watchtime',
                 labels={'event_date': 'Day ', 'total_watchtime': 'Total Video Watchtime (seconds)'},
                 title="Total Video Watchtime for Each Day")

    # Update the bar colors to repeat every 7 days
    fig.update_traces(marker_color=color_sequence)

    # Add vertical lines as dividers every 7 days
    for i in range(7, len(daily_watchtime), 7):
        fig.add_vline(x=daily_watchtime['event_date'][i], line_width=3, line_dash="dash", line_color="black")

    # Ensure x-axis only shows days present in the data
    fig.update_layout(xaxis_type='category')

    # Return the figure for display in Streamlit
    return fig

def plot_video_watchtime_to_duration_per_day(data):
    # Group by date and calculate the sum of video durations for each day
    data['watch_percentage'] = data['total_watchtime']/data['duration']*100
    daily_watchtime = data.groupby('event_date')['watch_percentage'].mean().reset_index()
    # Create a repeating color sequence for the days of the week
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink', 'cyan']
    color_sequence = [colors[i % len(colors)] for i in range(len(daily_watchtime))]

    # Create a bar plot using Plotly Express
    fig = px.bar(daily_watchtime, x='event_date', y='watch_percentage',
                 labels={'event_date': 'Day ', 'watch_percentage': 'Average watch percentage (%)'},
                 title="Average watch percentage for Each Day")

    # Update the bar colors to repeat every 7 days
    fig.update_traces(marker_color=color_sequence)

    # Add vertical lines as dividers every 7 days
    for i in range(7, len(daily_watchtime), 7):
        fig.add_vline(x=daily_watchtime['event_date'][i], line_width=3, line_dash="dash", line_color="black")

    # Ensure x-axis only shows days present in the data
    fig.update_layout(xaxis_type='category')

    # Return the figure for display in Streamlit
    return fig
def plot_video_count_per_day(data):
    # Ensure that 'event_date' is a datetime type column if not already done
    # Group by date and calculate the mean of 'videos_per_day' for each day
    user_video_counts = data.groupby(['event_date', 'viewer_uid']).size().reset_index(name='video_count')

    # Group by 'event_date' again to calculate the average number of videos watched per user for each day
    daily_avg_videos = user_video_counts.groupby('event_date')['video_count'].mean().reset_index()

    # Create a repeating color sequence for the days of the week
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink', 'cyan']
    color_sequence = [colors[i % len(colors)] for i in range(len(daily_avg_videos))]

    # Create a bar plot using Plotly Express
    fig = px.bar(daily_avg_videos, x='event_date', y='video_count',
                 labels={'event_date': 'Day', 'video_count': 'Average Videos Watched Per User'},
                 title="Average Number of Videos Watched Per User Per Day")

    # Update the bar colors to repeat every 7 days
    fig.update_traces(marker_color=color_sequence)

    # Add vertical lines as dividers every 7 days
    for i in range(7, len(daily_avg_videos), 7):
        fig.add_vline(x=daily_avg_videos['event_date'][i], line_width=3, line_dash="dash", line_color="black")

    # Ensure x-axis only shows days present in the data
    fig.update_layout(xaxis_type='category')

    # Return the figure for display in Streamlit
    return fig
def plot_category_views_per_day(data):
    # Ensure 'event_date' is a datetime type column if not already done
    data['event_date'] = pd.to_datetime(data['event_timestamp']).dt.date

    # Group by 'event_date' and 'category', and count the number of occurrences for each category per day
    category_views = data.groupby(['event_date', 'category']).size().reset_index(name='count')

    # Pivot the data to have categories as columns and dates as rows
    category_pivot = category_views.pivot(index='event_date', columns='category', values='count').fillna(0)

    # Create a stacked bar plot using Plotly Express
    fig = px.bar(category_pivot,
                 x=category_pivot.index,
                 y=category_pivot.columns,
                 labels={'value': 'Number of Entries', 'event_date': 'Day'},
                 title="Number of Entries for Each Category Per Day")

    # Update layout for better visualization
    fig.update_layout(barmode='stack', xaxis_title="Date", yaxis_title="Number of Entries")

    # Add vertical lines as dividers every 7 days
    for i in range(7, len(category_pivot.index), 7):
        fig.add_vline(x=category_pivot.index[i], line_width=3, line_dash="dash", line_color="black")

    # Return the figure for display in Streamlit
    return fig


# To display the chart in Streamlit:
# st.plotly_chart(plot_video_duration_per_day(data))
# Show the plot in Streamlit
st.write("#### 💙- Суббота 💚- Воскресенье ♥️- Понедельник 💜- Вторник 🧡- Среда 🩷- Четверг 🩵- Пятница")
viewcount, duration = st.columns(2)
viewcount.plotly_chart(plot_viewcount_hist(data))
duration.plotly_chart(plot_video_watchtime_per_day(data))
viewcount.plotly_chart(plot_video_watchtime_to_duration_per_day(data))
duration.plotly_chart(plot_video_count_per_day(data))
st.plotly_chart(plot_category_views_per_day(data))

