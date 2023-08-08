import requests

class AreaGeoDataParser:
    def __init__(self):
        pass
        
    @classmethod    
    def counties(self):
#        adding some headers 
        header = {'X-Client': 'QGIS NVDB Plugin'}
        response = requests.get(self.env + '/omrader/fylker.json', headers = header)
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
#        adding some headers 
        header = {'X-Client': 'QGIS NVDB Plugin'}
        response = requests.get(self.env + '/omrader/kommuner.json', headers = header)
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
        objectTypesEndPoint = self.env + "/vegobjekttyper.json"

#        adding some headers 
        header = {'X-Client': 'QGIS NVDB Plugin'}        
        response = requests.get(objectTypesEndPoint, headers = header)
        
        data = response.text
        
        parsedData = json.loads(data)
        
        dict = {}
        
        for item in parsedData:
            dict[item['navn']] = item['id']
        
        return dict
        
    @classmethod    
    def egenskaper(self, datakatalogId):
        endpointObjectType = self.env + "/vegobjekttyper/" + str(datakatalogId)
        
#        adding some headers 
        header = {'X-Client': 'QGIS NVDB Plugin'}
        data = requests.get(endpointObjectType, headers = header)
        
        raw = data.text
        parsed = json.loads(raw)

        egenskapType = parsed['egenskapstyper']
        listOfNames = {}
        
        for item in egenskapType:
            listOfNames[item['navn']] = item['id']
                
        return listOfNames
        
    @classmethod
    def especificEgenskaper(self, datakatalogId, egenskapName):
        endpointObjectType = self.env + "/vegobjekttyper/" + str(datakatalogId)

#        adding some headers 
        header = {'X-Client': 'QGIS NVDB Plugin'}
        data = requests.get(endpointObjectType, headers = header)
            
        raw = data.text
            
        parsed = json.loads(raw)
            
        egenskapType = parsed['egenskapstyper']
        listOfEspecificProps = {}
            
        for item in egenskapType:
            if item['navn'] == egenskapName:
                for name, props in item.items():
                    if name == 'datatype':
                        self.especificEgenskapDataType = props
                        
                    if name == 'tillatte_verdier':
                        for especificProp in props:
                           listOfEspecificProps[especificProp['verdi']] = especificProp['id']
                    
        return listOfEspecificProps
    
    @classmethod
    def egenskapDataType(self):
        return self.especificEgenskapDataType
        
    @classmethod
    def setEnvironmentEndPoint(self, env):
        self.env = env
        print(self.env)
