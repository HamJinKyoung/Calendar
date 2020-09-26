from django.db import models
from django.urls import reverse

class Event(models.Model):
    start_time = models.DateTimeField("시작시간")
    end_time = models.DateTimeField("마감시간")
    title = models.CharField("이벤트 이름", max_length=50)
    description = models.TextField("상세")

    class Meta:
        verbose_name = "이벤트 데이터"
        verbose_name_plural = "이벤트 데이터"

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'