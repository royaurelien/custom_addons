# -*- coding: utf-8 -*-

from multiprocessing import synchronize

from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)

XML_ACTIONS = {
    'custom_addons': "custom_addons.action_view_addons",
    'git_branch': "custom_addons.action_view_branch",
    'git_repository': "custom_addons.action_view_repository",
    'git_organization': "custom_addons.action_view_organization",
}

class GitMixin(models.AbstractModel):
    _name = "git.mixin"
    _description = "Git Mixin"


    def action_open_url(self):
        self.ensure_one()
        # url = getattr(self, 'url') if hasattr(self, 'url') else None
        action = {
            "type": "ir.actions.act_url",
            "url": self.url,
            "target": "new",
        }

        return action


    def _get_xml_action(self, name):
        ref = XML_ACTIONS.get(name)
        return self.env.ref(ref).sudo().read()[0]

    def _action_view(self, name, **kwargs):
        action = self._get_xml_action(name)
        action["context"] = dict(self.env.context)

        method = getattr(self, "_action_view_{}".format(name))
        action = method(action)

        # switch to form view if only one record
        if action['domain'] and action['domain'][0][0] == 'id':
            items = action['domain'][0][2]

            if len(items) == 1:
                action['res_id'] = items[0]
                action['views'] = [(False, 'form')]

        return action

    def action_view_git_repository(self):
        return self._action_view('git_repository')

    def action_view_git_branch(self):
        return self._action_view('git_branch')

    def action_view_git_organization(self):
        return self._action_view('git_organization')

    def action_view_custom_addons(self):
        return self._action_view('custom_addons')

