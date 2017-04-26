import ckan
import pylons
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from beaker.middleware import SessionMiddleware
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import odm_agreement_helper
from urlparse import urlparse
from pylons import config
import json
import collections
from routes.mapper import SubMapper
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

class OdmAgreementPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  '''OD Mekong agreement plugin.'''

  plugins.implements(plugins.IValidators, inherit=True)
  plugins.implements(plugins.IConfigurer)
  plugins.implements(plugins.ITemplateHelpers)
  plugins.implements(plugins.IRoutes, inherit=True)
  plugins.implements(plugins.IPackageController, inherit=True)

  def __init__(self, *args, **kwargs):

    log.debug('OdmAgreementPlugin init')
    wsgi_app = SessionMiddleware(None, None)
    odm_agreement_helper.session = wsgi_app.session

  def before_map(self, m):

    m.connect('odm_agreement_index','/agreement',controller='package',type='agreement',action='search')

    m.connect('odm_agreement_new','/agreement/new',controller='package',type='agreement',action='new')

    m.connect('odm_agreement_new_resource','/agreement/new_resource/{id}',controller='package',type='agreement',action='new_resource')

    m.connect('odm_agreement_read', '/agreement/{id}',controller='package',type='agreement', action='read', ckan_icon='book')

    m.connect('odm_agreement_edit', '/agreement/edit/{id}',controller='package',type='agreement', action='edit')

    m.connect('odm_agreement_delete', '/agreement/delete/{id}',controller='package',type='agreement', action='delete')

    return m

  def update_config(self, config):
    '''Update plugin config'''

    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('fanstatic', 'odm_agreement')
    toolkit.add_public_directory(config, 'public')

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

      # Create default Issue
      review_system = h.asbool(config.get("ckanext.issues.review_system", False))
      if review_system:
        if pkg_dict['type'] == 'agreement':
          odm_agreement_helper.create_default_issue_agreement(pkg_dict)

  def after_update(self, context, pkg_dict):

    dataset_type = context['package'].type if 'package' in context else pkg_dict['type']
    if dataset_type == 'agreement':
      log.info('after_update: %s', pkg_dict['name'])

      pkg_dict['open_contracting_id'] = "ocds-miumsd-" + pkg_dict["id"]
