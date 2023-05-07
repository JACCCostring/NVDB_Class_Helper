from nvdbWrapper import NVDBWrapperClass
from nvdbWrapper import EspecificObjectTasks

def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def main():
    raw = NVDBWrapperClass.rawObject(581)
    # data = EspecificObjectTasks.findRelation(EspecificObjectTasks.constructEndPoint(67, 89201351), 'Ventilasjonsanlegg')
    # vegRef = EspecificObjectTasks.findVegReferanse(67, 89201351)
    # d = EspecificObjectTasks.getMeta(581, 89201350)
    # print(data)
    more = raw.nesteForekomst()

    while more:
        for object in raw:
            name = EspecificObjectTasks.getMeta(object)['navn']
            id = EspecificObjectTasks.getMeta(object)['id']

            relation = object['relasjoner']
            barn = relation['barn']

            for object in barn:
                for vegObj in object['vegobjekter']:
                    data = EspecificObjectTasks.findRelation(EspecificObjectTasks.constructEndPoint(67, int(vegObj)), parentObjectName=name, objectType=id)
                    print(data)

        more = raw.nesteForekomst()
   
main()