# Copyright 2020-22 Sodexis
# License OEEL-1 (See LICENSE file for full copyright and licensing details).

from odoo.addons.web.controllers.main import Home
from odoo.http import request
from odoo.tools import config, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import fields

class HomeExtended(Home):

    def _login_redirect(self, uid, redirect=None):
        res = super()._login_redirect(uid=uid, redirect=redirect)
        get_param = request.env['ir.config_parameter'].sudo().get_param
        set_param = request.env['ir.config_parameter'].sudo().set_param
        expiry_date = fields.Datetime.to_datetime(get_param('database.expiration_date'))
        today = fields.Datetime.now()
        partner_code = config.get('partner_code', False)
        if partner_code and (expiry_date < today):
            set_param('database.enterprise_code', partner_code)
            request.env['publisher_warranty.contract'].update_notification()
        return res
