from app import *
import json,requests
from zipfile import ZipFile

BASE_URL = APP_CONFIG["api"]["base_url"]
DATASET_ENDPOINT = APP_CONFIG["api"]["dataset_endpoint"]
FULL_CUSTOM_ENDPOINT = APP_CONFIG["api"]["full_custom_endpoint"]

class API:
    def get_featuretypes(self,discard_features):
        with requests.Session() as s:
            try:
                r = s.get(BASE_URL + DATASET_ENDPOINT)
                data = r.json()["timeliness"]
                featuretypes = [feature["featuretype"] for feature in data]

                if "plaatsbepalingspunt" not in discard_features:
                    featuretypes.remove("plaatsbepalingspunt")

                if discard_features:
                    for feature in discard_features:
                        featuretypes.remove(feature)

                return featuretypes
            except Exception as e:
                print(f"Error: {e}")
                
    def await_download(self,status_endpoint,timeout=5):
        with requests.Session() as s:
            while True:
                r = s.get(BASE_URL+status_endpoint)
                data = r.json()
                if (status:=data["status"])!="COMPLETED":
                    print(f"{time.ctime()} | Download request progress: {status}",end='\r')
                    time.sleep(timeout)
                else:
                    return data["_links"]["download"]["href"]
                    break
    
    def extract_zip(self,zipfile_dir):
        zipfile = zipfile_dir+'.zip'
        os.makedirs(zipfile_dir,exist_ok=True)
        with ZipFile(zipfile, 'r') as src:
            src.extractall(zipfile_dir)
        os.remove(zipfile)
       
    def download(self,features,wkt,output,extract_format="stufgeo",unzip=True):
        headers = {'Content-Type':'application/json','Accept': 'application/json'}
        payload = {"featuretypes":features,"format":extract_format,"geofilter":wkt}

        if not os.path.isdir(output):
            with requests.Session() as s:
                try:
                    data = s.post(BASE_URL + FULL_CUSTOM_ENDPOINT,data=json.dumps(payload),headers=headers).json()
                    status_endpoint = data["_links"]["status"]["href"]
                    if (download_endpoint := self.await_download(status_endpoint)):
                        with s.get(BASE_URL+ download_endpoint) as r_content:
                            r_content.raise_for_status()
                            with open(output+".zip","wb") as dst:
                                for chunk in r_content.iter_content(chunk_size=1024):
                                    dst.write(chunk)

                        if unzip:
                            self.extract_zip(output)

                except Exception as e:
                    print(f"Error: {e}")
                else:
                    print(f"{extract_format.capitalize()} successfully downloaded to {output}")
                    
     
            
           


    
    


