from django.http import HttpResponse

from capritools2.stuff import render_page


def localscan_home(request):
    return render_page(
        "capritools2/localscan.html",
        {},
        request
    )



def localscan_submit(request):
    return HttpResponse(request.POST.get("scan"))
