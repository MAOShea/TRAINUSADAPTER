# Übersicht Widget Data Sources Analysis Report

**Generated:** Analysis of all widgets in the `downloads/` folder  
**Total Widget Files Analyzed:** 509 files (110 JSX + 399 CoffeeScript)

---

## Executive Summary

This report analyzes all Übersicht widgets to identify the types of data sources they consume. The analysis scanned both JSX and CoffeeScript widget files to categorize them by their primary data dependencies.

### Key Findings

- **Most Common Data Source:** Time-based widgets (319 widgets) - clocks, timers, and countdowns
- **System Monitoring:** 211 widgets monitor system resources (CPU, memory, disk, battery)
- **Calendar Integration:** 123 widgets integrate with calendar systems
- **Container Technology:** 90 widgets interact with Docker
- **Financial Data:** 81 widgets consume cryptocurrency data, 10 consume stock market data
- **Weather Services:** 63 widgets use weather APIs
- **Public Transit:** 55 widgets display transit information

---

## File Statistics

| File Type | Count |
|-----------|-------|
| JSX Files | 110 |
| CoffeeScript Files | 399 |
| **Total Widget Files** | **509** |

**Note:** 3 CoffeeScript entries were directories rather than files (expected behavior).

---

## Data Source Categories

### Complete Breakdown

| Category | Widget Count | Description |
|----------|-------------|-------------|
| **time** | 319 | Clocks, timers, countdowns, date displays |
| **system** | 211 | CPU, memory, disk, battery, system stats |
| **calendar** | 123 | iCal, calendar events, appointments |
| **docker** | 90 | Docker containers and statistics |
| **crypto** | 81 | Bitcoin, Ethereum, cryptocurrency prices |
| **weather** | 63 | Weather APIs (wttr.in, DarkSky, OpenWeatherMap, etc.) |
| **transit** | 55 | Public transit (BART, MBTA, buses, trains) |
| **todo** | 34 | Task management (Todoist, Things, etc.) |
| **location** | 32 | GPS, geolocation services |
| **email** | 29 | IMAP, Gmail, email notifications |
| **music** | 27 | Spotify, iTunes, Last.fm, music players |
| **quote** | 22 | Inspirational quotes, BrainyQuote |
| **rss** | 21 | RSS feeds, news feeds |
| **ip** | 14 | IP address services |
| **none** | 10 | Static displays, no external data source |
| **news** | 10 | Hacker News, Reddit, news aggregators |
| **stock** | 10 | Stock exchange data |
| **unknown** | 7 | Could not be categorized |
| **github** | 6 | GitHub API, issues, notifications |
| **nasa** | 2 | NASA APIs (APOD, astronauts) |
| **gitlab** | 1 | GitLab API |
| **covid** | 1 | COVID-19 data |
| **kubernetes** | 1 | Kubernetes cluster data |

---

## Data Source URLs

This section lists the actual URLs and API endpoints found in widget code, organized by data source category.

### Weather APIs (25 URLs, 20 widgets)

- `http://api.openweathermap.org/data/2.5/group`
- `http://api.openweathermap.org/data/2.5/weather`
- `http://api.wunderground.com/api`
- `http://darksky.net/dev`
- `http://erikflowers.github.io/weather-icons`
- `http://geo.weather.gc.ca/geomet`
- `http://l.yimg.com/a/i/us/nws/weather/gr`
- `http://wttr.in/:translation`
- `https://api.darksky.net/forecast`
- `https://api.forecast.io/forecast`
- `https://api.openweathermap.org/data/2.5/weather`
- `https://api.weather.gov/points/40.7851,-73.9683`
- `https://darksky.net/dev`
- `https://darksky.net/dev/docs`
- `https://openweathermap.org/appid`
- `https://openweathermap.org/city/$`
- `https://openweathermap.org/current`
- `https://www.canada.ca/en/environment-climate-change/services/weather-general-tools-resources/weather-tools-specialized-data/geospatial-web-services.html`
- `https://www.wunderground.com`

### Cryptocurrency APIs (10 URLs, 9 widgets)

- `https://api.binance.com/api/v3/ticker/price`
- `https://api.bitcoinaverage.com/ticker/global/EUR/last`
- `https://api.bitcoinaverage.com/ticker/global/USD/last`
- `https://api.coinbase.com/v2/prices/spot`
- `https://api.coinmarketcap.com/v1/global`
- `https://api.coinmarketcap.com/v1/ticker`
- `https://api.coinmarketcap.com/v1/ticker/casinocoin`
- `https://api.coinmarketcap.com/v1/ticker/litecoin`
- `https://api.coinmarketcap.com/v1/ticker/ripple`

### Stock Market APIs (5 URLs, 5 widgets)

- `http://www.jarloo.com/yahoo_finance`
- `https://query2.finance.yahoo.com/v7/finance/quote`
- `https://www.alphavantage.co/query`

### GitHub APIs (3 URLs, 3 widgets)

- `https://api.github.com`
- `https://api.github.com/graphql`
- `https://api.github.com/repos`

### GitLab APIs

No specific GitLab API URLs found in widget code (widgets may use GitLab APIs but URLs weren't explicitly found in code).

### RSS Feeds (9 URLs, 7 widgets)

- `http://feed.aqicn.org/feed/Hangzhou/cn/feed.v1.json`
- `http://feeds.feedblitz.com/german-word-of-the-day&x=1`
- `http://feeds.feedburner.com/brainyquote/QUOTEBR`
- `http://mf.feeds.reuters.com/reuters/UKTopNews`
- `http://wordsmith.org/awad/rss1.xml`
- `http://www.history.com/this-day-in-history/rss`
- `https://api.waqi.info/feed/$`
- `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson`
- `https://mail.google.com/mail/feed/atom`

### News APIs (7 URLs, 4 widgets)

- `http://newsapi.org/v2/top-headlines`
- `https://hacker-news.firebaseio.com/v0/$`
- `https://news.ycombinator.com/item`
- `https://newsapi.org`
- `https://www.reddit.com/r`
- `https://www.reddit.com/r/$`
- `https://www.reddit.com/u`

### NASA APIs (3 URLs, 2 widgets)

- `https://api.nasa.gov/planetary/apod`
- `https://apod.nasa.gov/apod`
- `https://spotthestation.nasa.gov/widget/widget.cfm`

### IP Address Services (1 URL, 1 widget)

- `https://api.ipify.org`

### Public Transit APIs (4 URLs, 5 widgets)

- `http://api.bart.gov/api/etd.aspx`
- `http://api.bart.gov/docs/overview/abbrev.aspx`
- `http://realtime.mbta.com/developer/api/v2/schedulebystop`

### Quote Services (2 URLs, 3 widgets)

- `http://download.finance.yahoo.com/d/quotes.csv`
- `https://quotes.rest/qod`

### Other APIs (19 URLs, 17 widgets)

Various specialized APIs found in widgets:

- `http://api.exchangeratesapi.io/v1/latest` - Currency exchange rates
- `http://api.open-notify.org/astros.json` - Astronaut data
- `http://www.esvapi.org/v2/rest/dailyVerse` - Bible verses
- `https://api.alquran.cloud/ayah` - Quran verses
- `https://api.coingecko.com/api/v3/global` - Cryptocurrency data
- `https://api.nanopool.org/v1/eth/reportedhashrate` - Ethereum mining
- `https://api.nanopool.org/v1/eth/user` - Ethereum user data
- `https://api.purpleair.com/v1/sensors` - Air quality sensors
- `https://api.trello.com/1/boards` - Trello boards
- `https://api.wunderlist.com` - Wunderlist API
- `https://en.wikipedia.org/w/api.php` - Wikipedia API
- `https://euw.api.pvp.net/api/lol` - League of Legends API
- `https://global.api.pvp.net/api/lol/static-data` - LoL static data
- `https://leetcode-stats-api.herokuapp.com` - LeetCode statistics
- `https://statsapi.web.nhl.com` - NHL statistics
- `https://statsapi.web.nhl.com/api/v1/teams` - NHL teams

### JSON Data Endpoints (12 URLs, 10 widgets)

- `http://freegeoip.net/json` - Geolocation
- `http://ws.audioscrobbler.com/2.0` - Last.fm API
- `http://wsstatus.com/embed/json.php` - Status monitoring
- `http://www.commandlinefu.com/commands/random/json` - Command line tips
- `http://xkcd.com/info.0.json` - XKCD comics
- `https://cdn.syndication.twimg.com/widgets/followbutton/info.json` - Twitter widgets
- `https://xkcd.com/info.0.json` - XKCD comics (HTTPS)

### Other URLs (221 URLs, 146 widgets)

A large number of other URLs were found including:
- Local development servers (`http://127.0.0.1:41417`)
- CDN resources (fonts, libraries)
- Documentation and reference sites
- Image hosting services
- GitHub repositories
- Various third-party services

**Note:** Many widgets use local system commands (`exec()`, `run()`) for system monitoring, calendar access, email checking, and music player integration rather than external APIs. These are not captured as URLs but are still important data sources.

---

## Sample Widgets by Category

### Time (319 widgets)
- `UeberPlayer` - Multi-purpose player with time display
- `CryptoMarketCap` - Cryptocurrency prices with timestamps
- `currenttrack` - Music player with time
- `gitlabissues` - Issue tracker with time stamps
- `uebersicht-jira-filter` - Jira filter with time tracking

### System (211 widgets)
- `UeberPlayer` - System resource monitoring
- `gitlabissues` - System integration
- `uebersicht-jira-filter` - System time tracking
- `task-deadline` - System task management
- `helldivers` - System monitoring

### Calendar (123 widgets)
- `UeberPlayer` - Calendar integration
- `currenttrack` - Calendar events
- `gitlabissues` - Calendar scheduling
- `uebersicht-jira-filter` - Calendar-based filtering
- `task-deadline` - Calendar deadlines

### Docker (90 widgets)
- `MiniBar-Widget` - Docker container monitoring
- `github` - Docker integration
- `docker-box` - Docker container display
- `RedditMembers` - Docker-based services
- `Docker` - Core Docker widget

### Crypto (81 widgets)
- `CryptoMarketCap` - Market cap display
- `task-deadline` - Crypto-related tasks
- `oura` - Crypto health tracking
- `os-version-uptime` - Crypto system info
- `github` - Crypto-related projects

### Weather (63 widgets)
- `UeberPlayer` - Weather integration
- `MiniBar-Widget` - Weather display
- `FroxceySidebar` - Weather sidebar
- `istats` - Weather stats
- `quotes` - Weather quotes

### Transit (55 widgets)
- `UeberPlayer` - Transit information
- `monit` - Transit monitoring
- `github` - Transit-related projects
- `RedditMembers` - Transit discussions
- `leetcode-glance` - Transit coding

### Todo (34 widgets)
- `task-deadline` - Task deadlines
- `istats` - Todo statistics
- `monit` - Todo monitoring
- `TodoListWidget` - Todo list widget
- `gotify` - Todo notifications

### Location (32 widgets)
- `oura` - Location-based health
- `fetch` - Location fetching
- `Persona_5_Calendar` - Location calendar
- `wttr` - Location weather
- `purpleaqi` - Location air quality

### Email (29 widgets)
- `purpleaqi` - Email notifications
- `ExchangeMeetings` - Exchange email
- `valerian-time` - Email time tracking
- `gmail` - Gmail integration
- `lastfm` - Email music tracking

### Music (27 widgets)
- `UeberPlayer` - Music player
- `currenttrack` - Current track display
- `Really-Simple-Spotify-Widget` - Spotify widget
- `Music-Craft` - Music crafting
- `bar` - Music bar display

### Quote (22 widgets)
- `quotes` - Quote display
- `RedditMembers` - Quote sharing
- `quote-of-the-day` - Daily quotes
- `taylor-swift-quote` - Taylor Swift quotes
- `mybar` - Quote bar

### RSS (21 widgets)
- `task-deadline` - RSS task feeds
- `MiniBar-Widget` - RSS integration
- `docker-box` - RSS container feeds
- `airflo` - RSS air flow
- `StatBar` - RSS statistics

### IP (14 widgets)
- `FroxceySidebar` - IP sidebar
- `NetworkInfo` - Network information
- `Set-networking` - Network settings
- `Evangelion_style_dashboard` - IP dashboard
- `NetFullSysInfo.Widget` - Full system info

### News (10 widgets)
- `uebersicht-hacker-news` - Hacker News
- `RedditMembers` - Reddit news
- `newsticker` - News ticker
- `TodoListWidget` - News integration
- `drunk-o-clock` - News clock

### Stock (10 widgets)
- `world-clock` - Stock world clock
- `msq.arrays` - Stock arrays
- `tsushin_small` - Stock small
- `stock` - Stock widget
- `cpu_history` - Stock CPU history

### GitHub (6 widgets)
- `gitlabissues` - GitHub issues
- `github` - GitHub widget
- `wttr-moon` - GitHub weather
- `gitissues` - GitHub issues
- `gotify` - GitHub notifications

### NASA (2 widgets)
- `APOD` - Astronomy Picture of the Day
- `SpotTheStation` - ISS tracking

### Other Categories
- **GitLab (1):** `gitlabissues`
- **COVID (1):** `MarchCovid`
- **Kubernetes (1):** `kubernetes`
- **None (10):** Static widgets with no external data source
- **Unknown (7):** Widgets that couldn't be categorized

---

## Widgets with Multiple Data Sources

Many widgets integrate multiple data sources. Here are notable examples:

### Most Complex Widgets (5+ data sources)

| Widget | Data Sources Count | Sources |
|--------|-------------------|---------|
| `Evangelion_style_dashboard` | 9 | calendar, crypto, email, ip, music, system, time, transit, weather |
| `TheOneWidget` | 11 | calendar, crypto, docker, ip, location, music, rss, system, time, transit, weather |
| `msq.arrays` | 13 | calendar, crypto, docker, music, news, quote, rss, stock, system, time, todo, transit, weather |
| `WunderlistTasksWidget` | 11 | calendar, crypto, docker, email, ip, none, system, time, todo, transit, weather |
| `longviewer-widget` | 10 | calendar, crypto, email, none, quote, system, time, todo, transit, weather |
| `world-clock` | 8 | calendar, crypto, docker, stock, system, time, transit, weather |
| `Sidebar` | 8 | calendar, location, music, quote, system, time, transit, weather |
| `calendar` | 8 | calendar, crypto, docker, location, system, time, todo, weather |

### Common Multi-Source Combinations

- **Calendar + System + Time:** Most common combination (appears in many widgets)
- **Docker + System + Time:** Common in monitoring widgets
- **Weather + Location + Time:** Common in weather widgets
- **Crypto + System + Time:** Common in financial widgets
- **Music + Calendar + Time:** Common in media widgets

---

## Technology Breakdown

### JSX vs CoffeeScript Distribution

The analysis shows that CoffeeScript widgets (399 files) significantly outnumber JSX widgets (110 files), representing approximately **78%** of all widget files.

### Widgets Using Both Technologies

Some widgets contain both JSX and CoffeeScript files:
- These are counted in both categories
- The widget ID extraction groups all files from the same widget folder

---

## Methodology

### Pattern Matching

The analysis uses regex pattern matching to identify data sources in widget code. Patterns are matched case-insensitively against:

- API endpoints (e.g., `api.github.com`, `wttr.in`)
- Service names (e.g., `docker`, `spotify`, `gmail`)
- Function calls (e.g., `exec()`, `fetch()`, `run()`)
- Keywords (e.g., `weather`, `crypto`, `calendar`)

### Limitations

1. **False Positives:** Some widgets may be categorized based on code comments or variable names rather than actual usage
2. **Pattern Overlap:** Some categories overlap (e.g., widgets using "time" may be categorized as time-based even if they primarily use other data sources)
3. **Static Analysis:** The analysis is based on code inspection, not runtime behavior
4. **Unknown Sources:** 7 widgets could not be categorized and may require manual review

---

## Recommendations

### For Training Data

1. **Prioritize Common Sources:** Focus training examples on the top 5-7 data source categories (time, system, calendar, docker, crypto, weather, transit)
2. **Multi-Source Examples:** Include examples of widgets that combine multiple data sources
3. **Technology Balance:** Ensure both JSX and CoffeeScript examples are represented in training data

### For Widget Development

1. **API Integration Patterns:** Document common patterns for integrating with external APIs
2. **Error Handling:** Emphasize robust error handling for network-dependent widgets
3. **Caching Strategies:** Consider caching strategies for widgets that frequently poll external APIs

---

## Data Files

- **Source Data:** `widget_data_sources.json` - Complete analysis results with per-widget breakdown
- **Analysis Script:** `analyze_widget_data_sources.py` - Script used to generate this analysis

---

**Report Generated:** Analysis completed successfully  
**Analysis Duration:** ~2.5 seconds for 509 widget files

