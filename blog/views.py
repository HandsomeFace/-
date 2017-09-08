# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import logging
from django.conf import settings
from models import *
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger, InvalidPage

# Create your views here.



def global_settings(request):
    # 先获取客户端提交的信息
    archive_list = Article.objects.distinct_date()
    # 得到所有分类列表
    category_list = Category.objects.all()
    return {
            'archive_list': archive_list,
            'category_list':category_list,
            'SITE_NAME': settings.SITE_NAME,
            'SITE_DESC': settings.SITE_DESC,
            }


#首页逻辑
def index(request):


    #得到所有文章列表
    article_list = Article.objects.all()
    #进行分页
    article_list = getPage(request, article_list)

    return render(request, 'index.html', locals())


#归档文章的逻辑
def archive(request):


    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
    article_list = getPage(request, article_list)

    return render(request, 'archive.html', locals())



def guide(request):
    guides = request.GET.get('category', None)
    #这是个大坑，也可以用  category__name（双下划线）查询
    article_list = Article.objects.filter(category__name__iexact=guides)
    article_list = getPage(request, article_list)
    return render(request, 'guide.html', locals())




def article(request):
    try:
        # 获取文章id
        archive_list = Article.objects.distinct_date()
        category_list = Category.objects.all()
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到相应的页面'})
    except Exception as e:
        pass
    return render(request, 'article.html', locals())


#分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 5)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, PageNotAnInteger, InvalidPage):
        article_list = paginator.page(1)
    return article_list