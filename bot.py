from curl_cffi import requests
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, base64, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class NodeGo:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://app.nodego.ai",
            "Referer": "https://app.nodego.ai/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random
        }
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Ping {Fore.BLUE + Style.BRIGHT}NodeGo - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Join: {Fore.YELLOW + Style.BRIGHT}https://t.me/D4rkCipherX
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                response = await asyncio.to_thread(requests.get, "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt")
                response.raise_for_status()
                content = response.text
                with open(filename, 'w') as f:
                    f.write(content)
                self.proxies = content.splitlines()
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = f.read().splitlines()
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def decode_token(self, token: str):
        try:
            header, payload, signature = token.split(".")
            decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
            parsed_payload = json.loads(decoded_payload)
            email = parsed_payload["email"]
            
            return email
        except Exception as e:
            return None
    
    def mask_account(self, account):
        if '@' in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"
    
    def print_message(self, account, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {account} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print("1. Run With Monosans Proxy")
                print("2. Run With Private Proxy")
                print("3. Run Without Proxy")
                choose = int(input("Choose [1/2/3] -> ").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "Run With Monosans Proxy" if choose == 1 else 
                        "Run With Private Proxy" if choose == 2 else 
                        "Run Without Proxy"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{proxy_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        nodes_count = 0
        if choose in [1, 2]:
            while True:
                try:
                    nodes_count = int(input("How Many Nodes Do You Want to Run For Each Account? -> "))
                    if nodes_count > 0:
                        break
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        return nodes_count, choose

    async def user_data(self, token: str, email: str, use_proxy: bool, proxy=None, retries=5):
        url = "https://nodego.ai/api/user/me"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="safari15_5")
                response.raise_for_status()
                result = response.json()
                return result["metadata"]
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                if not "520" in str(e):
                    self.rotate_proxy_for_account(email) if use_proxy else None

                return self.print_message(self.mask_account(email), proxy, Fore.RED, 
                    f"GET User Data Failed: "
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
            
    async def claim_checkin(self, token: str, email: str, day_checkin: int, proxy=None, retries=5):
        url = "https://nodego.ai/api/user/checkin"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": "0"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 400:
                    return self.print_message(self.mask_account(email), proxy, Fore.WHITE, 
                        f"Check-In Day {day_checkin}"
                        f"{Fore.RED + Style.BRIGHT} Isn't Claimed: {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Already Claimed{Style.RESET_ALL}"
                    )
                
                response.raise_for_status()
                result = response.json()
                return result["metadata"]
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(self.mask_account(email), proxy, Fore.RED, 
                    f"Checkin Day {day_checkin} Isn't Claimed: "
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )

    async def task_lists(self, token: str, email: str, proxy=None, retries=5):
        url = "https://nodego.ai/api/tasks"
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.get, url=url, headers=headers, proxy=proxy, timeout=60, impersonate="safari15_5")
                response.raise_for_status()
                result = response.json()
                return result["metadata"]
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(self.mask_account(email), proxy, Fore.RED, 
                    f"GET Available Tasks Failed: "
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
            
    async def complete_tasks(self, token: str, email: str, task_id: str, title: str, proxy=None, retries=5):
        url = "https://nodego.ai/api/user/task"
        data = json.dumps({"taskId":task_id})
        headers = {
            **self.headers,
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 400:
                    return self.print_message(self.mask_account(email), proxy, Fore.WHITE, 
                        f"Task {title}"
                        f"{Fore.RED + Style.BRIGHT} Isn't Completed: {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Not Eligible{Style.RESET_ALL}"
                    )
                
                response.raise_for_status()
                result = response.json()
                return result["metadata"]
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(self.mask_account(email), proxy, Fore.RED, 
                    f"Task {title} Isn't Completed: "
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )
            
    async def send_ping(self, token: str, email: str, num_id: int, proxy=None, retries=5):
        url = "https://nodego.ai/api/user/nodes/ping"
        data = json.dumps({"type":"extension"})
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": f"Bearer {token}",
            "Content-Length": str(len(data)),
            "Content-Type": "application/json",
            "Origin": "chrome-extension://jbmdcnidiaknboflpljihfnbonjgegah",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Storage-Access": "active",
            "User-Agent": FakeUserAgent().random
        }
        for attempt in range(retries):
            try:
                response = await asyncio.to_thread(requests.post, url=url, headers=headers, data=data, proxy=proxy, timeout=60, impersonate="safari15_5")
                if response.status_code == 429:
                    return self.print_message(self.mask_account(email), proxy, Fore.WHITE, 
                        f"Node {num_id} "
                        f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} PING Failed: {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Too many request!{Style.RESET_ALL}"
                    )
                response.raise_for_status()
                result = response.json()
                return result["metadata"]
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue

                return self.print_message(self.mask_account(email), proxy, Fore.WHITE, 
                    f"Node {num_id} "
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} PING Failed: {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}{str(e)}{Style.RESET_ALL}"
                )

    async def process_daily_checkin(self, user, token: str, email: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None

            day_checkin = user.get("checkinDay", 0)

            claim = await self.claim_checkin(token, email, day_checkin, proxy)
            if claim:
                message = claim.get("message", "N/A")
                self.print_message(self.mask_account(email), proxy, Fore.WHITE, 
                    f"Check-In Day {day_checkin+1}"
                    f"{Fore.GREEN + Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT} Reward: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{message}{Style.RESET_ALL}"
                )

            await asyncio.sleep(12 * 60 * 60)

    async def process_complete_tasks(self, user, token: str, email: str, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None

            completed_tasks = user.get("socialTask", [])
            tasks = await self.task_lists(token, email, proxy)
            if tasks:
                for task in tasks:
                    if task:
                        task_id = task.get("code")
                        title = task.get("title")
                        reward = task.get("reward")

                        if task_id in completed_tasks:
                            continue

                        complete = await self.complete_tasks(token, email, task_id, title, proxy)
                        if complete and complete.get("message") == "Task claimed successfully":
                            self.print_message(self.mask_account(email), proxy, Fore.WHITE, 
                                f"Task {title}"
                                f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.CYAN + Style.BRIGHT} Reward: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{reward} PTS{Style.RESET_ALL}"
                            )

            await asyncio.sleep(24 * 60 * 60)

    async def process_send_ping(self, token: str, email: str, num_id: int, use_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(num_id) if use_proxy else None

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Try to Sent Ping...{Style.RESET_ALL}                                   ",
                end="\r",
                flush=True
            )

            ping = await self.send_ping(token, email, num_id, proxy)
            if ping:
                message = ping.get("message")
                self.print_message(self.mask_account(email), proxy, Fore.WHITE, 
                    f"Node {num_id}"
                    f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}{message}{Style.RESET_ALL}"
                )

            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Wait For 10 Minutes For Next Ping...{Style.RESET_ALL}",
                end="\r"
            )
            await asyncio.sleep(10 * 60)

    async def process_get_user_data(self, token: str, email: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(email) if use_proxy else None

        user = None
        while user is None:
            user = await self.user_data(token, email, use_proxy, proxy)
            if not user:
                await asyncio.sleep(5)
                continue

            self.print_message(self.mask_account(email), proxy, Fore.GREEN, 
                f"GET User Data Success"
            )
            return user
        
    async def process_accounts(self, token: str, email: str, node_count: int, use_proxy: bool):
        user = await self.process_get_user_data(token, email, use_proxy)
        if user:

            tasks = []
            tasks.append(asyncio.create_task(self.process_daily_checkin(user, token, email, use_proxy)))
            tasks.append(asyncio.create_task(self.process_complete_tasks(user, token, email, use_proxy)))
            if use_proxy:
                for i in range(node_count):
                    num_id = i + 1
                    tasks.append(asyncio.create_task(self.process_send_ping(token, email, num_id, use_proxy)))

            else:
                num_id = 1
                tasks.append(asyncio.create_task(self.process_send_ping(token, email, num_id, use_proxy)))

            await asyncio.gather(*tasks)
        
    async def main(self):
        try:
            with open('tokens.txt', 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]

            node_count, use_proxy_choice = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(tokens)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

            while True:
                tasks = []
                for token in tokens:
                    if token:
                        email = self.decode_token(token)

                        if "@" in email:
                            tasks.append(asyncio.create_task(self.process_accounts(token, email, node_count, use_proxy)))

                await asyncio.gather(*tasks)
                await asyncio.sleep(10)

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'tokens.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise

if __name__ == "__main__":
    try:
        bot = NodeGo()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] NodeGo - BOT{Style.RESET_ALL}                                       "                              
        )
