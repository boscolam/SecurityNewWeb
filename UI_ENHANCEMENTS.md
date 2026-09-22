# UI Enhancements - Interactive Clickable Elements & Attack Map

Version 2.4.0 introduced comprehensive clickable UI elements. Version 2.5.0 adds a real-time cyber attack map visualization.

---

## 🎯 Overview

All badges, tags, and metadata in news cards are now **clickable** and will automatically filter or search the news.

**One-Click Navigation**: Click on any badge to instantly filter the news list without using dropdown menus.

---

## 📱 Clickable Elements

### 1. Priority Badges

**What**: Colored badges showing priority level (CRITICAL, HIGH, MEDIUM, LOW)

**Click Action**: Filter news by that priority level

**Visual Feedback**:
- Lifts up on hover (2px)
- Glows with shadow effect
- Scales slightly larger (1.05x)
- Cursor changes to pointer

**Example**:
```
Click "HIGH" badge → Redirects to /news?priority=high
```

---

### 2. Category Badges

**What**: Blue badges showing news category (Web News, Blog, Vendor Research, Government, CVE, etc.)

**Click Action**: Filter news by that category

**Visual Feedback**:
- Blue glow on hover
- Ripple effect animation
- Tooltip shows "Click to filter by..."

**Example**:
```
Click "Vendor Research" → /news?category=vendor_research
Click "Government CERT" → /news?category=government
```

---

### 3. Region Badges

**What**: Gray badges with globe icon showing geographic region

**Click Action**: Filter news by that region

**Visual Feedback**:
- Gray glow on hover
- Smooth transition
- Lifts on hover

**Example**:
```
Click "North America" → /news?region=north_america
Click "Europe" → /news?region=europe
Click "Asia Pacific" → /news?region=asia_pacific
```

---

### 4. Hacking Incident Badge

**What**: Red "HACK" badge with skull icon

**Click Action**: Show only hacking incidents

**Visual Feedback**:
- Red glow on hover
- Danger color emphasis
- Bold visual feedback

**Example**:
```
Click "HACK" badge → /news?hacking=1
```

---

### 5. CVE Badge

**What**: Yellow "CVE" badge with bug icon

**Click Action**: Show only CVE-related articles

**Visual Feedback**:
- Yellow glow on hover
- Warning color emphasis

**Example**:
```
Click "CVE" badge → /news?cve=1
```

---

### 6. Source Names

**What**: Source name in news metadata (e.g., "The Hacker News")

**Click Action**: Filter news from that specific source

**Visual Feedback**:
- Blue background on hover
- Underline appears
- Color change to primary blue

**Example**:
```
Click "The Hacker News" → /news?source_id=1
Click "BleepingComputer" → /news?source_id=5
```

---

### 7. CVE Tags

**What**: Individual CVE identifiers (e.g., "CVE-2024-1234")

**Click Action**: Search for that specific CVE

**Visual Feedback**:
- Yellow background on hover
- 🔍 search icon appears in corner
- Shadow effect

**Example**:
```
Click "CVE-2024-1234" → /news?search=CVE-2024-1234
Click "CVE-2024-5678" → /cve?search=CVE-2024-5678
```

---

### 8. Vendor Tags

**What**: Vendor names (e.g., "Cisco", "Palo Alto", "Fortinet")

**Click Action**: Filter CVE news by that vendor

**Visual Feedback**:
- Blue background on hover
- Icon with vendor name
- Shadow effect

**Example**:
```
Click "Cisco" → /cve?vendor=cisco
Click "Palo Alto" → /cve?vendor=paloaltonetworks
Click "Fortinet" → /cve?vendor=fortinet
```

---

## 🎨 Visual Design

### Hover Effects

All clickable elements feature:
- **Transform**: `translateY(-2px)` - Elements lift on hover
- **Shadow**: Color-coded glow effects
- **Scale**: Slight size increase (1.05x)
- **Transition**: Smooth 0.2s ease animation
- **Cursor**: Pointer cursor indicates clickability

### Color-Coded Glows

Different badge types have unique hover glows:
- 🔴 **Critical/High**: Red shadow (`rgba(220, 53, 69, 0.5)`)
- 🟡 **Medium/Warning**: Yellow shadow (`rgba(255, 193, 7, 0.5)`)
- 🟢 **Low/Success**: Green shadow (`rgba(40, 167, 69, 0.5)`)
- 🔵 **Info**: Blue shadow (`rgba(23, 162, 184, 0.5)`)

### Ripple Animation

Badges have a ripple effect on hover:
1. White semi-transparent circle expands from center
2. Creates subtle feedback
3. Professional polish

---

## 📱 Mobile Optimization

### Touch Targets

On mobile devices (< 768px):
- Minimum touch target: **32px height**
- Larger padding: **8px 12px**
- Better spacing: **4px margins**
- Easy tapping with fingers

### Responsive Design

- Elements scale appropriately
- No tiny touch targets
- Comfortable spacing
- No accidental clicks

---

## ♿ Accessibility

### Keyboard Navigation

- **Tab**: Navigate through clickable elements
- **Enter/Space**: Activate element
- **Focus Visible**: 3px outline on focus
- **Focus Ring**: Blue glow around focused element

### Screen Readers

- **Title Attributes**: Descriptive text on hover
- **ARIA-friendly**: Proper focus indicators
- **Context**: "Click to filter by..." hints

### High Contrast

- Clear visual distinction
- Strong hover states
- Obvious clickability
- Focus indicators

---

## 🚀 Usage Examples

### Scenario 1: Finding All High Priority News

**Old Way**:
1. Go to /news
2. Click priority dropdown
3. Select "High"
4. Click "Apply Filters"

**New Way**:
1. Click any "HIGH" badge → Done! ✅

---

### Scenario 2: Viewing News from a Specific Source

**Old Way**:
1. Go to /news
2. Scroll through source dropdown
3. Find and select source
4. Submit form

**New Way**:
1. Click source name → Done! ✅

---

### Scenario 3: Researching a Specific CVE

**Old Way**:
1. Go to /news or /cve
2. Type CVE-2024-1234 in search box
3. Click search button

**New Way**:
1. Click CVE-2024-1234 tag → Done! ✅

---

### Scenario 4: Finding Cisco Vulnerabilities

**Old Way**:
1. Go to /cve
2. Click vendor filter
3. Select Cisco

**New Way**:
1. Click "Cisco" vendor tag → Done! ✅

---

## 💡 Pro Tips

### 1. **Stack Filters**
Clickable elements preserve existing filters:
```
Start at: /news?priority=high
Click "Vendor Research" badge
Result: /news?priority=high&category=vendor_research
```

### 2. **Quick Source Check**
On dashboard, click source names to see all news from that source.

### 3. **CVE Investigation**
Click any CVE tag to instantly search for related articles across all sources.

### 4. **Vendor Monitoring**
Click vendor tags to track all vulnerabilities affecting that vendor.

### 5. **Regional Focus**
Click region badges to focus on specific geographic areas.

---

## 🎯 Page-Specific Behavior

### Dashboard (`/`)
- All clickable badges redirect to `/news` with filters
- Perfect starting point for exploration
- Top 10 news with full clickability

### News Page (`/news`)
- Badges modify current filters
- URL parameters preserved
- Page resets to 1 on filter change
- Full filtering capability

### CVE Monitor (`/cve`)
- Vendor tags stay in CVE context
- CVE tags search within CVE page
- Priority badges link to /news with CVE filter
- Optimized for vulnerability tracking

---

## 🛠️ Technical Details

### JavaScript Functions

Each page includes these functions:

```javascript
filterByPriority(priority)      // Filter by priority level
filterByCategory(category)      // Filter by category
filterByRegion(region)          // Filter by region
filterBySource(sourceId)        // Filter by source
filterByVendor(vendor)          // Filter by vendor
filterByHacking()               // Show hacking incidents
filterByCVE()                   // Show CVE articles
searchFor(term)                 // Search for text
```

### URL Manipulation

Uses modern JavaScript URL API:
```javascript
const url = new URL(window.location.href);
url.searchParams.set('priority', 'high');
url.searchParams.delete('page');  // Reset to page 1
window.location.href = url.toString();
```

### Performance

- **No AJAX**: Direct navigation is instant
- **Lightweight**: Minimal JavaScript overhead
- **No Dependencies**: Pure vanilla JavaScript
- **Fast**: No external library loading

---

## 🎨 CSS Classes

### Main Classes

- `.clickable` - Base class for all clickable elements
- `.priority-badge.clickable` - Clickable priority badges
- `.badge.clickable` - Clickable category/region badges
- `.source-link.clickable` - Clickable source names
- `.cve-tag.clickable` - Clickable CVE tags
- `.vendor-tag.clickable` - Clickable vendor tags

### Hover States

All clickable elements automatically get:
```css
cursor: pointer;
transition: all 0.2s ease;
transform: translateY(-2px) on hover;
box-shadow: colored glow on hover;
```

---

## 📊 Statistics

### v2.4.0 UI Enhancements

- **158 lines** of new CSS
- **8 JavaScript functions** per page
- **3 pages** enhanced (Dashboard, News, CVE)
- **8 types** of clickable elements
- **100%** mobile responsive
- **WCAG** compliant accessibility

### User Experience Improvements

- ⚡ **50% faster** filtering (1 click vs 3-4 clicks)
- 🎯 **More intuitive** - click what you see
- 📱 **Mobile friendly** - larger touch targets
- ♿ **Accessible** - full keyboard navigation
- 🎨 **Professional** - polished animations

---

## 🔄 Migration Notes

### From v2.3.x to v2.4.0

**No breaking changes!**

- Old dropdown filters still work
- New clickable elements are additions
- Fully backward compatible
- No database changes needed

### Update Steps

1. Pull latest from GitHub
2. Restart the application
3. Clear browser cache (Ctrl+Shift+R)
4. Enjoy clickable UI!

---

## 🐛 Troubleshooting

### Issue: Badges Not Clickable

**Solution**: Hard refresh browser
```
Chrome/Firefox: Ctrl+Shift+R
Mac: Cmd+Shift+R
```

### Issue: No Hover Effects

**Solution**: Clear browser cache
```
Settings → Privacy → Clear browsing data → Cached images
```

### Issue: Click Doesn't Navigate

**Solution**: Check JavaScript console for errors
```
F12 → Console tab → Look for errors
```

### Issue: Wrong Filter Applied

**Solution**: Check URL parameters
```
URL should show: ?priority=high&category=blog
```

---

## 📚 Related Documentation

- `CHANGELOG.md` - Version history and changes
- `README.md` - Project overview
- `RESTART_GUIDE.md` - How to restart after updates
- `LOGGING_GUIDE.md` - Logging system

---

## 💬 Feedback

If you have suggestions for additional clickable elements or UI improvements:

1. Open an issue on GitHub
2. Describe the element and desired behavior
3. We'll consider it for future versions!

---

---

## 🗺️ Real-Time Cyber Attack Map (v2.5.0)

### Overview

Version 2.5.0 adds a full-page animated cyber attack map at `/attack-map`.

### Features

- **World Map**: 20 filled continent/island polygons as background + 85+ city dots on dark canvas
- **Animated Arcs**: Bezier curve attacks from source to destination countries
- **Particle Effects**: Glowing particles travel along arcs with trailing light
- **Impact Ripples**: Expanding circles at attack destinations
- **Source Pulses**: Pulsing rings at attack origins

### Data Source

Attack data is derived from actual news articles in the database:
- Hacking incidents (`is_hacking_incident = 1`)
- Critical and high priority news
- Published within the last 30 days

### Attacker Detection

Keywords in article titles/summaries are matched to identify attack origins:
- **Russia**: APT28, APT29, Fancy Bear, Cozy Bear, Sandworm, Turla
- **China**: APT41, APT10, Hafnium, Winnti, Volt Typhoon, Salt Typhoon
- **North Korea**: Lazarus, Kimsuky, APT38, Andariel
- **Iran**: APT33, APT35, Charming Kitten, MuddyWater

### Target Detection

Target countries are determined by:
1. Keywords in title/summary (e.g., "U.S.", "British", "Ukrainian")
2. Article region field mapped to representative countries
3. Fallback to region-based random selection

### Interface Panels

| Panel | Position | Content |
|-------|----------|---------|
| Threat Overview | Top-left | Total threats, critical/high counts, country count |
| Top Attack Origins | Bottom-left | Ranked attacker countries with bar charts |
| Live Attack Feed | Right side | Scrolling log with severity badges |
| Legend | Bottom-center | Color-coded severity levels |
| Controls | Bottom-right | Pause/Resume button |

### Severity Colors

| Level | Color | RGB |
|-------|-------|-----|
| Critical | Red | `rgb(255, 45, 85)` |
| High | Orange | `rgb(255, 149, 0)` |
| Medium | Yellow | `rgb(255, 204, 0)` |
| Low | Green | `rgb(48, 209, 88)` |

### API Endpoint

`GET /api/attack-data` returns:
```json
{
  "attacks": [
    {
      "id": 123,
      "title": "Russian APT targets US infrastructure",
      "source": {"country": "Russia", "lat": 55.8, "lon": 37.6},
      "target": {"country": "United States", "lat": 39.8, "lon": -98.6},
      "severity": "critical",
      "type": "hacking",
      "time": "2026-09-22T10:30:00",
      "category": "web_news"
    }
  ],
  "stats": {"total_incidents": 150, "critical_count": 10},
  "total": 85
}
```

### Technical Details

- Canvas rendering with `requestAnimationFrame` (60fps)
- Device pixel ratio handling for HiDPI displays
- Equirectangular projection for lat/lon → canvas coordinates
- Max 35 concurrent arcs for performance
- Auto-refresh every 30 seconds
- Responsive: panels collapse on mobile (< 900px)

### Navigation

Access via: **Dashboard** → **Attack Map** in the main navigation bar

---

**Version**: 2.5.2  
**Updated**: 2026-09-22  
**Features**: Interactive Clickable UI + Real-Time Cyber Attack Map with World Map Background
