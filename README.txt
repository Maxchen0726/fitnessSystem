# 健身打卡系统

一个基于Django的健身打卡跟踪和数据分析系统，帮助用户记录健身活动和身体指标变化。

## 功能介绍

### 用户管理
- 用户注册/登录/登出
- 个人资料管理（包括身高、体重、目标体重等）
- 身体指标记录（体重、体脂率、围度测量等）

### 健身打卡
- 记录健身活动（类型、时间、消耗卡路里等）
- 记录健身中的具体运动项目、组数和重量
- 创建和管理健身计划

### 数据可视化
- 体重和体脂率变化趋势图
- 健身频率和类别分布图
- 卡路里消耗统计
- BMI指数和围度变化分析

## 技术栈

- **后端**: Django 4.2
- **前端**: 
  - Bootstrap 5
  - Chart.js（数据可视化）
  - Font Awesome（图标）
- **数据库**: SQLite（可轻松迁移至PostgreSQL或MySQL）

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/fitness-tracker.git
cd fitness-tracker
```

2. 创建虚拟环境并激活
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 设置数据库
```bash
python manage.py migrate
```

5. 创建超级用户
```bash
python manage.py createsuperuser
```

6. 加载初始数据
```bash
python manage.py loaddata workout_categories
python manage.py loaddata exercises
```

7. 运行开发服务器
```bash
python manage.py runserver
```

## 项目结构

```
fitness_tracker/
│
├── fitness_tracker/         # 项目主目录
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 主URL配置
│   └── ...
│
├── users/                   # 用户应用
│   ├── models.py            # 用户和身体指标模型
│   ├── views.py             # 视图函数
│   └── ...
│
├── workouts/                # 健身打卡应用
│   ├── models.py            # 健身记录和计划模型
│   ├── views.py             # 视图函数
│   └── ...
│
├── dashboard/               # 仪表盘和数据分析应用
│   ├── views.py             # 视图函数
│   └── ...
│
├── templates/               # HTML模板
├── static/                  # 静态文件
├── media/                   # 用户上传文件
└── manage.py                # Django管理脚本
```

## 主要模型

- **CustomUser**: 扩展Django用户模型，增加健身相关字段
- **UserBodyRecord**: 用户身体指标记录
- **WorkoutCategory**: 健身类别（如有氧、力量训练等）
- **Exercise**: 具体运动项目（如深蹲、卧推等）
- **Workout**: 用户的健身记录
- **WorkoutExercise**: 健身记录中的具体运动项目记录
- **WorkoutPlan**: 用户创建的健身计划

## 主要功能截图

### 仪表盘
![仪表盘](screenshots/dashboard.png)

### 健身打卡
![健身打卡](screenshots/workout_form.png)

### 身体指标分析
![身体指标分析](screenshots/body_analysis.png)

### 健身分析
![健身分析](screenshots/workout_analysis.png)

## 未来计划

1. **社交功能**
   - 好友系统
   - 分享健身记录
   - 健身挑战赛
   - 积分和排行榜

2. **更多数据分析**
   - 训练负荷分析
   - 进步曲线
   - 个性化健身建议
   - AI健身计划推荐

3. **整合可穿戴设备**
   - 与手环、手表等健身设备API对接
   - 自动导入健身数据

4. **健身知识库**
   - 运动项目教学
   - 健身方案推荐
   - 营养建议

5. **移动应用**
   - 开发配套的移动应用
   - 离线记录功能

## 贡献

欢迎贡献代码或提出建议！请先fork本仓库并创建Pull Request。

## 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 致谢

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/)