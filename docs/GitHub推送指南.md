# GitHub Pages部署指南 - 诉前智检(PLIC)

## ✅ 已完成步骤

1. ✅ 初始化Git仓库
2. ✅ 创建.gitignore文件
3. ✅ 添加并提交index.html和文档

## 📋 接下来需要你手动完成的步骤

### 第一步:创建GitHub仓库

1. **访问GitHub**
   - 打开浏览器,访问: https://github.com/new

2. **填写仓库信息**
   ```
   Repository name: plic-legal-ai
   Description: 诉前智检 - AI驱动的智能诉讼准备助手

   选择: ☑ Public (公开仓库)

   不要勾选:
   ☐ Add a README file
   ☐ Add .gitignore
   ☐ Choose a license
   ```

3. **点击"Create repository"**

### 第二步:推送代码到GitHub

在项目目录 `d:\Code\PLIC` 下,**依次执行**以下命令:

```bash
# 关联远程仓库(替换成你的GitHub用户名)
git remote add origin https://github.com/你的用户名/plic-legal-ai.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

**示例:**
如果你的GitHub用户名是 `zhangsan`,则命令为:
```bash
git remote add origin https://github.com/zhangsan/plic-legal-ai.git
git branch -M main
git push -u origin main
```

### 第三步:启用GitHub Pages

1. **进入仓库设置**
   - 在GitHub仓库页面,点击 **Settings** 标签

2. **配置Pages**
   - 左侧菜单找到 **Pages**
   - 在"Source"部分:
     ```
     Source: Deploy from a branch
     Branch: main
     Folder: / (root)
     ```
   - 点击 **Save**

3. **等待部署**
   - 约1-2分钟后,页面顶部会显示:
     ```
     ✅ Your site is live at https://你的用户名.github.io/plic-legal-ai/
     ```

4. **访问你的网站**
   - 访问: `https://你的用户名.github.io/plic-legal-ai/`
   - 应该能看到诉前智检的主界面

---

## 🔧 如果遇到问题

### 问题1: 推送时提示"Permission denied"

**原因:** GitHub用户名或仓库地址错误

**解决:** 检查远程仓库地址
```bash
git remote -v
# 应该显示: origin https://github.com/你的用户名/plic-legal-ai.git
```

如果错误,重新设置:
```bash
git remote remove origin
git remote add origin https://github.com/正确的用户名/plic-legal-ai.git
```

### 问题2: 要求输入用户名和密码

**原因:** GitHub已不再支持密码登录,需要使用Personal Access Token

**解决:**
1. 访问: https://github.com/settings/tokens
2. 点击"Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制token
5. 推送时:
   - 用户名: 你的GitHub用户名
   - 密码: 粘贴token(不是你的GitHub密码)

### 问题3: GitHub Pages一直显示部署中

**原因:** 首次部署需要1-2分钟

**解决:**
- 等待2分钟
- 刷新页面
- 检查是否选择了正确的分支(main)和目录(/)

---

## 📝 部署成功后的测试

1. **访问你的网站**
   ```
   https://你的用户名.github.io/plic-legal-ai/
   ```

2. **快速测试**
   - 选择"🏘️ 物业服务合同纠纷"
   - 点击"📋 填充完整测试数据"
   - 查看100+字段是否自动填充
   - 点击"🖨️ 打印"查看效果

3. **分享链接**
   - 将上述链接发送给测试人员
   - 说明:支持规则提取功能,AI提取需要配置后端

---

## 🎯 完成后的链接格式

部署成功后,你的链接会是这样的:

```
https://你的用户名.github.io/plic-legal-ai/
```

例如,如果用户名是 `zhangsan`:
```
https://zhangsan.github.io/plic-legal-ai/
```

---

## 📊 当前Git仓库状态

```bash
$ git status
On branch master
nothing to commit, working tree clean

$ git log
commit 78a397d
Author: PLIC Developer <plic@legal-ai.dev>
Date:   Fri Apr 18 2025

Initial commit: 诉前智检(PLIC) - 智能诉讼准备助手
```

---

## 🚀 下一步

1. 按照上面的步骤创建GitHub仓库
2. 执行推送命令
3. 启用GitHub Pages
4. 等待部署完成
5. 分享链接给测试人员!

**需要帮助?** 如果在任何步骤遇到问题,随时告诉我!
