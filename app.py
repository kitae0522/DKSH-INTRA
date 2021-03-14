from flask import Flask, render_template
import requests as req
import json
from datetime import datetime
from pytz import timezone
import random
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
    "Accept-Language": "ko",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
}

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def main():
	YMD = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d')

	url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?type=json&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7010137&MLSV_YMD={YMD}"
	res = req.get(url, headers=headers)
	data = json.loads(res.text)

	try:
		load_data = data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
		meal = ["".join(re.compile("[^0-9.]").findall(load_data)).split("<br/>"), True]
	except KeyError:
		meal = ["🤦🏻‍♂️학교 또는 기상청에서 제공하는 데이터 정보가 없습니다. 나중에 다시 시도해주세요.", False]

	return render_template(
		"index.html",
		date=YMD,
		title="메인",
		meal_data=meal
	)