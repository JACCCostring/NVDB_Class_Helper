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
        
    @classmethod    
    def egenskaper(self, datakatalogId):
        endpointObjectType = "https://nvdbapiles-v3.atlas.vegvesen.no/vegobjekttyper/"+str(datakatalogId)+".json"
        
        data = requests.get(endpointObjectType)
        
        raw = data.text
        
        parsed = json.loads(raw)
        
        egenskapType = parsed['egenskapstyper']
        listOfNames = {}
        
        for item in egenskapType:
            listOfNames[item['navn']] = item['id']
                
        return listOfNames
    
    @classmethod    
    def especificEgenskaper(self, datakatalogId, egenskapName):
        endpointObjectType = "https://nvdbapiles-v3.atlas.vegvesen.no/vegobjekttyper/"+str(datakatalogId)+".json"
            
        data = requests.get(endpointObjectType)
            
        raw = data.text
            
        parsed = json.loads(raw)
            
        egenskapType = parsed['egenskapstyper']
        listOfEspecificProps = {}
            
        for item in egenskapType:
            if item['navn'] == egenskapName:
                for name, props in item.items():
                    if name == 'tillatte_verdier':
                        for especificProp in props:
                           listOfEspecificProps[especificProp['verdi']] = especificProp['id']
                    
        return listOfEspecificProps
