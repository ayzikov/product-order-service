# base
# installed
from django.http import Http404
# local


def get_404_error(model):
    raise Http404(f"{model._meta.object_name} не найден в БД")