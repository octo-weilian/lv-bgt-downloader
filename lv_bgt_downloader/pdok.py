from . import *

HTTP_HEADER = {'Content-Type':'application/json','Accept': 'application/json'}

BASE_URL = "https://api.pdok.nl"
FULL_CUSTOM_URL = BASE_URL + "/lv/bgt/download/v1_0/full/custom"
DATASET_URL = BASE_URL + "/lv/bgt/download/v1_0/dataset"

class BGT_API:
    
    @staticmethod   
    def get_features():
        with requests.Session() as s:
            try:
                response = s.get(DATASET_URL).json()
                features = {} 
                for row in response["timeliness"]:
                    features[row.get("featuretype")] = row.get('datetimeTo')

                return features
            except Exception as e:
                LOGGER.error(e)

    @staticmethod            
    def await_download(status_url,timeout=5):
        with requests.Session() as s:
            while True:
                response = s.get(status_url).json()
                if (status:=response["status"])!="COMPLETED":
                    RLOGGER.info(f"Download request progress: {status}")
                    time.sleep(timeout)
                else:
                    return response["_links"]["download"]["href"]
                    break

    @staticmethod
    def extract_zip(zipfile,outputdir,delete_zip = True):
        
        outputdir.mkdir(exist_ok=True)
        with ZipFile(zipfile, 'r') as src:
            src.extractall(outputdir)
        if delete_zip:
            Path.unlink(zipfile)

    @staticmethod   
    def download_full_custom(features,wkt,format,output_zip):
        
        payload = {"featuretypes":features,"format":format,"geofilter":wkt}
        try:

            with requests.Session() as s:
                response = s.post(FULL_CUSTOM_URL,
                                    data=json.dumps(payload),
                                    headers=HTTP_HEADER).json()

                status_url = BASE_URL + response["_links"]["status"]["href"]
                
                if (download_endpoint := BGT_API.await_download(status_url)):
                    download_url = BASE_URL + download_endpoint
                    with s.get(download_url) as content:
                        content.raise_for_status()
                        with open(output_zip,"wb") as dst:
                            for chunk in content.iter_content(chunk_size=1024):
                                dst.write(chunk)
                
        except Exception as e:
            LOGGER.error(e)
        else:
            return True
    
            

        
        


    
    


