import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

class AbstractPoster(ABC):
    def __init__(self, modified_data):
        #self.token = token
        self.modified_data = modified_data
        
    @abstractmethod
    def prepare_post(self):
        pass
        
    @abstractmethod
    def formXMLRequest(self, egenskaper_list):
        pass
