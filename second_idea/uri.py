from urlparse import urlsplit, urlunsplit

class UriDispatch(object):
    def __init__(self,root,scheme):
        self.root = root
        self.scheme = scheme

    def receive_request(self,uri,method):
        import api
        scheme = getattr(api,self.scheme.lower())

        try:
            method = getattr(scheme,method.lower())
        except AttributeError, e:
            return "Method Not Allowed 405"
        return method(uri)
