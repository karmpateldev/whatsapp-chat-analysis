import re
import pandas as pd

def preprocess(data):

    messagePattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\spm\s-\s|\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\sam\s-\s'
    messages = re.split(messagePattern, data)[1:]

    datesPattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\spm|\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\sam'
    dates = re.findall(datesPattern, data)

    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'])

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    df.loc[df['date'].dt.hour <= 12, 'hour'] = df['date'].dt.hour
    df.loc[df['date'].dt.hour > 12, 'hour'] = df['date'].dt.hour - 12
    df['hour'] = df['hour'].astype(int)
    df['minute'] = df['date'].dt.minute
    df.loc[df['date'].dt.hour <= 11, 'meridiem'] = 'AM' 
    df.loc[df['date'].dt.hour >  11, 'meridiem'] = 'PM'
    df.loc[df['date'].dt.hour ==  0, 'hour'] = 12

    period = []
    for i in range(df.shape[0]):
        if (df.iloc[i]["hour"] == 11) & (df.iloc[i]["meridiem"] == "PM"):
            period.append(str(df.iloc[i]["hour"]) + " PM" + " - " + str(df.iloc[i]["hour"] + 1) + " AM")
        elif (df.iloc[i]["hour"] == 11) & (df.iloc[i]["meridiem"] == "AM"):
            period.append(str(df.iloc[i]["hour"]) + " AM" + " - " + str(df.iloc[i]["hour"] + 1) + " PM")
        elif (df.iloc[i]["hour"] == 12):
            period.append(str(df.iloc[i]["hour"]) + " " + str(df.iloc[i]["meridiem"]) + " - " + "1" + " " + str(df.iloc[i]["meridiem"]))
        else:
            period.append(str(df.iloc[i]["hour"]) + " " + str(df.iloc[i]["meridiem"]) + " - " + str(df.iloc[i]["hour"] + 1) + " " + str(df.iloc[i]["meridiem"]))
            
    df["period"] = period
    
    return df
