import sys
from fastapi.testclient import TestClient
from app.main import app

sys.stdout.reconfigure(encoding='utf-8')
client = TestClient(app)

print('=== 1. General Knowledge: \"What is gravity?\" ===')
r = client.post('/chat/message', json={'session_id':'s4_1', 'message':'What is gravity?', 'user_name':'Sai Priya'})
print('Response:', r.json()['message'][:75], '...')
assert 'gravity' in r.json()['message'].lower()

print('\n=== 2. General Knowledge: \"What is photosynthesis?\" ===')
r = client.post('/chat/message', json={'session_id':'s4_2', 'message':'What is photosynthesis?', 'user_name':'Sai Priya'})
print('Response:', r.json()['message'][:75], '...')
assert 'photosynthesis' in r.json()['message'].lower() or 'sunlight' in r.json()['message'].lower()

print('\n=== 3. Comparison: \"Python vs JavaScript\" ===')
r = client.post('/chat/message', json={'session_id':'s4_3', 'message':'Python vs JavaScript', 'user_name':'Sai Priya'})
print('Response:', r.json()['message'][:85], '...')
assert 'python' in r.json()['message'].lower() and 'javascript' in r.json()['message'].lower()

print('\n=== 4. Comparison: \"iPhone vs Android\" ===')
r = client.post('/chat/message', json={'session_id':'s4_4', 'message':'iPhone vs Android', 'user_name':'Sai Priya'})
print('Response:', r.json()['message'][:85], '...')
assert 'iphone' in r.json()['message'].lower() and 'android' in r.json()['message'].lower()

print('\n=== 5. Comparison: \"Rice vs wheat\" ===')
r = client.post('/chat/message', json={'session_id':'s4_5', 'message':'Rice vs wheat', 'user_name':'Sai Priya'})
print('Response:', r.json()['message'][:85], '...')
assert 'rice' in r.json()['message'].lower() and 'wheat' in r.json()['message'].lower()

print('\n=== 6. Context Follow-up: Python -> When? ===')
r_py1 = client.post('/chat/message', json={'session_id':'s4_6', 'message':'Who invented Python?', 'user_name':'Sai Priya'})
print('Python Creator:', r_py1.json()['message'][:75], '...')
r_py2 = client.post('/chat/message', json={'session_id':'s4_6', 'message':'When?', 'user_name':'Sai Priya'})
print('Python When Follow-up:', r_py2.json()['message'][:75], '...')
assert '1991' in r_py2.json()['message'] or '1989' in r_py2.json()['message']

print('\n=== 7. Context Follow-up: India -> Capital? ===')
r_in1 = client.post('/chat/message', json={'session_id':'s4_7', 'message':'Tell me about India.', 'user_name':'Sai Priya'})
print('India info:', r_in1.json()['message'][:75], '...')
r_in2 = client.post('/chat/message', json={'session_id':'s4_7', 'message':'Capital?', 'user_name':'Sai Priya'})
print('India Capital Follow-up:', r_in2.json()['message'][:75], '...')
assert 'new delhi' in r_in2.json()['message'].lower() or 'delhi' in r_in2.json()['message'].lower()

print('\n=== 8. Context Follow-up: PM -> How long in office? ===')
r_pm1 = client.post('/chat/message', json={'session_id':'s4_8', 'message':'Who is the PM of India?', 'user_name':'Sai Priya'})
print('PM Info:', r_pm1.json()['message'][:75], '...')
r_pm2 = client.post('/chat/message', json={'session_id':'s4_8', 'message':'How long have they been in office?', 'user_name':'Sai Priya'})
print('PM Tenure Follow-up:', r_pm2.json()['message'][:75], '...')
assert '2014' in r_pm2.json()['message'] or 'years' in r_pm2.json()['message'].lower()

print('\n=== 9. Analogy Simplification: \"I don\'t understand binary search\" ===')
r_an = client.post('/chat/message', json={'session_id':'s4_9', 'message':"I don't understand binary search", 'user_name':'Sai Priya'})
print('Analogy Response:', r_an.json()['message'][:85], '...')
assert 'phonebook' in r_an.json()['message'].lower() or 'half' in r_an.json()['message'].lower()

print('\n=== 10. Telugu-English Mixed NLP: \"photosynthesis ante enti?\" ===')
r_tel1 = client.post('/chat/message', json={'session_id':'s4_10', 'message':'photosynthesis ante enti?', 'user_name':'Sai Priya'})
print('Telugu Science:', r_tel1.json()['message'][:85], '...')
assert 'glucose' in r_tel1.json()['message'].lower() or 'sunlight' in r_tel1.json()['message'].lower() or 'photosynthesis' in r_tel1.json()['message'].lower()

print('\n=== 11. Current Information: \"What is today\'s gold price?\" ===')
r_gold = client.post('/chat/message', json={'session_id':'s4_11', 'message':"What is today's gold price?", 'user_name':'Sai Priya'})
print('Gold Info:', r_gold.json()['message'][:75], '...')
assert 'gold' in r_gold.json()['message'].lower()

print('\n=== 12. Knowledge -> Quiz Transition ===')
r_sp1 = client.post('/chat/message', json={'session_id':'s4_12', 'message':'Tell me about the solar system', 'user_name':'Sai Priya'})
print('Solar system info:', r_sp1.json()['message'][:75], '...')
r_sp2 = client.post('/chat/message', json={'session_id':'s4_12', 'message':'Ask me questions', 'user_name':'Sai Priya'})
print('Solar system quiz:', r_sp2.json()['message'][:85], '...')
assert 'saturn' in r_sp2.json()['message'].lower() or 'moons' in r_sp2.json()['message'].lower() or 'planet' in r_sp2.json()['message'].lower()

print('\n=== 13. Contextual Culinary Connection ===')
r_rice = client.post('/chat/message', json={'session_id':'s4_13', 'message':'Tell me about rice varieties', 'user_name':'Sai Priya'})
print('Rice Varieties:', r_rice.json()['message'][:85], '...')
assert 'basmati' in r_rice.json()['message'].lower()
assert 'biryani' in r_rice.json()['message'].lower()

print('\n🎉 ALL 13 STEP 4 TEST CASES PASSED WITH 100% SUCCESS!')
