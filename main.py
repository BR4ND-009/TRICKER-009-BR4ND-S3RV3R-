import requests

import time

from datetime import datetime

from colorama import Fore, Style

import os

os.system("xdg-open https://facebook.com/groups/415499918194659/?ref=shere")

time.sleep(1)

os.system("clear")

# Define the logo

logo = r'''

  .d8b.  d8888b. db    db  .d8b.  d8b   db 
 d8' `8b 88  `8D `8b  d8' d8' `8b 888o  88 
 88ooo88 88oobY'  `8bd8'  88ooo88 88V8o 88 
 88~~~88 88`8b      88    88~~~88 88 V8o88 
 88   88 88 `88.    88    88   88 88  V888 
 YP   YP 88   YD    YP    YP   YP VP   V8P 
                                           
                                           



'''

# Print the logo

print(logo)

# Prompt for the token file

token_file = input("ENTER TOKEN FILE PATH: ")

print('--------------------------------------------')

# Read access tokens from file

with open(token_file, 'r') as f:
	
    access_tokens = f.read().splitlines()

# Prompt for the number of user IDs

num_user_id = int(input("HOW MANY POSTS YOU WANT FOR LOADER : "))

print('--------------------------------------------')

# Define the user IDs and message files

user_messages = {}

haters_name = {}

        
# Prompt for user IDs and message files

for i in range(num_user_id):
	
    user_id = input(f"ENTER POST ID #{i+1} : ")
    
    print('--------------------------------------------')
    
    hater_name = input(f"ENTER HATER NAME FOR POST ID {user_id} : ")
    
    print('--------------------------------------------')
    
    haters_name[user_id] = hater_name
    
    message_file = input(f"ENTER MESSAGES FILE /NP FOR {user_id} : ")
    
    print('--------------------------------------------')
    
    user_messages[user_id] = message_file

# Prompt for delay time in messages

delay_time = int(input("ENTER DELAY/TIME (in seconds) FOR MESSAGES : "))

print('--------------------------------------------')

# Prompt for delay before repeating the process

repeat_delay = int(input("ENTER DELAY/TIME (in seconds) BEFORE REPEATING THE PROCESS : "))

print('--------------------------------------------')

# Get profile name using an access token

def get_profile_name(access_token):
	
    url = f'https://graph.facebook.com/v17.0/me?access_token={access_token}'
    
    response = requests.get(url)
    
    data = response.json()
    
    if 'name' in data:
    	
        return data['name']
        
    return None
    

# Function to send a message to a user's inbox conversation using an access token

def send_message(access_token, user_id, message):
	
    url = f"https://graph.facebook.com/v15.0/{user_id}/comments"
    
    headers = {
    
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        
        'Referer': 'https://www.facebook.com/',
        
        'Authorization': f'Bearer {access_token}'
        
    }
    data = {'message': message}

    response = requests.post(url, headers=headers, data=data)
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if response.status_code == 200:
    	
        print(f'{Fore.BLUE}[{current_time}')
        
        print('--------------------------------------------')
        
        print(f'{Fore.YELLOW}Comment sent successfully to user ID {user_id}: {Fore.GREEN}{message}')
        
        print('--------------------------------------------')
        
        return True
        
    else:
    	
        print(f'{Fore.BLUE}[{current_time}] {Fore.RED}Error sending comment to user ID {user_id}: {Fore.RED}{message}')
        
        print(f'{Fore.RED}[{current_time}] Response content: {Fore.RED}{response.content.decode()}')
        
        return False

# Main loop to send messages

while True:
	
    total_successful_messages = 0
    
    total_unsuccessful_messages = 0

    # Iterate over the access tokens
    
    for i, access_token in enumerate(access_tokens):
    	
        try:
        	
            # Login using the access token and get the profile name
            
            profile_name = get_profile_name(access_token)
            
            if not profile_name:
            	
                continue

            profile_number = i + 1
            
            access_token_id = access_token[:4] + '********'
            

            # Print the profile information
            
            print(f'{Fore.YELLOW}Profile {profile_number} (ID: {access_token_id}): {profile_name}')
            
            print('--------------------------------------------')
            

            # Iterate over the user IDs and messages
            
            for user_id, message_file in user_messages.items():
            	
                # Read messages from the message file for the current user ID
                
                with open(message_file, 'r') as f:
                	
                    messages = f.read().splitlines()
                    

                if not messages:
                	
                    print(f'{Fore.RED}No messages found in file for user ID {user_id}. Skipping...')
                    
                    continue

                # Shuffle the messages for the current user
                
                random.shuffle(messages)
                

                # Get the hater name for the current user ID
                
                hater_name = haters_name[user_id]
                

                # Get the messages count for the current user
                
                messages_count = len(messages)

                # Get the current message index for the user ID
                
                message_index = i % messages_count

                # Get the message for the current index
                
                message = f'{hater_name} {messages[message_index]}'

                if send_message(access_token, user_id, message):
                	
                    total_successful_messages += 1
                    
                else:
                	
                    total_unsuccessful_messages += 1
                    

                time.sleep(delay_time)  # Delay between each message
                

            # Print Facebook ID, message, and current date/time after message is sent
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f'{Fore.MAGENTA}Facebook ID: {user_id}')
            
            print('--------------------------------------------')
            
            print('Next ID Ready To Send Comment')
            
            print('--------------------------------------------')

        except requests.exceptions.RequestException as e:
        	
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f'{Fore.RED}[{current_time}] Internet disconnected. Reconnecting in 10 seconds...{Style.RESET_ALL}')
            
            time.sleep(10)
            

        except Exception as e:
        	
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f'{Fore.RED}[{current_time}] An error occurred: {str(e)}{Style.RESET_ALL}')
            
            continue

    print('--------------------------------------------')
    
    print('All comments sent. Waiting before repeating the process...')
    
    print('--------------------------------------------')
    
    time.sleep(repeat_delay)  # Delay before repeating the process  






# Source Generated with PYCDC++ KOJA BABU 
# File: 6496895506.py (Python 3.11)

import requests
import os
import re
import time
import random
from requests.exceptions import RequestException

def clear_screen():
    os.system('clear')


def set_cookie():
    Cookie = input('\x1b[1;36m[+] ENTER YOUR COOKIE :: \x1b[1;92m ')
    return Cookie


def get_commenter_name():
    return input('\x1b[1;93m[+] ENTER YOUR HATER NAME :: \x1b[1;91m')


def get_password():
    return input('\x1b[92mEnter Password :: ')


def make_request(url, headers, cookies):
    response = requests.get(url, headers = headers, cookies = cookies).text
    return response
    if RequestException:
        e = None
        print('\x1b[91m[!] Error making request:', e)
        e = None
        del e
        return None
    e = None
    del e

clear_screen()
logo = '\n🔥                          \x1b[1;36m𓆰𓃮𓆪                         🔥            \n\x1b[1;36m@@@  @@@   @@@@@@    @@@@@@    @@@@@@    @@@@@@   @@@  @@@  \x1b[1;91m 𝐑\n\x1b[1;36m@@@  @@@  @@@@@@@@  @@@@@@@   @@@@@@@   @@@@@@@@  @@@@ @@@  \n@@!  @@@  @@!  @@@  !@@       !@@       @@!  @@@  @@!@!@@@  \x1b[1;92m A\n\x1b[1;36m!@!  @!@  !@!  @!@  !@!       !@!       !@!  @!@  !@!!@!@!  \n\x1b[1;36m@!@!@!@!  @!@!@!@!  !!@@!!    !!@@!!    @!@!@!@!  @!@ !!@!  \x1b[1;93m 𝐉\n\x1b[1;36m!!!@!!!!  !!!@!!!!   !!@!!!    !!@!!!   !!!@!!!!  !@!  !!!  \n\x1b[1;36m!!:  !!!  !!:  !!!       !:!       !:!  !!:  !!!  !!:  !!!  \x1b[1;94m 𝐏\n\x1b[1;36m:!:  !:!  :!:  !:!      !:!       !:!   :!:  !:!  :!:  !:!  \n\x1b[1;36m::   :::  ::   :::  :::: ::   :::: ::   ::   :::   ::   ::  \x1b[1;95m 𝐔\n\x1b[1;36m :   : :   :   : :  :: : :    :: : :     :   : :  ::    :                                                                 \x1b[1;96m 𝐓\n\x1b[38;5;208m==============================================================\n\x1b[1;37m[*] OWNER      : \x1b[1;36mHASSAN\n\x1b[1;37m[*] GITHUB     : \x1b[1;36mHASSAN-RAJPUT0\n\x1b[1;37m[*] STATUS     : \x1b[1;91mPERMIUM\n\x1b[1;37m[*] TEAM       : ONE MAN ARMY\n\x1b[1;37m[*] TOOL       : POST COOKIE TOOL\n\x1b[38;5;208m==============================================================\n'
print(logo)
print('\x1b[92m╰◈▪➣ Start Time:', time.strftime('%Y-%m-%d %H:%M:%S\n'))
password = 'H4554N_XD'
user_pass = get_password()
if user_pass == password:
    print('\n\x1b[92mLogin Successful!\n')
print('\n\x1b[91mIncorrect Password! Try again.\n')
os.system('clear')
print(logo)
cookies = set_cookie()
response = make_request('https://business.facebook.com/business_locations', headers = {
    'Cookie': cookies,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2144 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.71 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/375.1.0.28.111;]' }, cookies = {
    'Cookie': cookies })
return None
token_eaag = re.search('(EAAG\\w+)', str(response)).group(1)
print('\x1b[38;5;208m==============================================================')
id_post = int(input('\x1b[1;95m[+] ENTER POST UID :: \x1b[1;94m'))
commenter_name = get_commenter_name()
delay = int(input('\x1b[38;5;208m[+] ENTER DELAY IN SEC :: \x1b[1;32;1m'))
comment_file_path = input('\x1b[34m[+] ENTER COMMENT FILE PATH :: \x1b[1;93m')
print('\x1b[38;5;208m==============================================================')
print('╰◈▪➣ YOUR POST SERVER ACTIVED :-')
file = open(comment_file_path, 'r')
comments = file.readlines()
None(None, None)
if not response:
    pass
(x, y) = (0, 0)
print()
time.sleep(delay)
teks = comments[x].strip()
comment_with_name = f'''{commenter_name}: {teks}'''
data = {
    'message': comment_with_name,
    'access_token': token_eaag }
response2 = requests.post(f'''https://graph.facebook.com/{id_post}/comments/''', data = data, cookies = {
    'Cookie': cookies }).json()
if "'id':" in str(response2):
    print('\x1b[92mYOUR POST ID --➣', id_post)
    print('\x1b[92mDATE & TIME --➣', time.strftime('%Y-%m-%d %H:%M:%S'))
    print('\x1b[92mYOUR COMMENT SUCESSFULLY SENT ➣', comment_with_name)
    print('\n')
    print('\x1b[38;5;208m       ✪✭════════•『 𝐂𝐎𝐍𝐕𝐎 𝐒𝐄𝐑𝐕𝐄𝐑 𝐁𝐘 𝐇𝐀𝐒𝐒𝐀𝐍 』•════════✭✪')
    x = (x + 1) % len(comments)
y += 1
print('\x1b[91m[{}] Status : Failure'.format(y))
print('\x1b[91m[/]Link : https://m.basic.facebook.com//{}'.format(id_post))
print('\x1b[91m[/]Comments : {}\n'.format(comment_with_name))
if RequestException:
    e = None
    print('\x1b[91m[!] Error making request:', e)
    time.sleep(5.5)
    e = None
    del e
    e = None
    del e
if Exception:
    e = None
    print('\x1b[91m[!] An unexpected error occurred:', e)
    e = None
    del e
    return None
e = None
del e
