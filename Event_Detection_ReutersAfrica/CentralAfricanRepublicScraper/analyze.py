import pandas as pd
from nltk import word_tokenize
from utils import recognize_entities, check_for_mission_verbs, process_content, extract_data
from geopy.geocoders import Nominatim


geolocator = Nominatim()

def filter_and_analyze_content(raw_dataframe, mission_verbs):
    '''
    Takes a dataframe of scraped content, processes it and returns a dataframe with the events of interest and
    the coordinates for those events.

    These events are displayed on a map in an ipynb file, because PyCharm does not support Folium (python
    mapping package) rendering.
    '''

    # Create dataframe to save filtered the filtered event
    event_dataframe = pd.DataFrame(columns=['title','content',
                                            'date','link','tags', 
                                            'location', 'organisation','longitude', 'latitude'])
    
    for idx in range(len(raw_dataframe.index)):
        
        row = raw_dataframe.loc[idx]
        
        title, content, time, source = extract_data(row)
        
        content_processed = process_content(content)
        
        content_tokenized = word_tokenize(content_processed)
        
        mission_verb_tags = check_for_mission_verbs(content_tokenized, mission_verbs)
        
        if len(mission_verb_tags) != 0:
            location, organization, longitude, latitude = recognize_entities(content_processed)
    
            row = [title, content_processed, time, source, mission_verb_tags, location, organization, longitude, latitude]
            
            event_dataframe.loc[len(event_dataframe)] = row


            
    return event_dataframe, len(event_dataframe)  