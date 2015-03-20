from django.views.generic import ListView
from .models import l10n_ec_partner


class BdView(ListView):
    model = l10n_ec_partner
    template_name = 'fec/showdata.html'
