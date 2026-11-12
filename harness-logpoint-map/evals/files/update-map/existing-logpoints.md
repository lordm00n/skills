# 日志地图

## CR 审核合入

| 场景 | 日志文案 |
| --- | --- |
| 合入失败，打印异常堆栈 | `review_action action=approve`；`result=error` |
| DEBUG 开启时，记录合入写入完成 | `review_persisted` |
| 合入完成 | `review_finished` |

人工备注：审核卡住时先确认 CR 是否仍是 pending，不要直接重试。

## 文件导出

| 场景 | 日志文案 |
| --- | --- |
| 导出文件准备完成 | `export_action`；`result=ready` |

人工备注：下载链接只有十分钟有效期，过期后重新生成。
