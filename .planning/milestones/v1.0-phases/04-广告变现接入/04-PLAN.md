---
phase: 4-广告变现接入
plan: 1
type: execute
wave: 1
depends_on: []
files_modified:
  - layouts/partials/extend_head.html
  - static/ads.txt
  - hugo.yaml
autonomous: true
requirements:
  - AD-01
  - AD-02
user_setup: []
gap_closure: false

must_haves:
  truths:
    - "Google AdSense 脚本正确注入到页面 <head> 中"
    - "广告位在文章内容区域合理展示，不影响阅读体验"
    - "ads.txt 授权文件正确部署到静态资源目录"
  artifacts:
    - path: "layouts/partials/extend_head.html"
      provides: "AdSense 自动广告脚本注入"
      contains: "adsbygoogle.js"
    - path: "static/ads.txt"
      provides: "AdSense 授权验证文件"
      contains: "ca-pub-8708502478021488"
  key_links:
    - from: "layouts/partials/extend_head.html"
      to: "所有页面"
      via: "PaperMod partial 机制"
      pattern: "extend_head.html 自动加载到 <head>"
    - from: "static/ads.txt"
      to: "https://example.org/ads.txt"
      via: "Hugo static 目录"
      pattern: "static/* -> 根路径"
---

<objective>
实现 Google AdSense 广告脚本注入与广告位布局适配，使博客具备基本广告变现能力。

Purpose: 通过 AdSense 自动广告实现页面级广告投放，无需手动管理广告位
Output: AdSense 脚本正确注入到所有页面，ads.txt 授权文件部署
</objective>

<context>
@/Users/zhihu/projects/claw-blog/hugo.yaml
@/Users/zhihu/projects/claw-blog/.planning/phases/04-广告变现接入/04-RESEARCH.md
@/Users/zhihu/projects/claw-blog/.planning/phases/04-广告变现接入/04-VALIDATION.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: 创建 AdSense 脚本注入 partial</name>
  <files>layouts/partials/extend_head.html</files>
  <action>
创建 layouts/partials/extend_head.html 文件，注入 Google AdSense 自动广告脚本：
- 使用 async 属性避免阻塞页面渲染
- 包含 crossorigin="anonymous" 属性
- 使用用户提供的 AdSense ID: ca-pub-8708502478021488
- 添加基本的广告容器样式，确保不破坏页面布局
  </action>
  <verify>
grep -q "adsbygoogle" layouts/partials/extend_head.html && grep -q "ca-pub-8708502478021488" layouts/partials/extend_head.html
  </verify>
  <done>AdSense 脚本成功注入到 extend_head.html，使用正确的 pub ID</done>
</task>

<task type="auto">
  <name>Task 2: 创建 ads.txt 授权文件</name>
  <files>static/ads.txt</files>
  <action>
创建 static/ads.txt 文件，包含 Google AdSense 授权信息：
- 从 AdSense 后台获取的标准授权行
- 格式: google.com, pub-ID, DIRECT, f08c47fec0942fa0
- 确保文件位于 static 目录，这样会被部署到站点根路径
  </action>
<verify>
test -f static/ads.txt && grep -q "ca-pub-8708502478021488" static/ads.txt
  </verify>
  <done>ads.txt 文件创建成功，位于 static 目录</done>
</task>

<task type="auto">
  <name>Task 3: 验证构建输出包含广告脚本</name>
  <files>hugo.yaml</files>
  <action>
运行 hugo 构建并验证广告脚本已正确注入到输出页面：
- 执行 hugo -E 构建
- 检查 public/index.html 中包含 adsbygoogle
- 检查 public/ads.txt 存在
  </action>
<verify>
hugo -E --quiet && grep -q "adsbygoogle" public/index.html && test -f public/ads.txt
  </verify>
  <done>Hugo 构建成功，广告脚本注入到所有页面</done>
</task>

</tasks>

<verification>
- [ ] extend_head.html 包含正确的 AdSense 脚本代码
- [ ] ads.txt 包含正确的授权信息
- [ ] hugo -E 构建成功无错误
- [ ] public/index.html 包含 adsbygoogle 引用
- [ ] public/ads.txt 文件存在且可访问
</verification>

<success_criteria>
1. Google AdSense 脚本正确注入到页面 `<head>` 中
2. 广告位在文章内容区域合理展示，不影响阅读体验
3. ads.txt 授权文件正确部署
</success_criteria>

<output>
After completion, create `.planning/phases/04-广告变现接入/04-01-SUMMARY.md`
</output>
