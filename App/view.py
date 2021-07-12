"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- (Requisito 1) Consultar los Top x videos por likes de un pais, de una categoria especifica")
    print("3- (Requisito 2) Consultar video con mas dias en trending para un país especifico con recepción altamente positiva")
    print("4- (Requisito 3) Consultar video con mas dias en trending para una categoría especifica con recepción sumamente positiva")
    print("5- (Requisito 4) Consultar los Top x videos con mas comentarios en un pais con un tag especifico")
    print("6- (Requisito primera entrega) Consultar los n videos con más views para el nombre de una categoría especifica")
    print("0- Salir")


def initCatalog(map, lf):
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog(map, lf)


def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    return controller.loadData(catalog)


def printCategoryList(catalog):
    """
    Imprime los nombres de las categorias cargadas
    """
    size = lt.size(catalog['category_names'])
    for i in range(1, size+1):
        element = lt.getElement(catalog['category_names'], i)
        print(element['name'])


def printPrimeraEntrega(lst):
    for video in lt.iterator(lst):
        print("trending_date: "+ str(video['trending_date'])+ ' title: '+ str(video['title']) + 
              ' channel_title: '+ str(video['channel_title'])+ ' publish_time: '+ str(video['publish_time'])
              + ' views: '+ str(video['views']) + ' likes: ' + str(video['likes'])+ ' dislikes: ' + str(video['dislikes']))


def printReq1(lst):
    for video in lt.iterator(lst):
        print("trending_date: "+ str(video['trending_date'])+ ' title: '+ str(video['title']) + 
              ' channel_title: '+ str(video['channel_title'])+ ' publish_time: '+ str(video['publish_time'])
              + ' views: '+ str(video['views']) + ' likes: ' + str(video['likes'])+ ' dislikes: ' + str(video['dislikes']))


def printReq2(video, max):
    title = "title: " + str(video['title'])
    channel_title = " channel_title: " + str(video['channel_title'])
    country = " country: " + str(video['country'])
    ratio = int(video['likes'])/int(video['dislikes'])
    ratio_likes_dislikes = " ratio_likes_dislikes: " + str(ratio)
    dias = " Días: " + str(max)
    
    print(title + channel_title + country + ratio_likes_dislikes + dias)


def printReq3(tuple): 
    video = tuple[0]
    days = tuple[1]

    ratio = 0 
    if video['dislikes'] == 0: 
        ratio = "No tiene dislikes"
    else: 
        ratio = (int(video['likes'])) / (int(video ['dislikes']))
    print("Title: " + str(video['title']) + ' channel_title: ' + str(video['channel_title']) + ' category_id: ' + str(video['category_id']) + ' ratio_likes_dislikes: ' +  str(ratio) + ' days: ' + str(days)) 

def printReq4(lst): 

    for video in lt.iterator(lst):
        print(' title: ' + str(video ['title']) + ' channel_title: ' + str(video['channel_title']) +
                ' publish_time: ' + str(video['publish_time']) + ' views: ' + str(video['views']) + 
                ' likes: ' + str(video['likes']) + ' dislikes: ' + str(video['dislikes']) + 
                'comment_count: ' + str(video['comment_count']) + 'tags: ' + str(video['tags']))


            


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:

        map = 'PROBING'
        lf = 0.8
        print("Cargando información de los archivos ....")
        catalog = initCatalog(map, lf)

        prueba = loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        printCategoryList(catalog)
        print("Tiempo [ms]: ", f"{prueba[0]:.3f}", "    ||  ", "Memoria [kB]: ", f"{prueba[1]:.3f}")       

    elif int(inputs[0]) == 2:

        number = int(input("Buscando los top: ? "))
        country = input("Buscando del Pais: ? ")
        category = input("Buscando en la categoria: ? ")
        
        Req1 = controller.getReq1(catalog, category, country, number)
        printReq1(Req1[0])
        print("\n")
        print("Tiempo [ms]: ", f"{Req1[1]:.3f}", "    ||  ", "Memoria [kB]: ", f"{Req1[2]:.3f}")
        print("\n")

    elif int(inputs[0]) == 3:

        country = input("Buscando del Pais: ? ")
        
        Req2 = controller.getReq2(catalog, country)
        printReq2(Req2[0][0], Req2[0][1])
        print("\n")
        print("Tiempo [ms]: ", f"{Req2[1]:.3f}", "    ||  ", "Memoria [kB]: ", f"{Req2[2]:.3f}")
        print("\n")

    elif int(inputs[0]) == 4:

        category = input("Buscando en la categoria: ? ")

        Req3 = controller.getReq3(catalog, category)

        printReq3(Req3[0])
        print("\n")
        print("Tiempo [ms]: ", f"{Req3[1]:.3f}", "    ||  ", "Memoria [kB]: ", f"{Req3[2]:.3f}")
        print("\n")

    elif int(inputs[0]) == 5:

        number = int(input("Buscando los top: ? "))
        country = input("Buscando del Pais: ? ")
        tag = input("Buscando el tag: ?")

        Req4 = controller.getReq4(catalog, country, tag, number)
        
        printReq4(Req4[0])
        print("\n")
        print("Tiempo [ms]: ", f"{Req4[1]:.3f}", "    ||  ", "Memoria [kB]: ", f"{Req4[2]:.3f}")
        print("\n")

    elif int(inputs[0]) == 6:
        number = int(input("Buscando los top: ? "))
        category_name = input("Buscando en la categoria: ? ")

        PrimeraEntrega = controller.getPrimeraEntrega(catalog, category_name, number)
        printPrimeraEntrega(PrimeraEntrega)

    else:
        sys.exit(0)
