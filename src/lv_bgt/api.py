import time
import json
import requests
from zipfile import ZipFile
from pathlib import Path
from typing import Literal,Union,Iterable
import os
from datetime import datetime

URL = "https://api.pdok.nl"
FULL_CUSTOM_ENDPOINT = URL + "/lv/bgt/download/v1_0/full/custom"
DATASET_ENDPOINT = URL + "/lv/bgt/download/v1_0/dataset"
HEADER = {"Content-Type":"application/json","Accept": "application/json"}

class API:
    
    def get_features(drop_features=Iterable[str]) -> Iterable[str]:
        with requests.get(DATASET_ENDPOINT,headers=HEADER) as response:
            features = [row.get("featuretype") for row in response.json()["timeliness"]]
            if drop_features:
                features = list(set(features) - set(drop_features))
            features.sort()
            return features
         
    def _poll_download(status_url:str, timeout:int=5) -> str:
        with requests.Session() as session:
            while True:
                response = session.get(status_url,headers=HEADER).json()
                if (status:=response["status"])=="COMPLETED":
                    return response["_links"]["download"]["href"]
                    break
                else:
                    print(f"BGT extract download status: {status}",end="\r")
                    time.sleep(timeout)
                    
    def unpack_zip(zipfile:Path,delete_zip:bool=True) -> None:
        extract_folder = zipfile.with_suffix('')
        if not extract_folder.exists():
            with ZipFile(zipfile, "r") as src:
                src.extractall(extract_folder)
        if delete_zip:
            Path.unlink(zipfile)
            
        return extract_folder

    def download_full_custom(features:Iterable[str],format:Literal["citygml","gmllight","stufgeo"],geofilter:str,output:Union[str, os.PathLike]):
        
        if Path(output).suffix=='.zip':
            zipfile = Path(output)
        elif Path(output).is_dir() and Path(output).exists():
            zipfile = Path(output,f"{format}_extract.zip")
        else:
            raise IOError(f"Incorrect filename or location {output}")
        
        if not Path(zipfile).exists():
            try:
                payload = json.dumps({"featuretypes":features,"format":format,"geofilter":geofilter})
                
                with requests.post(FULL_CUSTOM_ENDPOINT,data=payload,headers=HEADER) as response:
                    status_url = URL + response.json()["_links"]["status"]["href"]
                    if (download_endpoint := API._poll_download(status_url)):
                        download_url = URL + download_endpoint
                        with requests.get(download_url,headers=HEADER) as content:
                            content.raise_for_status()
                            with open(zipfile,"wb") as dst:
                                for chunk in content.iter_content(chunk_size=1024):
                                    dst.write(chunk)
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
            else:
                print(f"BGT extract successfully downloaded to {zipfile}")
                
        else:
            print(f"{zipfile} already exists. Download skipped.")
            
        return zipfile
    
            

        
        


    
    


