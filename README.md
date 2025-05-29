# Free AugmentCode

Free AugmentCode 是一个用于清理AugmentCode相关数据的工具，可以在同一台电脑上无限次登录不同的账号，避免账号被锁定。

## 功能特性

- 📝 修改遥测 ID
  - 重置设备 ID 和机器 ID
  - 自动备份原始数据
  - 生成新的随机 ID

- 🗃️ 数据库清理
  - 清理 SQLite 数据库中的特定记录
  - 自动备份数据库文件
  - 删除包含 'augment' 关键字的记录

- 💾 工作区存储管理
  - 清理工作区存储文件
  - 自动备份工作区数据

## 安装说明

1. 确保你的系统已安装 Python 3.10及以上
2. 克隆此仓库到本地：
   ```bash
   git clone https://github.com/yourusername/free-augmentcode.git
   cd free-augmentcode
   ```

## 使用方法

1. 退出AugmentCode插件
2. 完全退出 VS Code
3. 执行脚本：

```bash
python index.py
```

4. 重新启动 VS Code
5. AugmentCode 插件中使用新的邮箱进行登录

## 项目结构

```
free-augmentcode/
├── index.py              # 主程序入口
├── augutils/             # 工具类目录
│   ├── json_modifier.py      # JSON 文件修改工具
│   ├── sqlite_modifier.py    # SQLite 数据库修改工具
│   └── workspace_cleaner.py  # 工作区清理工具
└── utils/                # 通用工具目录
    └── paths.py             # 路径管理工具
```

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 许可证

此项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。 