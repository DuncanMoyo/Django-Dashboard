from django.shortcuts import render


def company_article_list(request):
    return render(request, 'plotly.html', {})
