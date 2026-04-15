from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Report
from .models import Post
from .forms import ReportForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Comment  

def delete_comment(request, comment_id):
    # Получаем комментарий, который нужно удалить
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Удаляем комментарий
    comment.delete()

    # Перенаправляем на страницу после удаления
    return redirect('moderation:report_list') 

# Функция для удаления поста
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()  # Удаление поста

    # Перенаправляем на страницу со списком отчетов или другую нужную страницу
    return redirect('moderation:report_list')  # 

# Блокировка пользователя (бан)
def ban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False  # Делаем пользователя неактивным (бан)
    user.save()
    
    # Перенаправляем на страницу с отчетами после бана
    return redirect('moderation:report_list')

# Восстановление пользователя (разбан)
def unban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True  # Восстанавливаем активность пользователя
    user.save()
    
    # Перенаправляем на страницу с отчетами после разбанивания
    return redirect('moderation:report_list')

@staff_member_required
def resolve_report(request, report_id):
    # Получаем отчет по ID
    report = get_object_or_404(Report, id=report_id)

    # Пример: меняем статус отчета на "resolved"
    report.status = 'resolved'
    report.save()

    # Перенаправляем на страницу со списком отчетов
    return redirect('moderation:report_list')


@staff_member_required
def report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'moderation/reports.html', {'reports': reports})

@staff_member_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'moderation/report_detail.html', {'report': report})
