#coding: UTF-8
import glob
import csv
import shutil
import os
import pandas as pd
from datetime import datetime

b_ken_dict = {}

def create_a_sub_list(prev_time, a_reader_2, a_sub_list):
    if a_sub_list is None:
        a_sub_list = []
    else:
        a_sub_list = a_sub_list[-1:]
    for a_row in a_reader_2:
        if a_row[0] == prev_time:
            a_sub_list.append(a_row)
        else:
            a_sub_list.append(a_row)
            return a_sub_list
    return a_sub_list

def write_csv_1(a_csv, prefecture_name, new_csv):
    global b_ken_dict
    prev = 0
    # j= file_count

    a_csvfile = open(a_csv, 'r')
    a_reader = csv.reader(a_csvfile)
    next(a_reader) # Skipping the header
    a_csvfile_2 = open(a_csv, 'r')
    a_reader_2 = csv.reader(a_csvfile_2)
    next(a_reader_2) # Skipping the header

    b_csv = "./納品/計測地点番号/{prefecture_name}.csv"
    b_csv = b_ken_dict[prefecture_name]
    b_csvfile = open(b_csv, 'r')
    b_reader = csv.reader(b_csvfile)
    next(b_reader) # Skipping the header

    out = []
    b_dict = {}
    b_dict_full = {}
    exception_list = {}

    header_row = ["情報源コード", "計測地点番号", "計測地点名", "2次メッシュコード", "交通管理リンク番号", "経度", "緯度", "時刻", "断面交通量", "摘要", "最寄り幹線道路平行1_情報源コード", "最寄り幹線道路平行1_計測地点番号", "最寄り幹線道路平行1_計測地点名", "最寄り幹線道路平行1_2次メッシュコード", "最寄り幹線道路平行1_交通管理リンク番号", "最寄り幹線道路平行1_緯度", "最寄り幹線道路平行1_経度", "最寄り幹線道路平行1_接続タイプ", "最寄り幹線道路平行1_車線数", "最寄り幹線道路平行1_断面交通量", "最寄り幹線道路平行1_市区町村道との距離", "最寄り幹線道路平行1_摘要", "最寄り幹線道路平行2_情報源コード", "最寄り幹線道路平行2_計測地点番号", "最寄り幹線道路平行2_計測地点名", "最寄り幹線道路平行2_2次メッシュコード", "最寄り幹線道路平行2_交通管理リンク番号", "最寄り幹線道路平行2_緯度", "最寄り幹線道路平行2_経度","最寄り幹線道路平行2_接続タイプ", "最寄り幹線道路平行2_車線数", "最寄り幹線道路平行2_断面交通量", "最寄り幹線道路平行2_市区町村道との距離", "最寄り幹線道路平行2_摘要", "最寄り幹線道路直行1_情報源コード", "最寄り幹線道路直行1_計測地点番号", "最寄り幹線道路直行1_計測地点名", "最寄り幹線道路直行1_2次メッシュコード", "最寄り幹線道路直行1_交通管理リンク番号", "最寄り幹線道路直行1_緯度", "最寄り幹線道路直行1_経度","最寄り幹線道路直行1_接続タイプ", "最寄り幹線道路直行1_車線数", "最寄り幹線道路直行1_断面交通量", "最寄り幹線道路直行1_市区町村道との距離", "最寄り幹線道路直行1_摘要", "最寄り幹線道路直行2_情報源コード", "最寄り幹線道路直行2_計測地点番号", "最寄り幹線道路直行2_計測地点名", "最寄り幹線道路直行2_2次メッシュコード", "最寄り幹線道路直行2_交通管理リンク番号", "最寄り幹線道路直行2_緯度", "最寄り幹線道路直行2_経度","最寄り幹線道路直行2_接続タイプ", "最寄り幹線道路直行2_車線数", "最寄り幹線道路直行2_断面交通量", "最寄り幹線道路直行2_市区町村道との距離", "最寄り幹線道路直行2_摘要"]
    # Reading B
    for b_row in b_reader:
        if "市町村道" in b_row:
            b_dict[b_row[1]] = b_row[0:25]
            b_dict_full[b_row[1]] = b_row[0:25]
        else:
            b_dict_full[b_row[1]] = b_row[0:25]
    time_untill_now = 0
    prev_time = None
    a_sub_list = None
    # Reading A
    for i, a_row in enumerate(a_reader):
        if a_row[0] != prev_time:
            prev_time = a_row[0]
            print(prefecture_name, prev_time)
            a_sub_list = create_a_sub_list(prev_time, a_reader_2, a_sub_list)
        if a_row[2] in b_dict:
            try:
                b_row = b_dict[a_row[2]].copy()
                temp_b_row = b_row
                #2017/07
                # temp_b_row += [a_row[0], "", a_row[6]]
                #2017/08以降
                temp_b_row += [a_row[0], a_row[6], a_row[7]]
                if len(temp_b_row[8]) > 0: # If we have I column
                    temp_b_i_row = b_dict_full[temp_b_row[8]] 
                    temp_b_row += [temp_b_i_row[0] , temp_b_i_row[2], temp_b_i_row[3], temp_b_i_row[4], temp_b_i_row[5], temp_b_i_row[6], temp_b_i_row[24]]
                    temp_a_sub_val = ""
                    for a_sub_row in a_sub_list:
                        if a_sub_row[2]==temp_b_row[8]:
                            temp_a_sub_val = a_sub_row[6]
                            break
                    temp_b_row += [temp_a_sub_val]
                else:
                    temp_b_row += ["", "", "", "", "", "", "", ""]

                if len(temp_b_row[12]) > 0:
                    temp_b_i_row = b_dict_full[temp_b_row[12]] 
                    temp_b_row += [temp_b_i_row[0] , temp_b_i_row[2], temp_b_i_row[3], temp_b_i_row[4], temp_b_i_row[5], temp_b_i_row[6], temp_b_i_row[24]]
                    temp_a_sub_val = ""
                    for a_sub_row in a_sub_list:
                        if a_sub_row[2]==temp_b_row[12]:
                            temp_a_sub_val = a_sub_row[6]
                            break
                    temp_b_row += [temp_a_sub_val]
                else:
                    temp_b_row += ["", "", "", "", "", "", "", ""]

                if len(temp_b_row[16]) > 0:
                    temp_b_i_row = b_dict_full[temp_b_row[16]] 
                    temp_b_row += [temp_b_i_row[0] , temp_b_i_row[2], temp_b_i_row[3], temp_b_i_row[4], temp_b_i_row[5], temp_b_i_row[6], temp_b_i_row[24]]
                    temp_a_sub_val = ""
                    for a_sub_row in a_sub_list:
                        if a_sub_row[2]==temp_b_row[16]:
                            temp_a_sub_val = a_sub_row[6]
                            break
                    temp_b_row += [temp_a_sub_val]
                else:
                    temp_b_row += ["", "", "", "", "", "", "", ""]

                if len(temp_b_row[20]) > 0:
                    temp_b_i_row = b_dict_full[temp_b_row[20]] 
                    temp_b_row += [temp_b_i_row[0] , temp_b_i_row[2], temp_b_i_row[3], temp_b_i_row[4], temp_b_i_row[5], temp_b_i_row[6], temp_b_i_row[24]]
                    temp_a_sub_val = ""
                    for a_sub_row in a_sub_list:
                        if a_sub_row[2]==temp_b_row[20]:
                            temp_a_sub_val = a_sub_row[6]
                            break
                    temp_b_row += [temp_a_sub_val]
                else:
                    temp_b_row += ["", "", "", "", "", "", "", ""]

                temp_b_row_2 = [temp_b_row[0], temp_b_row[1], temp_b_row[2], temp_b_row[3], temp_b_row[4], temp_b_row[5], temp_b_row[6], temp_b_row[25], temp_b_row[27], temp_b_row[24]]
                parallel_1= [temp_b_row[28], temp_b_row[8], temp_b_row[29], temp_b_row[30], temp_b_row[31], temp_b_row[32], temp_b_row[33], temp_b_row[11], temp_b_row[10], temp_b_row[35], temp_b_row[9], temp_b_row[34]]
                parallel_2 = [temp_b_row[36], temp_b_row[12], temp_b_row[37], temp_b_row[38], temp_b_row[39], temp_b_row[40], temp_b_row[41], temp_b_row[15], temp_b_row[14], temp_b_row[43], temp_b_row[13], temp_b_row[42]]      
                straight_1 = [temp_b_row[44], temp_b_row[16], temp_b_row[45], temp_b_row[46], temp_b_row[47], temp_b_row[48], temp_b_row[49], temp_b_row[19], temp_b_row[18], temp_b_row[51], temp_b_row[17], temp_b_row[50]]
                straight_2 = [temp_b_row[52], temp_b_row[20], temp_b_row[53], temp_b_row[54], temp_b_row[55], temp_b_row[56], temp_b_row[57], temp_b_row[23], temp_b_row[22], temp_b_row[59], temp_b_row[21], temp_b_row[58]]
                temp_b_row_2 += parallel_1 + parallel_2 + straight_1 + straight_2
                out.append(temp_b_row_2)
                
            except Exception as e:
                print(e)
                exception_list[a_row[2]]=1
                
    print(exception_list)
    # Create output files
    new_csvfile = open(new_csv + ".csv", 'w', newline="")
    writer = csv.writer(new_csvfile)
    writer.writerow(header_row)
    writer.writerows(out)
    new_csvfile.close()
    
year_list = ["2017","2018","2019","2020"]
month_list = ["01","02","03","04","05","06","07","08","09","10","11","12"]
in_list = ["愛知県警", "愛媛県警", "茨城県警", "岡山県警", "沖縄県警", "岩手県警","岐阜県警", "宮崎県警", "宮城県警", "京都府警", "熊本県警", "群馬県警", "警視庁", "広島県警", "香川県警", "高知県警", "佐賀県警","埼玉県警","三重県警", "山形県警", "山口県警", "山梨県警", "滋賀県警", "鹿児島県警","秋田県警", "新潟県警", "神奈川県警", "青森県警", "静岡県警", "石川県警","千葉県警", "大阪府警", "大分県警", "長崎県警", "長野県警", "鳥取県警", "島根県警", "徳島県警", "栃木県警", "奈良県警", "富山県警", "福井県警", "福岡県警", "福島県警", "兵庫県警", "北海道警（旭川方面）", "北海道警（釧路方面）", "北海道警（札幌方面）", "北海道警（函館方面）", "北海道警（北見方面）", "和歌山県警"]

ken_list = ["愛知", "愛媛", "茨城", "岡山", "沖縄", "岩手", "岐阜", "宮崎", "宮城", "京都", "熊本", "群馬", "警視庁", "広島", "香川", "高知", "佐賀", "埼玉","三重", "山形", "山口", "山梨", "滋賀", "鹿児島", "秋田", "新潟", "神奈川", "青森", "静岡", "石川", "千葉", "大阪", "大分", "長崎", "長野", "鳥取", "島根", "徳島", "栃木", "奈良", "富山", "福井", "福岡", "福島", "兵庫", "旭川", "釧路", "札幌","函館", "北見", "和歌山"]

b_ken_dict = {}

def master():
    for year in year_list:
        for month in month_list:
            for i, input_file in enumerate(in_list):
                prefecture_name = ken_list[i]

                if os.path.isdir("./納品/納品/" + prefecture_name):
                    pass
                else:
                    os.mkdir("./納品/納品/" + prefecture_name)
            
                #201701
                if os.path.isdir("./納品/" + year + "年" + "/" + year + month):
                    time_dir = glob.glob("./納品/" + year + "年" + "/" + year + month + "/*")
                    for file in time_dir:
                        #三重県警_201701.csv
                        if input_file in file and ".csv" in file:
                            a_csv = file
                            out_csv = "./納品/納品/" + prefecture_name + "/" + prefecture_name + "_" + year + month + ".csv"
                            
                            out_csv_temp = out_csv + ".csv"
                            if os.path.exists(out_csv_temp):
                                pass
                            else:
                                write_csv_1(a_csv, prefecture_name, out_csv)
                        elif input_file in file:
                            #神奈川県警_201701
                            if os.path.isdir("./納品/" + year + "年" + "/" + year + month + "/" + input_file + "_" + year + month):
                                a_dir = glob.glob("./納品/" + year + "年" + "/" + year + month + "/" + input_file + "_" + year + month + "/*")

                                #merge the csv if it's separated
                                merge_list = []
                                for a_file in a_dir:
                                    #神奈川県警_20170101-15.csv, 神奈川県警_20170116-31.csv
                                    if ".csv" in a_file:
                                        a_csv = a_file
                                        out_csv = "./納品/納品/" + prefecture_name + "/" + prefecture_name + "_" + year + month + ".csv"

                                        out_csv_temp = out_csv + ".csv"
                                        if os.path.exists(out_csv_temp):
                                            pass
                                        else:
                                            write_csv_1(a_csv, prefecture_name, out_csv)

def create_b_ken_dict():
    global b_ken_dict, ken_list
    b_ken = glob.glob("./納品/計測地点番号/*")
    for file in b_ken:
        for ken_name in ken_list:
            if ken_name in file:
                b_ken_dict[ken_name] = file.replace("\\", "/")
                break
    return b_ken_dict

create_b_ken_dict()
start_time = datetime.now()
master()
print("Start", start_time)
print("Finish", datetime.now())