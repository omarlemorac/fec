from django.http import HttpResponse
from django.views.generic import ListView
from fec.models import l10n_ec_partner

"""from django.shortcuts import render
from fec.models import l10n_ec_partner"""


"""def showDB(request):

    table_fields = l10n_ec_partner._meta.local_fields
    field_names = [f.name for f in table_fields]
    context_dict = {'boldmessage': 'Listado de Registros en Base de datos'}

    return render(request, 'fec/index.html', context_dict)"""

class BdView(ListView):
    model = l10n_ec_partner
    template_name = 'fec/index.html'
