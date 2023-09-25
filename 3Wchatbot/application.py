from flask import Flask, render_template, request, jsonify, abort
import requests, json
import urllib.request
import sys
import xml.etree.ElementTree as elemTree
import openpyxl
import pandas as pd

application = Flask(__name__)

def extract_forecast_data(location, date):
    url = 'http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108'
    response = requests.get(url)
    xmldatas = elemTree.fromstring(response.text)

    matching_forecasts = []
    for item in xmldatas.findall('.//location'):
        if item.find('city').text == location:
            for data in item.findall('data'):
                if data.find('tmEf').text == date:
                    matching_forecasts.append({
                        '지역': location,
                        '날짜': data.find('tmEf').text.split()[0],
                        '날씨': data.find('wf').text,
                        '최저온도': data.find('tmn').text,
                        '최고온도': data.find('tmx').text,
                        '평균온도': (int(data.find('tmn').text) + int(data.find('tmx').text)) // 2
                    })

    return matching_forecasts

def clothing_recommendation(tmn, tmx, wf):
    tma = (int(tmn)+int(tmx))//2 + 2
    
    if wf == "흐림" or wf == "흐리고 비" or wf == "흐리고 눈":
        if tma >= 28:
            return ["민소매", "반팔", "반바지", "원피스", "우산"]
        elif tma >= 23 and tma <= 27:
            return ["반팔", "얇은 셔츠", "반바지", "면바지", "우산"]
        elif tma >= 20 and tma <= 22:
            return ["얇은 가디건", "긴팔", "면바지", "청바지", "우산"]
        elif tma >= 17 and tma <= 19:
            return ["얇은 니트", "맨투맨", "가디건", "청바지", "우산"]
        elif tma >= 12 and tma <= 16:
            return ["자켓", "가디건", "야상", "청바지", "면바지", "우산"]
        elif tma >= 9 and tma <= 11:
            return ["자켓", "트렌치코트", "니트", "청바지", "스타킹", "우산"]
        elif tma >= 5 and tma <= 8:
            return ["코트", "가죽자켓", "히트텍", "니트", "레깅스", "우산"]
        elif tma <= 4:
            return ["패딩", "두꺼운코트", "목도리", "기모제품", "우산"]
    else:
        if tma >= 28:
            return ["민소매", "반팔", "반바지", "원피스"]
        elif tma >= 23 and tma <= 27:
            return ["반팔", "얇은 셔츠", "반바지", "면바지"]
        elif tma >= 20 and tma <= 22:
            return ["얇은 가디건", "긴팔", "면바지", "청바지"]
        elif tma >= 17 and tma <= 19:
            return ["얇은 니트", "맨투맨", "가디건", "청바지"]
        elif tma >= 12 and tma <= 16:
            return ["자켓", "가디건", "야상", "청바지", "면바지"]
        elif tma >= 9 and tma <= 11:
            return ["자켓", "트렌치코트", "니트", "청바지", "스타킹"]
        elif tma >= 5 and tma <= 8:
            return ["코트", "가죽자켓", "히트텍", "니트", "레깅스"]
        elif tma <= 4:
            return ["패딩", "두꺼운코트", "목도리", "기모제품"]
        
def get_weather(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

def weather_word_recommendation(tmn, tmx):
    tma = (int(tmn)+int(tmx))//2 
    word = ""
    
    if tma >= 28:
        word = "폭염에 주의하세요! 저의 추천 아이템은 다음과 같습니다.\n민소매, 반팔, 반바지, 원피스\n\n"
        return word
    elif tma >= 23 and tma <= 27:
        word = "더위에 치친 당신을 위한 저의 추천 아이템은 다음과 같습니다.\n반팔, 얇은 셔츠, 반바지, 면바지\n\n"
        return word
    elif tma >= 20 and tma <= 22:
        word = "따뜻한 날씨에 맞는 추천 아이템을 소개해드릴게요.\n얇은 가디건, 긴팔, 면바지, 청바지\n\n"
        return word
    elif tma >= 17 and tma <= 19:
        word = "선선한 날씨에 맞는 저의 추천 아이템은 다음과 같습니다.\n얇은 니트, 맨투맨, 가디건, 청바지\n\n"
        return word
    elif tma >= 12 and tma <= 16:
        word = "선선함과 쌀쌀함이 느껴지는 날씨입니다.\n저의 추천 아이템은 다음과 같습니다.\n자켓, 가디건, 야상, 청바지, 면바지\n\n"
        return word
    elif tma >= 9 and tma <= 11:
        word = "쌀쌀한 날씨에 걸칠 겉옷을 챙기면 좋을 것 같아요.\n저의 추천 아이템은 다음과 같습니다.\n자켓, 트렌치코트, 니트, 청바지, 스타킹\n\n"
        return word
    elif tma >= 5 and tma <= 8:
        word = "오늘 날씨는 추워요.\n이런 아이템은 어떨까요?\n코트, 가죽자켓, 히트텍, 니트, 레깅스\n\n"
        return word
    elif tma <= 4:
        word = "매우 추운 날씨네요. 감기조심하세요.\n오늘의 추천 아이템입니다.\n패딩, 두꺼운코트, 목도리, 기모제품\n\n"
        return word
    
@application.route("/", methods=['POST', 'GET'])
def index():
    forecast_data = []
    recomm_data = []
    recomm_filename = []
    wf_filename = "sunny"
    shop_data_matrix = []
    
    location = '대구'
    date = '2023-09-25'
    date = date + " 00:00"
    print(location, date)
    forecast_data = extract_forecast_data(location, date)       
    
    if request.method == 'POST':
        location = request.form['location']
        date = request.form['date']
        date = date + " 00:00"
        print(location, date)
        forecast_data = extract_forecast_data(location, date)       
    print(forecast_data)
    
    for forecast in forecast_data:
        tmn = forecast['최저온도']
        tmx = forecast['최고온도']
        wf = forecast['날씨']
        recomm_data = clothing_recommendation(tmn, tmx, wf)
        print(recomm_data)
        print((recomm_data)[0])
        dic = {'민소매':'sleeveless', '반팔':'Short Sleeve', '반바지':'shorts', '원피스':'onepiece', '얇은 셔츠':'shirt', '면바지':'Cotton pants', '얇은 가디건':'cardigan', '맨투맨':'denim_jacket',
               '긴팔':'shirt', '청바지':'jeans', '자켓':'jacket', '트렌치코트':'trench_coat', '야상':'trench_coat', '니트':'hood', '얇은 니트':'hood', '코트':'trench_coat', '가죽자켓':'leather_jacket', 
               '히트텍':'Gloves', '패딩':'padding', '두꺼운코트':'fur_hat', '목도리':'muffler', '기모제품':'brushed_products', '우산':'umbrella_boots'}
        recomm_filename = [dic.get(item, '') for item in recomm_data]
        print(recomm_filename)
    
        dic2 = {'맑음':'sunny', '구름많음':'cloudy', '흐림':'cloudy', '흐리고 비':'rain', '흐리고 눈':'snow'}
        # wf_filename = dic2[forecast['날씨']]
        wf_filename = dic2.get(forecast['날씨'], '')
        print(wf_filename)
        
        shop_data = pd.read_excel('shop_data.xlsx', engine='openpyxl')
        # print(shop_data)
        for recomm in recomm_data:
            row_numbers = shop_data.index[shop_data['분류'] == recomm].tolist()
            print(row_numbers)
            for row in row_numbers:
                shop_data_matrix.append(shop_data.loc[row])
        # print(shop_data_matrix)
        # print(shop_data_matrix[0][1])
        print(len(shop_data_matrix))
        
    return render_template("index.html", forecast_data=forecast_data, recomm_data=recomm_data, recomm_filename=recomm_filename, wf_filename=wf_filename, shop_data_matrix=shop_data_matrix)

@application.route("/tpchatbot", methods=['POST'])
def tpchatbot():
    authKey = "mKh5p+FHQam9BqayzZLq"
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': authKey
    }
    user_key = request.get_json()['user']
    msg = request.get_json()
    print(msg.get('textContent', {}).get('text', ''))
    response_message = ""
    
    if 'textContent' in msg and msg['textContent']['text'] == '옷 추천해줘':
        city = 'Daegu'
        api_key = 'ce80f5390e343adaa7a74678a59fa9b4'
        weather_data = get_weather(city, api_key)
        if weather_data['cod'] == 200:
            temp_min = weather_data["main"]["temp_min"]
            temp_max = weather_data["main"]["temp_max"]
        print(temp_min, temp_max)
        text = weather_word_recommendation(temp_min, temp_max)
        response_message = text + "(스타일링 추천은 아래 링크를 참고해 주세요)"
        data = {
            'event': 'send',
            'user': user_key,
            'textContent': {'text': response_message}
        }
        message = json.dumps(data)
        response = requests.post('https://gw.talk.naver.com/chatbot/v1/event', headers=headers, data=message)   
        data = {
            'event' : 'send',
            'user' : user_key,
            'compositeContent': {
                'compositeList': [
                    {
                        'image': {'imageUrl': 'https://proxy.goorm.io/service/64f9b3b95d121c59f23480d5_ddhpcjROtEiOJw5c9yj.run.goorm.io/9080/file/load/chatbot_sum.png?path=d29ya3NwYWNlJTJGVGVhbVByb2plY3QlMkZzdGF0aWMlMkZpbWFnZXMlMkZpY29ucyUyRmNoYXRib3Rfc3VtLnBuZw==&docker_id=ddhpcjROtEiOJw5c9yj&secure_session_id=NyGjt9g2oLKNXO4dMgjYtno7BQvutLVB'},
                        'buttonList': [
                            {
                                'type': 'LINK',                             
                                'data': {
                                    'title': '이옷어때 사이트로 이동하기',
                                    'url': 'https://teamproject-ncgqy.run.goorm.site/',
                                    'mobileUrl': 'https://teamproject-ncgqy.run.goorm.site/'
                                }
                            }
                        ]
                    }
                    
                ]
            }
        }
        message = json.dumps(data)
        response = requests.post('https://gw.talk.naver.com/chatbot/v1/event', headers=headers, data=message)
    elif 'textContent' in msg and msg['textContent']['text'] == '안녕하세요':
        response_message = "안녕하세요\n스타일 추천을 원하시면 '옷 추천해줘'를 입력해주세요"
        data = {
            'event': 'send',
            'user': user_key,
            'textContent': {'text': response_message}
        }
        message = json.dumps(data)
        response = requests.post('https://gw.talk.naver.com/chatbot/v1/event', headers=headers, data=message)
    elif 'textContent' in msg:
        response_message = "스타일 추천을 원하시면 '옷 추천해줘'를 입력해주세요"     
        data = {
            'event': 'send',
            'user': user_key,
            'textContent': {'text': response_message}
        }
        message = json.dumps(data)
        response = requests.post('https://gw.talk.naver.com/chatbot/v1/event', headers=headers, data=message)

    return jsonify({'message': response_message})

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)
