from django.utils.cache import add_never_cache_headers


class PrintGet(object):
    def process_request(self, request):
        request.GET = request.GET.copy()
        if 'style' in request.GET.keys():
            request.style = request.GET['style']
            request.GET.pop('style')
        elif not len(request.GET.keys()):
            request.printlink = request.path_info + '?style=print'
        else:
            request.printlink = '%s?%s&style=print' % (
                request.path_info, request.GET.urlencode())


class DisableClientSideCachingMiddleware(object):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
