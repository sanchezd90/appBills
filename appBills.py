import os
import re
import json
import openpyxl


def trackFiles():
    """
    DESCRIPCIÓN: Esta función sirve para controlar los documentos
    hay en la carpeta. Revisa qué facturas están en la carpeta y 
    si falta alguna según el número de factura más alto. 

    DESCRIPTION: This function allows file tracking within the 
    current directory. It serves the purpose to detect missing
    bills.

    """
    #declaro las variables en las que necesito almacenar los datos
    #this variables store the main data, which become at the end the output 
    counter=0
    numbers=[]
    first=None
    last=None
    missing=[]
    
    #busco dentro de la carpeta las facturas (que son archivos de texto)
    #loops through every bill within the current directory
    for x in os.listdir("."):
        if x.endswith(".txt"):
            counter+=1
            numbers.append(int(x[-7:-4]))
            first=min(numbers)
            last=max(numbers)
    #controlo si falta algun número de factura en el medio del min y max
    #looks out for missing bills based on the min and max bill number
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
    """
    DESCRIPCIÓN: Esta función permite leer cada archivo y extraer los
    datos más relevantes de la factura. 

    DESCRIPTION: This function reads every bill file and extracts
    the most important data in the bill. 
    """

    #declaro la lista que va a contener los diccionarios de cada archivo
    #data stores the list of dictionaries, which hold the relevant data of every file
    data=[]

    #recorro cada documento y defino las keys del diccionario del archivo
    #loops through every file and sets the keys of the file's dictionary
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
                    #parse every line (binary) into string 
                    str_texto=[]
                    for x in texto:
                        str_texto.append(str(x))
                    
                    #Busqueda de datos
                    #Data search: 
                    i_total=None #index variable used to retrieve the line where the total price is
                    for x in str_texto:
                        
                        #buscar monto total
                        #search total price 
                        if "Importe Total" in x:
                            i_total=str_texto.index(x)+1
                            split=str_texto[i_total].split(" ")
                            total=float(split[0].strip("b'").replace(",",".")) #hago un split porque esa linea tiene más de un valor y solo interesa el primero
                            datos_archivo["total"]=total
                        
                        #buscar fecha de emision
                        #search issue date
                        if "Fecha de Emisi" in x:
                            split=x.split(":")
                            fecha=split[1].strip()
                            datos_archivo["fecha"]=fecha[0:-3]
                        
                        #buscar CUIT
                        #search for provider id 
                        if "CUIT" in x and datos_archivo["cuitPrestador"] not in x:
                            split=x.split(":")
                            cuitCliente=split[1].strip()
                            datos_archivo["cuitCliente"]=cuitCliente[0:11]

                        #buscar razón social
                        #search for clients business name
                        if "Social:" in x:
                            split=x.split("Social:")
                            razonSocial=split[1].strip()
                            datos_archivo["razonSocial"]=razonSocial[0:-3]
                        
                        #buscar servicio
                        #search for the provided service's name
                        if "Producto / Servicio" in x:
                            i_servicio=str_texto.index(x)+1
                            servicio=str_texto[i_servicio]
                            search=re.search("\s[a-zA-Z]",servicio) #busco en la linea el punto en el que comienza la descripción del servicio prestado. Antes hay espacios en blanco.
                            servicio=servicio[search.start():]
                            datos_archivo["servicio"]=servicio[0:-3]

                data.append(datos_archivo)                  
    return data

def writeJSON(data):
    """
    DESCRIPCION: Esta función crea un documento JSON en el que almacena los datos extraidos
    DESCRIPTION: This function stores the retrieved data into a JSON file.  
    """
    with open("data.json","w",encoding="utf-8") as f:
        content=json.dumps(data,indent=4)
        f.write(content)


def writeExcel(data):
    """
    DESCRIPCION: Esta función crea un documento XLSX en el que almacena los datos extraidos
    DESCRIPTION: This function stores the retrieved data into an XLSX file.  
    """
    wb = openpyxl.Workbook()
    sheet = wb["Sheet"]
    #headers
    sheet["A1"]="numero"
    sheet["B1"]="puntoVenta"
    sheet["C1"]="cuitPrestador"
    sheet["D1"]="fecha"
    sheet["E1"]="cuitCliente"
    sheet["F1"]="razonSocial"
    sheet["G1"]="servicio"
    sheet["H1"]="total"
    #data rows
    i=2 #this index is necessary to insert every data set into a new row
    for x in data:
        a="A"+str(i)
        b="B"+str(i)
        c="C"+str(i)
        d="D"+str(i)
        e="E"+str(i)
        f="F"+str(i)
        g="G"+str(i)
        h="H"+str(i)
        sheet[a]=x["numero"]
        sheet[b]=x["puntoVenta"]
        sheet[c]=x["cuitPrestador"]
        sheet[d]=x["fecha"]
        sheet[e]=x["cuitCliente"]
        sheet[f]=x["razonSocial"]
        sheet[g]=x["servicio"]
        sheet[h]=x["total"]
        i+=1
    wb.save("facturasAFIP.xlsx")

def loadExcel(data):
    """
    DESCRIPCION: Esta función actualiza el documento XLSX con nuevos datos si ya tiene información previa. 
    También permite crear un archivo nuevo si no había un anterior. 
    
    DESCRIPTION: This function updates the XLSX file with new data sets.  
    It creates a new file if there's no previous XLSX file in the directory. 
    """
    if "facturasAFIP.xlsx" in os.listdir("."):
        wb=openpyxl.load_workbook("facturasAFIP.xlsx")
        sheet=wb.active
        numeros=[]
        for x in list(sheet.columns)[0]:
            numeros.append(x.value)
        i=len(numeros)+1 #this index is necessary to insert every data set into a new row
        for x in data:
            if x["numero"] not in numeros:
                a="A"+str(i)
                b="B"+str(i)
                c="C"+str(i)
                d="D"+str(i)
                e="E"+str(i)
                f="F"+str(i)
                g="G"+str(i)
                h="H"+str(i)
                sheet[a]=x["numero"]
                sheet[b]=x["puntoVenta"]
                sheet[c]=x["cuitPrestador"]
                sheet[d]=x["fecha"]
                sheet[e]=x["cuitCliente"]
                sheet[f]=x["razonSocial"]
                sheet[g]=x["servicio"]
                sheet[h]=x["total"]
                i+=1
        wb.save("facturasAFIP.xlsx")
    writeExcel(data)


writeJSON(getData())
loadExcel(getData())



