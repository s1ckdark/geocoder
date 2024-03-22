import googlemaps
import requests
from dotenv import load_dotenv
import os


def service(service, query):
    load_dotenv()
    if service == 'gcp':
        api_key = os.getenv('GCP_API_KEY') 
        return gcp(api_key, query)
    elif service == 'ncp':
        client_id = os.getenv('NCP_CLIENT_ID')
        secret = os.getenv("NCP_SECRET")
        api_key = {'client_id':client_id, 'secret':secret}
        return ncp(api_key, query)
    else:
        return None

def gcp(api_key, query):
    maps = googlemaps.Client(key=api_key)
    try:
        geo_location = maps.geocode(query)[0].get('geometry')['location']
        return geo_location
    except:
        return None

def ncp(api_key, query, **kwargs):
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    nheaders = {
        "X-NCP-APIGW-API-KEY-ID": api_key['client_id'],
        "X-NCP-APIGW-API-KEY": api_key['secret'],
        "Content-Type": "application/json",
    }   
    params = {
        "query": query
    }
    params.update(kwargs)
    res = requests.get(url, headers=nheaders, params=params)
    if res.status_code == 200:
        lat = res.json().get('addresses')[0].get('y')
        lng = res.json().get('addresses')[0].get('x')
        return {"lat":float(lat), "lng":float(lng)}
    else:
        return res