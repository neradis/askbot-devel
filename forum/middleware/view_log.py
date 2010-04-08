import logging
from django.conf import settings
from forum.views.readers import questions as questions_view
from forum.views.commands import vote as vote_view
from django.views.static import serve as django_serve_view

class ViewLog(object):
    """must be modified only in this middlware
    however, can be read anywhere else
    """
    def __init__(self):
        self.views = []
        self.depth = 3 #todo maybe move this to const.py
    def set_current(self, view_name):
        thi

    def get_previous(self, num):
        if num > self.depth - 1:
            raise Exception("view log depth exceeded")
        elif num < 0:
            raise Exception("num must be positive");
        elif num <= len(self.views) - 1:
            return self.views[num]
        else:
            return None

    def set_current(self, view_name):
        self.views.insert(0, view_name)
        if len(self.views) > self.depth:
            self.views.pop()

    def __str__(self):
        return str(self.views) + ' depth=%d' % self.depth

class ViewLogMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func == questions_view:
            view_str = 'questions'
        elif view_func in (django_serve_view, vote_view):
            return
        elif settings.DEBUG == True:
            #todo: dependency!
            from debug_toolbar.views import debug_media_view
            if view_func == debug_media_view:
                return
            else:
                view_str = view_func.__name__
        else:
            view_str = view_func.__name__

        if request.user.is_authenticated():
            user_name = request.user.username
        else:
            user_name = request.META['REMOTE_ADDR']
        logging.debug('user %s, view %s' % (request.user.username, view_str))

        if 'view_log' in request.session:
            view_log = request.session['view_log']
        else:
            view_log = ViewLog()

        view_log.set_current(view_str)
        request.session['view_log'] = view_log
