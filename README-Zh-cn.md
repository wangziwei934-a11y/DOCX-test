## ✅ 第三方插件签名验证完整流程（自托管 Dify 社区版）

### 📌 场景前提：

* 你是 **Dify 的管理员**
* 你使用的是 **自托管版（Docker Compose 部署）**
* 你希望为某个插件进行签名验证后再安装（或允许其他人安装你签名的插件）

---

## 🧩 步骤详解

---

### ① 在插件开发者机器上生成密钥对（你自己使用或提供给他人）

```bash
# 创建保存密钥的文件夹
mkdir -p ~/dify_plugin_keys

# 生成密钥对（推荐使用新版 dify CLI 工具）
dify signature generate -f ~/dify_plugin_keys/my_key
```

生成结果：

* 私钥：`~/dify_plugin_keys/my_key.private.pem`
* 公钥：`~/dify_plugin_keys/my_key.public.pem`

---

### ② 打包插件（示例）

```bash
# 进入插件目录
cd ~/dify/DOC-Dify-Plugin-main

# 打包为未签名插件文件
dify plugin package . -o ../doc_plugin.difypkg
```

---

### ③ 使用私钥为插件添加签名

```bash
dify signature sign ../doc_plugin.difypkg -p ~/dify_plugin_keys/my_key.private.pem
```

生成一个签名后的插件文件：

```
../doc_plugin.signed.difypkg
```

你现在可以把这个 `.signed.difypkg` 文件发给使用者或自己上传。

---

### ④ 在 Dify 服务端启用插件签名验证

#### 🗂 放置公钥文件

将 `my_key.public.pem` 放入 Dify 容器可访问的路径：

```bash
mkdir -p docker/volumes/plugin_daemon/public_keys
cp ~/dify_plugin_keys/my_key.public.pem docker/volumes/plugin_daemon/public_keys/
```

> 这路径会挂载到容器的 `/app/storage/public_keys`

---

#### 🧾 修改 Docker Compose 配置

编辑 `docker-compose.override.yaml`（如没有则新建）：

```yaml
services:
  plugin_daemon:
    environment:
      FORCE_VERIFYING_SIGNATURE: true
      THIRD_PARTY_SIGNATURE_VERIFICATION_ENABLED: true
      THIRD_PARTY_SIGNATURE_VERIFICATION_PUBLIC_KEYS: /app/storage/public_keys/my_key.public.pem
```

---

### 🔄 重启 Dify 服务

```bash
cd docker
docker compose down
docker compose up -d
```

---

### ✅ 上传并安装你签名的插件

进入 Dify 控制台 → 插件中心 → 上传 `.signed.difypkg`，即可安全通过验证安装。

---

## 🔍 其他可选操作

### ✅ 验证插件签名有效性（可选）

```bash
dify signature verify ../doc_plugin.signed.difypkg -p ~/dify_plugin_keys/my_key.public.pem
```

---

## 📎 注意事项

| 项          | 要点                                   |
| ---------- | ------------------------------------ |
| 签名验证仅支持社区版 | 云端 SaaS 不支持此功能                       |
| 签名必须匹配公钥   | 否则安装时会报错 PluginDaemonBadRequestError |
| 可配置多个公钥    | 用逗号分隔多个 `.pem` 路径                    |
| 不建议频繁更换密钥  | 保持发布方签名可信一致性                         |

---
