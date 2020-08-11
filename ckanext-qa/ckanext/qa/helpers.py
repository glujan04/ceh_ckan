# coding: utf8
import copy
from ckan.plugins import toolkit as tk
import lib
import os
from ckan import model
import plugin as QAPlugin


def qa_openness_stars_resource_html(resource):
    qa = resource.get('qa')
    qa = {'openness_score': 3, 'openness_score_reason': 'Content of file appeared to be format \"CSV\" which receives openness score: 3.',
               'updated': '2015-11-19T16:54:49.480393'}
    if not qa:
        return tk.literal('<!-- No qa info for this resource -->')
    if not isinstance(qa, dict):
        return tk.literal('<!-- QA info was of the wrong type -->')

    # Take a copy of the qa dict, because weirdly the renderer appears to add
    # keys to it like _ and app_globals. This is bad because when it comes to
    # render the debug in the footer those extra keys take about 30s to render,
    # for some reason.
    extra_vars = copy.deepcopy(qa)
    return tk.literal(
        tk.render('qa/openness_stars.html',
                  extra_vars=extra_vars))


def qa_openness_stars_dataset_html(dataset):
    qa = dataset.get('qa')
    qa = {'openness_score': 3, 'openness_score_reason': 'Content of file appeared to be format \"CSV\" which receives openness score: 3.',
               'updated': '2015-11-19T16:54:49.480393'}
    print(dataset)
    print(qa)
    if not qa:
        return tk.literal('<!-- No qa info for this dataset -->')
    if not isinstance(qa, dict):
        return tk.literal('<!-- QA info was of the wrong type -->')
    extra_vars = copy.deepcopy(qa)
    return tk.literal(
        tk.render('qa/openness_stars_brief.html',
                  extra_vars=extra_vars))

class dicRes(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 

def qa_openness_stars_dataset2_html(dataset):
    qa = dataset.get('qa')
    #Pregunta si es de tipo dataset
    field_name = getattr(dataset, 'type')
    #valida que el dataset no sea de tipo harvest
    if field_name != 'dataset':
        return tk.literal('<!-- No qa info for this dataset -->')
    #se obtienen los formatos disponibles
    jsonFormats = lib.resource_format_scores()
    #for item in jsonFormats:
    #   print jsonFormats[item]
    id_ = getattr(dataset, 'id')
    pkg = model.Package.get(id_)
    #print 'Package %s %s' % (pkg.name, pkg.id)
    _RESOURCES = dicRes()
    def_score = 1
    #print pkg.resources
    for res in pkg.resources:
        #print res
        #obtiene el formato  p.j. JPEG
        name = getattr(res, 'name').upper() if getattr(res, 'format') is None else getattr(res, 'format').upper()
        #obtiene el indice de la extension del archivo
        _index = name.rfind('.') 
        if _index != -1:
            formato = name[_index+1:]
        else:
            formato = name
        #obtiene el valor de la extension del config. None si no existe
        x = jsonFormats.get(formato)
        #print _RESOURCES
        if not formato in _RESOURCES:
            if x is not None:
                _RESOURCES.add(formato, x)
            else:
                _RESOURCES.add(formato, def_score)
        #    raise ValueError('Formato duplicado %s' % formato)
    #print _RESOURCES
    maximum = max(_RESOURCES, key=_RESOURCES.get)  # Just use 'min' instead of 'max' for minimum.
    #print maximum.encode('utf-8')
    lb_star = 'estrellas'
    if _RESOURCES[maximum] == 1:
        lb_star = 'estrella'
    qa = {'openness_score': _RESOURCES[maximum], 'openness_score_reason': 'El conjunto de datos recibe una puntuación de {0} {1} al disponer de un recurso en formato \"{2}\".'.format(_RESOURCES[maximum], lb_star, maximum.encode('utf-8')),
               'updated': None}
    if not qa:
        return tk.literal('<!-- No qa info for this dataset -->')
    if not isinstance(qa, dict):
        return tk.literal('<!-- QA info was of the wrong type -->')

    schema = dataset
    #schema.update({
    #            'openness': [tk.get_validator('ignore_missing'),
    #                            tk.get_converter('convert_to_extras')(55)]
    #        })
    print schema
    #schema = self._modify_package_schema(schema)
    # Take a copy of the qa dict, because weirdly the renderer appears to add
    # keys to it like _ and app_globals. This is bad because when it comes to
    # render the debug in the footer those extra keys take about 30s to render,
    # for some reason.
    extra_vars = copy.deepcopy(qa)
    return tk.literal(
        tk.render('qa/openness_stars.html',
                  extra_vars=extra_vars))
