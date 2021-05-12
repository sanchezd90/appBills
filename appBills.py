import os
import re

def trackFiles():
    counter=0
    numbers=[]
    first=None
    last=None
    missing=[]
    for x in os.listdir("."):
        if x.endswith(".txt"):
            counter+=1
            numbers.append(int(x[-7:-4]))
            first=min(numbers)
            last=max(numbers)
    for num in range(first,last+1):
        if num not in numbers:
            missing.append(num)
    return {
        "total":counter,
        "first":first,
        "last":last,
        "missing":missing
    }

def getData():
    #declaro el diccionario que va a contener toda la información
    data=[]

    #recorro cada documento para extraer los datos
    for x in os.listdir("."):
            if x.endswith(".txt"):
                datos_archivo={
                    "codigo":x.strip(".txt"),
                    "total":None,
                    "fecha":None,
                }
                with open(x,"rb") as f:
                    texto=f.readlines()

                    #convierto cada linea a string para poder hacer búsquedas de string
                    str_texto=[]
                    for x in texto:
                        str_texto.append(str(x))
                    
                    #Busqueda de datos
                    #declaro variables que me sirven cómo indices de búsqueda
                    i_total=None 
                    #recorro cada linea buscando información relevante
                    for x in str_texto:
                        if "Importe Total" in x:
                            i_total=str_texto.index(x)+1
                            split=str_texto[i_total].split(" ")
                            total=float(split[0].strip("b'").replace(",",".")) #hago un split porque esa linea tiene más de un valor y solo interesa el primero
                            datos_archivo["total"]=total
                        #TODO agregar el resto de los datos relevantes: fecha_emision,razon_social,servicio     
                data.append(datos_archivo)                  
    return data

print(getData()) 




