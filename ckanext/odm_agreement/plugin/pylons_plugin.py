import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
log = logging.getLogger(__name__)


class OdmAgreementMixinPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  '''OD Mekong agreement plugin.'''
  plugins.implements(plugins.IRoutes, inherit=True)

  def before_map(self, m):

    m.connect('odm_agreement_index','/agreement',controller='package',type='agreement',action='search')

    m.connect('odm_agreement_new','/agreement/new',controller='package',type='agreement',action='new')

    m.connect('odm_agreement_new_resource','/agreement/new_resource/{id}',controller='package',type='agreement',action='new_resource')

    m.connect('odm_agreement_read', '/agreement/{id}',controller='package',type='agreement', action='read', ckan_icon='book')

    m.connect('odm_agreement_edit', '/agreement/edit/{id}',controller='package',type='agreement', action='edit')

    m.connect('odm_agreement_delete', '/agreement/delete/{id}',controller='package',type='agreement', action='delete')

    return m

