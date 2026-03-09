# Phase 4: 广告变现接入 - Research

**Researched:** 2026-03-08
**Domain:** Hugo + PaperMod + Google AdSense 集成
**Confidence:** HIGH

## Summary

研究了在 Hugo + PaperMod 博客中接入 Google AdSense 广告的最佳方案。PaperMod 主题通过 `extend_head.html` 和 `extend_footer.html` partials 支持自定义 JS 注入，无需修改主题文件。Google AdSense 需要放置 ads.txt 文件到 static 目录，并使用自动广告代码实现响应式展示。

**Primary recommendation:** 使用 PaperMod 的 extend_head.html partial 注入 AdSense 自动广告代码，在文章页面添加内嵌广告位，在侧边栏添加展示广告位。

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Hugo | >=0.146.0 | 静态网站生成器 | PaperMod 最低要求 |
| PaperMod | 最新 | Hugo 主题 | 项目已集成 |

### AdSense Integration
| Component | Format | Purpose |
|-----------|--------|---------|
| adsbygoogle.js | 自动广告脚本 | 页面级广告自动投放 |
| ads.txt | 授权卖方文件 | 防止广告欺诈，必需 |

---

## Architecture Patterns

### Recommended Project Structure
```
claw-blog/
├── layouts/
│   └── partials/
│       ├── extend_head.html      # AdSense 脚本注入
│       └── extend_footer.html    # (可选) 页面底部广告
├── static/
│   └── ads.txt                   # AdSense 授权文件
└── hugo.yaml                     # 配置 AdSense publisher ID
```

### Pattern 1: PaperMod 自定义 Head/Footer

**What:** 通过创建自定义 partials 扩展主题 head 和 footer 区域

**When to use:** 需要添加第三方脚本（Google Analytics、Google AdSense、自定义 JS）时

**How:**
```bash
# 创建 layouts/partials 目录
mkdir -p layouts/partials
```

**File: layouts/partials/extend_head.html**
```html
<!-- Google AdSense 自动广告 -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8708502478021488" crossorigin="anonymous"></script>
```

**File: layouts/partials/extend_footer.html**
```html
<!-- 可选: 页面底部广告或其他脚本 -->
```

### Pattern 2: AdSense 自动广告 (Auto Ads)

**What:** Google AdSense 自动广告会根据页面内容自动选择最佳广告格式和位置

**Advantages:**
- 无需手动创建广告位
- 自动响应式适配
- 持续优化广告展示

**Script Format (添加到 extend_head.html):**
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8708502478021488" crossorigin="anonymous"></script>
```

### Pattern 3: 手动广告位 (可选)

**What:** 对于特定位置的精确控制，可以使用手动广告位

**When to use:** 当需要在文章中间、侧边栏等特定位置放置广告时

**Implementation in layouts/_default/single.html 或创建自定义模板:**
```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-8708502478021488"
     data-ad-slot="YOUR_AD_SLOT_ID"
     data-ad-format="fluid"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
```

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 第三方 JS 注入 | 修改 PaperMod 主题源码 | extend_head.html partial | 主题升级会丢失修改 |
| 广告位管理 | 手动硬编码每个广告位 | AdSense 自动广告 | 自动优化，更少维护 |
| ads.txt | 从其他博客复制 | 在 AdSense 后台生成 | 包含正确的授权信息 |

---

## Common Pitfalls

### Pitfall 1: ads.txt 放置位置错误
**What goes wrong:** 广告无法展示，AdSense 后台显示 "ads.txt 警告"

**Why it happens:** 放在了错误目录，Hugo 不会处理 static 以外的文件

**How to avoid:** 确保 ads.txt 在 `static/ads.txt`，访问路径为 `example.com/ads.txt`

**Warning signs:** AdSense 后台显示 "找不到 ads.txt" 或 "ads.txt 格式错误"

### Pitfall 2: 脚本加载阻塞页面渲染
**What goes wrong:** 页面加载变慢，影响用户体验和 SEO

**Why it happens:** 未使用 async 属性加载广告脚本

**How to avoid:** 始终使用 `async` 属性：
```html
<script async src="..."></script>
```

### Pitfall 3: 手动修改主题文件
**What goes wrong:** 主题升级后自定义丢失

**Why it happens:** 直接修改 themes/PaperMod 目录下的文件

**How to avoid:** 使用 layouts/partials 覆盖机制，不修改主题源码

### Pitfall 4: 广告展示影响阅读体验
**What goes wrong:** 广告遮挡内容或分散注意力，导致用户流失

**Why it happens:** 广告位过于密集或位置不当

**How to avoid:**
- 限制每页广告数量（自动广告可配置）
- 避免文章开头插入广告
- 保持广告与内容间距

### Pitfall 5: 跨域属性缺失
**What goes wrong:** 广告无法正常加载，控制台报错

**Why it happens:** 缺少 crossorigin 属性

**How to avoid:** 始终包含 `crossorigin="anonymous"`:
```html
<script async src="...?client=..." crossorigin="anonymous"></script>
```

---

## Code Examples

### Example 1: 完整的 extend_head.html

Source: [PaperMod Wiki - FAQs](https://github.com/adityatelange/hugo-PaperMod/wiki/FAQs)

```html
{{- /* layouts/partials/extend_head.html */ -}}
{{- /* Google AdSense 自动广告脚本 */ -}}
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8708502478021488" crossorigin="anonymous"></script>

{{- /* 可选: 自定义样式 */ -}}
<style>
    /* 广告容器样式 */
    .ad-container {
        margin: 2rem 0;
        text-align: center;
        min-height: 90px;
    }
    /* 确保广告不破坏布局 */
    .ad-container ins.adsbygoogle {
        display: block !important;
    }
</style>
```

### Example 2: ads.txt 文件格式

```text
google.com, pub-8708502478021488, DIRECT, f08c47fec0942fa0
```

**Note:** ads.txt 内容应从 AdSense 后台获取，不同账户内容可能不同。

### Example 3: 侧边栏广告位 (可选增强)

如果要手动在侧边栏添加广告，需要覆盖 PaperMod 的侧边栏模板。创建 `layouts/partials/sidebar.html`:

```html
{{- /* layouts/partials/sidebar.html */ -}}
<aside class="sidebar">
    <!-- 侧边栏广告 -->
    <div class="ad-container">
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-8708502478021488"
             data-ad-slot="YOUR_SIDEBAR_AD_SLOT"
             data-ad-format="vertical"
             data-full-width-responsive="true"></ins>
        <script>
            (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
</aside>
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 手动广告位 | AdSense 自动广告 | 2018+ | 减少维护，智能优化 |
| 主题内直接修改 | partials 覆盖机制 | PaperMod 支持后 | 主题可升级 |
| 固定广告尺寸 | 响应式 fluid 广告 | 移动端普及 | 更好的移动体验 |

**Deprecated/outdated:**
- 固定尺寸广告位: 不推荐，使用 data-ad-format="auto" 或 "fluid"
- 直接修改主题文件: 应该使用 layouts 覆盖

---

## Open Questions

1. **广告位数量控制**
   - What we know: AdSense 自动广告可通过配置限制显示数量
   - What's unclear: 具体配置参数和效果
   - Recommendation: 先使用默认设置，后期根据需要调整

2. **自动广告 vs 手动广告选择**
   - What we know: 自动广告更简单，手动广告更可控
   - What's unclear: 哪种更适合博客场景
   - Recommendation: Phase 4 优先使用自动广告，Phase 5+ 可考虑手动广告位

3. **国内访问问题**
   - What we know: AdSense 在国内访问可能受限
   - What's unclear: 是否需要考虑替代方案
   - Recommendation: 目前阶段不考虑，先完成基本集成

---

## Validation Architecture

> Skip this section entirely if workflow.nyquist_validation is explicitly set to false in .planning/config.json. If the key is absent, treat as enabled.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Hugo build validation |
| Config file | none |
| Quick run command | `hugo --quiet` |
| Full suite command | `hugo --quiet --verbose` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AD-01 | AdSense 脚本注入到 head | Build | 检查 extend_head.html 包含 adsbygoogle.js | `layouts/partials/extend_head.html` |
| AD-02 | 广告位合理展示 | Build | 检查 ads.txt 存在于 static/ | `static/ads.txt` |

### Sampling Rate
- **Per task commit:** `hugo --quiet`
- **Per wave merge:** `hugo --quiet --verbose`
- **Phase gate:** Build passes before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `layouts/partials/extend_head.html` — 注入 AdSense 脚本
- [ ] `static/ads.txt` — AdSense 授权文件

---

## Sources

### Primary (HIGH confidence)
- [PaperMod Wiki - FAQs](https://github.com/adityatelange/hugo-PaperMod/wiki/FAQs) - 自定义 head/footer 方式
- [Hugo Embedded Templates](https://gohugo.io/templates/embedded/) - partials 机制参考

### Secondary (MEDIUM confidence)
- [Google AdSense 官方文档](https://support.google.com/adsense) - 广告代码格式
- Hugo 社区实践 - 常见集成方式

### Tertiary (LOW confidence)
- 各种 Hugo 博客集成教程 - 需要验证时效性

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Hugo + PaperMod 组合稳定，文档完善
- Architecture: HIGH - PaperMod partials 覆盖机制清晰
- Pitfalls: MEDIUM - 基于社区经验，具体情况可能不同

**Research date:** 2026-03-08
**Valid until:** 2026-04-08 (30 days for stable integration patterns)
