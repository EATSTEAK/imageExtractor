from uuid import uuid4

from django.http import HttpResponseRedirect, Http404, FileResponse
from django.shortcuts import render

from imageExtractor.models import Request
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


def extract(request):
    ret = {
        'req_id': None,
        'url': None
    }
    if request.method == 'GET':
        logger.debug("REQUEST:" + request.GET.get('extract_url'))
        ret['url'] = request.GET.get('extract_url')
        ret['req_id'] = request.GET.get('req_id')
    if not request.GET._mutable:
        request.GET._mutable = True
    if ret['req_id'] is None and ret['url'] is not None:
        ret['req_id'] = uuid4()
        request.GET['req_id'] = ret['req_id']
        req_model = Request(req_id=ret['req_id'], url=ret['url'])
        req_model.add_to_queue()
        print(request.GET.urlencode())
        return HttpResponseRedirect('/extract?' + request.GET.urlencode())
    return render(request, 'extract.html', ret)


def download(request):
    requests = Request.objects.filter(req_id=request.GET['req_id'])
    if len(requests) != 1:
        return Http404
    request = requests[0]
    filepath = request.path
    if filepath is None:
        return Http404
    response = FileResponse(open(filepath, 'rb'))
    return response
