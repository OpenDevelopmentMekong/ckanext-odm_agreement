import ckan
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from beaker.middleware import SessionMiddleware
import sys
import os
from ckanext.odm_agreement.lib import odm_agreement_helper
from urlparse import urlparse
from ckan.common import config
import json
import collections
from routes.mapper import SubMapper
import ckan.lib.helpers as h

log = logging.getLogger(__name__)


if toolkit.check_ckan_version(min_version='2.9.0'):
    from ckanext.odm_agreement.plugin.flask_plugin import OdmAgreementMixinPlugin
else:
    from ckanext.odm_agreement.plugin.pylons_plugin import OdmAgreementMixinPlugin


class OdmAgreementPlugin(OdmAgreementMixinPlugin):
    '''OD Mekong agreement plugin.'''

    plugins.implements(plugins.IValidators, inherit=True)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    def __init__(self, *args, **kwargs):

        log.debug('OdmAgreementPlugin init')
        wsgi_app = SessionMiddleware(None, None)
        odm_agreement_helper.session = wsgi_app.session

    def get_helpers(self):
        '''Register the plugin's functions above as a template helper function.'''

        return {
          'odm_agreement_get_dataset_type': odm_agreement_helper.get_dataset_type,
          'odm_agreement_validate_fields' : odm_agreement_helper.validate_fields
        }

    def get_validators(self):
        '''Register the plugin's functions above as validators.'''

        log.debug("get_validators")

        return {
          'odm_agreement_generate_ocds_id': odm_agreement_helper.generate_ocds_id
        }

    def after_create(self, context, pkg_dict):
        dataset_type = context['package'].type if 'package' in context else pkg_dict['type']

        if dataset_type == 'agreement':
            log.debug('after_create: %s', pkg_dict['name'])

            review_system = toolkit.asbool(config.get("ckanext.issues.review_system", False))
            if review_system:
                if pkg_dict['type'] == 'agreement':
                    odm_agreement_helper.create_default_issue_agreement(pkg_dict)

