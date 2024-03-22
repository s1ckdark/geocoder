from geocoder import service as geocoder
import pandas as pd
import time
from datetime import datetime

def fetch(service):
    df = pd.read_json('data.json',encoding='utf-8-sig')
    geo = []
    t1 = time.time() #지오코딩 코드 처리 전 시각
       
    for idx, address in enumerate(df['kraddr']):   
        try:
            geo_location = geocoder(service, address)
            geo.append(geo_location)
            print(f"{idx}번째 인덱스 {address}의 좌표 {geo_location} 입니다.")
        
        except:
            print("%d번 인덱스 에러"%(idx))
            geo.append({})
        
    df['geo_location']=geo
    df.to_json('data.json',orient='records',force_ascii=False)

if __name__ == "__main__": 
    # ngeolocation = geocoder('ncp','서울특별시 용산구 유엔빌리지길 252 b101')
    # ggeolocation = geocoder('gcp','서울특별시 용산구 유엔빌리지길 252 b101')
    # print(ngeolocation)
    # print(ggeolocation)
    fetch('ncp')
