from django.http import HttpResponse

from capritools2.stuff import render_page


def home(request):
    return render_page(
        "capritools2/home.html",
        {},
        request
    )
