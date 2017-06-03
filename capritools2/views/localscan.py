from django.http import HttpResponse
from django.shortcuts import redirect

from capritools2.parsers.localscanparser import LocalScanParser
from capritools2.stuff import render_page


def localscan_home(request):
    return render_page(
        "capritools2/localscan.html",
        {},
        request
    )


def localscan_view(request, key):
    return render_page(
        "capritools2/localscan_view.html",
        {},
        request
    )



def localscan_submit(request):
    parser = LocalScanParser()
    status = parser.parse(request.POST.get("scan"))
    if status == True:
        return redirect("localscan_view", key=parser.scan.key)
