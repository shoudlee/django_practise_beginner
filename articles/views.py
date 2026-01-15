from .models import Article
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    DetailView,
    CreateView,
)
from django.urls import reverse_lazy
from django.template.loader import select_template
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "articles/article_list.html"

    # CBV中寻找模板的convention包含一个 DIR/APPNAME/MODELNAME_xxx.html
    # def render_to_response(self, context, **response_kwargs):
    #     names = self.get_template_names()  # CBV 真正使用的候选列表
    #     t = select_template(names)  # 按同样规则选中最终模板
    #     print("TEMPLATE CANDIDATES =", names)
    #     print("TEMPLATE ORIGIN =", t.origin.name)  # 最终命中的绝对路径
    #     return super().render_to_response(context, **response_kwargs)


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "articles/article_delete.html"
    # 如果view中没有success_url, model中没有get_absolute_url会报错
    success_url = reverse_lazy("article_list")

    def test_func(self):
        return self.get_object().author == self.request.user


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = "articles/article_update.html"
    fields = ["title", "body"]

    def test_func(self):
        return self.get_object().author == self.request.user


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "articles/article_detail.html"


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "articles/article_new.html"
    fields = (
        "title",
        "body",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
