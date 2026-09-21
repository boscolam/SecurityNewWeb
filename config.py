"""
Configuration file for the Cybersecurity News Dashboard.
Contains default settings, feed sources, and priority rules.
"""

import os

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'cybersec_news.db')

# Default refresh interval in minutes
DEFAULT_REFRESH_INTERVAL = 30

# Maximum number of news items to keep in database
MAX_NEWS_ITEMS = 10000

# Number of days to keep news before cleanup
NEWS_RETENTION_DAYS = 90

# ============================================================
# DEFAULT RSS FEED SOURCES
# Organized by category: darkweb, rss, web news, blog,
# vendor research teams, CVE sources, Chinese vendors
# ============================================================

DEFAULT_FEEDS = [
    # --- Major Cybersecurity News (RSS) ---
    {"name": "The Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews", "category": "web_news", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "BleepingComputer", "url": "https://www.bleepingcomputer.com/feed/", "category": "web_news", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "SecurityWeek", "url": "https://www.securityweek.com/feed/", "category": "web_news", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml", "category": "web_news", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "category": "blog", "feed_type": "rss", "region": "north_america", "enabled": True},
    {"name": "Threatpost", "url": "https://threatpost.com/feed/", "category": "web_news", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "SC Magazine", "url": "https://www.scmagazine.com/feed", "category": "web_news", "feed_type": "rss", "region": "north_america", "enabled": True},
    {"name": "CSO Online", "url": "https://www.csoonline.com/index.rss", "category": "web_news", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Infosecurity Magazine", "url": "https://www.infosecurity-magazine.com/rss/news/", "category": "web_news", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CyberScoop", "url": "https://cyberscoop.com/feed/", "category": "web_news", "feed_type": "rss", "region": "north_america", "enabled": True},
    {"name": "The Record by Recorded Future", "url": "https://therecord.media/feed/", "category": "web_news", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Graham Cluley", "url": "https://grahamcluley.com/feed/", "category": "blog", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "Troy Hunt Blog", "url": "https://www.troyhunt.com/rss/", "category": "blog", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "Schneier on Security", "url": "https://www.schneier.com/feed/", "category": "blog", "feed_type": "rss", "region": "north_america", "enabled": True},

    # --- Darkweb / Threat Intelligence ---
    {"name": "DarkOwl Blog", "url": "https://www.darkowl.com/blog/rss.xml", "category": "darkweb", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Flashpoint Intel", "url": "https://flashpoint.io/feed/", "category": "darkweb", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Recorded Future Blog", "url": "https://www.recordedfuture.com/feed", "category": "darkweb", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Intel471 Blog", "url": "https://intel471.com/blog/feed/", "category": "darkweb", "feed_type": "rss", "region": "global", "enabled": True},

    # --- Vendor Security Research Teams ---
    {"name": "Palo Alto Unit42", "url": "https://unit42.paloaltonetworks.com/feed/", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Cisco Talos Blog", "url": "https://blog.talosintelligence.com/feeds/posts/default", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Microsoft Security Blog", "url": "https://www.microsoft.com/en-us/security/blog/feed/", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Google Project Zero", "url": "https://googleprojectzero.blogspot.com/feeds/posts/default", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Google TAG (Threat Analysis)", "url": "https://blog.google/threat-analysis-group/rss/", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Mandiant Blog", "url": "https://www.mandiant.com/resources/blog/rss.xml", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "CrowdStrike Blog", "url": "https://www.crowdstrike.com/blog/feed/", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "SentinelOne Labs", "url": "https://www.sentinelone.com/labs/feed/", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Trend Micro Research", "url": "https://www.trendmicro.com/en_us/research.html/rss", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Kaspersky SecureList", "url": "https://securelist.com/feed/", "category": "vendor_research", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "ESET WeLiveSecurity", "url": "https://www.welivesecurity.com/feed/", "category": "vendor_research", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "Sophos Naked Security", "url": "https://nakedsecurity.sophos.com/feed/", "category": "vendor_research", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "Fortinet Threat Research", "url": "https://feeds.fortinet.com/fortinet/blog/threat-research", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Check Point Research", "url": "https://research.checkpoint.com/feed/", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Juniper Threat Labs", "url": "https://blogs.juniper.net/en-us/threat-research/feed", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "FireEye Blog", "url": "https://www.fireeye.com/blog/feed", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Symantec Threat Intel", "url": "https://symantec-enterprise-blogs.security.com/blogs/threat-intelligence/rss", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Zscaler ThreatLabz", "url": "https://www.zscaler.com/blogs/security-research/rss", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Proofpoint Threat Insight", "url": "https://www.proofpoint.com/us/blog/threat-insight/feed", "category": "vendor_research", "feed_type": "rss", "region": "global", "enabled": True},

    # --- CVE Sources ---
    {"name": "NVD CVE Feed", "url": "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml", "category": "cve", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "CISA Known Exploited Vulns", "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml", "category": "cve", "feed_type": "rss", "region": "north_america", "enabled": True},
    {"name": "US-CERT Alerts", "url": "https://us-cert.cisa.gov/ncas/alerts.xml", "category": "cve", "feed_type": "rss", "region": "north_america", "enabled": True},
    {"name": "Cisco Security Advisories", "url": "https://tools.cisco.com/security/center/psirtrss20/CiscoSecurityAdvisory.xml", "category": "cve", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Palo Alto Security Advisories", "url": "https://security.paloaltonetworks.com/rss.xml", "category": "cve", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Fortinet PSIRT Advisories", "url": "https://www.fortiguard.com/rss/ir.xml", "category": "cve", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Checkpoint Advisories", "url": "https://advisories.checkpoint.com/defense/advisories/public/feed.rss", "category": "cve", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Juniper Security Advisories", "url": "https://kb.juniper.net/InfoCenter/index?page=rss&channel=SECURITY_ADVISORIES", "category": "cve", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Exploit-DB", "url": "https://www.exploit-db.com/rss.xml", "category": "cve", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "VulnDB", "url": "https://vuldb.com/?rss.recent", "category": "cve", "feed_type": "rss", "region": "global", "enabled": True},

    # --- Chinese Cybersecurity Vendors ---
    {"name": "Qihoo 360 Threat Intel (360)", "url": "https://blog.netlab.360.com/rss/", "category": "vendor_research", "feed_type": "rss", "region": "china", "enabled": True},
    {"name": "NSFOCUS Threat Intel", "url": "https://nsfocusglobal.com/feed/", "category": "vendor_research", "feed_type": "rss", "region": "china", "enabled": True},
    {"name": "Antiy Labs (CERT)", "url": "https://www.antiy.net/feed/", "category": "vendor_research", "feed_type": "rss", "region": "china", "enabled": True},
    {"name": "Knownsec (Seebug)", "url": "https://paper.seebug.org/rss/", "category": "vendor_research", "feed_type": "rss", "region": "china", "enabled": True},
    {"name": "QiAnXin Threat Intel", "url": "https://ti.qianxin.com/blog/rss.xml", "category": "vendor_research", "feed_type": "rss", "region": "china", "enabled": True},
    {"name": "Venustech (Topsec)", "url": "https://www.venustech.com.cn/feed/", "category": "vendor_research", "feed_type": "rss", "region": "china", "enabled": True},
    {"name": "DBAPPSecurity Blog", "url": "https://www.dbappsecurity.com.cn/feed/", "category": "vendor_research", "feed_type": "rss", "region": "china", "enabled": True},

    # --- Social / Blog Platforms ---
    {"name": "Medium - Cybersecurity", "url": "https://medium.com/feed/tag/cybersecurity", "category": "blog", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Medium - InfoSec Write-ups", "url": "https://medium.com/feed/bugbountywriteup", "category": "blog", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Reddit - r/netsec", "url": "https://www.reddit.com/r/netsec/.rss", "category": "blog", "feed_type": "rss", "region": "global", "enabled": True},
    {"name": "Reddit - r/cybersecurity", "url": "https://www.reddit.com/r/cybersecurity/.rss", "category": "blog", "feed_type": "rss", "region": "global", "enabled": True},

    # --- Government / CERT ---
    {"name": "JPCERT/CC", "url": "https://www.jpcert.or.jp/english/rss/jpcert-en.rdf", "category": "cve", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "CERT-EU News", "url": "https://cert.europa.eu/publications/security-advisories/rss", "category": "cve", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CNVD (China)", "url": "https://www.cnvd.org.cn/rss/bulletin", "category": "cve", "feed_type": "rss", "region": "china", "enabled": True},
    {"name": "AusCERT", "url": "https://auscert.org.au/rss/bulletins/", "category": "cve", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "CERT-In (India)", "url": "https://www.cert-in.org.in/Rss.jsp", "category": "cve", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
]

# ============================================================
# REGIONS
# ============================================================

REGIONS = {
    "global": "Global",
    "north_america": "North America",
    "europe": "Europe",
    "asia_pacific": "Asia Pacific",
    "china": "China",
    "middle_east": "Middle East",
    "africa": "Africa",
    "south_america": "South America",
}

# ============================================================
# NEWS CATEGORIES
# ============================================================

NEWS_CATEGORIES = {
    "hacking_incident": "Hacking Incident",
    "company_news": "Company News",
    "blog": "Blog / Analysis",
    "cve": "CVE / Vulnerability",
    "vendor_research": "Vendor Research",
    "darkweb": "Dark Web Intelligence",
    "web_news": "Web News",
    "social_media": "Social Media",
}

# ============================================================
# FEED TYPES
# ============================================================

FEED_TYPES = {
    "rss": "RSS Feed",
    "web_scrape": "Web Scraping",
    "api": "API",
    "social": "Social Media",
}

# ============================================================
# DEFAULT PRIORITY RULES
# Keywords that indicate higher priority
# ============================================================

DEFAULT_PRIORITY_RULES = {
    "critical": {
        "score": 100,
        "keywords": [
            "breach", "breached", "hacked", "ransomware", "zero-day", "0-day",
            "critical vulnerability", "actively exploited", "nation-state",
            "APT", "data leak", "data breach", "supply chain attack",
            "remote code execution", "RCE", "critical CVE", "CVSS 10",
            "CVSS 9", "emergency patch", "mass exploitation"
        ]
    },
    "high": {
        "score": 75,
        "keywords": [
            "vulnerability", "CVE-", "exploit", "malware", "phishing",
            "DDoS", "botnet", "trojan", "backdoor", "cyberattack",
            "cyber attack", "patch", "security update", "advisory",
            "threat actor", "campaign", "targeted attack", "spyware",
            "rootkit", "privilege escalation"
        ]
    },
    "medium": {
        "score": 50,
        "keywords": [
            "security", "privacy", "compliance", "regulation", "GDPR",
            "encryption", "authentication", "authorization", "firewall",
            "intrusion", "detection", "prevention", "audit", "risk",
            "assessment", "penetration test", "bug bounty"
        ]
    },
    "low": {
        "score": 25,
        "keywords": [
            "conference", "training", "certification", "career",
            "market", "acquisition", "partnership", "funding",
            "report", "survey", "study", "research", "whitepaper"
        ]
    }
}

# Hacking incident keywords (always top priority)
HACKING_INCIDENT_KEYWORDS = [
    "breach", "breached", "hacked", "hack", "ransomware", "ransom",
    "data leak", "data stolen", "compromised", "attack on", "attacked",
    "defaced", "ddos attack", "phishing attack", "malware attack",
    "supply chain compromise", "unauthorized access", "cyber incident",
    "security incident", "data exposure", "leaked", "exploitation",
    "mass exploitation", "zero-day attack", "0-day attack"
]

# CVE pattern for detection
CVE_PATTERN = r'CVE-\d{4}-\d{4,7}'

# Vendor-specific CVE keywords
CVE_VENDOR_KEYWORDS = {
    "cisco": ["cisco", "ios xe", "ios xr", "asa", "firepower", "webex", "nexus", "catalyst"],
    "paloaltonetworks": ["palo alto", "pan-os", "panorama", "cortex", "prisma", "globalprotect"],
    "fortinet": ["fortinet", "fortigate", "fortios", "fortimanager", "fortianalyzer", "fortiweb"],
    "checkpoint": ["check point", "checkpoint", "gaia", "smartconsole", "cloudguard"],
    "juniper": ["juniper", "junos", "srx", "mx series", "ex series", "qfx"],
    "qihoo360": ["360", "qihoo", "netlab"],
    "nsfocus": ["nsfocus"],
    "antiy": ["antiy", "antiylab"],
    "knownsec": ["knownsec", "seebug", "zoomeye"],
    "qianxin": ["qianxin", "qi-anxin", "奇安信"],
}
