import tweepy

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMpprAEAAAAAEDyK%2Fp%2Fg6mFfrcY6viqsnUjowc8%3DhuKZ5jZOmnowj5vXIJKQwu17EVJp3jji4eLvJS6v9yWNlY6hdq"

client = tweepy.Client(bearer_token=bearer_token)

# Eksempel: Find de nyeste tweets med 'breaking' fra DRNyheder
query = 'from:DRNyheder breaking lang:da -is:retweet'

tweets = client.search_recent_tweets(query=query, max_results=1)

print(tweets)
