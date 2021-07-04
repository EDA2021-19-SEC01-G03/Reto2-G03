
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
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog():
    catalog = {'videos': None, 'category_names': None, 'categoriesIds': None}

    catalog['categoriesIds'] = mp.newMap(211, maptype='PROBING', loadfactor=0.5, comparefunction=compareMapcategories)
    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['category_names'] = lt.newList('ARRAY_LIST')

    return catalog
# Funciones para agregar informacion al catalogo


def addVideo(catalog, video):

    lt.addLast(catalog['videos'], video)


def addCategory(catalog, cat):

    c = newCategory(cat['name'], cat['id'])

    lt.addLast(catalog['category_names'], c)


def addVideoCategory(catalog, video):

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

# Funciones para creacion de datos


def newcategoryid(CatName):
    cat = {'category': "", 'videos': None}
    cat['category'] = CatName
    cat['videos'] = lt.newList('ARRAY_LIST', comparecategories)

    return cat


def newCategory(name, id):

    cat = {'name': '', 'id': ''}
    cat['name'] = name
    cat['id'] = id
    return cat
# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista


def comparecategories(cat1, cat2):
    if (cat1 == cat2):
        return 0
    elif (cat1 > cat2):
        return 1
    else:
        return 0


def compareMapcategories(id, cat):

    catentry = me.getKey(cat)
    if (id == catentry):
        return 0
    elif (id > catentry):
        return 1
    else:
        return -1

# Funciones de ordenamiento
