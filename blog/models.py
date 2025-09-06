import markdown  # 需要安装：pip install markdown
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from='name',   # 从哪个字段生成 slug
        unique=True,             # 确保 slug 是唯一的
        editable=True,           # 在后台管理中是否可编辑（可选）
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from='name',   # 从哪个字段生成 slug
        unique=True,             # 确保 slug 是唯一的
        editable=True,           # 在后台管理中是否可编辑（可选）
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )
    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from='title',   # 从哪个字段生成 slug
        unique=True,             # 确保 slug 是唯一的
        editable=True,           # 在后台管理中是否可编辑（可选）
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 这个字段用于存储你写的原始 Markdown 源码
    markdown_content = models.TextField()  # 原来是 `content = models.TextField()`
    # 修改2: 新增一个字段，用于存储由 Markdown 转换后的 HTML
    # 这个字段可以被缓存，避免每次访问都重新转换
    html_content = models.TextField(editable=False, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 在保存模型之前，自动将 Markdown 转换为 HTML
        if self.markdown_content:
            self.html_content = markdown.markdown(
                self.markdown_content,
                extensions=[
                    'extra',  # 支持表格、代码块等扩展语法
                    'codehilite',  # 代码高亮（需要安装Pygments：pip install Pygments）
                    'toc'  # 自动生成目录
                ]
            )
        # 调用父类的 save 方法将数据保存到数据库
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
