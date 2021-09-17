#import matplotlib.pyplot as plt
import datetime

def main(): # Funcion principal
    
    # Aqui se imprime la primera parte del menu principal
    print("Datos de la demanda de New York ISO Load Data – USA.\n"
          "Seleccione una de las opciones o un archivo:\n"
          "0) Procesar todos los archivos.")
    
    # Este ciclo se encarga de imprimir todos los nombres de los archivos
    for i in range(1, 32): 
        print(str(i)+") " + str(i+20200100)+"pal.csv")
    
    # opFile almacenara el numero de la opcion escogida
    opFile = isValidOption(0, 31)
    
    clearScreen() # Se da la ilusion de limpiar la terminal
    
    # Esta lista almacena todas las zonas que se pueden graficar
    zones = ["CAPITL", "CENTRL", "DUNWOD", "GENESE", "HUD VL", "LONGIL", "MHK VL", 
             "MILLWD", "N.Y.C.", "NORTH", "WEST", "TOTAL"]
    
    # Se comprueba si se desean procesar todos los archivos o no y
    # se imprime un mensaje correspondiante a la opcion escogida
    if(opFile == 0):
        print("Usted selecciono procesar todos los archivos.")
    else:
        print("Usted selecciono el archivo", str(opFile+20200100)+"pal.csv")       
    print("Seleccione la zona a graficar:")     
    
    # Aqui se imprimen las zonas que hay de opciones
    for i in range(1,13):
        print(str(i)+")", zones[i-1])
        
    # opZone almacenara el numero de la zona escogida
    opZone = isValidOption(1, 12, "Ingrese el numero de la zona a graficar: ")
    print(opZone)
        
        
def isValidOption(rLower, rUpper, messaje = "Ingrese su opcion: "):
    
    option = input(messaje)
    while not(option.isdigit()) or int(option)<rLower or int(option)>rUpper:
        print("Opcion no valida. Intente de nuevo") # Mensaje de error
        option = input(messaje) # Se pide que se ingrese nuevamente una opcion
        
    return int(option) # Se retorna la opcion escogida por el usuario
        
def clearScreen():
    print("\n"*20)

def processDay(_day_): # Esta funcion se encarga de procesar los datos de un dia especifico
    # _day_: Variable que contiene el dia a procesar    
    
    file = open("data/" + _day_+ "pal.csv",'r') # Se abre el archivo correspondiente al dia a procesar
    text = file.readlines()[1:] # Esto es una lista donde cada una de sus posiciones es una linea del archivo anteriormente abierto
    data = {} # data almacenara los datos del archivo con el siguente formato {Time Stamp:{Name:Load}}
      
    for line in text:        
        # Aqui se crea una lista temporal con el formato [Time Stamp, Time zone, Name, PTID, Load]
        aux = line[:-1].split(',') # Variable auxiliar
        
        # Este ciclo se encarga de eliminar las comillas que estan al principio y final de las
        # las tres primeras posiciones de la lista 'aux'
        for i in range(0,3):
            aux[i] = aux[i][1:-1]            
        
        # Aqui se convierten de str a datetime los valores de Time Stamp 
        tempDate = datetime.datetime.strptime(aux[0], "%m/%d/%Y %H:%M:%S") # El valor de esta variable cambia con cada iteracion
        
        if aux[4] != "": # Se Load no tiene medida, se ignora ese tiempo en que debio ser tomada
            # Se verifica si existe una clave en 'data' igual a 'tempDate'
            if tempDate in data:
                # Si la clave existe se añade otro dato al diccionario correspondiente a su valor 
                data[tempDate][aux[2]] = float(aux[4])
            else:
                # Si la clave no existe, se crea y se le añade un diccionario con formato {Name: Load} como valor
                data[tempDate] = {aux[2]:float(aux[4])}
                
    file.close() # Se cierra el archivo correspondiente al dia _day_
    
    return data # Esta funcion retorna un diccionario con el formato {Time Stamp:{Name:Load}}

def hourlyAverage(_day_, _zone_="TOTAL"):
    zoneAverage = fiveMinutesResolution(_day_, _zone_)
    hourlyAverages = []
 
    for average in range(0,len(zoneAverage),12):
        tempAverage = 0
        for h in range(average,average+12):
            tempAverage += zoneAverage[h]
            
        hourlyAverages.append(tempAverage/12)
        
    return hourlyAverages

def fiveMinutesResolution(_day_, _zone_="TOTAL"):
    timeReference = list(_day_.keys())[0]
    resolution = []
    
    for mainKey in _day_:
        tempAverage = 0
        if mainKey == timeReference or mainKey > timeReference:
            for secondKey in _day_[mainKey]:
                if secondKey == _zone_ or _zone_=="TOTAL":
                    tempAverage += _day_[mainKey][secondKey]
            
            resolution.append(tempAverage)
            timeReference += datetime.timedelta(minutes=5)
        
    return resolution

hourlyAverage(processDay("20200115"))
    
if __name__ == '__main__':
    main()