# tenkenapp/views.py
# -*- coding: utf-8 -*-

import logging
import traceback
from datetime import datetime

# 2. サードパーティライブラリ
from flask import abort, current_app as app, flash, jsonify, redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import desc, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

# 3. 自作モジュール（tenkenapp配下）
from tenkenapp import db

from tenkenapp.models.koutei import Koutei, Person, Tenken
from tenkenapp.models.setubi import Nct, Baritori, Press, Tap, Bender, Spot, Weld, Kensa, Syukka, Compressor_setubi
from tenkenapp.models.nct import Acies, Em, C1, Compressor
from tenkenapp.models.baritori import Esthe
from tenkenapp.models.press import Cdstud, Gunman, Highspin, Heager, Press25t45t, Shirring, Arcstud #,T_driver,T_driver_tenken,
from tenkenapp.models.tap import Tap1, Cts1
from tenkenapp.models.bender import Rg, Hds, Hg, Atc, Astro, Egb, Egar
from tenkenapp.models.spot import Spotweld, Myspot
from tenkenapp.models.weld import Weld1, Weld_Robot, Fiver_Hand, AlufaJULIA
from tenkenapp.models.kensa import Analog_nogisu, Digital_nogisu, Keyence
from tenkenapp.models.syukka import Senjyoki, Forklift, Forklift_model, Senjyoki_monthly
from tenkenapp.models.comp import Comp_list, Comp_tenken #, Comp_test_list
from tenkenapp.models.mail import Email_schedule


# ログ設定（ファイルに保存する設定とコンソールに出力）
logging.basicConfig(filename='app.log', level=logging.INFO) #ログに保存するにはlogging.info("ユーザーがこのビューを開きました") のような出力必要
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

# エラーが発生した際にもログに記録
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"エラーが発生しました: {e}")
    return "An error occurred", 500


#点検リストを読み込み
def get_tenken_data(koutei, setubi):
    try:
        
        #print("get_tenken_data/koutei.id",koutei.id)
        #print("get_tenken_data/setubi.id",setubi.id)
        tenken_dict = {}
        
        if koutei.id == 1:#NCT
            tenken_NCT_dict = {
                1: Acies.query.all(),
                2: Em.query.all(),
                3: C1.query.all(),
                4: Compressor.query.all(),
            }
            tenken_dict = tenken_NCT_dict
                            
        elif koutei.id == 2: #バリ取り
            tenken_BARI_dict = {
                1: Esthe.query.all(),
            }
            tenken_dict = tenken_BARI_dict
            
        elif koutei.id == 3: #プレス
            tenken_PRESS_dict = {
                1:Cdstud.query.all(),
                2:Gunman.query.all(),
                3:Highspin.query.all(),
                4:Highspin.query.all(),
                5:Heager.query.all(),
                6:Press25t45t.query.all(),
                7:Press25t45t.query.all(),
                8:Shirring.query.all(),
                9:Arcstud.query.all(),
            }
            tenken_dict = tenken_PRESS_dict
            
        if koutei.id == 4: #タップ
            tenken_TAP_dict = {
                1: Tap1.query.all(),
                2: Tap1.query.all(),
                3: Cts1.query.all(),
                4: Cts1.query.all(),
            }
            tenken_dict = tenken_TAP_dict
        
        elif koutei.id == 5: #ベンダー
            tenken_BENDER_dict = {
                1:Rg.query.all(), #RG1号機
                2:Rg.query.all(), #RG2号機
                3:Rg.query.all(), #RG3号機
                4:Rg.query.all(), #RG4号機
                5:Hds.query.all(),
                6:Hg.query.all(), #HG1号機
                7:Hg.query.all(), #HG2号機
                8:Atc.query.all(),
                9:Astro.query.all(),
                10:Egb.query.all(),
                11:Egar.query.all(),
            }
            tenken_dict = tenken_BENDER_dict
        
        elif koutei.id == 6: #スポット
            tenken_SPOT_dict = {
                1:Spotweld.query.all(), #3
                2:Spotweld.query.all(), #A-2
                3:Spotweld.query.all(), #A-3
                4:Spotweld.query.all(), #A-4
                5:Spotweld.query.all(), #A-5
                6:Myspot.query.all(), #My-2
                7:Myspot.query.all(), #My-3
                8:Myspot.query.all(), #My-4
            }
            tenken_dict = tenken_SPOT_dict
        
        elif koutei.id == 7: #溶接
            tenken_WELD_dict = {
                1:Weld1.query.all(), #TIG-1
                2:Weld1.query.all(), #TIG-2
                3:Weld1.query.all(), #TIG-3
                4:Weld1.query.all(), #TIG-4
                5:Weld1.query.all(), #TIG-5
                6:Weld1.query.all(), #TIG-6
                7:Weld1.query.all(), #TIG-7
                8:Weld1.query.all(), #TIG-9
                9:Weld1.query.all(), #TIG-10
                10:Weld1.query.all(), #TIG-1
                11:Weld1.query.all(), #炭酸-1
                12:Weld1.query.all(), #炭酸-2
                13:Weld1.query.all(), #炭酸-3
                14:Weld1.query.all(), #炭酸-4
                15:Weld1.query.all(), #炭酸-5
                16:Weld_Robot.query.all(), #ロボットCO2
                17:Weld_Robot.query.all(), #ロボットTIG
                18:Fiver_Hand.query.all(), #ファイバーレーザーハンド
                19:AlufaJULIA.query.all(), #アルファJULIA
            }
            tenken_dict = tenken_WELD_dict
        
        elif koutei.id == 8: #検査
            tenken_WELD_dict = {
                1:Digital_nogisu.query.all(),
                2:Digital_nogisu.query.all(),
                3:Digital_nogisu.query.all(),
                4:Digital_nogisu.query.all(),
                5:Digital_nogisu.query.all(),
                6:Digital_nogisu.query.all(),
                7:Digital_nogisu.query.all(),
                8:Digital_nogisu.query.all(),
                9:Digital_nogisu.query.all(),
                10:Digital_nogisu.query.all(),
                11:Digital_nogisu.query.all(),
                12:Digital_nogisu.query.all(),
                13:Digital_nogisu.query.all(),
                14:Digital_nogisu.query.all(),
                15:Digital_nogisu.query.all(),
                16:Keyence.query.all(),
                17:Digital_nogisu.query.all(),
                18:Analog_nogisu.query.all(),
                19:Analog_nogisu.query.all(),
                20:Digital_nogisu.query.all(),
                21:Digital_nogisu.query.all(),
            }
            tenken_dict = tenken_WELD_dict
        
        elif koutei.id == 9: #syukka
            tenken_SYUKKA_dict = {
                1:Senjyoki.query.all(), #洗浄機 日常
                2:Senjyoki_monthly.query.all(), #洗浄機 月次点検
                3:Forklift.query.all(), #フォークリフト
            }
            tenken_dict = tenken_SYUKKA_dict
        
        elif koutei.id == 10: #syukka
            tenken_COMP_dict = {
                1:Comp_list.query.all(), #コンプレッサー
                #3:Comp_test_list.query.all() #テスト用
            }
            tenken_dict = tenken_COMP_dict
    
        return tenken_dict.get(setubi.id, []) #[]は辞書にキーがないときにデフォルト値を返すために必要
        
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。(点検データ読み込み)")
    except Exception as e:  # その他の予期しないエラーをキャッチ
        abort(500, description=f"予期しないエラーが発生しました: {str(e)}")


#点検データの保存処理
def handle_tenken_post_request(koutei, setubi, tenken_list, save_func):
    
    try:
        if koutei.koutei == "NCT":
            
            if str(setubi.id) == "1" or str(setubi.id) == "2" or str(setubi.id) == "3": #ACIE, EM, C1
                tenken_user = request.form['tenken_person']
                tenken_datetime = request.form['tenken_date']
                remarks = request.form['remarks']
                gr_ck = request.form.get('gr_check')  # NCT の場合のみ使用
                
                save_func(koutei, setubi, tenken_list, tenken_user, tenken_datetime, gr_ck, remarks, Tenken)
            else: #コンプレッサー
                tenken_user = request.form['tenken_person']
                tenken_datetime = request.form['tenken_date']
                remarks = request.form['remarks']
                
                save_func(koutei, setubi, tenken_list, tenken_user, tenken_datetime, remarks, Tenken)
                
        elif koutei.koutei =="出荷":
            if str(setubi.id) == "3": #フォークリフト
                tenken_datetime = request.form['tenken_date']
                save_func(koutei, setubi, tenken_datetime, tenken_list, Tenken)
            else: #洗浄機
                tenken_user = request.form['tenken_person']
                tenken_datetime = request.form['tenken_date']
                remarks = request.form['remarks']
                save_func(koutei, setubi, tenken_list, tenken_user, tenken_datetime, remarks, Tenken)
                
        elif koutei.koutei == "コンプレッサー":
            if str(setubi.id) == "1": #コンプレッサー
                tenken_user = request.form['tenken_person']
                tenken_datetime = request.form['tenken_date']
                remarks = request.form['remarks']
                save_func(koutei, setubi, tenken_list, tenken_user, tenken_datetime, remarks, Comp_tenken)
                
        else: #その他
            tenken_user = request.form['tenken_person']
            tenken_datetime = request.form['tenken_date']
            remarks = request.form['remarks']
            save_func(koutei, setubi, tenken_list, tenken_user, tenken_datetime, remarks, Tenken)
        
        
        return redirect(url_for('success_page'))

    except SQLAlchemyError as e:
        # SQLAlchemyエラーの処理
        logging.error(f"SQLAlchemyエラー: {str(e)}")
        abort(500, description="(データベースエラーが発生しました。(点検データ保存)")
    
    except KeyError as e:
        # キーエラー（フォームから必要なキーが欠けている場合）の処理
        logging.error(f"KeyError: フォームに必要なキーが含まれていません: {str(e)}")
        abort(400, description="必要なデータが不足しています。")

    except Exception as e:
        # その他の予期しないエラーの処理
        logging.error(f"予期しないエラー: {str(e)}")
        abort(500, description=f"予期しないエラーが発生しました: {str(e)}")
        

#点検履歴ゲット 最新５件のみ
def get_tenken_rireki(koutei, setubi):
    
    try:
        if str(koutei) == "NCT": #NCTの場合
            rireki = (
                Tenken.query \
                .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.gr_check, Tenken.biko) \
                .filter(Tenken.setubi_name == str(setubi))
                .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                .limit(5)  # 5件に絞り込む
                .all()
            )
            
            #コンプレッサーの時
            if str(setubi.setubi) == "コンプレッサー":
                rireki = (
                    Tenken.query \
                    .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.gr_check, Tenken.biko,) \
                    .filter(Tenken.setubi_name == str(setubi))
                    .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                    .limit(5)  # 5件に絞り込む
                    .all()
                )

        elif str(koutei) == "出荷":
            if setubi.id == 3: #出荷のフォークリトは少しデータが違う。
                rireki = (
                    Tenken.query
                    .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.model_no, Tenken.product_no )
                    .filter(Tenken.setubi_name == str(setubi))
                    .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                    .limit(5)  # 5件に絞り込む
                    .all()
                )
                
            else: #洗浄機 日常と月次点検
                rireki = (
                Tenken.query
                .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.biko)
                .filter(Tenken.setubi_name == str(setubi))
                .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                .limit(5)  # 5件に絞り込む
                .all()
            )
        
        elif str(koutei) == "コンプレッサー":
            if setubi.id == 1: #コンプレッサーはテーブルが違う
                rireki = (
                    db.session.query(
                        Comp_tenken.tenken_person,
                        Comp_tenken.inspection_id,
                        Comp_tenken.biko,
                        Comp_tenken.tenken_date
                    )
                    .filter(
                        Comp_tenken.setubi_name == str(setubi),
                        Comp_tenken.machine_no == "1号機"  # 1号機のみを絞り込む
                    )
                    .order_by(desc(Comp_tenken.tenken_date))  # tenken_dateで降順にソート
                    .limit(5)
                    .all()
                )
                
        else: #NCT以外
            rireki = (
                Tenken.query
                .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.biko)
                .filter(Tenken.setubi_name == str(setubi))
                .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                .limit(5)  # 5件に絞り込む
                .all()
            )
        return rireki

    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。(履歴)")


#点検履歴全件取得
#点検履歴ゲット
def get_tenken_rireki_ALL(koutei, setubi):
    
    try:
        if str(koutei) == "NCT": #NCTの場合
            rireki = (
                Tenken.query \
                .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.gr_check, Tenken.biko) \
                .filter(Tenken.setubi_name == str(setubi))
                .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                .all()
            )
            
            #コンプレッサーの時
            if str(setubi.setubi) == "コンプレッサー":
                rireki = (
                    Tenken.query \
                    .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.gr_check, Tenken.biko,) \
                    .filter(Tenken.setubi_name == str(setubi))
                    .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                    .all()
                )

        elif str(koutei) == "出荷":
            if setubi.id == 3: #フォークリフト
                rireki = (
                    Tenken.query
                    .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.model_no, Tenken.product_no )
                    .filter(Tenken.setubi_name == str(setubi))
                    .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                    .all()
                )
                
            else: #洗浄機　日常と月次
                rireki = (
                Tenken.query
                .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.biko)
                .filter(Tenken.setubi_name == str(setubi))
                .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                .all()
            )
        
        elif str(koutei) == "コンプレッサー":
            if setubi.id == 1: #コンプレッサーはテーブルが別
                rireki = (
                    db.session.query(
                        Comp_tenken.tenken_person,
                        Comp_tenken.inspection_id,
                        Comp_tenken.biko,
                        Comp_tenken.tenken_date
                    )
                    .filter(
                        Comp_tenken.setubi_name == str(setubi),
                        Comp_tenken.machine_no == "1号機"  # 1号機のみを絞り込む
                    )
                    .order_by(desc(Comp_tenken.tenken_date))  # tenken_dateで降順にソート
                    .all()
                )
        
        else: #NCT以外
            rireki = (
                Tenken.query
                .with_entities(Tenken.tenken_person, Tenken.tenken_date, Tenken.biko)
                .filter(Tenken.setubi_name == str(setubi))
                .order_by(desc(Tenken.tenken_date))  # tenken_dateを降順にソート
                .all()
            )
        return rireki

    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。(履歴)")


#点検履歴ゲット NCT コンプレッサー
def get_tenken_rireki_COMP(koutei, setubi):
    
    try:
        #if str(koutei) == "NCT": #NCTの場合            
            #コンプレッサーの時
            
        if str(setubi.setubi) == "コンプレッサー":
            # 最新のオイルデータとその担当者
            latest_nc_1st_oil = db.session.query(
                Tenken.nc_1st_oil_date, 
                Tenken.nc_1st_oil_person
            ).filter(Tenken.nc_1st_oil_date != None).order_by(Tenken.nc_1st_oil_date.desc()).first()

            # 最新のフィルターデータとその担当者
            latest_nc_2nd_filter = db.session.query(
                Tenken.nc_2nd_filter_date, 
                Tenken.nc_2nd_filter_person
            ).filter(Tenken.nc_2nd_filter_date != None).order_by(Tenken.nc_2nd_filter_date.desc()).first()

            # 最新のシリンダーデータとその担当者
            latest_nc_4th_cylinder = db.session.query(
                Tenken.nc_4th_cylinder_date, 
                Tenken.nc_4th_cylinder_person
            ).filter(Tenken.nc_4th_cylinder_date != None).order_by(Tenken.nc_4th_cylinder_date.desc()).first()

            # 最新のピストンデータとその担当者
            latest_nc_4th_piston = db.session.query(
                Tenken.nc_4th_piston_date, 
                Tenken.nc_4th_piston_person
            ).filter(Tenken.nc_4th_piston_date != None).order_by(Tenken.nc_4th_piston_date.desc()).first()

            # 最新のピストンリングデータとその担当者
            latest_nc_4th_pistonring = db.session.query(
                Tenken.nc_4th_pistonring_date, 
                Tenken.nc_4th_pistonring_person
            ).filter(Tenken.nc_4th_pistonring_date != None).order_by(Tenken.nc_4th_pistonring_date.desc()).first()

            # 最新のフェザーバルブデータとその担当者
            latest_nc_4th_fethervalve = db.session.query(
                Tenken.nc_4th_fethervalve_date, 
                Tenken.nc_4th_fethervalve_person
            ).filter(Tenken.nc_4th_fethervalve_date != None).order_by(Tenken.nc_4th_fethervalve_date.desc()).first()

            # 最新の連接棒データとその担当者
            latest_nc_4th_conrod = db.session.query(
                Tenken.nc_4th_conrod_date, 
                Tenken.nc_4th_conrod_person
            ).filter(Tenken.nc_4th_conrod_date != None).order_by(Tenken.nc_4th_conrod_date.desc()).first()

            # 最新の逆止め弁中身セットデータとその担当者
            latest_nc_4th_non_returnvalve = db.session.query(
                Tenken.nc_4th_non_returnvalve_date, 
                Tenken.nc_4th_non_returnvalve_person
            ).filter(Tenken.nc_4th_non_returnvalve_date != None).order_by(Tenken.nc_4th_non_returnvalve_date.desc()).first()
                    
            return latest_nc_1st_oil, latest_nc_2nd_filter, latest_nc_4th_cylinder, latest_nc_4th_piston, latest_nc_4th_pistonring, latest_nc_4th_fethervalve, latest_nc_4th_conrod, latest_nc_4th_non_returnvalve

    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。(履歴コンプレッサー)")


#出荷フォークリフト
def save_tenken_data_FORK(busyo, setubi, tenken_datetime, tenken_list, model_name):
    try:
        
        fork = Forklift_model.query.filter(Forklift_model.id == 1).first()
        
        #点検日時取得
        #tenken_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tenken_datetime = tenken_datetime
        
        # モデルのカラムを動的に取得
        column_names = [col.name for col in model_name.__table__.columns if col.name.startswith('c')]
        
        # 初期ステータスをNGに設定
        status_dict = {col: '' for col in column_names}
        
        # チェックボックスの処理
        if tenken_list:
            for item in tenken_list:
                item_id = item.id
                column_name = f'c{item_id}' 
                #column_name = f'c{item.id}'  # 例: item_id=1なら c1, item_id=22なら c22
                
                if f'check_c{item.id}' in request.form:
                    status_dict[column_name] = 'OK'  # OKに更新
                
                input_hour_meter = request.form.get('hour_meter','').strip()
                if input_hour_meter == '':
                    input_hour_meter = None  # 空文字の場合は None に設定
                input_syuzenkasyo = request.form.get('syuzenkasyo','').strip()
                input_syuzen_irai_date = request.form.get('syuzen_irai_date','').strip()
                input_syuzen_irai_date = input_syuzen_irai_date if input_syuzen_irai_date else None  # 空なら NULL にする
                input_syuzen_date = request.form.get('syuzen_date','').strip()
                input_syuzen_date = input_syuzen_date if input_syuzen_date else None  # 空なら NULL にする
                input_syuzen_naiyo = request.form.get('syuzen_naiyo','').strip()
                
            # 新しい点検データをデータベースに保存
            new_tenken = model_name(
                busyo_name = busyo.koutei,
                setubi_name = setubi.setubi,
                tenken_date = tenken_datetime,
                tenken_person = fork.user,
                model_no = fork.model_no,
                product_no = fork.product_no,
                hour_meter = input_hour_meter,
                **status_dict,  # 辞書を展開して動的にカラムをセット
                syuzenkasyo = input_syuzenkasyo,
                syuzen_irai_date = input_syuzen_irai_date,
                syuzen_date = input_syuzen_date,
                syuzen_naiyo = input_syuzen_naiyo,
            )

        # 各モデル（データベース）にデータを追加
        db.session.add(new_tenken)
        db.session.commit()
    
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。(保存フォークリト)")

#NCT
def save_tenken_data_NCT(busyo, setubi, tenken_list, tenken_user, tenken_datetime, gr_ck, remarks, model_name):
    
    try:
        #点検日時取得
        #tenken_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tenken_date = tenken_datetime
        
        # モデルのカラムを動的に取得
        column_names = [col.name for col in model_name.__table__.columns if col.name.startswith('c')]

        # 初期ステータスをNGに設定
        status_dict = {col: '' for col in column_names}
        
        gr_date = None
        grease_worker =""
        gr_string = ""
        
        input_air_pressure = 0
        input_residual_pressure = 0
        input_air_pressure = request.form.get('air_pressure','').strip() #AC, C1, EM 全部有り
        if str(setubi) == 'ACIES' or str(setubi) == 'C1':
            input_residual_pressure = request.form.get('residual_pressure','').strip() # AC, C1のみ
        
        if tenken_list:
            # チェックボックスの処理
            for item in tenken_list:
                item_id = item.id
                column_name = f'c{item_id}'  # 例: item_id=1なら c1, item_id=22なら c22

                if column_name in status_dict and f'check_c{item_id}' in request.form:
                    status_dict[column_name] = 'OK'  # OKに更新
                
                #グリスアップのチェックがあった場合
                if gr_ck:
                    gr_string = "実施済"
                    gr_date = tenken_date
                    grease_worker = tenken_user
                else:
                    gr_string = ""
                    gr_date = None
                    grease_worker =""

            
            
            # 新しい点検データをデータベースに保存
            new_tenken = model_name(
                busyo_name = busyo,
                setubi_name = setubi,
                **status_dict,  # 辞書を展開して動的にカラムをセット
                tenken_date = tenken_date,
                tenken_person = tenken_user,
                gr_check = gr_string,
                grease_date = gr_date,
                grease_person = grease_worker,
                nct_air_pressure = input_air_pressure,
                nct_residual_pressure = input_residual_pressure,
                biko = remarks
            )

            # 各モデル（データベース）にデータを追加
            db.session.add(new_tenken)
            db.session.commit()
    
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。(保存NCT)")
        flash("⚠️ 登録中にエラーが発生しました。やり直してください。(保存NCT)")  # エラーメッセージ


#NCTコンプレッサー
def save_tenken_data_COMP(busyo, setubi, tenken_list, tenken_user, tenken_datetime, remarks, model_class):
    
    try:
        # 点検日時取得
        #tenken_date = datetime.now()
        tenken_date = tenken_datetime
        input_nc_1st_oil_date = None
        input_nc_2nd_filter_date = None
        input_nc_4th_cylinder_date = None
        input_nc_4th_piston_date = None
        input_nc_4th_pistonring_date = None
        input_nc_4th_fethervalve_date = None
        input_nc_4th_conrod_date = None
        input_nc_4th_non_returnvalve_date = None

        
        # モデルのカラムを動的に取得
        column_names = [col.name for col in model_class.__table__.columns if col.name.startswith('c')]

        # 初期ステータスをNGに設定
        status_dict = {col: '' for col in column_names}

        if tenken_list:
            # チェックボックスの処理
            for item in tenken_list:
                item_id = item.id
                column_name = f'c{item_id}'  # 例: item_id=1なら c1, item_id=22なら c22

                #通常の処理
                if column_name in status_dict and f'check_c{item_id}' in request.form:
                    status_dict[column_name] = 'OK'  # OKに更新
                
                #コンプレッサーのc8~c17の処理
                if setubi.setubi == "コンプレッサー": 
                    if column_name in status_dict and 'check_c8' in request.form:
                        status_dict['c8'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c9' in request.form:
                        status_dict['c9'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c10' in request.form:
                        status_dict['c10'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c11' in request.form:
                        status_dict['c11'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c12' in request.form:
                        status_dict['c12'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c13' in request.form:
                        status_dict['c13'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c14' in request.form:
                        status_dict['c14'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c15' in request.form:
                        status_dict['c15'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c16' in request.form:
                        status_dict['c16'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c17' in request.form:
                        status_dict['c17'] = 'OK'  # OKに更新
                    
                    #交換部品の処理
                    input_nc_1st_oil_person = request.form.get('nc_1st_oil')
                    input_nc_2nd_filter_person = request.form.get('nc_2nd_filter')
                    input_nc_4th_cylinder_person = request.form.get('nc_4th_cylinder')
                    input_nc_4th_piston_person = request.form.get('nc_4th_piston')
                    input_nc_4th_pistonring_person = request.form.get('nc_4th_pistonring')
                    input_nc_4th_fethervalve_person = request.form.get('nc_4th_fethervalve')
                    input_nc_4th_conrod_person = request.form.get('nc_4th_conrod')
                    input_nc_4th_non_returnvalve_person = request.form.get('nc_4th_non_returnvalve')

                    if request.form.get('nc_1st_oil'):
                        input_nc_1st_oil_date = tenken_date.date()
                    if request.form.get('nc_2nd_filter'):
                        input_nc_2nd_filter_date = tenken_date.date()
                    if request.form.get('nc_4th_cylinder'):
                        input_nc_4th_cylinder_date = tenken_date.date()
                    if request.form.get('nc_4th_piston'):
                        input_nc_4th_piston_date = tenken_date.date()
                    if request.form.get('nc_4th_pistonring'):
                        input_nc_4th_pistonring_date = tenken_date.date()
                    if request.form.get('nc_4th_fethervalve'):
                        input_nc_4th_fethervalve_date = tenken_date.date()
                    if request.form.get('nc_4th_conrod'):
                        input_nc_4th_conrod_date = tenken_date.date()
                    if request.form.get('nc_4th_non_returnvalve'):
                        input_nc_4th_non_returnvalve_date = tenken_date.date()
                    
            # 新しい点検データをデータベースに保存
            new_tenken = model_class(
                busyo_name = busyo,
                setubi_name = setubi,
                **status_dict,  # 辞書を展開して動的にカラムをセット
                tenken_date=tenken_date,
                tenken_person=tenken_user,
                nc_1st_oil_person=input_nc_1st_oil_person,
                nc_2nd_filter_person=input_nc_2nd_filter_person,
                nc_4th_cylinder_person=input_nc_4th_cylinder_person,
                nc_4th_piston_person=input_nc_4th_piston_person,
                nc_4th_pistonring_person=input_nc_4th_pistonring_person,
                nc_4th_fethervalve_person=input_nc_4th_fethervalve_person,
                nc_4th_conrod_person=input_nc_4th_conrod_person,
                nc_4th_non_returnvalve_person=input_nc_4th_non_returnvalve_person,
                nc_1st_oil_date=input_nc_1st_oil_date,
                nc_2nd_filter_date=input_nc_2nd_filter_date,
                nc_4th_cylinder_date=input_nc_4th_cylinder_date,
                nc_4th_piston_date=input_nc_4th_piston_date,
                nc_4th_pistonring_date=input_nc_4th_pistonring_date,
                nc_4th_fethervalve_date=input_nc_4th_fethervalve_date,
                nc_4th_conrod_date=input_nc_4th_conrod_date,
                nc_4th_non_returnvalve_date=input_nc_4th_non_returnvalve_date,
                biko=remarks
            )

            # 各モデル（データベース）にデータを追加
            db.session.add(new_tenken)
            db.session.commit()
    
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。(保存COMP)")
        flash("⚠️ 登録中にエラーが発生しました。やり直してください。(保存COMP)")  # エラーメッセージ
        
    
#NCT以外
def save_tenken_data_ALL(busyo, setubi, tenken_list, tenken_user, tenken_datetime, remarks, model_class):
    
    try:
        # 点検日時取得
        #tenken_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tenken_date = tenken_datetime
        
        # モデルのカラムを動的に取得
        column_names = [col.name for col in model_class.__table__.columns if col.name.startswith('c')]

        # 初期ステータスをNGに設定
        status_dict = {col: '' for col in column_names}

        if tenken_list:
            # チェックボックスの処理
            for item in tenken_list:
                item_id = item.id
                column_name = f'c{item_id}'  # 例: item_id=1なら c1, item_id=22なら c22

                #通常の処理
                if column_name in status_dict and f'check_c{item_id}' in request.form:
                    status_dict[column_name] = 'OK'  # OKに更新

                
                #洗浄機のc9~c11の処理
                if setubi.setubi == "メタルシート洗浄機": 
                    if column_name in status_dict and 'check_c9' in request.form:
                        status_dict['c9'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c10' in request.form:
                        status_dict['c10'] = 'OK'  # OKに更新
                    if column_name in status_dict and 'check_c11' in request.form:
                        status_dict['c11'] = 'OK'  # OKに更新
                
            # 新しい点検データをデータベースに保存
            new_tenken = model_class(
                busyo_name = busyo,
                setubi_name = setubi,
                **status_dict,  # 辞書を展開して動的にカラムをセット
                tenken_date=tenken_date,
                tenken_person=tenken_user,
                biko=remarks
            )

            # 各モデル（データベース）にデータを追加
            db.session.add(new_tenken)
            db.session.commit()
    
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。(保存ALL)")
        flash("⚠️ 登録中にエラーが発生しました。やり直してください。(保存ALL)")  # エラーメッセージ

#プレス　トルクドライバー M3, M4
def save_tenken_data_TDriver(m_size, memori_data, jissoku_data, tenken_user, remarks, model_class):
    
    try:
        #点検日時取得
        tenken_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
        # 新しい点検データをデータベースに保存
        if memori_data:                     
            new_tenken = model_class(
                msize = m_size,
                memori = memori_data,
                jissoku = jissoku_data,
                tenken_date=tenken_date,
                tenken_person=tenken_user,
                biko=remarks
            )
            
            #モデル（データベース）にデータを追加
            db.session.add(new_tenken)
            db.session.commit()

    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。")
        flash("⚠️ 登録中にエラーが発生しました。やり直してください。(保存トルクドライバー)")

#設備コンプレッサー
def save_tenken_data_COMPRESSOR(busyo, setubi, tenken_list, tenken_user, tenken_datetime, remarks, model_class):
    
    try:      
        # 新しい点検データをデータベースに保存
        
        today = datetime.now().strftime("%Y%m%d")
        existing_count = db.session.query(func.count(Comp_tenken.inspection_id)).filter(Comp_tenken.inspection_id.like(f"{today}%")).scalar()
        
        #1号機
        new_tenken = model_class(          
            inspection_id = f"{today}-{existing_count + 1:03d}",
            setubi_name=setubi,
            machine_no="1号機",
            c1=request.form.get('work_time_1'),
            c2=request.form.get('discharge_pressure_1'),
            c3=request.form.get('discharge_temperature_1'),
            c4=request.form.get('monitor_1'),
            c5=request.form.get('indicator_lamp_1_1'),
            c6=request.form.get('indicator_lamp_2_1'),
            c7=request.form.get('indicator_lamp_3_1'),
            c8=request.form.get('oil_1_1'),
            c9=request.form.get('oil_2_1'),
            c10=request.form.get('oil_leaks_1_1'),
            c11=request.form.get('oil_leaks_2_1'),
            c12=request.form.get('vib_noise_1'),
            c13=request.form.get('dustfilter_cleaning_1_1'),
            c14=request.form.get('dustfilter_cleaning_2_1'),
            c15=request.form.get('intakefilter_cleaning_1'),
            c16=request.form.get('intakefilter_replacement_1'),
            c17=request.form.get('oilfilter_replacement_1'),
            c18=request.form.get('oil_replacement_1'),
            c19=request.form.get('element_replacement_1'),
            c20=request.form.get('cooler_replacement_1'),
            c21=request.form.get('year_tenken_1'),
            
            c22=request.form.get('drain_leaks_1'), #ドレン処理は１つのみ
            c23=request.form.get('drain_leaks_2'),
            c24=request.form.get('water_leaks'),
            c25=request.form.get('treated_water_1'),
            c26=request.form.get('treated_water_2'),
            
            main_work=request.form.get('main_work_1'),
            tenken_date=tenken_datetime,
            tenken_busyo=request.form.get('tenken_busyo'),
            tenken_person=tenken_user,
            is_completed = True ,
            biko=remarks,
        )
        db.session.add(new_tenken)
        db.session.commit()
          
        #2号機      
        new_tenken2 = model_class(          
            inspection_id = f"{today}-{existing_count + 1:03d}",
            setubi_name=setubi,
            machine_no="2号機",
            c1=request.form.get('work_time_2'),
            c2=request.form.get('discharge_pressure_2'),
            c3=request.form.get('discharge_temperature_2'),
            c4=request.form.get('monitor_2'),
            c5=request.form.get('indicator_lamp_1_2'),
            c6=request.form.get('indicator_lamp_2_2'),
            c7=request.form.get('indicator_lamp_3_2'),
            c8=request.form.get('oil_1_2'),
            c9=request.form.get('oil_2_2'),
            c10=request.form.get('oil_leaks_1_2'),
            c11=request.form.get('oil_leaks_2_2'),
            c12=request.form.get('vib_noise_2'),
            c13=request.form.get('dustfilter_cleaning_1_2'),
            c14=request.form.get('dustfilter_cleaning_2_2'),
            c15=request.form.get('intakefilter_cleaning_2'),
            c16=request.form.get('intakefilter_replacement_2'),
            c17=request.form.get('oilfilter_replacement_2'),
            c18=request.form.get('oil_replacement_2'),
            c19=request.form.get('element_replacement_2'),
            c20=request.form.get('cooler_replacement_2'),
            c21=request.form.get('year_tenken_2'),
            
            c22=request.form.get('drain_leaks_1'), #ドレン処理は１つのみ
            c23=request.form.get('drain_leaks_2'),
            c24=request.form.get('water_leaks'),
            c25=request.form.get('treated_water_1'),
            c26=request.form.get('treated_water_2'),
            
            main_work=request.form.get('main_work_1'), #メイン稼働号機はhtmlの名前は_1のみ
            tenken_date=tenken_datetime,
            tenken_busyo=request.form.get('tenken_busyo'),
            tenken_person=tenken_user,
            is_completed = True ,
            #biko=remarks,
        )
        db.session.add(new_tenken2)
        db.session.commit()
        
        #Email_scheduleにも保存
        # email_schedule = Email_schedule.query.filter_by(
        #     busyo=request.form.get('tenken_busyo'),
        #     name=tenken_user,
        #     work_start_date=tenken_datetime.date()
        # ).first()

        # if email_schedule:
        #     email_schedule.is_completed = True
        #     db.session.commit()
        # else:
        #     print("該当する Email_schedule が見つかりませんでした。")
        
        
    except Exception as e:
        db.session.rollback()  # ロールバックしてDBの状態を元に戻す
        print("データベース保存エラー:", e)
        print(traceback.format_exc())  # 詳細なエラーメッセージを表示
        flash("⚠️ 登録中にエラーが発生しました。やり直してください。(設備コンプレッサー)")  # エラーメッセージ

@app.route('/')
def index():
    
    try:
        # koutei_tblテーブルから工程名を取得
        koutei_list = Koutei.query.all()  # 全ての工程を取得
        return render_template('index.html', processes=koutei_list)
    
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。")

        
@app.route('/koutei/<int:id>')
def koutei_page(id):
    
    # idとクラスを辞書で対応付け
    setubi_classes = {
        1: Nct,
        2: Baritori,
        3: Press,
        4: Tap,
        5: Bender,
        6: Spot,
        7: Weld,
        8: Kensa,
        9: Syukka,
        10: Compressor_setubi
    }
    
    try:
        # Kouteiデータの取得
        koutei_id = Koutei.query.get_or_404(id)

        # idに対応するクラスを取得
        setubi_class = setubi_classes.get(id)

        if setubi_class is None:
            abort(404, description="無効なIDです。")
        
        # 対応するクラスからデータを取得
        setubi_list = setubi_class.query.all()
            
        return render_template("koutei.html", koutei=koutei_id,setubi_list=setubi_list)
    
    except NoResultFound:
        abort(404, description="対象のデータが見つかりませんでした。")
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。（トップ）")


@app.route('/tenken/<int:koutei_id>/<int:setubi_id>', methods=['GET', 'POST'])
def tenken_page(koutei_id, setubi_id):
    
    try:
        htmlpage = 'tenken.html' #デフォルト
        koutei = Koutei.query.get_or_404(koutei_id)  # 工程名の取得
        
        if koutei_id == 1:

            setubi = Nct.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'NCT').all()
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            
            
            if setubi_id != 4: #コンプレッサー以外の時（AC,EM,C1）
                if setubi_id == 1: #AC
                    htmlpage ='tenken_nct_ac.html'
                elif setubi_id == 2: #EM
                   htmlpage ='tenken_nct_em.html'
                elif setubi_id == 3: #C1のとき
                    htmlpage ='tenken_nct_c1.html'
                if request.method == 'POST':
                    return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_NCT)
                
            elif setubi_id == 4: #コンプレッサーの時
                tenken_rireki_COMP = get_tenken_rireki_COMP(koutei, setubi)
                htmlpage ='tenken_nct_comp.html'
                if request.method == 'POST':
                    return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_COMP)
                            
                return render_template(htmlpage,koutei=koutei, setubi=setubi, tenken_list=tenken_list,person_list=person_list,tenken_rireki=tenken_rireki, tenken_rireki_COMP=tenken_rireki_COMP)
            
            
        elif koutei_id == 2:
            #バリ取り
            setubi = Baritori.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'BARI').all() #作業者名取得 バリ取り 
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            
            if request.method == 'POST':
                return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)

        elif koutei_id == 3:
            #プレス
            setubi = Press.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'PRESS').all() #作業者名取得 プレス
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            
            if request.method == 'POST':
                return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)
            
            #
            #
            #トルクドライバーはつかわないけど、とりあえずとっておく
            #if setubi.id == 9: #トルクドライバーM3
            #    tenken_list = T_driver.query.filter_by(id=1).all()
            #    tenken_rireki = (
            #        T_driver_tenken.query
            #        .with_entities(T_driver_tenken.tenken_person, T_driver_tenken.tenken_date, T_driver_tenken.biko,T_driver_tenken.msize)
            #        .filter(T_driver_tenken.msize == "M3")  # msizeが"M3"のデータを絞り込み
            #        .order_by(desc(T_driver_tenken.tenken_date))  # tenken_dateを降順にソート
            #        .limit(5)  # 5件に絞り込む
            #        .all()
            #    )
            #    if request.method == 'POST':
            #        memori_data = request.form['memori_data']
            #        jissoku_data = request.form['jissoku_data']
            #        tenken_user = request.form['tenken_person']
            #        remarks = request.form['remarks']
            
            #        save_tenken_data_TDriver("M3", memori_data, jissoku_data, tenken_user, remarks, T_driver_tenken)
                
                    # 成功ページにリダイレクト（必要に応じて設定）
            #        return redirect(url_for('success_page'))
            
            #elif setubi.id == 10: #トルクドライバーM4
            #    tenken_list = T_driver.query.filter_by(id=2).all()
            #    tenken_rireki = (
            #        T_driver_tenken.query
            #        .with_entities(T_driver_tenken.tenken_person, T_driver_tenken.tenken_date, T_driver_tenken.biko,T_driver_tenken.msize)
            #        .filter(T_driver_tenken.msize == "M4")  # msizeが"M4"のデータを絞り込み
            #        .order_by(desc(T_driver_tenken.tenken_date))  # tenken_dateを降順にソート
            #        .limit(5)  # 5件に絞り込む
            #        .all()
            #    )
            #    if request.method == 'POST':
            #        memori_data = request.form['memori_data']
            #        jissoku_data = request.form['jissoku_data']
            #        tenken_user = request.form['tenken_person']
            #        remarks = request.form['remarks']
            
            #        save_tenken_data_TDriver("M4", memori_data, jissoku_data, tenken_user, remarks, T_driver_tenken)
                
                    # 成功ページにリダイレクト（必要に応じて設定）
            #        return redirect(url_for('success_page'))
            
            #if setubi.id == 9 or setubi.id == 10:
                #トルクドライバーのとき
            #    htmlpage = 'tenken_driver.html'
        
        elif koutei_id == 4:
            #タップ
            setubi = Tap.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'PRESS').all() #作業者名取得 プレス・タップ同じ
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)

            if request.method == 'POST':
                return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)
            
        elif koutei_id == 5:
            #ベンダー
            setubi = Bender.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'BENDER').all() #作業者名取得 ベンダー
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            
            if request.method == 'POST':
                return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)
        
        elif koutei_id == 6:
            #スポット
            setubi = Spot.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'SPOT').all() #作業者名取得 ベンダー
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            
            if request.method == 'POST':
                return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)
                    
        elif koutei_id == 7:
            #溶接
            setubi = Weld.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'WELD').all() #作業者名取得 溶接仕上げ
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            
            if request.method == 'POST':
                return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)
        
        elif koutei_id == 8:
            #検査
            setubi = Kensa.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'KENSA').all() #作業者名取得 検査
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            htmlpage ='tenken_kensa.html'
            
            if request.method == 'POST':
                return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)
            
        elif koutei_id == 9:
            #出荷
            setubi = Syukka.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'SYUKKA').all() #作業者名取得 出荷
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            
            if str(setubi.id) == "1": #洗浄機　日常
                if request.method == 'POST':
                    return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)    
            
            elif str(setubi.id) == "2": #洗浄機　月次
                htmlpage = 'tenken_syukka_monthly.html'
                if request.method == 'POST':
                    return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_ALL)  
            
            elif str(setubi.id) == "3": #フォークリフトの時
                htmlpage = 'tenken_forklift.html'
                tenken_model = Forklift_model.query.get_or_404(1)
                if request.method == 'POST':
                    return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_FORK)
                        
        
        elif koutei_id == 10:
            #コンプレッサー
            setubi = Compressor_setubi.query.get_or_404(setubi_id)
            person_list = Person.query.filter(Person.busyo == 'COMP').all() #作業者名取得 主査の名前
            tenken_list = get_tenken_data(koutei, setubi)
            tenken_rireki = get_tenken_rireki(koutei, setubi)
            
            if str(setubi.id) == "1": #コンプレッサー
                setubi = Compressor_setubi.query.get_or_404(setubi_id)
                person_list = Person.query.filter(Person.busyo == 'COMP').all() #作業者名取得 主査の名前
                tenken_list = get_tenken_data(koutei, setubi)
                tenken_rireki = get_tenken_rireki(koutei, setubi)
                htmlpage = 'tenken_comp.html'
                if request.method == 'POST':
                    return handle_tenken_post_request(koutei, setubi, tenken_list, save_tenken_data_COMPRESSOR)
                
                
        #表示
        if koutei_id == 9 and setubi_id == 3: #フォークリフトの時
            return render_template(htmlpage,koutei=koutei, setubi=setubi, tenken_list=tenken_list,person_list=person_list,tenken_rireki=tenken_rireki, tenken_model=tenken_model)
        
        else: #他
            return render_template(htmlpage,koutei=koutei, setubi=setubi, tenken_list=tenken_list,person_list=person_list,tenken_rireki=tenken_rireki)
    
    
    #get_or_404を使う場合はNoResultFoundは不要
    except SQLAlchemyError:
       abort(500, description="データベースエラーが発生しました。（設備）")



#favicon.icoのリクエストを無視
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content


@app.route('/success')
def success_page():
    
    flash("処理が完了しました。")
    # インデックスページにリダイレクト
    return redirect(url_for('index'))


@app.route('/back')
def go_back():
    referer = request.headers.get('Referer')
    if referer:
        return redirect(referer)
    return redirect(url_for('index'))


 
#履歴ページ 5件
@app.route('/rireki/<int:koutei_id>/')
def rireki_page(koutei_id):
    
    try:
        htmlpage = "rireki.html"
        
        koutei = Koutei.query.get_or_404(koutei_id)  # 工程名の取得        
        
        # 工程ごとに適用するモデルをマッピング
        setubi_mapping = {
            1: Nct,
            2: Baritori,
            3: Press,
            4: Tap,
            5: Bender,
            6: Spot,
            7: Weld,
            8: Kensa,
            9: Syukka,
            10: Compressor_setubi,
        }
               
         # デフォルトを設定（マッピングにない場合の処理）
        ModelClass = setubi_mapping.get(koutei_id)       
        
        # 設備情報を動的に取得（設備IDはすべて取得）
        setubi_list = ModelClass.query.all()  # 設備情報を全て取得
        
        # 各設備ごとの点検履歴を取得
        rireki_results = {}
        for setubi in setubi_list:
            rireki_results[setubi] = get_tenken_rireki(koutei, setubi)  # setubiオブジェクトをキーにする　超重要！
        
        # レンダリング
        return render_template(
            htmlpage,
            koutei=koutei,
            setubi=setubi_list,
            rireki_results=rireki_results  # 動的に点検履歴結果をテンプレートに渡す
        )
    
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。")   


#履歴リストページ  全件表示
@app.route('/rireki_list/<int:koutei_id>/<int:setubi_id>')
def rireki_list_page(koutei_id, setubi_id):
    
    #デフォルト
    htmlpage = "rireki_list.html"
    columns = ['tenken_person', 'tenken_date','biko'] # デフォルト カラム名（キー）をリストで定義
    
    # 工程ごとに適用するモデルをマッピング
    setubi_mapping = {
        1: Nct,
        2: Baritori,
        3: Press,
        4: Tap,
        5: Bender,
        6: Spot,
        7: Weld,
        8: Kensa,
        9: Syukka,
        10: Compressor_setubi,
    }
    
    # 工程ごとに適用するモデルをマッピング
    person_mapping = {
        1: "NCT",
        2: "BARI",
        3: "PRESS",
        4: "PRESS",
        5: "BENDER",
        6: "SPOT",
        7: "WELD",
        8: "KENSA",
        9: "SYUKKA",
        10: "COMP",
    }
            
    # デフォルトを設定（マッピングにない場合の処理）
    ModelClass = setubi_mapping.get(koutei_id)       
    # 設備情報を動的に取得（設備IDはすべて取得）
    setubi = ModelClass.query.get_or_404(setubi_id)  # 設備情報を取得
    koutei = Koutei.query.get_or_404(koutei_id)  # 工程名の取得
    tenken_rireki_ALL = get_tenken_rireki_ALL(koutei,setubi)
    busyo = person_mapping.get(koutei_id, None)
    person_list = Person.query.filter(Person.busyo == busyo).all() if busyo else []
    
    # --- ここからフィルタリング処理 ---
    # フィルタリング用のリクエストパラメータを取得
    filter_person = request.args.get('person', default=None, type=str)
    filter_date = request.args.get('date', default=None, type=str)

    # フィルタリング
    if filter_person:
        tenken_rireki_ALL = [record for record in tenken_rireki_ALL if record._mapping['tenken_person'] == filter_person]

    if filter_date:
        tenken_rireki_ALL = [record for record in tenken_rireki_ALL if str(record._mapping['tenken_date']).startswith(filter_date)]
    
    # もし日付だけ、作業者だけでフィルタリングを行う場合
    if not filter_person and not filter_date:
        # フィルタリングがない場合は全件表示
        tenken_rireki_ALL = tenken_rireki_ALL
    
    
    # 10件ずつのページネーションを適用
    page = request.args.get('page', 1, type=int)  # ページ番号を取得、デフォルトは1
    per_page = 10  # 1ページあたり10件表示
    
    # ページネーション
    start = (page - 1) * per_page
    end = start + per_page
    tenken_rireki_paginated = tenken_rireki_ALL[start:end]  # ページに応じたデータを取得   
    
    if koutei_id == 1 and setubi_id !=4: #AC,EM,C1 の時は別ページ
        htmlpage = "rireki_list_nct.html"
        columns = ['tenken_person', 'tenken_date', 'gr_check', 'biko'] # カラム名（キー）をリストで定義
        
    elif koutei_id == 9 and setubi_id == 3: #フォークリフト
        htmlpage = "rireki_list_forklift.html"
        columns = ['tenken_person', 'tenken_date', 'model_no', 'product_no'] # カラム名（キー）をリストで定義
        
        
    # タプルを辞書に変換
    tenken_rireki_dict = [{key: record._mapping[key] for key in columns} for record in tenken_rireki_paginated]
    
    # ページネーションのための情報を渡す
    total = len(tenken_rireki_ALL)  # 総データ件数
    pages = (total // per_page) + (1 if total % per_page > 0 else 0)  # 総ページ数
    
    
    return render_template(htmlpage, koutei=koutei, setubi=setubi,
                           tenken_rireki=tenken_rireki_dict, page=page, pages=pages, person_list=person_list)



#履歴詳細ページ  1件ごと表示
@app.route('/rireki_detail/<int:koutei_id>/<int:setubi_id>/<string:tenken_date>/')
def rireki_detail_page(koutei_id, setubi_id, tenken_date):
    
         # **変数の初期化**
        tenken_data1 = None
        tenken_data2 = None
        tenken_data = None
    
        htmlpage = "rireki_detail.html" #デフォルト
        
        if koutei_id == 1 and setubi_id != 4: # AC,EM,C1
            htmlpage = "rireki_detail_nct.html"
            
        elif koutei_id == 9 and setubi_id == 3: #フォークリフト
            htmlpage = "rireki_detail_forklift.html"

        elif koutei_id == 10 and setubi_id == 1: #コンプレッサー
            htmlpage = "rireki_detail_compressor.html"
        
        koutei = Koutei.query.get_or_404(koutei_id)  # 工程名の取得
        #setubi = Nct.query.get_or_404(setubi_id)
        
        # 工程ごとに適用するモデルをマッピング
        setubi_mapping = {
            1: Nct,
            2: Baritori,
            3: Press,
            4: Tap,
            5: Bender,
            6: Spot,
            7: Weld,
            8: Kensa,
            9: Syukka,
            10: Compressor_setubi,
        }

        ModelClass = setubi_mapping.get(koutei_id, setubi_id)
         # setubi_id に応じて動的にテーブルを取得
        setubi = ModelClass.query.get_or_404(setubi_id)
        tenken_list = get_tenken_data(koutei, setubi)
        if not isinstance(tenken_list, list):  
            tenken_list = []  # 念のためリストで初期化
        tenken_data = None
        
        tenken_result = []
        
        # 文字列の日付を datetime に変換
        tenken_date_obj = datetime.strptime(tenken_date, "%Y-%m-%d %H:%M:%S")
        
        if koutei_id == 10: #コンプレッサー
            tenken_data1 = (
                db.session.query(Comp_tenken)
                .filter(Comp_tenken.setubi_name == setubi.setubi)
                .filter(Comp_tenken.tenken_date == tenken_date_obj)
                .filter(Comp_tenken.machine_no == "1号機") #1号機用
                .first()
            )
            tenken_data2 = (
                db.session.query(Comp_tenken)
                .filter(Comp_tenken.setubi_name == setubi.setubi)
                .filter(Comp_tenken.tenken_date == tenken_date_obj)
                .filter(Comp_tenken.machine_no == "2号機") #2号機用
                .first()
            )
            
        else: #コンプレッサー以外
            tenken_data = (
                db.session.query(Tenken)
                .filter(Tenken.setubi_name == setubi.setubi)
                .filter(Tenken.tenken_date == tenken_date_obj) 
                .first()
            )
        
        for tenken in tenken_list:
            id = tenken.id  # tenken_list の ID (c1～c25 に対応)

            # tenken_data から一致する点検結果を取得
            if koutei_id == 10: #コンプレッサー
                result1 = getattr(tenken_data1, f'c{id}', None)
                result2 = getattr(tenken_data2, f'c{id}', None)
            else: #コンプレッサー以外
                result = getattr(tenken_data, f'c{id}', None) # c1, c2, ... c25 を動的に取得

            
            if koutei_id == 9 and setubi_id == 3: #フォークリフト
                # データを辞書として格納
                tenken_result.append({
                    "id": id,
                    "list":tenken.tenken_list,
                    "contents": tenken.contents,  # 点検内容
                    "kensa_method":tenken.kensa_method, # 検査方法
                    "result": result,  # 点検結果
                })
            
            elif koutei_id == 10: #コンプレッサー
                tenken_result.append({
                    "id": id,
                    "list":tenken.tenken_list,
                    "contents": tenken.contents,  # 点検内容
                    "result1": result1,  # 1号機
                    "result2": result2,  # 2号機  
                })
                
            else: #その他
                # データを辞書として格納
                tenken_result.append({
                    "id": id,
                    "list":tenken.tenken_list,
                    "contents": tenken.contents,  # 点検内容
                    "result": result,  # 点検結果
                })
        
        
        return render_template(htmlpage,koutei=koutei, setubi=setubi, tenken_result=tenken_result, tenken_data=tenken_data,tenken_data1=tenken_data1, tenken_data2=tenken_data2)


##
#詳細ページ備考を更新
@app.route('/update_biko', methods=['POST'])
def update_biko():
    data = request.get_json()
    tenken_id = data.get('id')
    new_biko = data.get('biko')

    tenken = Tenken.query.get(tenken_id)
    if tenken:
        tenken.biko = new_biko  # 備考データを更新
        db.session.commit()
        return jsonify({"success": True})
    
    return jsonify({"success": False})


#詳細ページ備考を更新 コンプレッサー用
@app.route('/update_biko_comp', methods=['POST'])
def update_biko_comp():
    data = request.get_json()
    tenken_id = data.get('id')
    new_biko = data.get('biko')

    tenken = Comp_tenken.query.get(tenken_id)
    if tenken:
        tenken.biko = new_biko  # 備考データを更新
        db.session.commit()
        return jsonify({"success": True})
    
    return jsonify({"success": False})
##



#管理者ページ
@app.route('/admin')
def admin_page():
    
    return render_template('admin_index.html')
    


## 社員 テーブルCRUD機能##
# データをJSONで返すAPI
@app.route('/admin_person_data')
def get_peron_data():
    people = Person.query.all()
    data = [{"id": p.id, "busyo":p.busyo  ,"name": p.name, "email": p.email} for p in people]
    return jsonify({"data": data})  # DataTables形式に合わせる

# データ作成
@app.route('/admin_person/create', methods=['POST'])
def create_person():
    data = request.get_json()  # request.json ではなく request.get_json() を使う
    if not data:
        return jsonify({"message": "リクエストデータがありません"}), 400

    new_person = Person(busyo=data['busyo'], name=data['name'], email=data['email'])
    db.session.add(new_person)
    db.session.commit()
    return jsonify({"message": "作成完了", "id": new_person.id})

# データ更新
@app.route('/admin_person/update/<int:id>', methods=['POST'])
def update_person(id):
    data = request.json
    person = Person.query.get(id)
    if person:
        person.busyo = data['busyo']
        person.name = data['name']
        person.email = data['email']
        db.session.commit()
        return jsonify({"message": "更新完了"})
    return jsonify({"message": "対象データが見つかりません"}), 404

# データ更新リクエスト処理
@app.route('/admin_person/get/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    if person:
        return jsonify({
            "id": person.id,
            "busyo": person.busyo,
            "name": person.name,
            "email": person.email
        })
    else:
        return jsonify({"error": "Person not found"}), 404

# データ削除
@app.route('/admin_person/delete/<int:id>', methods=['DELETE'])
def delete_person(id):
    person = Person.query.get(id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "削除完了"})
    else:
        return jsonify({"message": "対象データが見つかりません"}), 404
    
#personテーブルを表示
@app.route('/admin_person')
def admin_person():
    # ここにビューのロジックを記述
    return render_template('admin_person.html')
##ここまで社員テーブルCRUD機能##




## 工程 テーブルCRUD機能##
#kouteiテーブルを表示
@app.route('/admin_koutei')
def admin_koutei():
    # ここにビューのロジックを記述
    return render_template('admin_koutei.html')

# データをJSONで返すAPI
@app.route('/admin_koutei_data')
def get_koutei_data():
    koutei = Koutei.query.all()
    data = [{"id": k.id, "koutei":k.koutei} for k in koutei]
    return jsonify({"data": data})  # DataTables形式に合わせる

# データ作成
@app.route('/admin_koutei/create', methods=['POST'])
def create_koutei():
    data = request.get_json()  # request.json ではなく request.get_json() を使う
    if not data:
        return jsonify({"message": "リクエストデータがありません"}), 400

    new_koutei = Koutei(koutei=data['koutei'])
    db.session.add(new_koutei)
    db.session.commit()
    return jsonify({"message": "作成完了", "id": new_koutei.id})

# データ更新
@app.route('/admin_koutei/update/<int:id>', methods=['POST'])
def update_koutei(id):
    data = request.json
    koutei = Koutei.query.get(id)
    if koutei:
        koutei.koutei = data['kotuei']
        db.session.commit()
        return jsonify({"message": "更新完了"})
    return jsonify({"message": "対象データが見つかりません"}), 404

# データ更新リクエスト処理
@app.route('/admin_koutei/get/<int:id>', methods=['GET'])
def get_koutei(id):
    koutei = Koutei.query.get(id)
    if koutei:
        return jsonify({
            "id": koutei.id,
            "koutei": koutei.koutei,
        })
    else:
        return jsonify({"error": "Koutei not found"}), 404
# データ削除はつけない
##ここまで工程テーブルCRUD機能##



##ここから設備テーブル
#設備テーブル インデックスページ
@app.route('/admin_setubi_index/')
def admin_setubi_index():

    try:
        # koutei_tblテーブルから工程名を取得
        koutei_list = Koutei.query.all()  # 全ての工程を取得
        return render_template('admin_setubi_index.html', processes=koutei_list)
    
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。")


#HTMLを返すエンドポイント
@app.route('/admin_setubi_koutei_page/<int:koutei_id>/', methods=['GET'])
def admin_setubi_koutei_page(koutei_id):
    # koutei_idに基づいてkouteiを取得
    try:
        koutei = Koutei.query.get(koutei_id)
        if not koutei:
            return abort(404)  # koutei_idが存在しない場合は404エラーを返す
    except Exception as e:
        print(f"Error: {e}")
        return "内部サーバーエラー", 500  # エラー発生時は500を返す
    
    setubi = None  # 初期化

    # 工程ごとに対応するテーブルから設備を取得
    if koutei_id == 1:  # NCT
        setubi = Nct.query.all()
    elif koutei_id == 2:  # バリ取り
        setubi = Baritori.query.all()
    elif koutei_id == 3:  # プレス
        setubi = Press.query.all()
    elif koutei_id == 4:  # タップ
        setubi = Tap.query.all()
    elif koutei_id == 5:  # ベンダー
        setubi = Bender.query.all()
    elif koutei_id == 6:  # スポット
        setubi = Spot.query.all()
    elif koutei_id == 7:  # 仕上げ
        setubi = Weld.query.all()
    elif koutei_id == 8:  # 検査
        setubi = Kensa.query.all()
    elif koutei_id == 9:  # 出荷
        setubi = Syukka.query.all()
    elif koutei_id == 10:  # コンプレッサー
        setubi = Compressor_setubi.query.all()
    else:
        return "Invalid koutei_id", 404  # 存在しない工程IDならエラーを返す

    # HTMLテンプレートにデータを渡してレンダリング
    return render_template('admin_setubi_koutei.html', koutei=koutei, setubi=setubi)


# JSONを返すエンドポイント
@app.route('/admin_setubi_data/<int:koutei_id>/', methods=['GET'])
def get_setubi_data(koutei_id):
    # 工程情報を取得
    koutei = Koutei.query.get(koutei_id)
    if not koutei:
        return jsonify({"error": "工程が見つかりません"}), 404  

    # 工程ごとに対応する設備データを取得
    koutei_map = {
        1: Nct,
        2: Baritori,
        3: Press,
        4: Tap,
        5: Bender,
        6: Spot,
        7: Weld,
        8: Kensa,
        9: Syukka,
        10: Compressor_setubi
    }

    setubi_model = koutei_map.get(koutei_id)
    if not setubi_model:
        return jsonify({"error": "無効な工程ID"}), 404

    setubi_data = setubi_model.query.all()
    setubi_list = [{"id": s.id, "setubi": s.setubi} for s in setubi_data]

    return jsonify(setubi_list)

# 新規設備作成のエンドポイント
@app.route('/admin_setubi_create/<int:koutei_id>/', methods=['POST'])
def create_setubi(koutei_id):
    setubi_name = request.form.get('setubi')

    # 工程ごとに対応するテーブルに設備を追加
    if koutei_id == 1:  # NCT
        new_setubi = Nct(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 2:  # バリ取り
        new_setubi = Baritori(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 3:  # プレス
        new_setubi = Press(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 4:  # タップ
        new_setubi = Tap(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 5:  # ベンダー
        new_setubi = Bender(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 6:  # スポット
        new_setubi = Spot(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 7:  # 仕上げ
        new_setubi = Weld(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 8:  # 検査
        new_setubi = Kensa(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 9:  # 出荷
        new_setubi = Syukka(setubi=setubi_name)
        db.session.add(new_setubi)
    elif koutei_id == 10:  # コンプレッサー
        new_setubi = Compressor_setubi(setubi=setubi_name)
        db.session.add(new_setubi)
    else:
        return jsonify({"error": "Invalid koutei_id"}), 404  # 存在しない工程IDならエラーを返す

    db.session.commit()  # 保存
    return jsonify({"success": True})

# 設備 編集用 [個別情報取得]
@app.route('/admin_get_setubi_data/<int:koutei_id>/<int:setubi_id>/', methods=['GET'])
def get_setubi_data_detail(koutei_id, setubi_id):
    # koutei_id と setubi_id に基づいて設備情報を取得
    setubi = None
    if koutei_id == 1:  # NCT
        setubi = Nct.query.get(setubi_id)
    elif koutei_id == 2:  # バリ取り
        setubi = Baritori.query.get(setubi_id)
    elif koutei_id == 3:  # プレス
        setubi = Press.query.get(setubi_id)
    elif koutei_id == 4:  # タップ
        setubi = Tap.query.get(setubi_id)
    elif koutei_id == 5:  # ベンダー
        setubi = Bender.query.get(setubi_id)
    elif koutei_id == 6:  # スポット
        setubi = Spot.query.get(setubi_id)
    elif koutei_id == 7:  # 仕上げ
        setubi = Weld.query.get(setubi_id)
    elif koutei_id == 8:  # 検査
        setubi = Kensa.query.get(setubi_id)
    elif koutei_id == 9:  # 出荷
        setubi = Syukka.query.get(setubi_id)
    elif koutei_id == 10:  # コンプレッサー
        setubi = Compressor_setubi.query.get(setubi_id)
    else:
        return jsonify({"error": "Invalid koutei_id"}), 404  # 存在しない工程IDならエラーを返す

    if not setubi:
        return jsonify({"error": "設備が見つかりません"}), 404

    return jsonify({"id": setubi.id, "setubi": setubi.setubi})

# 設備　更新処理
@app.route('/admin_setubi_update/<int:koutei_id>/<int:setubi_id>/', methods=['POST'])
def update_setubi(koutei_id, setubi_id):
    setubi_name = request.form.get('setubi')
    #print(f"Received update request for setubi_id: {setubi_id} with new name: {setubi_name}")  # デバッグ用
     
    # 更新対象の設備を取得
    setubi = None
    if koutei_id == 1:  # NCT
        setubi = Nct.query.get(setubi_id)
    elif koutei_id == 2:  # バリ取り
        setubi = Baritori.query.get(setubi_id)
    elif koutei_id == 3:  # プレス
        setubi = Press.query.get(setubi_id)
    elif koutei_id == 4:  # タップ
        setubi = Tap.query.get(setubi_id)
    elif koutei_id == 5:  # ベンダー
        setubi = Bender.query.get(setubi_id)
    elif koutei_id == 6:  # スポット
        setubi = Spot.query.get(setubi_id)
    elif koutei_id == 7:  # 仕上げ
        setubi = Weld.query.get(setubi_id)
    elif koutei_id == 8:  # 検査
        setubi = Kensa.query.get(setubi_id)
    elif koutei_id == 9:  # 出荷
        setubi = Syukka.query.get(setubi_id)
    elif koutei_id == 10:  # コンプレッサー
        setubi = Compressor_setubi.query.get(setubi_id)
    else:
        return jsonify({"error": "Invalid koutei_id"}), 404  # 存在しない工程IDならエラーを返す

    if not setubi:
        return jsonify({"error": "設備が見つかりません"}), 404

    # 設備名を更新
    setubi.setubi = setubi_name
    db.session.commit()

    return jsonify({"success": True})

#設備削除
@app.route('/admin_setubi_delete/<int:koutei_id>/<int:setubi_id>/', methods=['POST'])
def delete_setubi(koutei_id, setubi_id):
    # 削除対象の設備を取得
    setubi = None
    if koutei_id == 1:  # NCT
        setubi = Nct.query.get(setubi_id)
    elif koutei_id == 2:  # バリ取り
        setubi = Baritori.query.get(setubi_id)
    elif koutei_id == 3:  # プレス
        setubi = Press.query.get(setubi_id)
    elif koutei_id == 4:  # タップ
        setubi = Tap.query.get(setubi_id)
    elif koutei_id == 5:  # ベンダー
        setubi = Bender.query.get(setubi_id)
    elif koutei_id == 6:  # スポット
        setubi = Spot.query.get(setubi_id)
    elif koutei_id == 7:  # 仕上げ
        setubi = Weld.query.get(setubi_id)
    elif koutei_id == 8:  # 検査
        setubi = Kensa.query.get(setubi_id)
    elif koutei_id == 9:  # 出荷
        setubi = Syukka.query.get(setubi_id)
    elif koutei_id == 10:  # コンプレッサー
        setubi = Compressor_setubi.query.get(setubi_id)
    else:
        return jsonify({"error": "Invalid koutei_id"}), 404  # 存在しない工程IDならエラーを返す

    if not setubi:
        return jsonify({"error": "設備が見つかりません"}), 404

    db.session.delete(setubi)
    db.session.commit()

    return jsonify({"success": True})

##ここまで設備テーブル##
##




##
##tenkenテーブルここから
@app.route('/admin_tenken_data', methods=['GET'])
def get_tenken_data_admin():
    # データベースからTenkenテーブルの全データを取得
    # IDが大きい方順に並べ替え(降順)
    tenkens = Tenken.query.all()
    # データをリストに変換
    data = []
    for tenken in tenkens:
        data.append({
            'id': tenken.id,
            'busyo_name': tenken.busyo_name,
            'setubi_name': tenken.setubi_name,
            'tenken_person': tenken.tenken_person,
            'tenken_date': tenken.tenken_date.strftime('%Y-%m-%d %H:%M:%S'),  # 日付フォーマット
            'biko': tenken.biko
        })
    return jsonify({"data": data})  # {"data": data}の形に変更

@app.route('/admin_tenken/get/<int:id>', methods=['GET'])
def get_tenken(id):
    # IDに基づいてデータを取得する処理
    tenken = db.session.query(Tenken).get(id)
    if tenken:
        return jsonify({
            'id': tenken.id,
            'busyo_name': tenken.busyo_name,
            'setubi_name': tenken.setubi_name,
            'tenken_person': tenken.tenken_person,
            'tenken_date': tenken.tenken_date.strftime('%Y-%m-%d %H:%M:%S'),  # 日付フォーマット
            'biko': tenken.biko
        })
    return jsonify({'error': 'Tenken not found'}), 404


@app.route('/admin_tenken/update/<int:id>', methods=['POST'])
def update_tenken(id):
    data = request.get_json()
    
    # 既存のデータを取得
    tenken = Tenken.query.get(id)
    if tenken is None:
        return jsonify({'message': 'データが見つかりません'}), 404
    
    # データを更新
    tenken.busyo_name = data['busyo_name']
    tenken.setubi_name = data['setubi_name']
    tenken.tenken_person = data['tenken_person']
    tenken.tenken_date = data['tenken_date']
    tenken.biko = data['biko']
    
    db.session.commit()
    
    return jsonify({'message': 'データが更新されました'}), 200

@app.route('/admin_tenken/delete/<int:id>', methods=['DELETE'])
def delete_tenken(id):
    tenken = Tenken.query.get(id)
    if tenken is None:
        return jsonify({'message': 'データが見つかりません'}), 404
    
    db.session.delete(tenken)
    db.session.commit()
    
    return jsonify({'message': 'データが削除されました'}), 200


@app.route('/admin_tenken')
def admin_tenken():
    return render_template('admin_tenken.html')

##tenkenテーブルここまで
##




##
##コンプレッサー点検テーブルここから
@app.route('/admin_comp_data', methods=['GET'])
def get_comp_data_admin():

    comps = Comp_tenken.query.all()
    # データをリストに変換
    data = []
    for tenkencomp in comps:
        data.append({
            'id': tenkencomp.id,
            'inspection_id': tenkencomp.inspection_id,
            'machine_no': tenkencomp.machine_no,
            'tenken_person': tenkencomp.tenken_person,
            'tenken_c1': tenkencomp.c1,
            'tenken_c2': tenkencomp.c2,
            'tenken_c3': tenkencomp.c3,
            'tenken_date': tenkencomp.tenken_date.strftime('%Y-%m-%d %H:%M:%S'),  # 日付フォーマット
            'biko': tenkencomp.biko
        })
    return jsonify({"data": data})  # {"data": data}の形に変更

@app.route('/admin_tenkencomp/get/<int:id>', methods=['GET'])
def get_tenkencomp(id):
    # IDに基づいてデータを取得する処理
    tenkencomp = db.session.query(Comp_tenken).get(id)
    if tenkencomp:
        return jsonify({
            'id': tenkencomp.id,
            'inspection_id': tenkencomp.inspection_id,
            'machine_no': tenkencomp.machine_no,
            'tenken_person': tenkencomp.tenken_person,
            'tenken_c1': tenkencomp.c1,
            'tenken_c2': tenkencomp.c2,
            'tenken_c3': tenkencomp.c3,
            'tenken_date': tenkencomp.tenken_date.strftime('%Y-%m-%d %H:%M:%S'),  # 日付フォーマット
            'biko': tenkencomp.biko
        })
    return jsonify({'error': 'Tenken not found'}), 404

@app.route('/admin_comp/update/<int:id>', methods=['POST'])
def update_tenkencomp(id):
    data = request.get_json()
    
    # 既存のデータを取得
    tenkencomp = Comp_tenken.query.get(id)
    if tenkencomp is None:
        return jsonify({'message': 'データが見つかりません'}), 404
    
    # データを更新
    #tenkencomp.inspection_id = data['inspection_id']
    tenkencomp.machine_no = data['machine_no']
    tenkencomp.tenken_person = data['tenken_person']
    tenkencomp.tenken_date = data['tenken_date']
    tenkencomp.c1 = data['tenken_c1']
    tenkencomp.c2 = data['tenken_c2']
    tenkencomp.c3 = data['tenken_c3']
    tenkencomp.biko = data['biko']
    
    db.session.commit()
    
    return jsonify({'message': 'データが更新されました'}), 200

@app.route('/admin_tenkencomp/delete/<int:id>', methods=['DELETE'])
def delete_tenkencomp(id):
    tenkencomp = Comp_tenken.query.get(id)
    if tenkencomp is None:
        return jsonify({'message': 'データが見つかりません'}), 404
    
    db.session.delete(tenkencomp)
    db.session.commit()
    
    return jsonify({'message': 'データが削除されました'}), 200

@app.route('/admin_tenkencomp')
def admin_tenkencomp():
    return render_template('admin_tenkencomp.html')

##コンプレッサー点検テーブルここまで
##





##
##点検リストテーブルここから
#点検リスト インデックスページルーティング
@app.route('/admin_list_index/')
def admin_list_index():

    try:
        # koutei_tblテーブルから工程名を取得
        koutei_list = Koutei.query.all()  # 全ての工程を取得
        return render_template('admin_list_index.html', processes=koutei_list)
    
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。")


#点検リスト 各工程ページ エンドポイント
@app.route('/admin_list_koutei/<int:id>')
def admin_list_koutei_page(id):
    
    # idとクラスを辞書で対応付け
    setubi_classes = {
        1: Nct,
        2: Baritori,
        3: Press,
        4: Tap,
        5: Bender,
        6: Spot,
        7: Weld,
        8: Kensa,
        9: Syukka,
        10: Compressor_setubi
    }
    
    try:
        # Kouteiデータの取得
        koutei_id = Koutei.query.get_or_404(id)

        # idに対応するクラスを取得
        setubi_class = setubi_classes.get(id)

        if setubi_class is None:
            abort(404, description="無効なIDです。")
        
        # 対応するクラスからデータを取得
        setubi_list = setubi_class.query.all()
            
        return render_template("admin_list_koutei.html", koutei=koutei_id,setubi_list=setubi_list)
    
    except NoResultFound:
        abort(404, description="対象のデータが見つかりませんでした。")
    except SQLAlchemyError:
        abort(500, description="データベースエラーが発生しました。（トップ）")


@app.route('/admin_list_detail/<int:koutei_id>/<int:setubi_id>', methods=['GET', 'POST'])
def admin_list_page(koutei_id, setubi_id):
    
    try:
        htmlpage = 'admin_list_detail.html' #デフォルト
        koutei = Koutei.query.get_or_404(koutei_id)  # 工程名の取得
        
        if koutei_id == 1: #NCT
            setubi = Nct.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 2: #バリ取り
            setubi = Baritori.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 3: #プレス
            setubi = Press.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 4: #タップ            
            setubi = Tap.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 5: #ベンダー            
            setubi = Bender.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 6: #スポット
            setubi = Spot.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 7: #溶接
            setubi = Weld.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 8: #検査
            setubi = Kensa.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)          
        elif koutei_id == 9: #出荷
            setubi = Syukka.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
            if str(setubi.id) == "3": #フォークリフトの時
                tenken_model = Forklift_model.query.get_or_404(1)                        
        elif koutei_id == 10: #コンプレッサー
            setubi = Compressor_setubi.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
            if str(setubi.id) == "1": #コンプレッサー
                setubi = Compressor_setubi.query.get_or_404(setubi_id)
                tenken_list = get_tenken_data(koutei, setubi)
                
        #表示
        if koutei_id == 9 and setubi_id == 3: #フォークリフトの時
            return render_template(htmlpage,koutei=koutei, setubi=setubi, tenken_list=tenken_list,tenken_model=tenken_model)
        
        else: #他
            return render_template(htmlpage,koutei=koutei, setubi=setubi, tenken_list=tenken_list)
    
    
    #get_or_404を使う場合はNoResultFoundは不要
    except SQLAlchemyError:
       abort(500, description="データベースエラーが発生しました。（設備）")

#点検リストデータを取得
@app.route('/get_list_detail_data/<int:koutei_id>/<int:setubi_id>/', methods=['GET'])
def get_list_data(koutei_id, setubi_id):
    try:
        koutei = Koutei.query.get_or_404(koutei_id)  # 工程名の取得
        
        if koutei_id == 1: #NCT
            setubi = Nct.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 2: #バリ取り
            setubi = Baritori.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 3: #プレス
            setubi = Press.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 4: #タップ            
            setubi = Tap.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 5: #ベンダー            
            setubi = Bender.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 6: #スポット
            setubi = Spot.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 7: #溶接
            setubi = Weld.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
        elif koutei_id == 8: #検査
            setubi = Kensa.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)          
        elif koutei_id == 9: #出荷
            setubi = Syukka.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
            if str(setubi.id) == "3": #フォークリフトの時
                tenken_model = Forklift_model.query.get_or_404(1)                        
        elif koutei_id == 10: #コンプレッサー
            setubi = Compressor_setubi.query.get_or_404(setubi_id)
            tenken_list = get_tenken_data(koutei, setubi)
            if str(setubi.id) == "1": #コンプレッサー
                setubi = Compressor_setubi.query.get_or_404(setubi_id)
                tenken_list = get_tenken_data(koutei, setubi)    
        
        # 詳細情報を返す
        data = [{
            "id": item.id,
            "tenken_list": item.tenken_list,
            "contents": item.contents
            } 
            for item in tenken_list
        ]
        
        return jsonify(data)
    
    except SQLAlchemyError:
        return jsonify({'error': 'データ取得エラー'}), 500


#点検リスト編集(UPDATE)
@app.route('/update_list_detail_data/<int:koutei_id>/<int:setubi_id>/<int:id>/', methods=['PUT'])
def update_list_data(koutei_id, setubi_id, id):
    koutei = Koutei.query.get_or_404(koutei_id)  # 工程名の取得
 
    # setubi に基づいて、対応するセットの情報を取得
    if koutei_id == 1:  # NCT
        setubi = Nct.query.get_or_404(setubi_id)
    elif koutei_id == 2:  # バリ取り
        setubi = Baritori.query.get_or_404(setubi_id)
    elif koutei_id == 3:  # プレス
        setubi = Press.query.get_or_404(setubi_id)
    elif koutei_id == 4:  # タップ
        setubi = Tap.query.get_or_404(setubi_id)
    elif koutei_id == 5:  # ベンダー
        setubi = Bender.query.get_or_404(setubi_id)
    elif koutei_id == 6:  # スポット
        setubi = Spot.query.get_or_404(setubi_id)
    elif koutei_id == 7:  # 溶接
        setubi = Weld.query.get_or_404(setubi_id)
    elif koutei_id == 8:  # 検査
        setubi = Kensa.query.get_or_404(setubi_id)
    elif koutei_id == 9:  # 出荷
        setubi = Syukka.query.get_or_404(setubi_id)
    elif koutei_id == 10:  # コンプレッサー
        setubi = Compressor_setubi.query.get_or_404(setubi_id)
    
    # tenken_list を取得
    tenken_list = get_tenken_data(koutei, setubi)
    
    # 編集の場合
    data = request.json
    item_to_update = next((item for item in tenken_list if item.id == id), None)
    
    if item_to_update:
        if 'tenken_list' in data:
            item_to_update.tenken_list = data['tenken_list']
        if 'contents' in data:
            item_to_update.contents = data['contents']
        
        # 更新後にDBにコミット
        db.session.commit()
        
        return jsonify({"message": "更新成功"})
    else:
        return jsonify({"error": "IDに該当するデータが見つかりません"}), 404


# 点検リスト削除 (DELETE)
@app.route('/delete_tenkenlist/<int:koutei_id>/<int:setubi_id>/<int:id>/', methods=['DELETE'])
def delete_tenkenlist(koutei_id, setubi_id, id):
    
    koutei = Koutei.query.get_or_404(koutei_id)  # 工程名の取得
    
    # setubi に基づいて、対応するセットの情報を取得
    if koutei_id == 1:  # NCT
        setubi = Nct.query.get_or_404(setubi_id)
    elif koutei_id == 2:  # バリ取り
        setubi = Baritori.query.get_or_404(setubi_id)
    elif koutei_id == 3:  # プレス
        setubi = Press.query.get_or_404(setubi_id)
    elif koutei_id == 4:  # タップ
        setubi = Tap.query.get_or_404(setubi_id)
    elif koutei_id == 5:  # ベンダー
        setubi = Bender.query.get_or_404(setubi_id)
    elif koutei_id == 6:  # スポット
        setubi = Spot.query.get_or_404(setubi_id)
    elif koutei_id == 7:  # 溶接
        setubi = Weld.query.get_or_404(setubi_id)
    elif koutei_id == 8:  # 検査
        setubi = Kensa.query.get_or_404(setubi_id)
    elif koutei_id == 9:  # 出荷
        setubi = Syukka.query.get_or_404(setubi_id)
    elif koutei_id == 10:  # コンプレッサー
        setubi = Compressor_setubi.query.get_or_404(setubi_id)
        
    # tenken_list を取得
    tenken_list = get_tenken_data(koutei, setubi)
    
    # 編集の場合
    item_to_delete = next((item for item in tenken_list if item.id == id), None)
    
    if item_to_delete is None:
        return jsonify({"error": "該当する点検リストが見つかりませんでした"}), 404
    
    try:
        # データベースから削除
        db.session.delete(item_to_delete)
        db.session.commit()
        return jsonify({"message": "削除成功"})
    except Exception as e:
        db.session.rollback()  # 失敗時にはロールバック
        return jsonify({"error": f"削除失敗: {str(e)}"}), 500
    
#点検リスト 追加 (ADD)エンドポイント
@app.route('/add_list_detail_data/<int:koutei_id>/<int:setubi_id>/', methods=['POST'])
def add_list_detail_data(koutei_id, setubi_id):
    
    model_mapping = {
        1: {  # NCT
            1: Acies,
            2: Em,
            3: C1,
            4: Compressor,
        },
        2: {  # バリ取り
            1: Esthe,
        },
        3: {  # プレス
            1: Cdstud,
            2: Gunman,
            3: Highspin,
            4: Highspin,
            5: Heager,
            6: Press25t45t,
            7: Press25t45t,
            8:Shirring,
            9:Arcstud,
        },
        4: {  # タップ
            1: Tap1,
            2: Tap1,
            3: Cts1,
            4: Cts1,
        },
        5: {  # ベンダー
            1: Rg,
            2: Rg,
            3: Rg,
            4: Rg,
            5: Hds,
            6: Hg,
            7: Hg,
            8: Atc,
            9: Astro,
            10: Egb,
            11: Egar,
        },
        6: {  # スポット
            1: Spotweld,
            2: Spotweld,
            3: Spotweld,
            4: Spotweld,
            5: Spotweld,
            6: Myspot,
            7: Myspot,
            8: Myspot,
        },
        7: {  # 溶接
            1: Weld1,
            2: Weld1,
            3: Weld1,
            4: Weld1,
            5: Weld1,
            6: Weld1,
            7: Weld1,
            8: Weld1,
            9: Weld1,
            10: Weld1,
            11: Weld1,
            12: Weld1,
            13: Weld1,
            14: Weld1,
            15: Weld1,
            16: Weld_Robot,
            17: Weld_Robot,
            18: Fiver_Hand,
            19: AlufaJULIA,
        },
        8: {  # 検査
            1: Digital_nogisu,
            2: Digital_nogisu,
            3: Digital_nogisu,
            4: Digital_nogisu,
            5: Digital_nogisu,
            6: Digital_nogisu,
            7: Digital_nogisu,
            8: Digital_nogisu,
            9: Digital_nogisu,
            10: Digital_nogisu,
            11: Digital_nogisu,
            12: Digital_nogisu,
            13: Digital_nogisu,
            14: Digital_nogisu,
            15: Digital_nogisu,
            16: Keyence,
            17: Digital_nogisu,
            18: Analog_nogisu,
            19: Analog_nogisu,
            20: Digital_nogisu,
            21: Digital_nogisu,
        },
        9: {  # 出荷
            1: Senjyoki,
            2: Senjyoki_monthly,
            3: Forklift,
        },
        10: {  # コンプレッサー
            1: Comp_list,  # 設備1
            #3: Comp_test_list,  # 設備2
        },
    }
    
    data = request.json #ブラウザのデータ取得
    if not data:
        return jsonify({"error": "No data provided"}), 400

    model_class = model_mapping.get(koutei_id, {}).get(setubi_id) #モデルクラス②マッピングして適切な点検リストを取得
    if not model_class:
        return jsonify({"error": "Invalid koutei_id or setubi_id"}), 400

    new_tenken = model_class(
        tenken_list=data.get('tenken_list', ''),
        contents=data.get('contents', '')
    )

    db.session.add(new_tenken)
    db.session.commit()

    return jsonify({"message": "Tenken list added successfully"}), 201
    
##点検リストテーブルここまで
##






##
#閲覧のみ　コンプレッサー　スケジュールここから 
#エンドポイントを作成
@app.route('/compressor_mail_data', methods=['GET'])
def get_compressor_mail_data():
    # データベースからすべてのレコードを取得
    compressor_mails = Email_schedule.query.all()

    
    # レコードを辞書型に変換して返す
    email_data = [
        {
            'id': record.id,
            'busyo': record.busyo,
            'name': record.name,
            'work_start_date': record.work_start_date.strftime('%Y-%m-%d') if record.work_start_date else None,  # 日付があればフォーマット、なければNone
            'work_end_date': record.work_end_date.strftime('%Y-%m-%d') if record.work_end_date else None,  # 日付があればフォーマット、なければNone
            'last_mail_send_date': record.last_mail_send_date.strftime('%Y-%m-%d %H:%M:%S') if record.last_mail_send_date else None,  # 同じく
            'biko': record.biko,
        }
        for record in compressor_mails
    ]
    
    # Comp_tenkenのデータ取得
    compressor_tenken = Comp_tenken.query.all()
    tenken_data = [
        {
            'id': record.id,
            'inspection_id': record.inspection_id,
            'setubi_name': record.setubi_name,
            'machine_no': record.machine_no,
            'c1': record.c1,
            'c2': record.c2,
            'c3': record.c3,
            'c4': record.c4,
            'c5': record.c5,
            'c6': record.c6,
            'c7': record.c7,
            'c8': record.c8,
            'c9': record.c9,
            'c10': record.c10,
            'c11': record.c11,
            'c12': record.c12,
            'c13': record.c13,
            'c14': record.c14,
            'c15': record.c15,
            'c16': record.c16,
            'c17': record.c17,
            'c18': record.c18,
            'c19': record.c19,
            'c20': record.c20,
            'c21': record.c21,
            'c22': record.c22,
            'c23': record.c23,
            'c24': record.c24,
            'c25': record.c25,
            'c26': record.c26,
            'main_work': record.main_work,
            'tenken_date': record.tenken_date.strftime('%Y-%m-%d %H:%M:%S') if record.tenken_date else None,
            'tenken_busyo': record.tenken_busyo,
            'tenken_person': record.tenken_person,
            'biko': record.biko,
            'is_completed': getattr(record, 'is_completed', False)  # もし追加済みなら
        }
        for record in compressor_tenken
    ]
    
     # まとめて返す
    return jsonify({
        'email_schedules': email_data,
        'comp_tenken': tenken_data
    })

#Flaskアプリケーションのルーティング
@app.route('/compressor_mail')
def compressor_mail():
    return render_template('compressor_mail.html')

#閲覧のみ　コンプレッサー　スケジュールここまで
##
