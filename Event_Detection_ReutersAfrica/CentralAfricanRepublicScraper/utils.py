import re
import spacy
import pandas as pd
#import en_core_web_sm
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from geopy.geocoders import Nominatim

#nlp = en_core_web_sm.load()
nlp = spacy.load('en_core_web_sm')

stemmer = PorterStemmer()
stopwords_english = stopwords.words('english')
geolocator = Nominatim()

def remove_html_tags(text):
    html_tag = re.compile(r'<[^>]+>')
    return html_tag.sub('', text)

def remove_punctuation(text):
    return re.sub("([^\\s\\w])"," ",text)

def extract_data(row):
    return row[0], row[1], row[2], row[4]

def process_content(content):
    html_removed_content = remove_html_tags(content)
    processed_content = remove_punctuation(html_removed_content)
    return processed_content

def check_for_mission_verbs(tokenized_content, mission_verbs):
    '''
    takes tokenized content (output of NLTK's 'word_tokenize()') and NATO mission verbs,
    stems it and returns entities containing NATO mission verbs. This creates a new dataset that will be used
    to recognize entities (cities, organizations).
    '''
    mission_verb_tags = []
    for word in tokenized_content:
        word = word.lower()
        
        if word not in stopwords_english:
            word_stemmed = stemmer.stem(word)
            for verb in mission_verbs:
                if word_stemmed == verb and verb not in mission_verb_tags:
                    mission_verb_tags.append(verb)
                    
    return mission_verb_tags 
            
def recognize_entities(processed_content):
    '''
    Uses Spacy's nlp method and identifies entities with location ('GPE') and organization ('ORG'). From the location
    it extracts the latitude and longitude so the event can be displayed on a map.
    '''
    location = []
    organization = []
    longitude =[]
    latitude = []
    
    ner = nlp(processed_content)

    for entity in ner.ents:
        
        if entity.label_ == 'GPE':
            loc = geolocator.geocode(entity)
            print(entity)
            long = loc.longitude
            lat = loc.latitude

            location.append(entity)
            longitude.append(long)
            latitude.append(lat)

        if entity.label_ == 'ORG':
            organization.append(entity)

    return location, organization, longitude, latitude


def stem_mission_verbs(mission_verbs):
    stemmed_mission_verbs = []
    for verb in mission_verbs:
        verb = re.sub("\n","",verb)
        stem_verb = stemmer.stem(verb)
        stemmed_mission_verbs.append(stem_verb)
    return stemmed_mission_verbs

def mapping_data(df): #not used
    x, y = [], []
    for i in df.iterrows():
        x.append(df['longitude'][1])
        y.append(df['latitude'][1])
    return x, y


def process_coordinates(analyzed_content):
    '''
    Takes analyzed content (DataFrame), extracts first coordinates (in case there are multiple cities identified),
    converts the coordinates (strings) to floats so they can be plotted on a map.

    The map can not be rendered in PyCharm - See ipynb file 'Event Detection - Reuters Map' for interactive map.
    '''
    coords = []

    latitude = []
    longitude = []
    for i, row in analyzed_content.iterrows():
        single_coord = []
        if not row['latitude']:
            lat = 0
            long = 0
        else:
            lat = (row['latitude'][0])
            long = (row['longitude'][0])


        latitude.append(lat)
        longitude.append(long)
        coords.append(single_coord)

    analyzed_content['lat'] = latitude
    analyzed_content['long'] = longitude

    analyzed_content['lat'] = pd.to_numeric(analyzed_content['lat'])
    analyzed_content['long'] = pd.to_numeric(analyzed_content['long'])

    return analyzed_content