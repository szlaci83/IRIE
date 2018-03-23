from urllib import urlencode
import requests
import json

PORT = '443'
SERVER_URL = 'http://46.101.25.210'
LOCALHOST = 'http://0.0.0.0'

URL = SERVER_URL

loc_endpoint = URL + ':' + PORT + '/location'
event_endpoint = URL + ':' + PORT + '/event'
emotion_endpoint = URL + ':' + PORT + '/emotion'
headers = {'content-type': 'application/json'}

# Should return 200 if it was successful
def createEvent(event):
    if 'name' in event:
        res = requests.post(event_endpoint, json.dumps(event, ensure_ascii=False), headers=headers)
    else:
        raise ValueError('ERROR : JSON does not contain id or name fields!')
    return res.status_code

# if id given returns single event as dict, otherwise events as list of dicts
def getEvent(id = None):
    if id is not None:
        res = requests.get(event_endpoint + '/' + str(id), headers=headers).json()[0]
    else:
        res = requests.get(event_endpoint, headers=headers).json()
    return res

# Should return 200 if it was successful
def createLocation(location):
    if 'name' in location:
        res = requests.post(loc_endpoint, json.dumps(location, ensure_ascii=False), headers=headers)
    else:
        raise ValueError('ERROR : JSON does not contain id or name fields!')
    return res.status_code

# if id given returns single location as dict, otherwise locations as list of dicts
def getLocation(id = None):
    if id is not None:
        res = requests.get(loc_endpoint + '/' + str(id), headers=headers).json()[0]
    else:
        res = requests.get(loc_endpoint, headers=headers).json()
    return res

# Should return 200 if it was successful
def createEmotion(emotion):
    fields = ['timestamp', 'event', 'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    for field in fields:
        if not emotion or not field in emotion:
            raise ValueError('ERROR : JSON does not contain the right fields!')

    res = requests.post(emotion_endpoint, json.dumps(emotion, ensure_ascii=False), headers=headers)
    return res.status_code

# returns list of emotions
def getEmotion(location, event, fromDate, toDate):
    params = {}
    if location is not None:
        params['location'] =  location
    if event is not None:
        params['event'] =  event
    if fromDate is not None:
        params['fromDate'] = fromDate
    if toDate is not None:
        params['toDate'] =  toDate

    return requests.get(emotion_endpoint, headers=headers, params=urlencode(params)).json()

if __name__ == "__main__":
    # example usage:
    test_emotion = {
    "angry": 9.0,
    "disgust": 5.0,
    "event": "TEST2",
    "fear": 0.08635248243808746,
    "happy": 0.0003344165743328631,
    "neutral": 0.82928866147995,
    "sad": 0.0723159909248352,
    "surprise": 0.0016576687339693308,
    "timestamp": "08-03-2018"
    }

    print(getLocation())
    print(getEvent())
    #print(createEvent({'name': 'TEST1'}))
    #print(createLocation({'name':'TEST1'}))
    #print (createEmotion(test_emotion))
    print(getEmotion(None,test_emotion['event'],None,None))