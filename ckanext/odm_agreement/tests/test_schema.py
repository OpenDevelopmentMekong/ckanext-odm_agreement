import pytest
from ckanext.odm_agreement.tests import helpers as test_h
import ckan.plugins.toolkit as toolkit
import ckan.tests.helpers as helpers
from ckan.tests import factories
from ckan import model


@pytest.mark.usefixtures("clean_db", "with_request_context")
class TestAgreementActions:

    def setup(self):
        self._org = factories.Organization()
        self._sysadmin = factories.Sysadmin()
        self.context = {
            "user": self._sysadmin['name'],
            "model": model,
            "session": model.Session
        }

    def test_odm_agreement_create(self):
        pkg = test_h.OdmAgreementDataset().create(
            type='agreement',
            odm_agreement_environmental_protection={
                "en": "he company has environmental management plan in different."
            },

        )
        assert "type" in pkg
        assert pkg.get('type', '') == 'agreement'
        assert "notes_translated" in pkg
        assert "odm_agreement_contracting_parties" in pkg and isinstance(pkg['odm_agreement_contracting_parties'], list)
        assert "odm_agreement_environmental_protection" in pkg and \
               pkg['odm_agreement_environmental_protection']['en'] == \
               "he company has environmental management plan in different."

    def test_agreement_update(self):
        pkg = test_h.OdmAgreementDataset().create(
            type='agreement',
            odm_agreement_environmental_protection={
                "en": "he company has environmental management plan in different."
            }
        )

        pkg_show = toolkit.get_action('package_show')(self.context, {"id": pkg['id']})

        assert pkg['id'] == pkg_show['id']
        assert pkg_show['type'] == 'agreement'

        pkg_show['odm_agreement_environmental_protection']['en'] = "test update"
        pkg_sh = toolkit.get_action('package_update')(self.context, pkg_show)

        assert "odm_agreement_environmental_protection" in pkg_sh and \
               pkg_sh['odm_agreement_environmental_protection']['en'] == \
               "test update"

    def test_agreement_delete(self):
        pkg = test_h.OdmAgreementDataset().create(
            type='agreement',
            odm_agreement_environmental_protection={
                "en": "he company has environmental management plan in different."
            }
        )
        toolkit.get_action('package_delete')(self.context, {"id": pkg['id']})
        pkg_show = toolkit.get_action('package_show')(self.context, {"id": pkg['id']})
        assert pkg_show['state'] == 'deleted'
