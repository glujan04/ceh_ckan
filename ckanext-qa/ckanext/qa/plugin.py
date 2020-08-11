import logging

import ckan.model as model
import ckan.plugins as p

from ckanext.archiver.interfaces import IPipe
from logic import action, auth
from model import QA, aggregate_qa_for_a_dataset
import helpers
import lib
#from ckanext.report.interfaces import IReport


log = logging.getLogger(__name__)


class QAPlugin(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):
    #p.implements(p.IFacets)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    #p.implements(IPipe, inherit=True)
    #p.implements(IReport)
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IDatasetForm)
    p.implements(p.IPackageController, inherit=True)


    # IDatasetForm

    def show_package_schema(self):
        schema = super(QAPlugin, self).show_package_schema()
        print 'aqui esquema'
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        schema.update({
            'openness': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')(55)]
        })
        return schema


    # IPackageController

    #def before_search(self, search_params):
    #    print search_params
    #    return search_params

    #def after_search(self, search_results, search_params):
    #    print search_results
    #    print search_params
    #    return search_results

    def before_view(self, pkg_dict):
        schema = super(QAPlugin, self).show_package_schema()
        #schema.update({
        #    'openness2': [p.toolkit.get_validator('ignore_missing'),
        #                    p.toolkit.get_converter('convert_to_extras')]
        #})
        print 'pkg_ddddddd'
        print schema
        return pkg_dict

    #def update_facet_titles(self, facet_titles):
    #    print facet_titles
    #    return facet_titles


    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        #facets_dict['openness'] = p.toolkit._('Openness')

        # Return the updated facet dict.
        print facets_dict
        return facets_dict

    # IConfigurer

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')

    # IRoutes

    def before_map(self, map):
        # Link checker - deprecated
        res = 'ckanext.qa.controllers:LinkCheckerController'
        map.connect('qa_resource_checklink', '/qa/link_checker',
                    conditions=dict(method=['GET']),
                    controller=res,
                    action='check_link')
        return map

    # IPipe

    def receive_data(self, operation, queue, **params):
        '''Receive notification from ckan-archiver that a dataset has been
        archived.'''
        if not operation == 'package-archived':
            return
        dataset_id = params['package_id']

        dataset = model.Package.get(dataset_id)
        assert dataset

        lib.create_qa_update_package_task(dataset, queue=queue)

    # IReport

    def register_reports(self):
        """Register details of an extension's reports"""
        from ckanext.qa import reports
        return [reports.openness_report_info]

    # IActions

    def get_actions(self):
        return {
            'qa_resource_show': action.qa_resource_show,
            'qa_package_openness_show': action.qa_package_openness_show,
            }

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            'qa_resource_show': auth.qa_resource_show,
            'qa_package_openness_show': auth.qa_package_openness_show,
            }

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'qa_openness_stars_resource_html':
            helpers.qa_openness_stars_resource_html,
            'qa_openness_stars_dataset_html':
            helpers.qa_openness_stars_dataset_html,
            'qa_openness_stars_dataset2_html':
            helpers.qa_openness_stars_dataset2_html,
            }

    # IPackageController

    def after_show(self, context, pkg_dict):
        # Insert the qa info into the package_dict so that it is
        # available on the API.
        # When you edit the dataset, these values will not show in the form,
        # it they will be saved in the resources (not the dataset). I can't see
        # and easy way to stop this, but I think it is harmless. It will get
        # overwritten here when output again.
        qa_objs = QA.get_for_package(pkg_dict['id'])
        if not qa_objs:
            return
        # dataset
        dataset_qa = aggregate_qa_for_a_dataset(qa_objs)
        pkg_dict['qa'] = dataset_qa
        # resources
        qa_by_res_id = dict((a.resource_id, a) for a in qa_objs)
        for res in pkg_dict['resources']:
            qa = qa_by_res_id.get(res['id'])
            if qa:
                qa_dict = qa.as_dict()
                del qa_dict['id']
                del qa_dict['package_id']
                del qa_dict['resource_id']
                res['qa'] = qa_dict
