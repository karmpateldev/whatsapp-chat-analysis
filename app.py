import streamlit as st
import matplotlib.pyplot as plt
import preprocess, helper
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    # fetch uniques users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis Wrt.", user_list)

    if st.sidebar.button("Show Analysis"):
        
        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
        st.title("Total Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Total Media")
            st.title(num_media)

        with col4:
            st.header("Total Links")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            weekly_activity_map = helper.weekly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(weekly_activity_map.index, weekly_activity_map.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            monthly_activity_map = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_activity_map.index, monthly_activity_map.values, color="red")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        # Activity Heatmap
        st.title("Activity Heatmap")
        activity_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        st.pyplot(fig)

        # fetch the most busy users in chatting
        if selected_user == "Overall":

            st.title("Most Busy Users")

            num_users, per_users = helper.most_busy_user(df)
            col1, col2 = st.columns(2)
            fig, ax = plt.subplots()

            with col1:
                ax.bar(num_users.index, num_users.values, color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(per_users)
        
        # wordcloud
        st.title("WordCloud")
        wordcloud_img = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud_img)
        st.pyplot(fig)

                
        # most common words
        st.title("Most Common word")
        most_common_words = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_words[0], most_common_words[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
            
        # Emojis Analysis
        emojis_analysis = helper.emojis_analysis(selected_user, df)

        if len(emojis_analysis) != 0:
            st.title("Emojis Shared")

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emojis_analysis)

            with col2:
                fig, ax = plt.subplots()
                ax.pie(emojis_analysis[1].head(), labels=emojis_analysis[0].head(), autopct="%0.2f")
                st.pyplot(fig)



