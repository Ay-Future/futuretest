# 数据规范

D2–D3 定义 Pydantic 模型并从模型导出 JSON Schema，避免手写模型与 Schema 不一致。待定义对象：

- SourceSnapshot：来源、修订、类型、哈希、快照路径及定位格式。
- BusinessRule：条件、预期、证据、适用范围、事实类型及确认状态。
- SystemMapping：固定规则修订、页面、接口及可观测证据。
- Scenario：固定规则修订、前置条件、操作、断言及数据要求。
- OpenQuestion：影响对象、责任角色、阻塞属性及解决依据。
- ContextPackage：格式版本、包修订、需求、目标范围、冻结事实及 manifest。

本目录目前仅预留规范位置，尚未冻结字段与兼容性契约。详细语义以实施计划第 4 节为准。
