# 安装指南

本文档将帮助您完成USDA-CN的安装和配置。

## 目录

- [系统要求](#系统要求)
- [安装Python](#安装python)
- [安装USDA-CN](#安装usda-cn)
- [申请API密钥](#申请api密钥)
- [配置环境变量](#配置环境变量)
- [验证安装](#验证安装)
- [常见安装问题](#常见安装问题)

---

## 系统要求

- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8 或更高
- **网络**: 需要访问美国农业部API服务器

---

## 安装Python

### Windows系统

1. **下载Python**
   - 访问 https://www.python.org/downloads/
   - 点击下载 Python 3.8 或更高版本
   
2. **安装Python**
   - 双击下载的安装文件
   - **重要**：勾选 "Add Python to PATH"
   - 点击 "Install Now"
   
3. **验证安装**
   ```
   打开命令提示符（Win+R，输入cmd）
   输入：python --version
   应显示：Python 3.x.x
   ```

### macOS系统

1. 打开终端
2. 安装Homebrew（如未安装）：
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. 安装Python：
   ```bash
   brew install python
   ```

### Linux系统

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

---

## 安装USDA-CN

打开命令行（终端），输入以下命令：

```bash
pip install usda-cn
```

### 升级到最新版本

```bash
pip install --upgrade usda-cn
```

### 从GitHub安装最新开发版

```bash
pip install git+https://github.com/chan1919/USDA-CN.git
```

---

## 申请API密钥

USDA API是**免费**的，但需要申请密钥。

### 步骤

1. 访问 https://quickstats.nass.usda.gov/api

2. 在页面底部找到申请表单

3. 填写信息：
   - **Name/Organization**: 可选，填写姓名或组织
   - **Email Address**: 必填，接收密钥的邮箱
   - **勾选**: 接收更新邮件（可选）

4. 点击 Submit

5. 几秒钟后会收到邮件，包含您的API密钥

### API密钥示例

```
4AB84799-0BD2-3EBA-AC70-03E51B016275
```

**注意**：请妥善保管您的API密钥，不要分享给他人。

---

## 配置环境变量

### 方法一：使用.env文件（推荐）

1. 在您的项目文件夹中创建文件 `.env`

2. 文件内容如下：
   ```
   USDA_API_KEY=您的API密钥
   ```
   
3. 示例：
   ```
   USDA_API_KEY=4AB84799-0BD2-3EBA-AC70-03E51B016275
   ```

### 方法二：直接在代码中传入

```python
from usda_cn import NASSClient

client = NASSClient(api_key="您的API密钥")
```

### 方法三：设置系统环境变量

**Windows**:
```
控制面板 → 系统 → 高级系统设置 → 环境变量 → 新建
变量名：USDA_API_KEY
变量值：您的API密钥
```

**Linux/macOS**:
```bash
# 临时设置
export USDA_API_KEY="您的API密钥"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export USDA_API_KEY="您的API密钥"' >> ~/.bashrc
source ~/.bashrc
```

---

## 验证安装

创建测试文件 `test_install.py`：

```python
from usda_cn import NASSClient

# 如果配置了.env文件
client = NASSClient()

# 或者直接传入API密钥
# client = NASSClient(api_key="您的API密钥")

# 测试获取数据
data = client.get_soybean_production(year=2024)
print("安装成功！")
print(f"2024年大豆产量: {data['Value'].iloc[0]}")
```

运行测试：
```bash
python test_install.py
```

如果看到输出，说明安装成功！

---

## 常见安装问题

### Q1: pip不是内部或外部命令

**原因**：Python的pip未添加到系统路径

**解决**：
```bash
# 使用完整路径
python -m pip install usda-cn
```

### Q2: 安装速度很慢

**原因**：默认使用国外镜像

**解决**：使用国内镜像
```bash
pip install usda-cn -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 权限错误

**解决**：使用用户安装
```bash
pip install usda-cn --user
```

### Q4: 提示"未找到API密钥"

**原因**：环境变量未正确设置

**解决**：
1. 确认.env文件在项目根目录
2. 确认文件名是 `.env` 而不是 `.env.txt`
3. 或者在代码中直接传入API密钥

### Q5: 连接超时

**原因**：网络无法访问USDA服务器

**解决**：
1. 检查网络连接
2. 尝试使用VPN
3. 联系网络管理员开放访问权限

---

## 下一步

安装完成后，请阅读 [快速开始指南](quickstart.md) 开始使用。