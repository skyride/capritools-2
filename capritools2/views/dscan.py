from django.http import HttpResponse

from capritools2.stuff import render_page
from capritools2.parsers.dscanparser import DscanParser


def dscan_home(request):
    return render_page(
        "capritools2/dscan.html",
        {},
        request
    )


def dscan_submit(request):
    parser = DscanParser()
    parser.parse(request.POST.get("dscan"))

    return HttpResponse(parser.scan.system)
