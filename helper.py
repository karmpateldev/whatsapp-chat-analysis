from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # fetch the total messages number
    num_messages = df.shape[0]

    # fetch the total words number
    words = []
    for message in df["message"]:
        words.extend(message.split())

    # fetch the total media files number
    num_media = df[df["message"] == "<Media omitted>\n"].shape[0]

    # fetch the total links number
    links = []
    for message in df["message"]:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words), num_media, len(links)

def most_busy_user(df):
    num_users = df["user"].value_counts().head()
    per_users = round((df["user"].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns={"index":"name", "user":"percentage"})
    return num_users, per_users
    
def create_wordcloud(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != 'group_notification']
    temp = temp[temp["message"] != "<Media omitted>\n"]

    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=700, height=900, min_font_size=10, background_color="white")
    wordcloud = wc.generate(temp["message"].apply(remove_stop_words).str.cat(sep=" "))

    return wordcloud

def most_common_words(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != 'group_notification']
    temp = temp[temp["message"] != "<Media omitted>\n"]

    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()

    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    mcw_df = pd.DataFrame(Counter(words).most_common(20))

    return mcw_df

def emojis_analysis(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI["en"]])

    ea_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return ea_df

def monthly_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = df.groupby(['year', 'month']).count()["message"].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + " - " + str(timeline["year"][i]))
    timeline["time"] = time

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = df.groupby(['year', 'month', 'day']).count()["message"].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline["day"][i]) + " - " + timeline["month"][i] + " - " + str(timeline["year"][i]))
    timeline["time"] = time

    return timeline

def weekly_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["day_name"].value_counts()

def monthly_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["month"].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    activity_heatmap = df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0)

    return activity_heatmap

