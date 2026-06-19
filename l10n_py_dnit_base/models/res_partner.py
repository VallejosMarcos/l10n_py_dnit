from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from . import ruc


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_py_ruc_dv = fields.Char(
        string="Dígito verificador",
        compute="_compute_l10n_py_ruc_dv",
        help="Dígito verificador calculado para el número de RUC.",
    )

    def _is_py_ruc(self):
        """True si el contribuyente está identificado con RUC paraguayo."""
        self.ensure_one()
        ruc_type = self.env.ref("l10n_py_dnit_base.it_ruc", raise_if_not_found=False)
        return ruc_type and self.l10n_latam_identification_type_id == ruc_type

    @api.depends("vat", "l10n_latam_identification_type_id")
    def _compute_l10n_py_ruc_dv(self):
        for partner in self:
            if partner.vat and partner._is_py_ruc():
                number, _dv = ruc.split(partner.vat)
                partner.l10n_py_ruc_dv = str(ruc.check_digit(number)) if number else False
            else:
                partner.l10n_py_ruc_dv = False

    @api.constrains("vat", "l10n_latam_identification_type_id")
    def _check_l10n_py_ruc(self):
        for partner in self:
            if partner.vat and partner._is_py_ruc() and not ruc.is_valid(partner.vat):
                number, _dv = ruc.split(partner.vat)
                raise ValidationError(_(
                    "El RUC «%(ruc)s» no es válido. El dígito verificador "
                    "debería ser %(dv)s.",
                    ruc=partner.vat,
                    dv=ruc.check_digit(number) if number else "?",
                ))
