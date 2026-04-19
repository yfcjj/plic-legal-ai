# 大模型智能提取 Prompt 模板

## 一、物业服务合同纠纷提取 Prompt

```markdown
你是一个专业的法律文书要素提取助手。请从以下物业服务合同纠纷起诉状文本中提取所有关键信息。

## 起诉状文本：
{TEXT}

## 提取要求

请以严格的 JSON 格式返回以下所有字段。没有的字段留空字符串""，布尔值用 true/false：

### 一、原告信��（法人/非法人组织）
```json
{{
  "pName": "原告公司名称",
  "pAddr": "住所地",
  "pRegAddr": "注册地",
  "pLegal": "法定代表人姓名",
  "pPosition": "职务",
  "pPhone": "联系电话",
  "pUscc": "统一社会信用代码",
  "pTypeLLC": true,  // 是否有限责任公司
  "pOwnerPrivate": true  // 是否民营
}}
```

### 二、委托诉讼代理人
```json
{{
  "hasAgent": true,  // 是否有代理人
  "agent1Name": "代理人1姓名",
  "agent1Unit": "代理人1单位",
  "agent1Title": "代理人1职务",
  "agent1Phone": "代理人1电话",
  "agent1Special": true,  // 是否特别授权
  "agent1General": false,  // 是否一般授权
  "agent2Name": "代理人2姓名",
  "agent2Unit": "代理人2单位",
  "agent2Title": "代理人2职务",
  "agent2Phone": "代理人2电话",
  "agent2Special": false,
  "agent2General": true
}}
```

### 三、被告1信息（自然人）
```json
{{
  "dName": "被告1姓名",
  "dMale": true,  // 性别男
  "dFemale": false,  // 性别女
  "dBirth": "1973年4月28日",
  "dNation": "汉族",
  "dAddr": "住所地",
  "dIdNo": "身份证号",
  "dPhone": "电话"
}}
```

### 四、被告2信息（自然人）
```json
{{
  "d2Name": "被告2姓名",
  "d2Male": false,
  "d2Female": true,
  "d2Birth": "出生日期",
  "d2Nation": "民族",
  "d2Addr": "住所地",
  "d2IdNo": "身份证号",
  "d2Phone": "电话"
}}
```

### 五、诉讼请求
```json
{{
  "feeEndDate": "物业费截止日期",
  "feeAmount": "8078",
  "penaltyAmount": "1615.6",
  "payableToEndNo": true,  // 不请求至清偿日
  "claimFeeYes": true,  // 由被告承担诉讼费
  "claimTotal": "9693.6元"
}}
```

### 六、管辖与保全
```json
{{
  "noJurisdiction": true,  // 无管辖约定
  "noPreservation": true  // 无诉前保全
}}
```

### 七、事实与理由
```json
{{
  "factContractName": "《物业管理服务合同》",
  "factContract": "合同信息",
  "factContractAddr": "签订地点",
  "factPropCompany": "物业服务公司",
  "factOwner": "所有权人",
  "factLocation": "坐落位置",
  "factArea": "128.23平方米",
  "factFeeStd": "1.4元/㎡/月",
  "factStartYear": "2022",
  "factStartMonth": "4",
  "factStartDay": "1",
  "factEndYear": "2024",
  "factEndMonth": "4",
  "factEndDay": "30",
  "factServiceContinue": "到期后继续服务至今",
  "factPayMethod": "按季度交纳",
  "factPenaltyStd": "欠费金额的20%",
  "owedAmount": "8078",
  "owedCalc": "1.4元×128.23㎡×45个月",
  "penaltyAmount2": "1615.6",
  "penaltyCalc": "8078×20%",
  "factCollection": "催缴情况描述",
  "factCollectionDate": "2025年12月20日",
  "factOther": "其他说明",
  "factRecord": "备案情况",
  "factClaimLaw1": "《民法典》第九百三十九条",
  "factClaimLaw2": "《民法典》第九百四十四条",
  "factClaimLaw3": "《民法典》第九百四十八条",
  "factClaimContract": "《合同名称》相关条款",
  "factEvidence": "证据清单"
}}
```

### 八、具状信息
```json
{{
  "plaintiff": "具状人名称",
  "legalRepSign": "法定代表人签字",
  "signDate": "2026年3月3日"
}}
```

## 输出要求

1. **只返回 JSON**，不要其他任何解释文字
2. **布尔值统一使用 true/false**
3. **日期统一使用 "YYYY年MM月DD日" 格式**
4. **金额去除千位分隔符逗号**
5. **没有的字段留空字符串""**

## 注意事项

- 仔细识别被告1和被告2，通常按"被告："、"被告："的顺序
- 注意区分"特别授权"和"一般授权"
- 物业费金额可能以"元"或"万元"为单位，注意转换
- 违约金可能是固定金额或按比例计算
- 证据清单可能很长，提取全部内容

请开始提取：
```

---

## 二、金融借款合同纠纷提取 Prompt

```markdown
你是一个专业的法律文书要素提取助手。请从以下金融借款合同纠纷起诉状文本中提取所有关键信息。

## 起诉状文本：
{TEXT}

## 提取要求

请以严格的 JSON 格式返回以下所有字段：

### 一、原告信息
```json
{{
  "fLenderName": "贷款人/原告名称",
  "fLenderAddr": "住所地",
  "fLenderRegAddr": "注册地",
  "fLegalRep": "法定代表人",
  "fLegalRepPosition": "职务",
  "fLenderPhone": "联系电话",
  "fLenderUscc": "统一社会信用代码"
}}
```

### 二、被告信息
```json
{{
  "fBorrowerName": "借款人/被告名称",
  "fBorrowerAddr": "住所地",
  "dName": "被告姓名（自然人）",
  "dMale": false,
  "dFemale": false,
  "dBirth": "",
  "dNation": "",
  "dAddr": "",
  "dIdNo": "",
  "dPhone": ""
}}
```

### 三、借款信息
```json
{{
  "fPrincipalAmount": "500000",
  "fPrincipalAgreed": "约定金额",
  "fPrincipalActual": "实际发放金额",
  "fDisbursementDate": "2024年1月1日",
  "loanStartYear": "2024",
  "loanStartMonth": "1",
  "loanStartDay": "1",
  "loanEndYear": "2027",
  "loanEndMonth": "1",
  "loanEndDay": "1",
  "maturedYes": true,
  "fInterestRate": "4.2",
  "fOverdueRate": "5.0",
  "compound": true,
  "fPenaltyRate": "5.0"
}}
```

### 四、还款情况
```json
{{
  "fRepayEqualPrincipalInterest": false,
  "fRepayEqualPrincipal": false,
  "fRepayOneTime": true,
  "fRepayMonthlyInterest": false,
  "fRepaidPrincipal": "100000",
  "fRepaidInterest": "20000",
  "fInterestPaidToDate": "2025年1月1日",
  "overdueYes": true
}}
```

### 五、诉讼请求
```json
{{
  "fInterestAmount": "20000",
  "fPenaltyAmount": "5000",
  "fCompoundAmount": "1000",
  "payableToEnd": true,
  "earlyRepayment": false,
  "contractTermination": false,
  "claimCollateral": true,
  "claimExpense": false,
  "claimFeeYes": true,
  "claimTotal": "526000"
}}
```

### 六、担保信息
```json
{{
  "collateralContract": true,
  "collateralType": "抵押",
  "collateralDesc": "房产抵押",
  "guaranteeContract": true,
  "guarantorName": "保证人名称",
  "guaranteeGeneral": false,
  "guaranteeJoint": true,
  "maxCollateral": false,
  "registrationYes": true,
  "registrationNo": "登记编号"
}}
```

### 七、事实与理由
```json
{{
  "factContractName": "《借款合同》",
  "factContractNo": "合同编号",
  "factContractDate": "2024年1月1日",
  "factContractLocation": "签订地点",
  "factClaimLaw1": "《民法典》第六百七十四条",
  "factClaimLaw2": "",
  "factClaimLaw3": "",
  "factClaimContract": "《借款合同》第X条",
  "factEvidence": "证据清单"
}}
```

## 输出要求

同物业服务合同纠纷

## 特别注意事项

- 注意区分"本金"、"利息"、"罚息"、"复利"、"违约金"
- 利率可能是年利率、月利率或日利率，注意统一
- 还款方式有多种：等额本息、等额本金、到期一次还本付息等
- 担保方式：抵押、质押、保证（一般/连带责任）
- 逾期是判断违约的关键事实

请开始提取：
```

---

## 三、Prompt 优化技巧

### 3.1 结构化输出

**要求严格的 JSON 格式**：

```markdown
## 输出格式要求

1. **只返回 JSON 对象**，不要有任何前缀或后缀
2. **所有键名必须使用双引号**
3. **字符串值使用双引号**
4. **布尔值使用 true/false**
5. **数字不使用引号**
6. **null 表示空值**

## 正确示例
```json
{"pName": "XX公司", "dMale": true}
```

## 错误示例
- ❌ 原告名称：XX公司
- ❌ {'pName': 'XX公司'}
- ❌ {"pName": "XX公司"} // 提取完成
```

### 3.2 Few-Shot 学习

**提供 1-2 个完整示例**：

```markdown
## 示例1

输入：
原告：A物业公司。被告：张三，男，1990年出生，汉族。欠物业费5000元。

输出：
```json
{
  "pName": "A物业公司",
  "dName": "张三",
  "dMale": true,
  "dBirth": "1990年XX月XX日",
  "dNation": "汉族",
  "feeAmount": "5000"
}
```

## 示例2

输入：
[更复杂的示例...]

输出：
```json
{...}
```
```

### 3.3 错误纠正

**明确常见错误**：

```markdown
## 常见错误提醒

1. ❌ 把被告1和被告2混淆
   ✅ 按照"被告："出现的顺序依次提取

2. ❌ 混淆"特别授权"和"一般授权"
   ✅ 检查关键词"特别授权"为true，"一般授权"为true
   ⚠️ 两者可以同时为false（未填写）

3. ❌ 金额带逗号或"元"字
   ✅ 纯数字，如："8078" 而不是 "8,078元"

4. ❌ 日期格式不统一
   ✅ 统一为 "2025年12月31日" 格式

5. ❌ 遗漏嵌套结构
   ✅ 注意被告信息、代理人信息都有1和2两组
```

### 3.4 容错处理

```markdown
## 容错说明

- 如果某个字段在文本中找不到，留空字符串""而不是 null
- 如果无法判断性别，两个字段都填 false
- 如果日期不完整（如只有年月），日填"01"
- 如果身份证号只有15位或18位，都接受
- 如果金额单位是"万元"，自动换算为元（×10000）
```

---

## 四、Prompt 调试方法

### 4.1 测试用例

准备 3-5 个典型的起诉状文本，包括：
- 简单案例（字段少）
- 复杂案例（字段多、有嵌套）
- 边界案例（字段缺失、格式特殊）

### 4.2 评估指标

| 指标 | 说明 | 目标 |
|------|------|------|
| 准确率 | 提取正确的字段数 / 总字段数 | >90% |
| 召回率 | 成功提取的字段数 / 应提取的字段数 | >85% |
| F1分数 | 准确率和召回率的调和平均数 | >87% |
| 格式正确率 | 返回的 JSON 格式正确 | 100% |

### 4.3 迭代优化

1. **第一批测试**：使用基础 Prompt
2. **分析错误**：统计哪些字段容易出错
3. **针对性优化**：在 Prompt 中强调这些字段
4. **第二批测试**：验证优化效果
5. **循环迭代**：直到达到目标指标

---

## 五、质量保障

### 5.1 后处理规则

```python
# 提取结果后处理
def post_process(data):
    # 1. 日期标准化
    if '2025.12.31' in data.get('dBirth', ''):
        data['dBirth'] = data['dBirth'].replace('.', '年') + '日'
    
    # 2. 金额去逗号
    if ',' in data.get('feeAmount', ''):
        data['feeAmount'] = data['feeAmount'].replace(',', '')
    
    # 3. 布尔值规范化
    for key in data:
        if data[key] == '是':
            data[key] = True
        elif data[key] == '否':
            data[key] = False
    
    return data
```

### 5.2 逻辑校验

```python
def validate(data):
    errors = []
    
    # 必填字段检查
    if not data.get('pName'):
        errors.append('原告名称不能为空')
    if not data.get('dName'):
        errors.append('被告名称不能为空')
    
    # 逻辑一致性检查
    if data.get('dMale') and data.get('dFemale'):
        errors.append('被告性别不能既是男又是女')
    
    # 金额计算验证
    try:
        total = float(data.get('claimTotal', '0'))
        fee = float(data.get('feeAmount', '0'))
        penalty = float(data.get('penaltyAmount', '0'))
        if total > 0 and abs(total - fee - penalty) > total * 0.1:
            errors.append('标的总额与各项金额之和不匹配')
    except:
        pass
    
    return errors
```

---

## 六、使用建议

### 6.1 提取策略

**策略1：纯规则提取**
- 优点：快速、可控
- 缺点：覆盖率低
- 适用：格式标准的文本

**策略2：纯大模型提取**
- 优点：理解力强
- 缺点：成本高、速度慢
- 适用：复杂、非标准格式

**策略3：混合模式（推荐）**
- 优点：兼顾速度和准确率
- 缺点：实现复杂
- 适用：生产环境

### 6.2 成本控制

```python
# 分级提取策略
def extract_with_llm(text):
    # 先用规则快速提取
    rule_result = extract_by_rules(text)
    
    # 如果规则提取成功率高，直接返回
    if rule_result.confidence > 0.8:
        return rule_result
    
    # 否则调用大模型
    llm_result = extract_by_llm(text)
    
    # 合并结果（大模型覆盖规则）
    return merge_results(rule_result, llm_result)
```

### 6.3 缓存策略

- 相同文本不重复提取
- 相似文本可复用部分结果
- 提取结果缓存24小时

---

**文档版本**: v1.0  
**最后更新**: 2026-04-15  
**维护者**: PLIC 开发团队
