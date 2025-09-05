REST API для трекинга привычек, построенный на Django REST Framework. Позволяет создавать привычки и отслеживать ежедневный прогресс.

Эндпоинты авторизации:
  auth/ +
    /users/
    /users/me/
    /users/resend_activation/
    /users/set_password/
    /users/reset_password/
    /users/reset_password_confirm/
    /users/set_username/
    /users/reset_username/
    /users/reset_username_confirm/
    /token/login/
    /token/logout/
    
Эндпоинты приложения:
  habits/x/
  daily-records/x/
  где x это id

Пример использования:

1. Регистрация

curl -X POST http://localhost/auth/users/ \ 
	-H "Content-Type: application/json" \
	-d '{"username":"Lolo","email":"open@source.com","password":"archlinuxbtw"}'
	
		  {
			"email":"open@source.com",
			"username":"Lolo","id":1
		  }

2. Получение токена		
		
curl -X POST http://localhost/auth/token/login/ \
	-H "Content-Type: application/json" \
	-d '{"username":"Lolo","password":"archlinuxbtw"}'
	
		  {"auth_token":"72f710182673132606f0d575f3efa2de7fed55cd"}

3. Создание новой привычки

curl -X POST http://localhost/habits/ \
  -H "Authorization: Token 72f710182673132606f0d575f3efa2de7fed55cd" \
  -H "Content-Type: application/json" \
  -d '{"name":"Ни слова о линуксе","description":"Не рассказывать всем о том, что поставил себе линукс в течение часа","target":60,"unit":"мин"}'
  
		  {
		  	"id":1,
		  	"user":"Lolo",
		  	"name":"Ни слова о линуксе",
		  	"description":"Не рассказывать всем о том, что поставил себе линукс в течение часа",
		  	"target":60,
		  	"unit":"мин",
		  	"daily_records":[],
		  	"success":false
		  }
 
 4. Первого сентября продержался 20 мин
 
 curl -X POST http://localhost/daily-records/ \
  -H "Authorization: Token 72f710182673132606f0d575f3efa2de7fed55cd" \
  -H "Content-Type: application/json" \
  -d '{"habit":1,"date":"2025-09-01","amount_achieved":20}'
  
		  {
			"id":2,
			"habit":1,
			"date":"2025-09-01",
			"amount_achieved":20,
			"target":60,
			"unit":"мин"
		  }

5. Просмотр состояния привычки
 
 curl -X GET http://localhost/habits/1/ \
  -H "Authorization: Token 72f710182673132606f0d575f3efa2de7fed55cd" \
  -H "Content-Type: application/json"
  
		  {
			"id":1,
			"user":"Lolo",
			"name":"Ни слова о линуксе",
			"description":"Не рассказывать всем о том, что поставил себе линукс в течение часа",
			"target":60,
			"unit":"мин",
			"daily_records":[
				{"id":1,"date":"2025-09-01","amount_achieved":20}],
			"total":20,
			"average":20.0,
			"best":20,
			"success":false
		  }

6. Второго сентября продержался 35 мин

curl -X POST http://localhost/daily-records/ \
  -H "Authorization: Token 72f710182673132606f0d575f3efa2de7fed55cd" \
  -H "Content-Type: application/json" \
  -d '{"habit":1,"date":"2025-09-02","amount_achieved":35}'

		  {
		  	"id":2,
		  	"habit":1,
		  	"date":"2025-09-02",
		  	"amount_achieved":35,
		  	"target":60,
		  	"unit":"мин"
		  }

7. Снова просмотр состояния привычки

curl -X GET http://localhost/habits/1/ \
  -H "Authorization: Token 72f710182673132606f0d575f3efa2de7fed55cd" \
  -H "Content-Type: application/json"
  
		  {
		  	"id":1,
		  	"user":"Lolo",
		  	"name":"Ни слова о линуксе",
		  	"description":"Не рассказывать всем о том, что поставил себе линукс в течение часа",
		  	"target":60,"unit":"мин",
		  	"daily_records":[
		  		{
		  		  "id":1,
		  		  "date":"2025-09-01",
		  		  "amount_achieved":20
		  		},
		  		{
		  		  "id":2,
		  		  "date":"2025-09-02",
		  		  "amount_achieved":35
		  		 }
		  	],
		  	"total":55,
		  	"average":27.5,
		  	"best":35,
		  	"success":false
		  }
 
8. Пятого сентября смог продержаться аж 71 мин

curl -X POST http://localhost/daily-records/ \
  -H "Authorization: Token 72f710182673132606f0d575f3efa2de7fed55cd" \
  -H "Content-Type: application/json" \
  -d '{"habit":1,"date":"2025-09-05","amount_achieved":71}'

		  {
		  	"id":3,
		  	"habit":1,
		  	"date":"2025-09-05",
		  	"amount_achieved":71,
		  	"target":60,
		  	"unit":"мин"
		  }

9. И опять проверка состояния привычки

curl -X GET http://localhost/habits/1/ \
  -H "Authorization: Token 72f710182673132606f0d575f3efa2de7fed55cd" \
  -H "Content-Type: application/json"
  
		  {
			  "id":1,
			  "user":"Lolo",
			  "name":"Ни слова о линуксе",
			  "description":"Не рассказывать всем о том, что поставил себе линукс в течение часа",
			  "target":60,
			  "unit":"мин",
			  "daily_records":[
			  	{
			  	  "id":1,
			  	  "date":"2025-09-01",
			  	  "amount_achieved":20
			  	},
			  	{
			  	  "id":2,
			  	  "date":"2025-09-02",
			  	  "amount_achieved":35
			  	},
			  	{
			  	  "id":3,
			  	  "date":"2025-09-05",
			  	  "amount_achieved":71
			  	}
			  ],
			  "total":126,
			  "average":42.0,
			  "best":71,
			  "success":true - победа
		  }

10. Разрушение токена

curl -X POST http://localhost/auth/token/logout/ \
  -H "Authorization: Token 72f710182673132606f0d575f3efa2de7fed55cd" \   
  -H "Content-Type: application/json"
