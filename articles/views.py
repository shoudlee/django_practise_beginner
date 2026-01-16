from .models import Article
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    DetailView,
    CreateView,
    View,
    FormView,
)
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy, reverse
from django.template.loader import select_template
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm


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


class CommentGet(DetailView):
    model = Article
    template_name = "articles/article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(FormView, SingleObjectMixin):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object1 = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object1
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.object1
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


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
