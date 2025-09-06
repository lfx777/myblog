from django.shortcuts import render


# 暂时注释掉，等博客应用完善后再引入
# from blog.models import Post

def index(request):
    """主页视图"""
    # 等博客模型完成后，可以取消注释以下代码来显示最新文章
    # recent_posts = Post.objects.filter(status='published')[:5]

    context = {
        # 'recent_posts': recent_posts,
    }
    return render(request, 'core/index.html', context)