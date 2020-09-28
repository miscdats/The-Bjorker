# The-Bjorker
Are you as inspired as Bjork?

Using machine learning and Spotipy, this app compares the songs on Bjork's favorite albums to a playlist of your 
choice. The songs will be determined as inspiring to Bjork or not quite. The results will surprise you, so feel 
free to keep trying different playlists!

## Data pipeline
- Extracts songs data from Spotify with ```Redis``` queued workers using API wrapper Python package ```spotipy``` with ```pandas``` based on inputs and sets related to this project (i.e. Bjork's top 10 inspiring albums dataset part of training and validation set)
- Transforms track analysis data into usable tables, with values rescaled and used to train and test a machine learning model with ```scikit``` and ```keras```
- Loads downstream data after applying predict functions with model, visualizing test data results in ```Flask``` app deployed on Heroku

## Monitoring & Logs
DataDog

## Future Features
- Use URLs as well as URIs as input
- Able to enter multiple playlists at once
- Create joint playlists by inspiring tracks
- Create merged track lists by non-Bjork-approved songs
- More dashboard style options to visualize tracks data
- More!

## To Run
- ```python wsgi.py``` 
to start the local server
- ```localhost:5000``` 
to reach in your browser

App currently deployed on heroku at http://bjorker.herokuapp.com
