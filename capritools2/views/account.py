from django.db.models import Count, Sum, Q, Case, When

from capritools2.stuff import render_page
from capritools2.models import *


def account_scans(request):
    return render_page(
        "capritools2/account_scans.html",
        {
            'dscans': Dscan.objects.filter(user=request.user).order_by('-added').all(),

            'localscans': LocalScan.objects.filter(user=request.user).order_by('-added').annotate(
                chars=Count('characters')
            ).all(),

            'pastes': Paste.objects.filter(user=request.user).order_by('-added'),
        },
        request
    )
