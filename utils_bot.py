import logging 
 import os 
 import threading 
 import time 
 import aiohttp 
 from asyncio import TimeoutError 
 from pyrogram import filters 
 from Adarsh.vars import Var 
  
 logger = logging.getLogger(__name__) 
 SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'] 
  
 class setInterval: 
     def __init__(self, interval, action): 
         self.interval = interval 
         self.action = action 
         self.stopEvent = threading.Event() 
         thread = threading.Thread(target=self.__setInterval) 
         thread.start() 
  
     def __setInterval(self): 
         nextTime = time.time() + self.interval 
         while not self.stopEvent.wait(nextTime - time.time()): 
             nextTime += self.interval 
             self.action() 
  
     def cancel(self): 
         self.stopEvent.set() 
  
  
 def get_readable_file_size(size_in_bytes) -> str: 
     if size_in_bytes is None: 
         return '0B' 
     index = 0 
     while size_in_bytes >= 1024: 
         size_in_bytes /= 1024 
         index += 1 
     try: 
         return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}' 
     except IndexError: 
         return 'File too large' 
  
  
 def get_readable_time(seconds: int) -> str: 
     result = '' 
     (days, remainder) = divmod(seconds, 86400) 
     days = int(days) 
     if days != 0: 
         result += f'{days}d' 
     (hours, remainder) = divmod(remainder, 3600) 
     hours = int(hours) 
     if hours != 0: 
         result += f'{hours}h' 
     (minutes, seconds) = divmod(remainder, 60) 
     minutes = int(minutes) 
     if minutes != 0: 
         result += f'{minutes}m' 
     seconds = int(seconds) 
     result += f'{seconds}s' 
     return result 
  
  
  
 def readable_time(seconds: int) -> str: 
     result = '' 
     (days, remainder) = divmod(seconds, 86400) 
     days = int(days) 
     if days != 0: 
         result += f'{days}d' 
     (hours, remainder) = divmod(remainder, 3600) 
     hours = int(hours) 
     if hours != 0: 
         result += f'{hours}h' 
     (minutes, seconds) = divmod(remainder, 60) 
     minutes = int(minutes) 
     if minutes != 0: 
         result += f'{minutes}m' 
     seconds = int(seconds) 
     result += f'{seconds}s' 
     return result 
  
URL_SHORTENR_WEBSITE = "onepagelink.in" 
URL_SHORTNER_WEBSITE_API = "c47e1c4469c0a66e74af73153cb8f4d3b304d010" 
  
 async def get_shortlink(link): 
     https = link.split(":")[0] 
     if "http" == https: 
         https = "https" 
         link = link.replace("http", https) 
     url = f'https://{URL_SHORTENR_WEBSITE}/api' 
     params = {'api': URL_SHORTNER_WEBSITE_API, 
               'url': link, 
               } 
  
     try: 
         async with aiohttp.ClientSession() as session: 
             async with session.get(url, params=params, raise_for_status=True, ssl=False) as response: 
                 data = await response.json() 
                 if data["status"] == "success": 
                     return data['shortenedUrl'] 
                 else: 
                     logger.error(f"Error: {data['message']}") 
                     return f'https://{URL_SHORTENR_WEBSITE}/api?api={URL_SHORTNER_WEBSITE_API}&link={link}' 
  
     except Exception as e: 
         logger.error(e) 
         return f'{URL_SHORTENR_WEBSITE}/api?api={URL_SHORTNER_WEBSITE_API}&link={link}'  
 
