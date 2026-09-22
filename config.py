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

    # --- Government CERTs (from Pulsedive certrss) ---
    # Source: https://github.com/pulsedive/certrss
    # Updated: 2026-08-16

    # North America
    {"name": "CISA (US) - News", "url": "https://www.cisa.gov/uscert/ncas/all.xml", "category": "government", "feed_type": "rss", "region": "north_america", "enabled": True},
    {"name": "CISA (US) - Advisories", "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml", "category": "government", "feed_type": "rss", "region": "north_america", "enabled": True},
    {"name": "Canadian Cyber Centre - News", "url": "https://cyber.gc.ca/webservice/en/rss/news", "category": "government", "feed_type": "rss", "region": "north_america", "enabled": True},
    {"name": "Canadian Cyber Centre - Alerts", "url": "https://cyber.gc.ca/webservice/en/rss/alerts", "category": "government", "feed_type": "rss", "region": "north_america", "enabled": True},

    # Europe
    {"name": "CERT-EU - Advisories", "url": "https://cert.europa.eu/publications/security-advisories-rss", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT-EU - Threat Intel", "url": "https://cert.europa.eu/publications/threat-intelligence-rss", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "UK NCSC - All", "url": "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "UK NCSC - News", "url": "https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "NCSC Finland - News", "url": "https://www.kyberturvallisuuskeskus.fi/feed/rss/en", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "NCSC Finland - Vulnerabilities", "url": "https://www.kyberturvallisuuskeskus.fi/sites/default/files/rss/vulns.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT-FR", "url": "https://www.cert.ssi.gouv.fr/feed/", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT.at", "url": "https://cert.at/cert-at.en.blog.rss_2.0.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT.BE - News", "url": "https://ccb.belgium.be/news.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT.BE - Advisories", "url": "https://ccb.belgium.be/advisories.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "NCSC NL - News", "url": "https://feeds.ncsc.nl/nieuws.rss", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "NCSC NL - Advisories", "url": "https://advisories.ncsc.nl/rss/advisories", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "Swiss GovCERT", "url": "https://www.newsd.admin.ch/newsd/feeds/rss?lang=en&org-nr=1101", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT.PL", "url": "https://cert.pl/en/rss.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT.hr (Croatia)", "url": "https://www.cert.hr/feed/", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "NUKIB (Czech)", "url": "https://nukib.gov.cz/rss.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "DKCERT (Denmark)", "url": "https://www.cert.dk/news/rss", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT-EE (Estonia)", "url": "https://www.ria.ee/et/news-feed/all/feed", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CSIRT Italia", "url": "https://www.acn.gov.it/portale/feedrss/-/journal/rss/20119/723192", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT.LV (Latvia)", "url": "https://cert.lv/en/feed/rss/all", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "NSM NCSC (Norway)", "url": "https://nsm.no/fagomrader/digital-sikkerhet/nasjonalt-cybersikkerhetssenter/varsler-fra-ncsc/rss/", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT.RO (Romania)", "url": "https://dnsc.ro/feed", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "SI-CERT (Slovenia)", "url": "https://www.cert.si/en/category/news/feed/", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CCN-CERT (Spain)", "url": "https://www.ccn-cert.cni.es/en/communication-events/articles-and-reports.rss", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "INCIBE-CERT (Spain)", "url": "https://www.incibe.es/en/incibe-cert/alerta-temprana/avisos/feed", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT-SE (Sweden)", "url": "https://www.cert.se/feed.rss", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CERT-UA (Ukraine)", "url": "https://cert.gov.ua/api/articles/rss", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "NCSC Hungary", "url": "https://nki.gov.hu/figyelmeztetesek/riasztas/feed/", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},
    {"name": "CNCS Portugal", "url": "https://www.cncs.gov.pt/docs/noticias/feed-rss/index.xml", "category": "government", "feed_type": "rss", "region": "europe", "enabled": True},

    # Asia Pacific
    {"name": "AusCERT - Bulletins", "url": "https://portal.auscert.org.au/rss/bulletins/", "category": "government", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "JPCERT/CC - News", "url": "https://www.jpcert.or.jp/english/rss/jpcert-en.rdf", "category": "government", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "JPCERT/CC - Blog", "url": "https://blogs.jpcert.or.jp/en/atom.xml", "category": "government", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "SingCERT (Singapore)", "url": "https://www.csa.gov.sg/Content/RSS-Feed", "category": "government", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "GovCERT.HK", "url": "https://www.govcert.gov.hk/en/rss_security_alerts.xml", "category": "government", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "HKCERT", "url": "https://www.hkcert.org/getrss/security-bulletin", "category": "government", "feed_type": "rss", "region": "asia_pacific", "enabled": True},

    # South America
    {"name": "CERT.br (Brazil)", "url": "https://www.cert.br/rss/certbr-rss.xml", "category": "government", "feed_type": "rss", "region": "south_america", "enabled": True},

    # Middle East & Africa
    {"name": "EG-CERT (Egypt)", "url": "https://egcert.eg/feed/", "category": "government", "feed_type": "rss", "region": "africa", "enabled": True},
    {"name": "BGD e-GOV CIRT (Bangladesh)", "url": "https://www.cirt.gov.bd/feed/", "category": "government", "feed_type": "rss", "region": "asia_pacific", "enabled": True},
    {"name": "NISSA (Libya)", "url": "https://nissa.gov.ly/feed/", "category": "government", "feed_type": "rss", "region": "africa", "enabled": True},
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
    "hong_kong": "Hong Kong",
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
    "government": "Government CERT",
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
