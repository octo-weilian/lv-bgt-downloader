from app import *
import json
import requests
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
                featuretypes.remove('plaatsbepalingspunt')
                
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
                    r = s.post(BASE_URL + FULL_CUSTOM_ENDPOINT,data=json.dumps(payload),headers=headers)
                    data = r.json()
                    status_endpoint = data["_links"]["status"]["href"]
                    download_id = data["downloadRequestId"]
                    if (download_endpoint := self.await_download(status_endpoint)):
                        download_url = BASE_URL+ download_endpoint
                        download_content = s.get(download_url).content
                        with open(output+".zip","wb") as dst:
                            dst.write(download_content)

                        if unzip:
                            self.extract_zip(output)
                            
                        print(f"{extract_format.capitalize()} successfully downloaded to {output}")
                        

                except Exception as e:
                    print(f"Error: {e}")
        
        return os.path.abspath(output)
            
            
           


    
    


