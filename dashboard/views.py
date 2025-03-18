# dashboard/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from django.db.models.functions import ExtractMonth, ExtractWeek, ExtractYear
from datetime import datetime, timedelta

from workouts.models import Workout, WorkoutCategory
from users.models import UserBodyRecord


@login_required
def dashboard(request):
    """用户仪表盘首页"""
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    
    # 自定义JSON编码器处理日期和timedelta
    class CustomJSONEncoder(DjangoJSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.date):
                return obj.strftime('%Y-%m-%d')
            elif isinstance(obj, timedelta):
                total_seconds = obj.total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                return f"{hours}:{minutes:02d}"
            return super().default(obj)
    
    user = request.user
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # 最近的健身记录
    recent_workouts = Workout.objects.filter(user=user).order_by('-date', '-start_time')[:5]
    
    # 本周健身统计
    week_workouts = Workout.objects.filter(user=user, date__gte=week_ago)
    week_workout_count = week_workouts.count()
    week_total_duration = sum((w.duration for w in week_workouts if w.duration), timedelta())
    week_calories = week_workouts.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    
    # 健身类别统计
    category_stats = Workout.objects.filter(user=user).values('category__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # 月度健身频率
    monthly_stats = Workout.objects.filter(user=user, date__gte=today.replace(month=1, day=1)).annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # 体重变化数据
    weight_records = UserBodyRecord.objects.filter(user=user).order_by('date')
    weight_data = [[record.date.strftime('%Y-%m-%d'), record.weight] for record in weight_records]
    
    # 添加调试信息
    print(f"Weight data count: {len(weight_data)}")
    print(f"Category stats count: {len(category_stats)}")
    
    # 使用JSON序列化数据
    context = {
        'recent_workouts': recent_workouts,
        'week_workout_count': week_workout_count,
        'week_total_duration': week_total_duration,
        'week_calories': week_calories,
        'category_stats': json.dumps(list(category_stats), cls=CustomJSONEncoder),
        'monthly_stats': json.dumps(list(monthly_stats), cls=CustomJSONEncoder),
        'weight_data': json.dumps(weight_data),
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def workout_analysis(request):
    """健身分析页面"""
    user = request.user
    # 获取过滤条件
    year = request.GET.get('year', datetime.now().year)
    category_id = request.GET.get('category', None)
    
    # 基础查询
    queryset = Workout.objects.filter(user=user, date__year=year)
    
    # 按类别过滤
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    
    # 月度健身统计
    monthly_workouts = queryset.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        count=Count('id'),
        total_calories=Sum('calories_burned')
    ).order_by('month')
    
    # 周度健身统计
    weekly_workouts = queryset.annotate(
        week=ExtractWeek('date')
    ).values('week').annotate(
        count=Count('id'),
        total_calories=Sum('calories_burned')
    ).order_by('week')
    
    # 类别分布统计
    category_stats = queryset.values('category__name').annotate(
        count=Count('id'),
        total_calories=Sum('calories_burned')
    ).order_by('-count')
    
    # 健身时长趋势
    duration_trends = queryset.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        avg_duration=Avg('duration')
    ).order_by('month')
    
    # 可用的健身类别
    categories = WorkoutCategory.objects.all()
    
    context = {
        'monthly_workouts': list(monthly_workouts),
        'weekly_workouts': list(weekly_workouts),
        'category_stats': list(category_stats),
        'duration_trends': list(duration_trends),
        'categories': categories,
        'selected_year': year,
        'selected_category': category_id,
    }
    return render(request, 'dashboard/workout_analysis.html', context)


@login_required
def body_analysis(request):
    """身体指标分析页面"""
    import json
    from datetime import date, datetime
    from django.core.serializers.json import DjangoJSONEncoder
    
    user = request.user
    
    # 获取体重记录
    weight_records = UserBodyRecord.objects.filter(user=user).order_by('date')
    
    # 自定义JSON编码器，正确处理日期对象
    class CustomJSONEncoder(DjangoJSONEncoder):
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.strftime('%Y-%m-%d')
            return super().default(obj)
    
    # 准备数据
    weight_data = [[record.date.strftime('%Y-%m-%d'), record.weight] for record in weight_records]
    
    # 如果有目标体重，添加目标线
    target_weight = user.target_weight
    
    # 体脂率变化趋势 - 预先转换日期
    body_fat_data = [[record.date.strftime('%Y-%m-%d'), record.body_fat] 
                     for record in weight_records if record.body_fat]
    
    # 围度变化趋势 - 预先转换日期
    measurements = {
        'chest': [[record.date.strftime('%Y-%m-%d'), record.chest] 
                 for record in weight_records if record.chest],
        'waist': [[record.date.strftime('%Y-%m-%d'), record.waist] 
                 for record in weight_records if record.waist],
        'hips': [[record.date.strftime('%Y-%m-%d'), record.hips] 
                for record in weight_records if record.hips],
    }
    
    # 计算BMI趋势 - 预先转换日期
    bmi_data = []
    for record in weight_records:
        if user.height:
            height_in_meters = user.height / 100
            bmi = round(record.weight / (height_in_meters ** 2), 2)
            bmi_data.append([record.date.strftime('%Y-%m-%d'), bmi])
    
    # 序列化数据 - 不再需要自定义编码器，因为已经预先处理了日期
    context = {
        'weight_data': json.dumps(weight_data),
        'target_weight': target_weight,
        'body_fat_data': json.dumps(body_fat_data),
        'measurements': {
            'chest': json.dumps(measurements['chest']),
            'waist': json.dumps(measurements['waist']),
            'hips': json.dumps(measurements['hips']),
        },
        'bmi_data': json.dumps(bmi_data),
    }
    
    return render(request, 'dashboard/body_analysis.html', context)