from ulits import *
import time
import sys
Banner = """
\033[38;2;255;0;0m                          ███████╗███████╗██████╗  ██████╗ 
\033[38;2;230;0;0m                          ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗
\033[38;2;200;0;0m                            ███╔╝ █████╗  ██║  ██║██║   ██║
\033[38;2;140;0;0m                           ███╔╝  ██╔══╝  ██║  ██║██║   ██║
\033[38;2;140;0;0m                          ███████╗███████╗██████╔╝╚██████╔╝
\033[38;2;110;0;0m                          ╚══════╝╚══════╝╚═════╝  ╚═════╝      \033[0m
"""

options = """
\033[38;2;255;165;0m            ╔═════════════════════════════════════════════════════════════╗
\033[38;2;255;135;0m            ║                        Made By Realm                        ║
\033[38;2;255;105;0m            ╚═════════════════════════════════════════════════════════════╝
\033[38;2;255;75;0m                              *ZEDO* - BEST TOOL IN CORD
\033[38;2;240;0;0m            ╔════════════════════╦═══════════════════╦════════════════════╗
\033[38;2;240;0;0m            ║                    ║                   ║                    ║
\033[38;2;240;0;0m            ║   1: Promo Checker ║ 2: Token Info     ║ 3: Remove Friends  ║ 
\033[38;2;240;0;0m            ║   4: WebHook Spam  ║ 5: Leave All Guild║ 6: Webhook Delete  ║          
\033[38;2;240;0;0m            ║   7: Token Checker ║ 8: clear screen   ║ 9: Webhook info    ║
\033[38;2;240;0;0m            ║   10: Credits      ║ 11: Close DM      ║ 12: Exit           ║
\033[38;2;240;0;0m            ║                    ║                   ║                    ║
\033[38;2;240;0;0m            ╚════════════════════╩═══════════════════╩════════════════════╝
\033[0m
"""
def menu():
    clear()
    print(Banner)
    print(options)
while True:
    menu()
    set_title("Zedo Tools")
    choice=input(f"           \033[38;2;255;15;0m (ZEDO) >\033[38;2;255;0;0m  ")
    if choice == "1":        
        clear()
        print("""Enter the path of the promo codes file""")
        PromoFiles=input(f"\033[38;2;24;76;255m (Promo Path) >\033[38;2;255;0;0m  ")
        clear()
        print("""Enter the file path where valid promo codes will be stored?""")
        filename=input(f"\033[38;2;132;24;255m (Vaild Path) >\033[38;2;255;0;0m  ")
        with open(PromoFiles) as file:
            promos=file.read().splitlines()
            for promo in promos:
                CheckPromo(promo,filename)
    elif choice == "2":
        while True:
            clear()
            token=input(f"\033[38;2;132;24;255m (Token) >\033[38;2;255;0;0m  ")
            token_stutus=is_vaild_token(token)
            time.sleep(0.70)
            if token_stutus==True:
                break
            else:
                continue
        clear()
        TokenInfo(token)
        input(">... ")
    elif choice == "3":
        while True:
            clear()
            token=input(f"\033[38;2;132;24;255m (Token) >\033[38;2;255;0;0m  ")
            token_stutus=is_vaild_token(token)
            time.sleep(0.70)
            if token_stutus==True:
                break
            else:
                continue
        clear()
        remove_all_firends(token)
        input(">... ")
    elif choice == "4":
        clear()
        webhook_url=input(f"\033[38;2;132;24;255m (Webhook Url) >\033[38;2;255;0;0m  ")
        clear()
        message=input(f"\033[38;2;132;24;255m (Message) >\033[38;2;255;0;0m  ")
        clear()
        amount=input(f"\033[38;2;132;24;255m (amount) >\033[38;2;255;0;0m  ")
        clear()
        asyncio.run(send_webhook(webhook_url,message,int(amount)))
    elif choice == "5":
        while True:
            clear()
            token=input(f"\033[38;2;132;24;255m (Token) >\033[38;2;255;0;0m  ")
            token_stutus=is_vaild_token(token)
            time.sleep(0.70)
            if token_stutus==True:
                break
            else:
                continue
        clear()
        leave_all_guild(token)
        input(">... ")
    elif choice == "6":
        clear()
        webhook_url=input(f"\033[38;2;132;24;255m (Webhook Url) >\033[38;2;255;0;0m  ")
        delete_webhook(webhook_url)
        time.sleep(0.70)

    elif choice == "7":
        clear()
        token=input(f"\033[38;2;132;24;255m (Token) >\033[38;2;255;0;0m  ")
        is_vaild_token(token)
        time.sleep(0.70)
    elif choice=="8":
        clear()
    elif choice =="9":
        clear()
        webhook_url=input(f"\033[38;2;132;24;255m (Webhook Url) >\033[38;2;255;0;0m  ")
        info_webhook(webhook_url)
        time.sleep(0.70)
    elif choice=="10":
        clear()
        print("""
\033[38;2;255;75;0m                     ╔════════════════════════════════════════════╗
\033[38;2;253;72;0m                     ║                                            ║
\033[38;2;251;69;0m                     ║        DANGER ZONE - ZEDO IS THE BEST      ║
\033[38;2;249;66;0m                     ║                                            ║
\033[38;2;247;63;0m                     ╩════════════════════════════════════════════╩
\033[38;2;245;60;0m           
        """)
    elif choice == "11":
        while True:
            clear()
            token=input(f"\033[38;2;132;24;255m (Token) >\033[38;2;255;0;0m  ")
            token_stutus=is_vaild_token(token)
            time.sleep(0.70)
            if token_stutus==True:
                break
            else:
                continue
        clear()
        close_all_dm(token)
        input(">... ")
    elif choice == "12":
        sys.exit(0)
        
    input(">... ")
    
