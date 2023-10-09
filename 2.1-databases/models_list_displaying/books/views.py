from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()

    context = {
        'books': books
    }
    return render(request, template, context)


def books_date(request, pub_date):
    template = 'books/books_date.html'
    books_date_list = Book.objects.filter(pub_date=pub_date)

    # data_list = [f'{d.pub_date}' for d in books_date_list]
    # data_list.sort()
    # data_map = {}
    # flag = 0
    # for data in data_list:
    #     if data not in data_map:
    #         flag += 1
    #         data_map[data] = flag
    # datas = list(data_map.keys())
    # print(datas)
    # paginator = Paginator(books_date_list, 1)
    # page = paginator.get_page(data_map[pub_date])
    
    context= {
        # 'page': page,
        'books': books_date_list
    }
    return render(request, template, context)

