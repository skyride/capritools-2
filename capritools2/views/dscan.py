from capritools2.stuff import render_page


def dscan_home(request):
    return render_page(
        "capritools2/dscan.html",
        {},
        request
    )


def dscan_submit(request):
    return render_page(
        "capritools2/dscan.html",
        {},
        request
    )
