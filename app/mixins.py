import datetime
import calendar
from collections import deque


class BaseCalendarMixin:
    """カレンダー関連Mixinの、基底クラス"""
    first_weekday = 0  # 0は月曜から、1は火曜から。6なら日曜日からになります。お望みなら、継承したビューで指定してください。
    week_names = ['月', '火', '水', '木', '金', '土', '日']  # これは、月曜日から書くことを想定します。['Mon', 'Tue'...

    def setup_calendar(self):
        """内部カレンダーの設定処理

        calendar.Calendarクラスの機能を利用するため、インスタンス化します。
        Calendarクラスのmonthdatescalendarメソッドを利用していますが、デフォルトが月曜日からで、
        火曜日から表示したい(first_weekday=1)、といったケースに対応するためのセットアップ処理です。

        """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """first_weekday(最初に表示される曜日)にあわせて、week_namesをシフトする"""
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)  # リスト内の要素を右に1つずつ移動...なんてときは、dequeを使うと中々面白いです
        return week_names

class WeekWithScheduleMixin:
    """スケジュールのある週間カレンダー用Mixin"""

    def get_week_calendar(self):
        """現在の週に関連するカレンダーのデータを取得する"""
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]

        # スケジュールデータの取得
        # ここで week_dates に基づいてスケジュール情報を取得し、必要に応じてデータを付加します
        schedule_data = self.get_schedules_for_week(week_dates)

        return {
            'week_dates': week_dates,
            'schedule_data': schedule_data,
        }

    def get_schedules_for_week(self, week_dates):
        """各日付に関連するスケジュールを取得する（ダミー関数、実際にはデータベースから取得）"""
        # 実際のスケジュールデータを返す処理を実装
        # ここではダミーデータを返す
        return {date: [] for date in week_dates}