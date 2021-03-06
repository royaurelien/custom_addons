# -*- coding: utf-8 -*-

from multiprocessing import synchronize
from odoo import models, fields, api

import logging
from random import randint

_logger = logging.getLogger(__name__)


class CustomAddonVersion(models.Model):
    _name = "custom.addon.version"
    _description = "Custom Addon Version"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Name', required=True)
    color = fields.Integer(string='Color', default=_get_default_color)
    custom_addon_count = fields.Integer(compute='_compute_addons', string="# Addons")
    # custom_addon_ids = fields.One2many(comodel_name='custom.addon', inverse_name='version_id')
    # custom_addon_ids = fields.Many2many('custom.addon', string='Custom addons')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Version already exists!"),
    ]


    def _compute_addons(self):
        for record in self:
            branches = self.env['git.branch'].search([('name','=',record.name)])
            record.custom_addon_count = sum(branches.mapped('custom_addon_count'))

    @api.model
    def search_or_create(self, names):
        names = set(names)
        records = self.search([('name', 'in', list(names))])
        to_create = names - set(records.mapped('name'))
        _logger.warning(to_create)
        new_records = self.create([{'name':name} for name in to_create])
        _logger.warning(new_records)

        return records + new_records