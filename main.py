# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json as js
import pandas as pd
import matplotlib as mlp
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
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
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        maxResults=100
        )
    global data
    #data = []
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
    #data = pd.concat(data, ignore_index=False, sort=True)

if __name__ == "__main__":
    main()
    print(data)
    data.to_csv('data.csv', index=False)
