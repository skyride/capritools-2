from datetime import datetime, timedelta
from hashlib import sha256

from django.shortcuts import redirect
from django.db.models import Q

from capritools2.stuff import render_page, random_key
from capritools2.models import Paste


def paste_home(request):
    return render_page(
        "capritools2/paste.html",
        {},
        request
    )


def paste_view(request, key):
    #try:
        paste = Paste.objects.get(
            Q(expires__isnull=True) | Q(expires__gt=datetime.now()),
            key=key
        )

        if paste.password != None:
            # Check session for a verification
            if "paste_" + key not in request.session:
                try:
                    password = sha256(paste.salt + request.POST.get("password")).hexdigest()
                    if password == paste.password:
                        request.session['paste_'+key] = True
                    else:
                        request.session['alert_type'] = "danger"
                        request.session['alert_message'] = "Incorrect Password."

                        return render_page(
                            "capritools2/paste_password.html",
                            {},
                            request
                        )
                except Exception:
                    return render_page(
                        "capritools2/paste_password.html",
                        {},
                        request
                    )

        return render_page(
            "capritools2/paste_view.html",
            {
                'paste': paste
            },
            request
        )
    #except Exception:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "The paste you were looking for does not exist."
        return redirect("paste")


def paste_submit(request):
    try:
        paste = Paste(
            key=random_key(7),
            text = request.POST.get("paste")
        )

        expiry = int(request.POST.get("expiry"))
        if expiry > 0:
            paste.expires = datetime.now() + timedelta(seconds=expiry)

        password = request.POST.get("password")
        if len(password) > 0:
            paste.salt = random_key(32)
            paste.password = sha256(paste.salt + password).hexdigest()

            # Add it to their session so they aren't immedately prompted for it
            request.session['paste_'+paste.key] = True

        paste.save()
        return redirect("paste_view", key=paste.key)

    except Exception:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Could not save the paste."
        return redirect("paste")
