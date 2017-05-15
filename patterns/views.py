from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .processors import (
    alphabet,
    skeletonize,
    get_matches,
    mask_match,
)

# Create your views here.

def home_view(request):
    q = request.GET.get('q')
    lang = request.GET.get('lang')
    mask = request.GET.get('mask')
    maskword = request.GET.get('maskword')
    end_result = []
    context = {}
    if q and lang:
        errors = []
        if len(q) > 50:
            errors.append('50 letters max')
        if ' ' in q:
            errors.append('No spaces allowed (one-word check only)')
        if lang not in ('ru', 'en'):
            errors.append('Wrong language')
        if mask == 'on' and maskword is None:
            errors.append('You should provide a mask')
        if maskword and mask == 'on':
            if len(maskword) != len(q):
                errors.append('Word and mask should be of equal length')
        if mask == 'on' and maskword == '':
            errors.append('Please provide a mask if you checked the checkbox')
        if not errors:
            q_skeleton = skeletonize(q)
            result = get_matches(q_skeleton, lang)
            if result:
                if maskword is not None and mask == 'on':
                    if ' ' not in maskword and len(maskword) == len(q):
                        mask_result = []
                        for word in result:
                            if mask_match(maskword, word) ==  True:
                                print(word)
                                mask_result.append(word)
                        end_result = mask_result
                elif mask == None:
                    end_result = result
        # errors.append('another')
        num_on_page = 20
        paginator = Paginator(end_result, num_on_page)
        page = request.GET.get('page')
        try:
            list_words = paginator.page(page)
        except PageNotAnInteger:
            list_words = paginator.page(1)
        except EmptyPage:
            list_words = paginator.page(paginator.num_pages)

        # Determining first and last results on page
        if not list_words.has_other_pages():
            first_on_page = 1
            last_on_page = list_words.paginator.count
        elif not list_words.has_previous() and list_words.has_next():
            first_on_page = 1
            last_on_page = num_on_page
        elif list_words.has_previous():
            first_on_page = list_words.number * num_on_page - num_on_page + 1
            if list_words.has_next():
                last_on_page = list_words.number * num_on_page
            else:
                last_on_page = list_words.paginator.count
        context['first_on_page'] = first_on_page
        context['last_on_page'] = last_on_page
        print(first_on_page, last_on_page)
        full_path = request.get_full_path()
        if '&page' in full_path:
            full_path = full_path.split('&page')[0]
        context['end_result'] = end_result
        context['full_path'] = full_path
        context['result'] = list_words
        context['errors'] = errors
    return render(request, 'patterns/home_view.html', context)
