# HTML Calendar

Python 내장 HTML Calendar를 이용하여 나만의 달력 만들어보기

1. calendar.py

```python
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# '일'을 td 태그로 변환하고 이벤트를 '일'순으로 필터
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul class='event_line'> {d} </ul></td>"
		return '<td></td>'

	# '주'를 tr 태그로 변환
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# '월'을 테이블 태그로 변환
	# 각 '월'과 '연'으로 이벤트 필터
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

		cal = f'<table class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal
```

먼저 HTML Calendar의 속성을 이용하여 Table Tag로 달력을 띄워줄수 있도록 calendar.py에 위와 같이 작성해준다.

Calendar Class는 HTML Calendar 모듈을 상속받아 formatday, formatweek, formatmonth 세가지 함수를 Overriding한다. 먼저 ‘일’ 칸을 만들고 ‘일’ 칸들을 모아 ‘주’ 행을 만든 뒤 ‘주’ 행들을 모아 ‘월’ 달력을 만든다.(formatday -> formatweek -> formatmonth)

2. models.py

```python
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
```

메타 클래스의 verbose_name은 admin 상에서 해당 객체에 대한 단수 복수 형태를 어떻게 표시할 것인지에 대한 정의이다.
get_html_url()은 해당 객체의 공통 속성으로 적용되는 함수이며 해당 객체를 URL화 하였을 때 어떤 URL을 반환할 것인지 정해준다.

3. views.py

```python
from django.shortcuts import render, redirect, get_object_or_404, reverse
import datetime
from .models import Event
import calendar
from .calendar import Calendar
from django.utils.safestring import mark_safe
from .forms import EventForm

def calendar_view(request):
    today = get_date(request.GET.get('month'))

    prev_month_var = prev_month(today)
    next_month_var = next_month(today)

    cal = Calendar(today.year, today.month)
    html_cal = cal.formatmonth(withyear=True)
    result_cal = mark_safe(html_cal)

    context = {'calendar' : result_cal, 'prev_month' : prev_month_var, 'next_month' : next_month_var}

    return render(request, 'events/events.html', context)

#현재 달력을 보고 있는 시점의 시간을 반환
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

#현재 달력의 이전 달 URL 반환
def prev_month(day):
    first = day.replace(day=1)
    prev_month = first - datetime.timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

#현재 달력의 다음 달 URL 반환
def next_month(day):
    days_in_month = calendar.monthrange(day.year, day.month)[1]
    last = day.replace(day=days_in_month)
    next_month = last + datetime.timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

#새로운 Event의 등록 혹은 수정
def event(request, event_id=None):
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return redirect('calendar')
    return render(request, 'events/input.html', {'form': form})
```

get_date(): 페이지 첫 열람 시점에서의 ‘현재 월’ 혹은 prev_month / next_month로 달력의 월을 이동하였을 시점에서의 ‘월’을 반환

prev_month(), next_month(): 현재 달력 이용자가 열람하고 있는 ‘월’ 시점에서의 이전 달과 다음 달을 계산하여 반환하는 함수

event(): 새로운 Event 모델의 객체 등록 혹은 수정을 위한 함수

### 출처: http://hufsglobal.likelion.org/vacation-session2/
