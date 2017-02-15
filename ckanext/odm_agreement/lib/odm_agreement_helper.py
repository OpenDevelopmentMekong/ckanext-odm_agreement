#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylons
import logging
import json
import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from genshi.template.text import NewTextTemplate
from ckan.lib.base import render

log = logging.getLogger(__name__)

def get_dataset_type():
  '''Return the dataset type'''

  log.debug('get_dataset_type')

  return 'agreement'

def create_default_issue_agreement(pkg_info):
  ''' Uses CKAN API to add a default Issue as part of the vetting workflow for agreement records'''
  try:

    extra_vars = {
      't0': toolkit._("Thank you for uploading this item. Instructions about vetting system available on https://wiki.opendevelopmentmekong.net/partners:content_review#instructions_for_default_issue_on_agreements")
    }

    issue_message = render('messages/default_issue_agreement.txt',extra_vars=extra_vars,loader_class=NewTextTemplate)

    params = {'title':'User agreement record Upload Checklist','description':issue_message,'dataset_id':pkg_info['id']}
    toolkit.get_action('issue_create')(data_dict=params)

  except KeyError:

    log.error("Action 'issue_create' not found. Please make sure that ckanext-issues plugin is installed.")

session = {}
