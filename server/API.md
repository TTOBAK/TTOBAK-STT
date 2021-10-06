# 또박이-AUDIO API 정의 문서

API Document for **또박이**
**Markdown** 으로 작성되었습니다   

## GOP

발음 정확도 계산을 위해 호출해야 하는 API

**segscore**   
---

* **URL**   
    /api/segscore
* **Method**   
    `POST`
* **Data Params**   
    `gender=[m or f] | transcript=[alphanumeric] | file=[file]` 
* **Success Response**   
    * Code: 200   
      Content: 
      ```
      {
          'request': '/api/segscore', 
           'status': 'Success', 
           'score': [float], 
           'phone_score': [float], 
           'speed_score': [float], 
           'rhythm_score': [float], 
           'transcript': [alphanumeric], 
           'correct': [alphanumeric], 
           'student': [alphanumeric]
       }
      ```   
       여기서 transcript는 정답 문자열, correct는 정답 발음열, student는 음성 파일 발음열을 의미   
* **Error Response**   
    * gender, transcript, file이 data param에 없을 때   
      Content: `{'request': '/api/segscore', 'status': 'Fail', 'code': 1, 'message': 'Insufficient Parameters'}`
    * gender, transcript가 비어있을 때   
      Content: `{'request': '/api/segscore', 'status': 'Fail', 'code': 2, 'message': 'Parameter is not filled'}`   
      * 파일이 적절한 타입이 아닐 때
      Content: `{'request': '/api/segscore', 'status': 'Fail', 'code': 3, 'message': 'Invalid extensions'}`
      * 서버 내 처리에서 문제가 생겼을 때   
      Content: `{'request': '/api/segscore', 'status': 'Fail', 'code': 4, 'message': 'Processing error'}`
    * gender field가 'm'이나 'f'가 아닐 때
      Content: {'request': '/api/segscore', 'status': 'Fail', 'code': 5, 'message': 'Invalid Parameters'}
    * 파일이 너무 클 때
      Content: {'request': '/api/segscore', 'status': 'Fail', 'code': 6, 'message': 'Too Big File'}