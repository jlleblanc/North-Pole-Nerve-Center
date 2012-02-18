from django.http import HttpResponse
from django.contrib.auth.models import User
from npnc.accounts.models import UserProfile
from twilio import twiml
from gifts.models import WishItem
import re


# XXX: this should be moved to an authentication
# provider or a utils function
def user_from_twilio_request(request):
    raw_number = request.POST.get('From')
    if not raw_number:
        return None
    match = re.match(r'\+1(\d\d\d)(\d\d\d)(\d\d\d\d)', raw_number)
    if not match:
        raise Exception("Phone number aint right")
    usnumber = "-".join(match.groups())
    try:
        return UserProfile.objects.get(phone_number=usnumber).user
    except UserProfile.DoesNotExist:
        return None


def responds_sms(view):
    def inner(request):
        response = view(request)
        twiml_response = twiml.Response()
        twiml_response.sms(response)
        return HttpResponse(str(twiml_response), content_type="text/xml")
    inner.csrf_exempt = True
    return inner


@responds_sms
def recv_sms(request):
    if request.POST:
        this_user = user_from_twilio_request(request)
        if not this_user:
            return "Sorry, but I don't think I know who you are!"
        sms_body = request.POST.get('Body', '')
        if " " in sms_body:
            action, arguments = sms_body.split(' ', 1)
        else:
            action = sms_body
            arguments = ""
        handler = sms_handles.get(action.lower(), DEFAULT_HANDLER)
        return handler(this_user, arguments)
    else:
        return HttpResponse("gotta post, man")


def handle_help(user, rest):
    return "\n".join([
        "Commands are",
        "want - list an item you want",
        "list [name] - list the items for a person",
        "buy [name] [item number] - mark an item for a person as bought",
        "who - list all of the people",
    ])


def handle_buy(user, rest):
    return "you bought %s" % rest


def handle_list(user, rest):
    searching_for = rest.strip()
    try:
        found = User.objects.get(username=searching_for)
        items = WishItem.objects.wanted_by_user(found)
        if not items:
            return "{0} hasn't wished for anything!".format(searching_for)
        return "\n".join(["{0}) {1}".format(item.id, item.item_name) for item in items])

    except User.DoesNotExist:
        return "Nobody with that name here. Run `who` to see all users"


def handle_who(user, rest):
    users = User.objects.all()
    names = [user.username for user in users]
    return "\n".join(names)


def handle_want(user, rest):
    WishItem.objects.create(item_name=rest, wisher=user)
    return "Added {0} to your list!".format(rest)



sms_handles = {
    'buy': handle_buy,
    'list': handle_list,
    'help': handle_help,
    'who': handle_who,
    'want': handle_want,
}
DEFAULT_HANDLER = handle_help

