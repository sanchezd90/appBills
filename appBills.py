import os
import re
import json

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
                datos_iniciales=x.split("_")
                datos_archivo={
                    "cuitPrestador":datos_iniciales[0],
                    "puntoVenta":datos_iniciales[2],
                    "numero":datos_iniciales[3].strip(".txt"),
                    "fecha":None,
                    "cuitCliente":None,
                    "razonSocial":None,
                    "servicio":None,
                    "total":None,
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
                    for x in str_texto:
                        
                        #buscar monto total
                        if "Importe Total" in x:
                            i_total=str_texto.index(x)+1
                            split=str_texto[i_total].split(" ")
                            total=float(split[0].strip("b'").replace(",",".")) #hago un split porque esa linea tiene más de un valor y solo interesa el primero
                            datos_archivo["total"]=total
                        
                        #buscar fecha de emision
                        if "Fecha de Emisi" in x:
                            split=x.split(":")
                            fecha=split[1].strip()
                            datos_archivo["fecha"]=fecha[0:-3]
                        
                        #buscar CUIT
                        if "CUIT" in x and datos_archivo["cuitPrestador"] not in x:
                            split=x.split(":")
                            cuitCliente=split[1].strip()
                            datos_archivo["cuitCliente"]=cuitCliente[0:11]

                        #buscar razón social
                        if "Social:" in x:
                            split=x.split("Social:")
                            razonSocial=split[1].strip()
                            datos_archivo["razonSocial"]=razonSocial[0:-3]
                        
                        #buscar servicio
                        if "Producto / Servicio" in x:
                            i_servicio=str_texto.index(x)+1
                            servicio=str_texto[i_servicio]
                            search=re.search("\s[a-zA-Z]",servicio) #busco en la linea el punto en el que comienza la descripción del servicio prestado. Antes hay espacios en blanco.
                            servicio=servicio[search.start():]
                            datos_archivo["servicio"]=servicio[0:-3]

                data.append(datos_archivo)                  
    return data

def store(data):
    with open("data.json","w",encoding="utf-8") as f:
        content=json.dumps(data,indent=4)
        f.write(content)


#data=getData()
#store(data)



