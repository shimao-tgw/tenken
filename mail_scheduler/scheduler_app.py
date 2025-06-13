# scheduler_app.py
# メール送信に必要なライブラリとFlaskアプリケーションをインポートする
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tenkenapp import create_app, db, mail
from tenkenapp.models.mail import Email_schedule, Email_parameter
from flask_mail import Message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger  # 追加
from datetime import datetime, timedelta
import logging

# -----------------------------------
# Flaskアプリ生成（create_app関数は __init__.py で定義されている想定）
# -----------------------------------
app = create_app()


# -----------------------------------
# ログ設定
# -----------------------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # ルートロガーのレベル設定

# ファイル出力用ハンドラ
handler = logging.FileHandler('mail_scheduler.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# ハンドラ追加
logger.addHandler(handler)

# -----------------------------------
# メール送信関数
# -----------------------------------
def send_email(schedule):
    try:
        # メール本文と送信先などを構築
        msg = Message(
            subject="点検作業のお知らせ",  # 件名
            recipients=[email.strip() for email in schedule.email.split(',')],  # 複数メールアドレスに対応
            body=f'{schedule.busyo} の {schedule.name} さんへ、\n\n'
                 f'点検作業の開始日が {schedule.work_start_date} です。\n\n'
                 f'http://192.168.4.188:8080\n\n'
                 f'点検作業お願いします'
        )
        mail.send(msg)  # メール送信
        app.logger.info(f"メール送信成功: {schedule.email}")
    except Exception as e:
        app.logger.error(f"メール送信失敗: {schedule.email} ({e})")

# -----------------------------------
# スケジュールに基づいたメール送信・状態更新処理
# -----------------------------------
def send_email_based_on_schedule():
    # Flaskアプリのコンテキスト内で処理を行う
    with app.app_context():
        try:
            now = datetime.now()  # 現在の日時

            # 現在日時以前の全てのスケジュールを取得
            schedules = Email_schedule.query.filter(
                Email_schedule.work_start_date <= now.date()
            ).order_by(Email_schedule.id).all()

            # メール送信の基準時間などのパラメータを取得
            email_param = Email_parameter.query.first()
            if not email_param:
                app.logger.error("メールパラメータが設定されていません。")
                return

            for schedule in schedules:
                # 作業開始・終了日時に基準時刻を加える
                start_dt = datetime.combine(schedule.work_start_date, email_param.work_base_time)
                end_dt = datetime.combine(schedule.work_end_date, email_param.work_base_time)

                # ◆ メール送信判定
                if now >= start_dt:
                    # メール未送信または前回送信から14日以上経過しているかチェック
                    if schedule.last_mail_send_date is None or (now.date() - schedule.last_mail_send_date.date()).days >= 14:
                        send_email(schedule)  # メール送信
                        schedule.last_mail_send_date = now  # 送信日時を更新
                        db.session.commit()

                # ◆ 状態を「作業中」に変更（開始日時を過ぎていて、かつまだ「作業中」でない場合）
                if start_dt <= now <= end_dt and schedule.biko != "作業中":
                    schedule.biko = "作業中"
                    db.session.commit()

                # ◆ 状態を「作業完了」に変更（終了日時を過ぎていて、かつまだ「作業完了」でない場合）
                if now > end_dt and schedule.biko != "作業完了":
                    schedule.biko = "作業完了"
                    db.session.commit()

        except Exception as e:
            app.logger.error(f"スケジュール更新エラー: {e}")

# -----------------------------------
# APScheduler のジョブスケジュール設定
# -----------------------------------
scheduler = BackgroundScheduler()

# 毎週月曜日の9時に定期ジョブとして send_email_based_on_schedule を実行
def scheduled_job():
    send_email_based_on_schedule()


# メール送信ジョブの実行関数（スケジュールIDを引数に受ける）
def job_func(schedule_id):
    with app.app_context():
        schedule = Email_schedule.query.get(schedule_id)
        if not schedule:
            app.logger.error(f"スケジュールID {schedule_id} が見つかりません。")
            return

        try:
            send_email(schedule)
            schedule.last_mail_send_date = datetime.now()
            db.session.commit()
            print(f"メール送信完了: {schedule.email}（作業開始日: {schedule.work_start_date}）")
        except Exception as e:
            app.logger.error(f"メール送信エラー (ID: {schedule_id}): {e}")
            
# -----------------------------------
# スクリプトを直接実行したときの処理
# -----------------------------------
if __name__ == "__main__":
    with app.app_context():
        now = datetime.now()

        # メール送信時間を取得
        param = Email_parameter.query.first()
        if not param or not param.work_base_time:
            app.logger.error("送信時刻（work_base_time）が未設定のため、ジョブを登録できません。")
        else:
            # last_mail_send_date が None で、work_start_date が現在以降のレコードを取得
            schedules = Email_schedule.query.filter(
                Email_schedule.last_mail_send_date == None,
                Email_schedule.work_start_date >= now.date()
            ).order_by(Email_schedule.work_start_date).all()

            for sched in schedules:
                run_datetime = datetime.combine(sched.work_start_date, param.work_base_time)               
                
                # 過去日時は登録しない
                if run_datetime < now:
                    app.logger.info(f"過去日時のためジョブ登録スキップ: {sched.email} {run_datetime}")
                    continue
                
                job_id = f"email_jobID_{sched.id}"  # DBのidを使ったジョブID作成（文字列に変換）
                
                scheduler.add_job(
                    func=job_func,
                    trigger=DateTrigger(run_date=run_datetime),
                    args=[sched.id],
                    #id=f'email_schedule_job_{sched.id}',
                    id=job_id,
                    replace_existing=True
                )

                app.logger.info(f"ジョブ登録: {job_id} {sched.email} => {run_datetime}")
                
    print("メールスケジューラーを開始します...")
    scheduler.start()

    try:
        import time
        while True:
            time.sleep(1)  # CPU負荷軽減のためスリープ
    except (KeyboardInterrupt, SystemExit):
        print("スケジューラーを停止します...")
        scheduler.shutdown()