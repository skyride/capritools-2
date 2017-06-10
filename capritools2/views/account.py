from django.db.models import Count, Sum, Q, Case, When
from django.shortcuts import redirect, reverse

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

            'fleetscans': FleetScan.objects.filter(user=request.user).order_by('-added')
        },
        request
    )


def account_delete_dscan(request, key):
    try:
        Dscan.objects.get(key=key).delete()

        request.session['alert_type'] = "success"
        request.session['alert_message'] = "Successfully deleted Dscan %s" % key
        return redirect("%s#tab_dscans" % reverse('account_scans'))
    except Exception:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Couldn't delete Dscan %s" % key
        return redirect("%s#tab_dscans" % reverse('account_scans'))


def account_delete_localscan(request, key):
    try:
        LocalScan.objects.get(key=key).delete()

        request.session['alert_type'] = "success"
        request.session['alert_message'] = "Successfully deleted Local Scan %s" % key
        return redirect("%s#tab_localscans" % reverse('account_scans'))
    except Exception:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Couldn't delete Local Scan %s" % key
        return redirect("%s#tab_localscans" % reverse('account_scans'))


def account_delete_paste(request, key):
    try:
        Paste.objects.get(key=key).delete()

        request.session['alert_type'] = "success"
        request.session['alert_message'] = "Successfully deleted Paste %s" % key
        return redirect("%s#tab_pastes" % reverse('account_scans'))
    except Exception:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Couldn't delete Local Paste %s" % key
        return redirect("%s#tab_pastes" % reverse('account_scans'))


def account_delete_fleetscan(request, key):
    try:
        FleetScan.objects.get(key=key).delete()

        request.session['alert_type'] = "success"
        request.session['alert_message'] = "Successfully deleted Fleet Scan %s" % key
        return redirect("%s#tab_pastes" % reverse('account_scans'))
    except Exception:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Couldn't delete Local Fleet Scan %s" % key
        return redirect("%s#tab_pastes" % reverse('account_scans'))
