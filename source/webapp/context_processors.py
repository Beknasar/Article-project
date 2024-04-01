# Поисковая форма перемещена в контекстный процессор и выводится в базовом шаблоне.
from webapp.forms import SimpleSearchForm


def search_form(request):
    form = SimpleSearchForm(request.GET)
    return {'search_form': form}
