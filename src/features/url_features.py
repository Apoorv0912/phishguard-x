



# -*- coding: utf-8 -*-

# =========================
# IMPORTING REQUIRED PACKAGES
# =========================

from urllib.parse import urlparse
import ipaddress
import re
import socket
import io
from contextlib import redirect_stdout, redirect_stderr
from functools import lru_cache
from datetime import datetime
from pathlib import Path

import requests
import whois

# =========================
# TRANCO RANKING DATA
# =========================

TRANCO_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "tranco_top100k.csv"
)

TRANCO_RANK = {}

try:
    with open(TRANCO_FILE, "r", encoding="utf-8") as file:

        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split(",", 1)

            if len(parts) == 2:
                rank = parts[0].strip()
                domain = parts[1].strip().lower()

                try:
                    TRANCO_RANK[domain] = int(rank)
                except ValueError:
                    pass

    print("Tranco domains loaded:", len(TRANCO_RANK))

except Exception as e:
    print("Tranco file loading failed:", e)


# =========================
# 1. DOMAIN OF THE URL
# =========================

def getDomain(url):
    domain = urlparse(url).hostname

    if domain is None:
        return ""

    domain = domain.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


# =========================
# 2. IP ADDRESS IN URL
# =========================

def havingIP(url):
    try:
        ipaddress.ip_address(urlparse(url).netloc.split(":")[0])
        return 1
    except:
        return 0


# =========================
# 3. @ SYMBOL IN URL
# =========================

def haveAtSign(url):
    if "@" in url:
        return 1
    else:
        return 0


# =========================
# 4. URL LENGTH
# =========================

def getLength(url):
    if len(url) < 54:
        return 0
    else:
        return 1


# =========================
# 5. URL DEPTH
# =========================

def getDepth(url):
    s = urlparse(url).path.split("/")
    depth = 0

    for j in range(len(s)):
        if len(s[j]) != 0:
            depth = depth + 1

    return depth


# =========================
# 6. REDIRECTION //
# =========================

def redirection(url):
    pos = url.rfind("//")

    if pos > 6:
        if pos > 7:
            return 1
        else:
            return 0
    else:
        return 0


# =========================
# 7. HTTPS TOKEN IN DOMAIN
# =========================

def httpDomain(url):
    domain = urlparse(url).netloc

    if "https" in domain:
        return 1
    else:
        return 0


# =========================
# 8. URL SHORTENING SERVICES
# =========================

shortening_services = (
    r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|"
    r"tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|"
    r"url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|"
    r"budurl\.com|ping\.fm|post\.ly|just\.as|bkite\.com|snipr\.com|"
    r"fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|"
    r"om\.ly|to\.ly|bit\.do|lnkd\.in|db\.tt|qr\.ae|adf\.ly|bitly\.com|"
    r"cur\.lv|tinyurl\.com|ity\.im|q\.gs|po\.st|bc\.vc|twitthis\.com|"
    r"u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|prettylinkpro\.com|"
    r"scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|"
    r"v\.gd|link\.zip\.net"
)


def tinyURL(url):
    match = re.search(shortening_services, url, re.IGNORECASE)

    if match:
        return 1
    else:
        return 0


# =========================
# 9. PREFIX / SUFFIX "-"
# =========================

def prefixSuffix(url):
    if "-" in urlparse(url).netloc:
        return 1
    else:
        return 0


# =========================
# 11. DNS RECORD
# =========================

# DNS feature is calculated inside featureExtraction()

# =========================
# CACHED WHOIS LOOKUP
# =========================

WHOIS_TIMEOUT = 3


@lru_cache(maxsize=10000)
def get_whois_cached(domain):

    old_timeout = socket.getdefaulttimeout()

    try:

        socket.setdefaulttimeout(WHOIS_TIMEOUT)

        # Suppress WHOIS socket error messages
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):

            return whois.whois(domain)

    except Exception:

        return None

    finally:

        socket.setdefaulttimeout(old_timeout)


# =========================
# 12. WEB TRAFFIC
# =========================

def web_traffic(url):
    """
    Web Traffic feature using local Tranco ranking data.

    Top 100,000 domains -> 1
    Domains outside Top 100,000 / not found -> 0
    """

    try:
        domain = getDomain(url).lower().strip()

        if not domain:
            return 0

        # Direct domain lookup
        rank = TRANCO_RANK.get(domain)

        # Try root domain if subdomain is not found
        if rank is None:

            parts = domain.split(".")

            if len(parts) >= 2:
                root_domain = ".".join(parts[-2:])
                rank = TRANCO_RANK.get(root_domain)

        # Domain not present in Tranco
        if rank is None:
            return 0

        # Top 100,000 domains
        if rank <= 100000:
            return 1
        else:
            return 0

    except Exception:
        return 0


# =========================
# 13. DOMAIN AGE
# =========================

def domainAge(domain_name):

    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date

    if creation_date is None or expiration_date is None:
        return 1

    # WHOIS can return a list of dates
    if isinstance(creation_date, list):
        creation_date = creation_date[0]

    if isinstance(expiration_date, list):
        expiration_date = expiration_date[0]

    # Convert string dates if required
    if isinstance(creation_date, str):
        try:
            creation_date = datetime.strptime(
                creation_date,
                "%Y-%m-%d"
            )
        except:
            return 1

    if isinstance(expiration_date, str):
        try:
            expiration_date = datetime.strptime(
                expiration_date,
                "%Y-%m-%d"
            )
        except:
            return 1

    try:
        ageofdomain = abs(
            (expiration_date - creation_date).days
        )
    except:
        return 1

    # Existing project logic preserved
    if (ageofdomain / 30) < 6:
        return 1
    else:
        return 0


# =========================
# 14. DOMAIN END
# =========================

def domainEnd(domain_name):

    expiration_date = domain_name.expiration_date

    if expiration_date is None:
        return 1

    # WHOIS can return a list of dates
    if isinstance(expiration_date, list):
        expiration_date = expiration_date[0]

    # Convert string date if required
    if isinstance(expiration_date, str):
        try:
            expiration_date = datetime.strptime(
                expiration_date,
                "%Y-%m-%d"
            )
        except:
            return 1

    try:
        if expiration_date.tzinfo:
            today = datetime.now(expiration_date.tzinfo)
        else:
            today = datetime.now()

        end = abs(
            (expiration_date - today).days
        )

    except:
        return 1

    # Existing project logic preserved
    if (end / 30) < 6:
        return 0
    else:
        return 1


# =========================
# 15. IFRAME
# =========================

def iframe(response):

    if response == "":
        return 1

    else:
        if re.findall(
            r"<iframe|<frameBorder",
            response.text,
            re.IGNORECASE
        ):
            return 0
        else:
            return 1


# =========================
# 16. MOUSE OVER
# =========================

def mouseOver(response):

    if response == "":
        return 1

    else:
        if re.findall(
            r"<script>.+onmouseover.+</script>",
            response.text,
            re.IGNORECASE
        ):
            return 1
        else:
            return 0


# =========================
# 17. RIGHT CLICK
# =========================

def rightClick(response):

    if response == "":
        return 1

    else:
        if re.findall(
            r"event\.button\s*==\s*2",
            response.text,
            re.IGNORECASE
        ):
            return 0
        else:
            return 1


# =========================
# 18. WEBSITE FORWARDING
# =========================

def forwarding(response):

    if response == "":
        return 1

    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1


# =========================
# FEATURE EXTRACTION
# =========================

def featureExtraction(url, label):

    features = []

    # -------------------------
    # Address bar based features
    # -------------------------

    features.append(getDomain(url))
    features.append(havingIP(url))
    features.append(haveAtSign(url))

    features.append(getLength(url))
    features.append(getDepth(url))
    features.append(redirection(url))
    features.append(httpDomain(url))
    features.append(tinyURL(url))
    features.append(prefixSuffix(url))


    # -------------------------
    # Domain based features
    # -------------------------

    dns = 0
    domain_name = None

    # Extract domain
    domain = urlparse(url).netloc.split(":")[0]

    # DNS check
    try:
        socket.gethostbyname(domain)
    except Exception:
        dns = 1

    # WHOIS check
    if dns == 0:
        domain_name = get_whois_cached(domain)


    # DNS Record
    features.append(dns)

    # Web Traffic
    features.append(web_traffic(url))

    # Domain Age
    features.append(
        1 if domain_name is None
        else domainAge(domain_name)
    )

    # Domain End
    features.append(
        1 if domain_name is None
        else domainEnd(domain_name)
    )


    # -------------------------
    # HTML & JavaScript features
    # -------------------------

    try:

        response = requests.get(
            url,
            timeout=5,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        )

    except requests.RequestException:

        response = ""


    # IFrame
    features.append(iframe(response))

    # Mouse Over
    features.append(mouseOver(response))

    # Right Click
    features.append(rightClick(response))

    # Web Forwarding
    features.append(forwarding(response))


    # Label
    features.append(label)


    return features


# =========================
# FEATURE NAMES
# =========================

feature_names = [
    "Domain",
    "Have_IP",
    "Have_At",
    "URL_Length",
    "URL_Depth",
    "Redirection",
    "https_Domain",
    "TinyURL",
    "Prefix/Suffix",
    "DNS_Record",
    "Web_Traffic",
    "Domain_Age",
    "Domain_End",
    "iFrame",
    "Mouse_Over",
    "Right_Click",
    "Web_Forwards",
    "Label"
]