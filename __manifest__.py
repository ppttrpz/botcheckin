# -*- coding: utf-8 -*-
###################################################################################
#    Hydra Data and Consulting Ltd.
#    Copyright (C) 2019 Hydra Data and Consulting Ltd. (<http://www.hydradataandconsulting.co.th>).
#    Author: Hydra Data and Consulting Ltd. (<http://www.hydradataandconsulting.co.th>).
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Telegram Checkin',
    'version': '99.1',
    'category': '',
    'description': """
       Telegram can help for my work
    """,
    'depends': [
        'base',
        'crm',
        'product',
        'account',
        'stock',
        'sale_management',
        'sale',
        'sale_crm',
        "base_address_city",
        "contacts",
        'mail'],
    'data': [
        'data/ir_cron_data.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'application': True,
}
