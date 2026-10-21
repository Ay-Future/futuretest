# 架构与模块边界

| 模块 | 职责 | 关键约束 |
|---|---|---|
| ingest | 导入文件，保存来源快照、哈希与定位 | 更新生成新快照，来源文字作为数据处理 |
| agent | 一个主 Agent，检索、提取、比对及草稿生成 | 工具不能确认事实或发布包 |
| facts | SQLite 事实库、修订查询及确认记录 | 查询明确业务与适用版本；保留历史修订 |
| workflow | CLI、固定状态机、恢复、确认入口及发布服务 | 确认和发布由受控应用入口执行 |
| validation | 字段、引用、版本、覆盖和未决问题校验 | 校验失败不能发布 |
| adapters | 用例生成、接口自动化输入适配 | 两端使用同一包 ID、修订和 manifest 哈希 |

原始证据、分析草稿、已确认事实、发布包分别保存。事实数据库预留为 `facts.sqlite3`，LangGraph checkpoint 数据库预留为 `runs/checkpoints.sqlite3`；两者独立，待实现各自初始化及迁移。

计划状态流转：

```text
created → ingested → analyzing → draft_ready → awaiting_confirmation → validating
                                   ↑                                      │
                                   └──────── 校验失败 ─────────────────────┤
                                                                         └→ published
```

状态机、持久化恢复和发布事务尚未实现。后续必须在应用层约束转换，并记录失败阶段及恢复点。

正式发布包按实施计划输出 `manifest.json`、`context.json`、`summary.md`、`evidence-index.json`、`open-questions.json` 和 `validation.json`。引用需固定修订；发布必须验证实际确认记录、目标版本、取证方式和阻塞问题，并保证不可变及幂等。
