import threading
import webbrowser
from wsgiref.simple_server import make_server
import random
import sys
import os
import numpy as np
import csv

path1 = r"D:\Finish\BBQ"  # 當前上一層目錄的絕對路徑，os.path.abspath('..')  AI對打
sys.path.insert(1, path1)
import BBQ

FILE = r"D:\Finish\HighTwo\welcome.html" """記得改回原本的路徑"""
PORT = 8080
BBQ = BBQ.BBQ()
action = 0
data = []#AI對AI的動作


def request(environ, start_response):
    #寫AI對AI的紀錄資料
    file = open(r'D:\record.csv',mode='a+', newline='')
    writer = csv.writer(file)

    global data

    if environ["REQUEST_METHOD"] == "POST":
        try:
            request_body_size = int(environ["CONTENT_LENGTH"])
            request_body = environ["wsgi.input"].read(request_body_size)
            input = tokensplit(request_body)
            type = input.pop(0)
            type = type.replace("type=", "")
            print(type)
            if type == "predict":
                print("---input---")
                input = [int(x) for x in input]
                who = input[14]
                input = input[0:14]
                print("html input :", input)
                if who:
                    print("who : RF")
                    if input[7] == 0:
                        print("---第一階段")
                        hand1 = int(float(input[5]))
                        hand2 = int(float(input[6]))
                        level = BBQ.set_hands_level(hand1, hand2)
                        input[7] = level
                        print("level: ", level)
                        if level == 5:
                            if random.randrange(1, 100, 1) >= 40:  # true / false
                                output = action_predict_RF(input)
                                data.append('RF '+str(output[0]))
                            else:
                                output = [8, -1]
                                data.append('RF fold')
                                data.append('CNN win')
                                writer.writerow(data)
                                data = []

                        elif level == 4:
                            if random.randrange(1, 100, 1) >= 35:
                                output = action_predict_RF(input)
                                data.append('RF '+str(output[0]))
                            else:
                                output = [8, -1]
                                data.append('RF fold')
                                data.append('CNN win')
                                writer.writerow(data)
                                data = []
                        elif level == 3:
                            if random.randrange(1, 100, 1) >= 25:
                                output = action_predict_RF(input)
                                data.append('RF '+str(output[0]))
                            else:
                                output = [8, -1]
                                data.append('RF fold')
                                data.append('CNN win')
                                writer.writerow(data)
                                data = []
                        elif level == 2:
                            if random.randrange(1, 100, 1) >= 10:
                                output = action_predict_RF(input)
                                data.append('RF '+str(output[0]))
                            else:
                                output = [8, -1]
                                data.append('RF fold')
                                data.append('CNN win')
                                writer.writerow(data)
                                data = []
                        else:
                            output = action_predict_RF(input)
                            data.append('RF '+str(output[0]))
                        output.append(level)
                    else:
                        print("---第二階段")
                        output = action_predict_RF(input)
                        data.append('RF '+str(output[0]))
                else:
                    print("who : CNN")
                    if input[7] == 0:  # 第一階段
                        global action
                        action = 0
                        print("----------------------------------------------第一階段")
                        hand1 = int(float(input[5]))
                        hand2 = int(float(input[6]))
                        level = BBQ.set_hands_level(hand1, hand2)
                        input[7] = level
                        print("level: ", level)
                        if level == 5:
                            if input[9] > 1500:
                                if random.randrange(1, 100, 1) >= 80:  # true / false
                                    output = action_predict(input)
                                    data.append('CNN '+str(output[0]))
                                else:
                                    output = [8, -1]
                                    data.append('CNN fold')
                                    data.append('RF win')
                                    writer.writerow(data)
                                    data = []
                            else:
                                if random.randrange(1, 100, 1) >= 40:  # true / false
                                    output = action_predict(input)
                                    data.append('CNN '+str(output[0]))
                                else:
                                    output = [8, -1]
                                    data.append('CNN fold')
                                    data.append('RF win')
                                    writer.writerow(data)
                                    data = []
                        elif level == 4:
                            if input[9] > 1500:
                                if random.randrange(1, 100, 1) >= 70:  # true / false
                                    output = action_predict(input)
                                    data.append('CNN '+str(output[0]))
                                else:
                                    output = [8, -1]
                                    data.append('CNN fold')
                                    data.append('RF win')
                                    writer.writerow(data)
                                    data = []
                            else:
                                if random.randrange(1, 100, 1) >= 35:  # true / false
                                    output = action_predict(input)
                                    data.append('CNN '+str(output[0]))
                                else:
                                    output = [8, -1]
                                    data.append('CNN fold')
                                    data.append('RF win')
                                    writer.writerow(data)
                                    data = []
                        elif level == 3:
                            if random.randrange(1, 100, 1) >= 25:
                                output = action_predict(input)
                                data.append('CNN '+str(output[0]))
                            else:
                                output = [8, -1]
                                data.append('CNN fold')
                                data.append('RF win')
                                writer.writerow(data)
                                data = []
                        elif level == 2:
                            if random.randrange(1, 100, 1) >= 10:
                                output = action_predict(input)
                                data.append('CNN '+str(output[0]))
                            else:
                                output = [8, -1]
                                data.append('CNN fold')
                                data.append('RF win')
                                writer.writerow(data)
                                data = []
                        else:
                            output = action_predict(input)
                            data.append('CNN '+str(output[0]))
                        output.append(level)
                    else:  # 第二階段
                        print("----------------------------------------------第二階段")
                        output = abandon(input)
                        data.append('CNN '+str(output[0]))
                        if output[0] == 8:
                            data = []

                # print(input)
                print("---output---")
                print(output)
                print(data)
            elif type == "hands":
                print("hands_strength")
                player = input[:2] + input[4:]
                print("CNN: ", input[2:])
                print("RF: ", player)
                player_strength = hand_strength(player)
                computer = input[2:]
                computer_strength = hand_strength(computer)
                print("RF_strength :", player_strength)
                print("CNN_strength :", computer_strength)
                for i in range(len(player_strength)):
                    if player_strength[i] > computer_strength[i]:
                        output = 0
                        data.append('RF win')
                        break
                    elif player_strength[i] < computer_strength[i]:
                        output = 1
                        data.append('CNN win')
                        break
                    elif player_strength[i] == computer_strength[i]:
                        output = 2
                        continue
                if output == 2:
                    data.append('平')
                print(output)

                writer.writerow(data) #寫入csv
                data = [] #初始
            else:
                print("unknown type")
                output = type
        except (TypeError, ValueError):
            request_body = "0"
        try:
            response_body = str(output)
        except:
            response_body = "error"
        status = "200 OK"
        headers = [("Content-type", "text/plain")]
        start_response(status, headers)
        return [response_body.encode()]
    else:
        response_body = open(FILE).read()
        status = "200 OK"
        headers = [
            ("Content-type", "text/html"),
            ("Content-Length", str(len(response_body))),
        ]
        start_response(status, headers)
        return [response_body.encode()]


def open_browser():
    """Start a browser after waiting for half a second."""

    def _open_browser():
        webbrowser.open(FILE)

    thread = threading.Timer(0.5, _open_browser)
    thread.start()


def start_server():
    """Start the server."""
    print("start the server....")
    httpd = make_server("127.0.0.1", PORT, request)
    httpd.serve_forever()


def tokensplit(input):
    input = str(input)
    input = input.replace(r"b'", "")
    input = input.replace(r"'", "")
    input = input.replace(r"input%5B%5D=", "")
    token = input.split("&")
    return token


def abandon(input):  # 包含棄牌與all-in

    output = []
    new_input = []
    global action
    # type 0高牌 1一對 3三條 2兩對 4順子 5同花 6葫蘆 7鐵支 8同花順 9同順缺1 10同花缺1 11同花缺2 12順缺1
    # 順序大小0 < 1 < 3 < 2 < 4 < 5 < 6 < 7 < 8
    for i in range(0, len(input)):
        if i <= 9:
            if i == 8 or i == 9:
                new_input.append((input[i] / input[12]))
            else:
                new_input.append(input[i])
        elif (i % 3) == 1 and input[i] == -1:
            break
        elif (i % 3) == 0 and input[i] != -1:
            new_input.append((input[i] / input[12]))
        else:
            new_input.append(input[i])

    strength = BBQ.check_strength(new_input[0:7])[0]  # 牌型判斷參數
    print("strength: ", strength)

    if strength == 0:  # 高牌
        if input[8] <= (input[9] - input[8]) / 6:  # 3倍底池
            if random.randrange(1, 100, 1) >= 30:
                output = action_predict(input)
            else:
                output = [8, BBQ.bargain(input[0:7], input[8:10])]

        elif input[9] - input[8] > 1500:
            if random.randrange(1, 100, 1) >= 50:
                output = action_predict(input)
            else:
                output = [8, BBQ.bargain(input[0:7], input[8:10])]
        else:
            output = action_predict(input)

    elif strength == 1:  # 一對
        if input[8] <= (input[9] - input[8]) / 6:  # 3倍底池
            if random.randrange(1, 100, 1) >= 20:
                output = action_predict(input)
            else:
                output = [8, BBQ.bargain(input[0:7], input[8:10])]

        elif input[9] - input[8] > 1500:
            if random.randrange(1, 100, 1) >= 40:
                output = action_predict(input)
            else:
                output = [8, BBQ.bargain(input[0:7], input[8:10])]
        else:
            output = action_predict(input)
    # 順序大小0 < 1 < 2 < 3 < 4 < 5 < 6 < 7 < 8
    else:  # 其他，條件判斷all-in
        if input[8] == input[9]:  # 判斷是否有加注(check or call)
            action += 1
        # print("action: ", action)
        if strength == 2:  # 兩對
            if action == 1:
                if random.randrange(1, 100, 1) >= 5:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            elif action == 2:
                if random.randrange(1, 100, 1) >= 10:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            elif action == 3:
                if random.randrange(1, 100, 1) >= 15:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            else:
                output = action_predict(input)

        elif strength == 3:  # 三條
            if action == 1:
                if random.randrange(1, 100, 1) >= 20:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            elif action == 2:
                if random.randrange(1, 100, 1) >= 30:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            elif action == 3:
                if random.randrange(1, 100, 1) >= 40:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            else:
                output = action_predict(input)

        elif strength >= 4 and strength <= 8:  # 順子 同花 葫蘆 鐵支 同花順
            if action == 1:
                if random.randrange(1, 100, 1) >= 50:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            elif action == 2:
                if random.randrange(1, 100, 1) >= 60:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            elif action == 3:
                if random.randrange(1, 100, 1) >= 70:
                    output = [9, BBQ.bargain(input[0:7], input[8:10])]
                else:
                    output = action_predict(input)
            else:
                output = action_predict(input)

        else:  # 同順缺1 同花缺1 同花缺2 順缺1
            output = action_predict(input)

    # print("---abandon output: ", output)
    return output


def action_predict(input):
    new_input = []
    size = np.array([[0] * 13] * 13)  # 二維資料
    rrow = []

    for i in range(0, len(input)):
        if i <= 9:
            if i == 8 or i == 9:
                new_input.append((input[i] / input[12]))
            else:
                new_input.append(input[i])
        elif (i % 3) == 1 and input[i] == -1:
            break
        elif (i % 3) == 0 and input[i] != -1:
            new_input.append((input[i] / input[12]))
        else:
            new_input.append(input[i])

    action_list = (BBQ.check_strength(new_input[0:7]) + new_input[:] + [-1] * (14 - len(new_input)))  # 牌型判斷參數加入
    print("action list:", action_list)

    for c in range(15):
        if c == 9 or c == 10:
            action_list[c] = float(action_list[c])
        else:
            action_list[c] = int(float(action_list[c]))
    print("---start convert to 2d-array......")
    for j in range(15):
        if j == 0:
            size[j, int(action_list[j])] = 1  # 0~12 -> 1~13 填0會等於沒有
            continue
        if j >= 1 and j <= 7:  # 放撲克編碼
            if int(action_list[j]) == -1:
                size[j] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            else:
                rank = int(action_list[j]) // 4  # 牌號
                suit = int(action_list[j]) % 4 + 1  # 花色 0~3 -> 1~4 填0會等於沒有
                size[j, rank] = suit
            continue
        if j == 8:
            if int(action_list[j]) == 1:
                size[j, int(action_list[j])] = 1
            elif int(action_list[j]) == 2:
                size[j, 1] = 1
                size[j, 2] = 1
            elif int(action_list[j]) == 3:
                size[j, 2] = 1
                size[j, 3] = 1
                size[j, 4] = 1
            elif int(action_list[j]) == 4:
                size[j, 5] = 1
                size[j, 6] = 1
                size[j, 7] = 1
                size[j, 8] = 1
            elif int(action_list[j]) == 5:
                size[j, 8] = 1
                size[j, 9] = 1
                size[j, 10] = 1
                size[j, 11] = 1
                size[j, 12] = 1
            continue
        if j == 9:  # 小數籌碼
            if int(float(action_list[j])) == 0:
                size[j] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            else:
                if float(action_list[j]) <= 1:
                    size[j, 0] = 1
                elif float(action_list[j]) < 17:
                    size[j, 1] = 1
                elif float(action_list[j]) < 30:
                    size[j, 2] = 1
                elif float(action_list[j]) < 45:
                    size[j, 3] = 1
                elif float(action_list[j]) < 57:
                    size[j, 4] = 1
                elif float(action_list[j]) < 80:
                    size[j, 5] = 1
                elif float(action_list[j]) < 125:
                    size[j, 6] = 1
                elif float(action_list[j]) < 200:
                    size[j, 7] = 1
                elif float(action_list[j]) < 225:
                    size[j, 8] = 1
                elif float(action_list[j]) < 290:
                    size[j, 9] = 1
                elif float(action_list[j]) < 400:
                    size[j, 10] = 1
                elif float(action_list[j]) < 650:
                    size[j, 11] = 1
                else:
                    size[j, 12] = 1
            continue
        if j == 10:  # 小數籌碼
            if int(float(action_list[j])) == 0:
                size[j] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            else:
                if float(action_list[j]) <= 1:
                    size[j, 0] = 1
                elif float(action_list[j]) < 17:
                    size[j, 1] = 1
                elif float(action_list[j]) < 30:
                    size[j, 2] = 1
                elif float(action_list[j]) < 45:
                    size[j, 3] = 1
                elif float(action_list[j]) < 57:
                    size[j, 4] = 1
                elif float(action_list[j]) < 80:
                    size[j, 5] = 1
                elif float(action_list[j]) < 125:
                    size[j, 6] = 1
                elif float(action_list[j]) < 200:
                    size[j, 7] = 1
                elif float(action_list[j]) < 225:
                    size[j, 8] = 1
                elif float(action_list[j]) < 290:
                    size[j, 9] = 1
                elif float(action_list[j]) < 400:
                    size[j, 10] = 1
                elif float(action_list[j]) < 650:
                    size[j, 11] = 1
                else:
                    size[j, 12] = 1
            continue
        if j >= 11 and j <= 14:
            if (
                int(action_list[11]) == 0
                and int(action_list[12]) == 1
                and int(action_list[13]) == 1
                and int(action_list[14]) == 0
            ):
                size[11, 0:4] = [1, 1, 1, 1]
            elif (
                int(action_list[11]) == -1
                and int(action_list[12]) == -1
                and int(action_list[13]) == -1
                and int(action_list[14]) == -1
            ):
                size[11, 4:8] = [1, 1, 1, 1]
            elif (
                int(action_list[11]) == 0
                and int(action_list[12]) == 0
                and int(action_list[13]) == 1
                and int(action_list[14]) == 1
            ):
                size[11, 8:13] = [1, 1, 1, 1, 1]
            else:
                size[11] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            continue

    for k in range(13):
        rrow.extend(
            size[
                k,
            ]
        )
    # print(size)

    print("---finish convert to 2d-array & start predict---")

    new_move = BBQ.predict(rrow)  # bugg
    print("---finish predict---")
    new_input.append(new_move)
    new_input.append(0)
    print("new input :", new_input)
    output = [new_move, BBQ.bargain(input[0:7], input[8:10])]
    # output = [ 2 , BBQ.bargain(input[0:7],input[8:10])] #此為測試用
    return output


def action_predict_RF(input):
    new_input = []
    for i in range(0, len(input)):
        if i <= 9:
            if i == 8 or i == 9:
                new_input.append((input[i] / input[12]))
            else:
                new_input.append(input[i])
        elif (i % 3) == 1 and input[i] == -1:
            break
        elif (i % 3) == 0 and input[i] != -1:
            new_input.append((input[i] / input[12]))
        else:
            new_input.append(input[i])

    action_list = (
        BBQ.check_strength(new_input[0:7]) + new_input[:] + [-1] * (14 - len(new_input))
    )  # 牌型判斷參數加入
    print("action_list:", action_list)
    new_move = BBQ.predict_RF(action_list)
    # latina.splinter_predict(action_list)#各樹predict
    new_input.append(new_move)
    new_input.append(0)
    print("new input :", new_input)
    output = [new_move, BBQ.bargain(input[0:7], input[8:10])]
    # output = [ 2 , BBQ.bargain(input[0:7],input[8:10])] #此為測試用
    return output


def getDuplicatesWithCount(listOfElems):
    """Get frequency count of duplicate elements in the given list"""
    dictOfElems = dict()
    # Iterate over each element in list
    for elem in listOfElems:
        # If element exists in dict then increment its value else add it in dict
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1

    # Filter key-value pairs in dictionary. Keep pairs whose value is greater than 1 i.e. only duplicate elements from list.
    dictOfElems = {key: value for key, value in dictOfElems.items() if value > 1}
    # Returns a dict of duplicate elements and thier frequency count
    return dictOfElems


def group(L):
    first = last = L[0]
    for n in L[1:]:
        if n - 1 == last:  # Part of the group, bump the end
            last = n
        else:  # Not part of the group, yield current group and start a new
            yield first, last
            first = last = n
    yield first, last  # Yield the last group


def hand_strength(hands):  # 阿修阿修 這邊有bug 同花跟同花順跟順子判斷有問題
    for i in range(len(hands)):
        hands[i] = int(hands[i])
    hands_ranks = []
    hands_suits = []
    hands_type = []
    # 0-51除以4 商數為點數 餘數為花色 餘數0為2,12為A,11為K
    for i in range(len(hands)):
        hands_ranks.append(hands[i] // 4)
        hands_suits.append(hands[i] % 4)

    # 判斷FLUSH
    # 產生重複的花色的key與value
    dictOf_suits = getDuplicatesWithCount(hands_suits)
    flush = -1
    flush_suits = -1
    for key, value in dictOf_suits.items():

        # 重複超過五次確定為FLUSH(同花)
        if value >= 5:
            flush_suits = key
            flush = 1

    # 判斷STRAIGHT(順子)

    # 點數排序
    rank_sorted = sorted(hands_ranks)

    # 刪除重複的點數
    rank_list = list(set(rank_sorted))  # set()集合不會包含重複的資料
    print("rank_list: ", rank_list)

    # 判斷
    straight = -1
    result = 0
    straight_key = -1
    flag = 0  # 在[1 2 3 4] [5 6] [9]狀況下 被保留紀錄不被洗掉
    for i in range(0, len(rank_list)):  # 統計相等的個數 或者是否為順子
        if rank_list[i] - rank_list[i - 1] == 1:
            result += 1  # 如果為順子，則result=4
            if result == 4:
                flag = 1
                straight_key = rank_list[i]

        else:
            result = 0  # 中斷就歸零

        if flag == 1:
            straight = 1

    # A起頭 5結尾 的順子
    if (
        rank_list[len(rank_list) - 1] == 12
        and rank_list[0] == 0
        and rank_list[1] == 1
        and rank_list[2] == 2
        and rank_list[3] == 3
    ):
        straight = 1
        straight_key = 12

    # 同花順

    if flush == 1 and straight != -1:  # 避免同花和順子並非為同組牌 如[A2 A3 B4 A5 A6 C7 A1]
        hands = sorted(hands)
        if hands[4] >= 48 or hands[5] >= 48 or hands[6] >= 48:  # A開頭的同花順
            print("hey here ")
            for k in range(4, 7):  # 可能有[A2 A3 A4 A5 A1 B1 C1] 所以檢查第五張開始
                for l in range(0, 3):  # 只需檢查到第3張是否連得起來[A2 B2 [C2] C3 C4 C5 [C1]]
                    print("hey : ", k, " ", l)
                    if ((hands[k] + 4) % 52) == hands[l]:
                        # -----------------以下為連續檢查------------------
                        flag = 0
                        for j in range(l, 5):
                            for m in range(j + 1, 6):
                                if (hands[j] + 4) == hands[m]:
                                    flag = flag + 1
                                if flag == 3:
                                    print("FLUSH STRAIGHT : ", end="")
                                    print(straight_key)
                                    hands_type.append(10)
                                    hands_type.append(straight_key)
                                    return hands_type

        else:  # 普通同花順
            for i in range(6):  # 檢查到第6張就好 如[1 3 [5 6 7 [8 9]]]
                for j in range(i + 1, len(hands)):
                    if (hands[i] + 4) == hands[j]:
                        flag = flag + 1
                    if flag == 4:
                        print("FLUSH STRAIGHT : ", end="")
                        print(straight_key)
                        hands_type.append(10)
                        hands_type.append(straight_key)
                        return hands_type

    # ranks重複的判斷   0=none 2=pair 3=threeKind 4=fourKind 5=twoPairs 6=fullhouse
    ranks_type = 0
    ranks_type_keys = []
    dictOf_ranks = getDuplicatesWithCount(hands_ranks)
    for key, value in dictOf_ranks.items():

        # 重複超過四次確定為 FOUR OF A KIND
        if value == 4:
            ranks_type = 4
            ranks_type_keys.clear()
            ranks_type_ranks = key
            break

        # 重複超過四次確定為 FULL HOUSE or THREE OF A KIND
        if value == 3:

            # 已經有2 PAIRS 升級為 FULL HOUSE
            if ranks_type == 5:
                ranks_type_keys.remove(min(ranks_type_keys))
                ranks_type_keys.insert(0, key)
                ranks_type = 6
                break

            # 已經有1 PAIR 升級為 FULL HOUSE
            elif ranks_type == 2 or ranks_type == 3:
                ranks_type_keys.append(key)
                ranks_type = 6
                break

            # THREE OF A KIND
            else:
                ranks_type_keys.append(key)
                ranks_type = 3

        # 重複超過兩次確定為 FULL HOUSE or 2 PAIRS or PAIR
        if value == 2:

            # 已經有2 PAIRS 升級為 FULL HOUSE
            if ranks_type == 5:
                ranks_type_keys.append(key)
                ranks_type_keys.remove(min(ranks_type_keys))

            # 已經有THREE oF A KIND 升級為 FULL HOUSE
            elif ranks_type == 3:
                ranks_type_keys.append(key)
                ranks_type = 6
                break

            # 已經有PAIR 升級為 2 PAIRS
            elif ranks_type == 2:
                ranks_type_keys.append(key)
                ranks_type = 5

            # PAIR
            else:
                ranks_type_keys.append(key)
                ranks_type = 2

    # OUTPUT

    if ranks_type == 4:
        print("FOUR OF A KIND : ", end="")
        print(ranks_type_ranks)
        hands_type = [7, ranks_type_ranks]

    elif ranks_type == 6:
        print(ranks_type_keys)
        print("FULL HOUSE : ", end="")
        print(ranks_type_keys[0], end=",")
        print(ranks_type_keys[1])
        hands_type = [6, ranks_type_keys[0], ranks_type_keys[1]]

    elif flush == 1:
        print("FLUSH : ", end="")
        print(flush_suits)
        hands_type = [5, flush_suits]

    elif straight != -1:
        print("STRAIGHT : ", end="")
        print(straight_key)
        hands_type = [4, straight_key]

    elif ranks_type == 3:
        print("THREE OF A KIND : ", end="")
        print(ranks_type_keys[0])
        hands_type = [3, ranks_type_keys[0]]

    elif ranks_type == 5:
        print("TWO PAIRS : ", end="")
        print(max(ranks_type_keys), end=",")
        print(min(ranks_type_keys))
        hands_type = [2, max(ranks_type_keys), min(ranks_type_keys)]

    elif ranks_type == 2:
        print("PAIR : ", end="")  # 有個小bug都有一對時，沒有比雙方手牌，變平手了
        print(ranks_type_keys[0])
        hands_type = [
            1,
            ranks_type_keys[0],
            max(hands[0:2]),
        ]  # 這邊規則出問題了，當強度、pair都一樣時，要比雙方的hand card，已修改

    else:
        print("HIGH CARD : ", end="")
        print(max(hands))
        hands_type = [0, max(hands[0:2])]
    return hands_type


if __name__ == "__main__":
    print("trainig end, thank you.")
    open_browser()
    start_server()
"""
    #點數排序
    hands_rank_sorted = sorted(hands_ranks)


    #刪除重複的點數
    hands_rank_dict = list(dict.fromkeys(hands_rank_sorted))

    #把連續的點數分組
    hands_rank_group=list(group(hands_rank_dict))
    straight = -1
    for i in range(len(hands_rank_group)):
        if (hands_rank_group[i][1] - hands_rank_group[i][0] >= 4):
            straight = hands_rank_group[i][1]

    #A起頭 5結尾 的順子
    if(hands_rank_group[0][0] == 0 and hands_rank_group[0][1] == 3 and max(hands_rank_dict)):
        straight = 3
"""
