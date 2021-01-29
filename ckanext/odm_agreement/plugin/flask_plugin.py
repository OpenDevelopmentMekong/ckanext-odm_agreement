import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
log = logging.getLogger(__name__)


class OdmAgreementMixinPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  '''OD Mekong agreement plugin flask.'''

  plugins.implements(plugins.IBlueprint)