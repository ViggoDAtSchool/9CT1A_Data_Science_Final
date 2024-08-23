# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import pandas as pd
import chartify as ch
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main(z):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "./mysecretfile.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().list(
        part="snippet, statistics",
        chart="mostPopular",
        maxResults=z
        )
    global data
    response = request.execute()
    its = response['items']
    cols = {}
    for i in its[0]: # Will error if something bad happens
        if isinstance(its[0][i], str):
            cols[i] = [j[i] for j in its]
        else:
            for k in its[0][i]:
                cols[k] = [(None if k not in j[i] else j[i][k]) for j in its]
    global data
    data = pd.DataFrame(cols)
    for i in ['viewCount', 'likeCount']:
        data[i] = data[i].astype('int')
    for i in ['publishedAt', 'commentCount']:
        data[i] = data[i].astype('object')
    global data_clean
    data_clean = data[['title', 'id', 'viewCount', 'likeCount', 'publishedAt', 'commentCount']]

def plot(x,y):
    global view
    view = ch.Chart(blank_labels=True, x_axis_type='linear', y_axis_type='linear')
    view.plot.scatter(
        data_frame=data,
        x_column=x,
        y_column=y,
    )
    view.plot.text(
        data_frame=data,
        x_column=x,
        y_column=y,
        text_column='',
        x_offset=1,
        y_offset=0,
        font_size='10pt'
    )
    view.set_title(x+' vs. '+y)
    view.set_subtitle('A simple plot of '+x+' compared to '+y+'.')
    view.show()

if __name__ == "__main__":
    val=input("How many videos would you like to search for? ")
    main(val)
    choice=input("""What would you like to do?
                 1: Print the original DataFrame.
                 2: Print the cleaned DataFrame.
                 3: Show a scatterplot of viewcount vs. likecount for the videos you searched.
                 4: Transfer the original DataFrame to a .csv file.
                 5: Exit the program.
                 """)
    if choice == "1":
        print(data)
    elif choice == "2":
        print(data_clean)
    elif choice == "3":
        x='viewCount'
        y='likeCount'
        plot(x,y)
    elif choice == "4":
        data.to_csv('data.csv', index=False)
    elif choice == "5":
        pass
    else:
        print("That is not a valid value, dummy.")