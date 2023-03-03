from django.db import models


# 添加表字段后，需要更新数据库
# python manage.py makemigrations
# python manage.py migrate

# Create your models here.
class Case(models.Model):
    case_name = models.CharField(max_length=100, null=True)
    run_id = models.IntegerField(null=True, default=0)
    run_file = models.CharField(max_length=100, default='')
    run_main = models.CharField(max_length=100, default='FALSE')  # 是否属于核心
    run_result = models.CharField(max_length=100, default='Success')  # 上次执行结果
    run_time = models.CharField(max_length=100, default='2022-05-20 13:43:38')  # 运行时间点
    run_fail_count = models.IntegerField(null=True, default=0)
    run_success_count = models.IntegerField(null=True, default=0)

    def __str__(self):
        return str(self.run_id)
