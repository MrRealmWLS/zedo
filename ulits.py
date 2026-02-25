import requests
import os
import ctypes
from datetime import datetime
import time
import aiohttp
import asyncio
import json
from colorama import Fore, Style, init; init()
def leave_all_guild(token):
    guilds_response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=header(token))
    guilds=[guild['id'] for guild in guilds_response.json()]
    for i in guilds:
        leave_guild(i,token)
def close_dm(channel_id, token):
    headers = {
        "Authorization": token,  
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://discord.com/",
        "Origin": "https://discord.com",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}"
    response = requests.Session().delete(url, headers=headers)
    if response.status_code in {200, 201, 204}:
        Log.Success(f"Closed DM: {channel_id}")
def close_all_dm(token):
    headers = {
        "Authorization": token,  
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://discord.com/",
        "Origin": "https://discord.com",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }

    url = "https://discord.com/api/v9/users/@me/channels"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        Log.Error(f"Failed to fetch DM channels: {response.status_code} {response.text}")
        return

    try:
        data = response.json()
    except ValueError:
        Log.Error("Failed to parse JSON:", response.text)
        return

    if isinstance(data, dict) and data.get("message"):
        Log.Error("Discord API error:", data)
        return

    if not isinstance(data, list):
        Log.Error("Unexpected response format:", type(data))
        return

    dm_channels = [d["id"] for d in data if d.get("type") == 1 and "id" in d]

    Log.Success(f"Found {len(dm_channels)} DM(s). Closing them all...")

    for cid in dm_channels:
        try:
            close_dm(cid, token)
            time.sleep(0.3)  
        except Exception as e:
            pass
def leave_guild(guild_id, token):
    headers = {
        "Authorization": token, 
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://discord.com/",
        "Origin": "https://discord.com",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    url = f"https://discord.com/api/v9/users/@me/guilds/{guild_id}"
    while True:
        response = requests.Session().delete(url, headers=headers)
        
        if response.status_code in {200, 201, 204}:
            Log.Success(f"Left guild: {guild_id}")
            break
        
        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 1)
            Log.Warning(f"Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        
        else:
            Log.Error(f"Failed to leave guild {guild_id}: {response.status_code} - {response.text}")
            break
def remove_all_firends(token):
    headers = {
        "Authorization": token,  # For user tokens; use "Bot {token}" for bot tokens
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://discord.com/",
        "Origin": "https://discord.com",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }

    
    friends_response = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers)
    firends=[friend['id'] for friend in friends_response.json()]
    for i in firends:
        remove_friend(i,token)
def remove_friend(friend_id, token):
    url = f"https://discord.com/api/v9/users/@me/relationships/{friend_id}"
    response = requests.Session().delete(url, headers=header(token))
    if response.status_code in {200, 201, 204}:
        Log.Success(f"Removed friend: {friend_id}")
    else:
        Log.Error(f"Failed To Remove Firend {friend_id}")
async def send_webhook(webhook_url, content, times):
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'content': content,
    }

    async with aiohttp.ClientSession() as session:
        for i in range(times):
            async with session.post(webhook_url, headers=headers, json=data) as response:
                if response.status == 204:
                    Log.Success(f"[ + ] Message {i + 1} sent successfully!")
                else:
                    Log.Error(f"Failed to send message {i + 1}: {response.status}")
            await asyncio.sleep(0.2)
def delete_webhook(webhook_url):
    response = requests.delete(webhook_url)
    print(response)
    if response.status_code == 204:
        Log.Success("Webhook deleted successfully.")
    else:
        Log.Error(f"Failed to delete webhook. Status code: {response.status_code}, Response: {response.text}")

def info_webhook(webhook_url):
    response = requests.get(webhook_url)
    if response.status_code == requests.codes.ok:
        webhook_info = response.json()
        clear()
        print(f"\nWebhook Name: {webhook_info['name']}\nToken: {webhook_info['token']}\nGuild ID: {webhook_info['guild_id']}\nChannel ID: {webhook_info['channel_id']}\nWebhook ID: {webhook_info['id']}\nApplication ID: {webhook_info['application_id']}\nAvatar: {webhook_info['avatar']}\nWebhook Type: {webhook_info['type']}\nApplication ID: {webhook_info['application_id']}\n")
    else:
        clear()
        Log.Error(f'Respond: {response.status_code} - Please try again.')
def TokenInfo(token):
    headers = header(token)

    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

    if r.status_code == 200:
        tokenis = f"VALID"
        Log.Success(f"Token {token.split(".")[0]} is VALID")
    elif r.status_code == 403:
        tokenis = f"LOCKED"
        Log.Warning(f"Token {token.split(".")[0]} is LOCKED")
    else:
        tokenis = f"INVALID"
        Log.Error(f"Token {token.split(".")[0]} is INVALID")

    data = json.loads(r.text)
    username = data.get('username')
    tid = data.get('id')

    if data.get('premium_type') == 2:
        nitro = "Boost"
    elif data.get('premium_type') == 1:
        nitro = "Basic"
    else:
        nitro = "False"

    ev = "True" if data.get('verified') else "False"
    fv = "True" if data.get('phone') else "False"

    t = token.split(".")[0]

    tid = str(tid) if tid is not None else "None"
    username = username if username is not None else "None"

    print(f"\033[38;2;24;76;255m{tokenis.ljust(12)}\033[0m | \033[38;2;24;76;255mToken: {t}{'***'.rjust(21 - len(t))} | User: {username.ljust(20)} | Nitro: {nitro.ljust(5)} | EV: {ev.ljust(5)} | FV: {fv}\033[0m")

class Log:
    @staticmethod
    def _log(level, prefix, message):
        timestamp = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
        log_message = f"[{Fore.LIGHTBLACK_EX}{timestamp}{Fore.RESET}] {prefix} {message}"
        print(log_message)

    @staticmethod
    def Success(message, prefix="(+)", color=Fore.LIGHTGREEN_EX):
        Log._log("SUCCESS", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Error(message, prefix="(-)", color=Fore.LIGHTRED_EX):
        Log._log("ERROR", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Debug(message, prefix="(*)", color=Fore.LIGHTYELLOW_EX):
        Log._log("DEBUG", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Solved(message, prefix="(!)", color=Fore.LIGHTBLUE_EX):
        Log._log("SOLVED", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Info(message, prefix="(?)" , color=Fore.LIGHTWHITE_EX):
        Log._log("INFO", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Warning(message, prefix="(!)", color=Fore.LIGHTMAGENTA_EX):
        Log._log("WARNING", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Ask(tag: str, content: str, color=Fore.BLUE):
        ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        return input(Style.BRIGHT + ts + color + f" [{tag}] " + Fore.RESET + content + Fore.RESET)
def header(token: str) -> dict:
    return {
        "Authorization": token,
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Referer": "https://discord.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "Origin": "https://discord.com"
    }

def is_vaild_token(token):
    response = requests.get('https://discord.com/api/v9/users/@me', headers=header(token))
    if response.status_code == 200:
        Log.Success("Token Vaild")
        return True
    else:
        Log.Error("Token Invaild")
        return False
def set_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(f"Evils Tool | {title}")

def CheckPromo(promo,filename):
        headers = {
            'authority': 'discord.com',
            'method': 'GET',
            'scheme': 'https',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Debug-Options': 'bugReporterEnabled',
            'X-Discord-Locale': 'en-GB',
            'X-Discord-Timezone': 'Asia/Calcutta',
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1NjIzMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
        }

        data = "country_code=US&with_application=false&with_subscription_plan=true"

        while True:
            response = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{promo}?{data}", headers=headers)

            if response.status_code == 200:

                uses = response.json()['uses']

                if uses == 0:
                    Log.Success(f"Valid: {promo}")
                    with open(filename, "a") as f:
                        f.write(f"https://promos.discord.gg/{promo}\n")

                else:
                    Log.Error(f"Redeemed: {promo}")
                break

            elif "The resource is being rate limited." in response.text:
                retry_after = response.json()['retry_after']
                Log.Warning(f"Rate limited: {promo} | Retrying in {retry_after}ms")
                time.sleep(retry_after)
                continue

            else:
                Log.Error(f"Invalid: {promo}")
                break

def clear():
    os.system("cls")