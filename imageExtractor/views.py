from uuid import uuid4

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
    if ret['url'] is not None:
        ret['req_id'] = uuid4()
        req_model = Request(req_id=ret['req_id'], url=ret['url'])
        req_model.add_to_queue()
    return render(request, 'extract.html', ret)
