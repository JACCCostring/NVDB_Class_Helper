from nvdbapiv3 import nvdbFagdata

# from nvdbapiv3 import nvdbFagObjekt
# from nvdbapiv3 import nvdbVegnett
# from nvdbapiv3 import finnid

class EspecificObjectTasks:
    def __init__(self):
        pass

    @classmethod
    def constructEndPoint(self, datakatalogId, nvdbId):
        endpoint = f'https://nvdbapiles-v3.atlas.vegvesen.no/vegobjekter/{datakatalogId}/{nvdbId}' + '.json'
        self.objectType = datakatalogId
        
        response = requests.get(endpoint)

        if response.status_code == 200:
            return endpoint
            
        else: return 'empty'
    
    @classmethod
    def parseEndPoint(self, url):
        raw = requests.get(url)

        parsed = json.loads(raw.text)

        return parsed


    @classmethod
    def findVegReferanse(self, datakatalogId, nvdbId):
        endpoint = f'https://nvdbapiles-v3.atlas.vegvesen.no/vegobjekter/{datakatalogId}/{nvdbId}' + '.json'
        raw = requests.get(endpoint)

        parsed = json.loads(raw.text)

        for key, value in parsed.items():
            if key == 'lokasjon':
                for k, v in value.items():
                    if k == 'vegsystemreferanser':
                        for ke in v:
                            return ke['kortform']

    @classmethod
    def getMeta(self, raw):
        nvdbId = raw['id']
        
        for field, value in raw['metadata'].items():
            if field == 'type':
                return {
                    'id': value['id'],
                    'navn': value['navn'],
                    'nvdbId': nvdbId}
    
    @classmethod
    def findEspecificChildRelation(self, raw, child=True, name='Tunnelløp'):
        if child:
            for key, value in raw['relasjoner'].items():
                if key == 'barn':
                    for val in value:
                        type = val['type']
                        childName = type['navn']
                        
                        if childName == name:
                            return {
                                    'navn': type['navn'],
                                    'id': type['id'],
                                    'vegobjekter': val['vegobjekter']
                                        }
            
    @classmethod
    def findRelation(self, source, component='Ventilasjonsanlegg', parentObjectId=0, parentObjectName = 'foreldrenavn', objectType = 0):
        data = ""
        parsed = {}
        vegObj = ""
        
        if source != 'empty':
            raw = requests.get(source)

            if raw.status_code == 200:
                data = raw.text
                parsed = json.loads(data)

                vegObj = parsed['id']
            
        for key, value in parsed.items():
            if key == 'relasjoner':
                for item in value['barn']:
                    for key, value in item.items():
                        if key == 'type':
                            for k, v in value.items():
                                if k == 'navn':
                                    if value['navn'] == 'Vifte/Ventilator' or value['navn'] == component:
                                        dictionary = {
                                            'vegobjekt': parentObjectId,
                                            'relasjon': value['navn'],
                                            'objekttype': objectType,
                                            'navn': parentObjectName,
                                            'vegreferanse': self.findVegReferanse(self.objectType, int(vegObj))
                                        }

                                        return dictionary
    
    
    
class AreaGeoDataParser:
   def __init__(self):
       pass
        
    @classmethod    
    def counties(self):
        response = requests.get('https://nvdbapiles-v3.atlas.vegvesen.no/omrader/fylker.json')
        data = ''
        if response.status_code:
            data = response.text
            
            parsed = json.loads(data)
            dict = {}
            
            for iteration in parsed:
                dict[iteration['navn']] = iteration['nummer']
                
            return dict
            
    @classmethod    
    def communities(self):
        response = requests.get('https://nvdbapiles-v3.atlas.vegvesen.no/omrader/kommuner.json')
        data = ''
        if response.status_code:
            data = response.text
            
            parsed = json.loads(data)
            dict = {}
            self.communitiesInCounties = {}
            
            for iteration in parsed:
                dict[iteration['navn']] = iteration['nummer']
                self.communitiesInCounties[iteration['navn']] = iteration['fylke']
                
            return dict
            
    @classmethod
    def fetchAllNvdbObjects(self):
        objectTypesEndPoint = "https://nvdbapiles-v3.atlas.vegvesen.no/vegobjekttyper.json"
        
        response = requests.get(objectTypesEndPoint)
        
        data = response.text
        
        parsedData = json.loads(data)
        
        dict = {}
        
        for item in parsedData:
            dict[item['navn']] = item['id']
        
        return dict
