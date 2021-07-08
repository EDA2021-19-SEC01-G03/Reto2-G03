
"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog(map, lf):
    catalog = {'videos': None, 'category_names': None, 'categoriesIds': None, 'countryMap': None }

    catalog['categoriesIds'] = mp.newMap(211, maptype=map, loadfactor=lf, comparefunction=compareMapcategories)
    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['category_names'] = lt.newList('ARRAY_LIST')

    catalog['countryMap'] = mp.newMap(211, maptype=map, loadfactor=lf, comparefunction=compareMapcountry)

    return catalog
# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):

    lt.addLast(catalog['videos'], video)


def addCategory(catalog, cat):

    c = newCategory(cat['name'], cat['id'])

    lt.addLast(catalog['category_names'], c)


def addVideoCategory(catalog, video):
    """
    Añade un video al indice de categorias.
    La llave de cada pareja es el id de la categoria que esta guardada como un int
    El valor es una lista con los videos de la categoria de la llave
    """

    try:
        categoryMap = catalog['categoriesIds']

        categoryidKey = video['category_id']
        categoryidKey = int(categoryidKey)

        categoryExist = mp.contains(categoryMap, categoryidKey)

        if categoryExist:
            entry_videos = mp.get(categoryMap, categoryidKey)
            category_videos = me.getValue(entry_videos)
        else:
            category_videos = newcategoryid(categoryidKey)
            mp.put(categoryMap, categoryidKey, category_videos)

        lt.addLast(category_videos['videos'], video)
    except Exception:
        return None


def addVideoCountry(catalog, video):
    
    try:
        countryMap = catalog['countryMap']

        countryKey = video['country']
        
        countryExist = mp.contains(countryMap, countryKey)

        if countryExist:
            entry_videos = mp.get(countryMap, countryKey)
            country_videos = me.getValue(entry_videos)
        else:
            country_videos = newCountry(countryKey)
            mp.put(countryMap, countryKey, country_videos)

        lt.addLast(country_videos['videos'], video)
    except Exception:
        return None


# Funciones para creacion de datos


def newcategoryid(CatName):
    cat = {'category': "", 'videos': None}
    cat['category'] = CatName
    cat['videos'] = lt.newList('ARRAY_LIST', comparecategories)

    return cat


def newCountry(country):

    cou = {'country': "", 'videos': None}
    cou['country'] = country
    cou['videos'] = lt.newList('ARRAY_LIST', compareCountry)
    return cou


def newCategory(name, id):

    cat = {'name': '', 'id': ''}
    cat['name'] = name
    cat['id'] = id
    return cat

# Funciones de consulta


def getCategoryid(catalog, category_name):
    """
    Devuelve el id de una categoria del catalogo.
    Args:
        catalog: catalogo con la lista de videos y la lista de categorias
        category_name: nombre de la categoria que se consulta
    """
    for cat in lt.iterator(catalog['category_names']):
        if category_name in cat['name']:
            return cat['id']
    return "error"


def like_ratioCond(video, number):
    """
    Devuelve verdadero (True) si la taza de likes a dislikes es mayor a la condición representada por el
    numero number
    Args:
        video: el video sobre el cual se esta evaluando la condición
        number: un numero float que representa el numero que debe superar la tasa para que devuelva
        verdadero
    """
    if int(video['dislikes']) != 0:
        cond = int(video['likes'])/int(video['dislikes'])
        if cond > number:
            return True
        else:
            return False
    else:
        return True


def getPrimeraEntrega(catalog, category_name, number):
    """
    Retornar la lista de los top n videos con mas comentarios para un nombre de categoria
    """
    category_id = int(getCategoryid(catalog, category_name))
    cat = mp.get(catalog['categoriesIds'],category_id)
    if cat:
        sub_list = me.getValue(cat)['videos']
        sorted_list = sortbyViews(sub_list)
        top_n = lt.subList(sorted_list, 1, number)
        return top_n
    else:
        return None


def getReq3(catalog, category_name):

    category_id = int(getCategoryid(catalog, category_name))

    cat = mp.get(catalog['categoriesIds'], category_id)

    if cat: 
        videos = me.getValue(cat)['videos']

        list_ratio = lt.newList("ARRAY_LIST")

        for elem in lt.iterator(videos):#N

            if like_ratioCond(elem, 20) == True: 
                lt.addLast(list_ratio, elem)

        sort_list_name = sortbyName(list_ratio)

        # N log N
        
        compare = lt.firstElement(sort_list_name)['title']
        name_max = lt.firstElement(sort_list_name)['title']

        days = 0
        max = 0
        pos = 1
        
        for video in lt.iterator(sort_list_name):  #N

            if (video['title'] == compare):
                days += 1

            else:

                if days > max:
                    max = days
                    name_max = lt.getElement(sort_list_name, (pos-1))

                compare = video['title']
                days = 1

            pos += 1
            ######
        return name_max, max  
    else:
        return None


def getReq4(catalog, country, tag, number):

    country_pair = mp.get(catalog['countryMap'], country)

    if country_pair:
        videos = me.getValue(country_pair)['videos']

        sort_videos = sortbyComm(videos)

        sublist = lt.newList("ARRAY_LIST")
        names = []
        
        for elem in lt.iterator(sort_videos):

            if (tag.lower() in str(elem['tags'].lower()) and (elem['title'] not in names)):

                lt.addLast(sublist, elem)
                names.append(elem['title'])

        top_n = lt.subList(sublist, 1, number)
        return top_n
    else: 
        return None


# Funciones utilizadas para comparar elementos dentro de una lista


def comparecategories(cat1, cat2):
    if (cat1 == cat2):
        return 0
    elif (cat1 > cat2):
        return 1
    else:
        return 0


def compareCountry(nam1, nam2): 
    if (nam1 == nam2):
        return 0
    elif (nam1 > nam2):
        return 1
    else:
        return 0


def compareMapcategories(id, cat):

    catentry = me.getKey(cat)
    if (int(id) == int(catentry)):
        return 0
    elif (int(id) > int(catentry)):
        return 1
    else:
        return -1


def compareMapcountry(name, country):

    counentry = me.getKey(country)
    if (name == counentry):
        return 0
    elif (name > counentry):
        return 1
    else:
        return -1


def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los likes de video1 son menores que los del video2
    Args:
        video1: informacion del primer video que incluye su valor 'likes'
        video2: informacion del segundo video que incluye su valor 'likes'
    """
    return (int(video1['views']) > int(video2['views']))


def cmpVideosByComm(video1, video2):

    return (int(video1['comment_count']) > int(video2['comment_count']))


def cmpVideosbyName(video1, video2):
    return (video1['title'] > video2['title'])


# Funciones de ordenamiento


def sortbyViews(lst):
    sub_list = lst.copy()
    sorted = ms.sort(sub_list, cmpVideosByViews)

    return sorted


def sortbyComm(lst):

    sub_list = lst.copy()
    sorted = ms.sort(sub_list, cmpVideosByComm)
    return sorted


def sortbyName(lst):

    sub_list = lst.copy()
    sorted = ms.sort(sub_list, cmpVideosbyName)

    return sorted
