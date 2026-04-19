# 要素式起诉状智能提取 Prompt 完整版

## 设计原则

1. **按法院要素表结构建模**，不是自定义字段
2. **支持多主体**：原告/被告/第三人，自然人与法人，多名并存
3. **覆盖全部表单字段**：包括P0/P1优先级字段
4. **分层结构**：通用字段 + 案由专属字段
5. **便于自动填表**：标准化输出 + 字段映射

---

# 一、通用版 Prompt（推荐）

## 适用场景
- 自动识别案由
- 提取通用诉状字段
- 提取当事人信息（支持多主体）
- 提取案由专属字段

```markdown
你是一个专业的"民事要素式起诉状信息提取助手"。你的任务是从起诉状文本中提取全部可填写字段，用于自动填写法院要素式起诉状表单。

## 输入文本
{TEXT}

## 任务目标
请从文本中提取：
1. 案由识别
2. 通用诉状字段
3. 当事人信息（原告/被告/第三人，自然人与法人，支持多名）
4. 委托诉讼代理人信息（支持多名）
5. 诉讼请求
6. 管辖与保全
7. 事实与理由
8. 证据清单
9. 纠纷解决意愿
10. 具状信息
11. 案由专属字段

## 输出要求
- **只返回 JSON**，不要任何解释文字
- 所有不存在字段统一返回空字符串 ""、空数组 [] 或 false
- 日期统一格式："YYYY年MM月DD日"
- 金额统一为阿拉伯数字字符串，不带逗号、不带"元"
- 布尔值统一 true / false
- 同一类型主体允许多名，统一用数组输出
- 若文本无法明确判断，不要猜测，填空字符串或 false

## JSON 结构

```json
{
  "case_type": "",
  "common": {
    "filing_info": {
      "drafter_name": "",
      "drafter_sign_or_seal": "",
      "filing_date": ""
    },
    "plaintiffs_natural": [
      {
        "name": "",
        "gender": "",
        "birth_date": "",
        "nation": "",
        "work_unit": "",
        "position": "",
        "phone": "",
        "domicile_addr": "",
        "usual_residence": "",
        "id_type": "",
        "id_no": ""
      }
    ],
    "plaintiffs_entity": [
      {
        "name": "",
        "addr": "",
        "reg_addr": "",
        "legal_representative": "",
        "position": "",
        "phone": "",
        "uscc": "",
        "entity_type": "",
        "ownership_type": ""
      }
    ],
    "agents": [
      {
        "name": "",
        "unit": "",
        "position": "",
        "phone": "",
        "authorization": ""
      }
    ],
    "defendants_natural": [
      {
        "name": "",
        "gender": "",
        "birth_date": "",
        "nation": "",
        "work_unit": "",
        "position": "",
        "phone": "",
        "domicile_addr": "",
        "usual_residence": "",
        "id_type": "",
        "id_no": ""
      }
    ],
    "defendants_entity": [
      {
        "name": "",
        "addr": "",
        "reg_addr": "",
        "legal_representative": "",
        "position": "",
        "phone": "",
        "uscc": "",
        "entity_type": "",
        "ownership_type": ""
      }
    ],
    "third_parties_natural": [
      {
        "name": "",
        "gender": "",
        "birth_date": "",
        "nation": "",
        "work_unit": "",
        "position": "",
        "phone": "",
        "domicile_addr": "",
        "usual_residence": "",
        "id_type": "",
        "id_no": ""
      }
    ],
    "third_parties_entity": [
      {
        "name": "",
        "addr": "",
        "reg_addr": "",
        "legal_representative": "",
        "position": "",
        "phone": "",
        "uscc": "",
        "entity_type": "",
        "ownership_type": ""
      }
    ],
    "claims_common": {
      "claim_litigation_fee": false,
      "other_claims": "",
      "claim_total_amount": ""
    },
    "jurisdiction_and_preservation": {
      "has_jurisdiction_clause": false,
      "jurisdiction_clause_text": "",
      "has_pre_litigation_preservation": false,
      "preservation_court": "",
      "preservation_date": "",
      "preservation_case_no": ""
    },
    "fact_basis_common": {
      "liability_basis_contract": "",
      "liability_basis_law": "",
      "other_notes": "",
      "evidence_list": ""
    },
    "mediation_willingness": {
      "know_mediation": "",
      "know_benefit_1": "",
      "know_benefit_2": "",
      "know_benefit_3": "",
      "know_benefit_4": "",
      "know_benefit_5": "",
      "consider_pre_mediation": ""
    }
  },
  "property_service": {
    "claim_property_fee_amount": "",
    "claim_penalty_amount": "",
    "claim_penalty_to_actual_payment_date": false,
    "contract_name": "",
    "contract_no": "",
    "contract_sign_date": "",
    "contract_sign_location": "",
    "contract_party_owner_or_constructor": "",
    "contract_party_property_service_provider": "",
    "property_location": "",
    "property_area": "",
    "property_owner": "",
    "property_fee_standard": "",
    "service_start_date": "",
    "service_end_date": "",
    "service_continued_after_expiry": "",
    "payment_method": "",
    "penalty_standard": "",
    "owed_property_fee_amount": "",
    "owed_property_fee_calc": "",
    "owed_penalty_amount": "",
    "owed_penalty_calc": "",
    "collection_status": "",
    "record_filing_status": "",
    "request_basis_contract": "",
    "request_basis_law": "",
    "evidence_list": ""
  },
  "financial_loan": {
    "lender": "",
    "borrower": "",
    "co_repayer": "",
    "guarantor": "",
    "loan_contract_name": "",
    "loan_contract_no": "",
    "loan_contract_date": "",
    "loan_contract_location": "",
    "principal_agreed": "",
    "principal_actual": "",
    "loan_start_date": "",
    "loan_end_date": "",
    "loan_matured": false,
    "interest_rate_normal": "",
    "interest_rate_overdue": "",
    "compound_interest_rule": "",
    "penalty_rate": "",
    "disbursement_date": "",
    "repayment_method": "",
    "repaid_principal": "",
    "repaid_interest": "",
    "interest_paid_to_date": "",
    "is_overdue": false,
    "overdue_desc": "",
    "claim_principal_amount": "",
    "claim_interest_penalty_compound_amount": "",
    "claim_interest_to_actual_payment_date": false,
    "claim_interest_to_actual_payment_rule": "",
    "claim_early_repayment": false,
    "claim_contract_termination": false,
    "claim_guarantee_right": false,
    "claim_guarantee_right_desc": "",
    "claim_creditor_cost": false,
    "creditor_cost_desc": "",
    "has_collateral_contract": false,
    "collateral_type": "",
    "collateral_desc": "",
    "is_max_collateral": false,
    "max_collateral_limit": "",
    "max_collateral_debt_determination_date": "",
    "has_registration": false,
    "registration_type": "",
    "registration_no": "",
    "has_guarantee_contract": false,
    "guarantee_main_content": "",
    "guarantee_type": "",
    "other_guarantee_type": "",
    "other_guarantee_desc": "",
    "request_basis_contract": "",
    "request_basis_law": "",
    "evidence_list": "",
    "priority_repayment_claim": ""
  },
  "raw_spans": {
    "claims_text": "",
    "facts_text": "",
    "evidence_text": "",
    "jurisdiction_text": "",
    "mediation_text": ""
  }
}
```

## 提取规则

### 1. 案由识别
- 出现"物业服务合同纠纷"则 `case_type="物业服务合同纠纷"`
- 出现"金融借款合同纠纷"则 `case_type="金融借款合同纠纷"`

### 2. 当事人识别规则
- 原告、被告、第三人都可能同时存在"自然人"和"法人/非法人组织"
- 多人时按文本出现顺序放入数组
- 不得遗漏第二被告、第三被告、共同还款人、保证人等

### 3. 委托诉讼代理人
- 支持多名代理人
- `authorization` 只填写：`"一般授权"`、`"特别授权"`、`"一般授权+特别授权"`、`""`

### 4. 日期规则
- 年月日齐全则按原值输出
- 只有年月时补"01日"
- 只有年份时补"01月01日"

### 5. 金额规则
- 去掉"元""人民币""￥"","
- "万元"自动换算为元

### 6. 法律依据
- 合同依据、法律依据分开提取
- 若同时出现多个法条，用分号连接

### 7. 证据清单
- 尽量完整保留原文
- 多条证据用换行或分号分隔

## 特别规则

1. 输出的 JSON 必须足以直接回填法院要素式起诉状表单
2. 任何表单中出现、且文本中能识别的信息，都不得遗漏
3. 若同类主体存在多名，必须使用数组完整返回
4. 若文本中同时出现自然人被告、法人被告、共同还款人、保证人、抵押人、第三人，必须分别识别
5. "合同依据""法律依据""诉讼请求""事实与理由""证据清单"必须尽可能完整保留
6. 若案由为物业服务合同纠纷，只重点填充 `property_service`��`financial_loan` 置空
7. 若案由为金融借款合同纠纷，只重点填充 `financial_loan`，`property_service` 置空
8. 不得缺少 `common` 部分

只返回 JSON，不要其他解释。
```

---

# 二、字段映射表

## 物业服务合同纠纷映射

### 原告法人信息
```
common.plaintiffs_entity[0].name -> pName
common.plaintiffs_entity[0].addr -> pAddr
common.plaintiffs_entity[0].reg_addr -> pRegAddr
common.plaintiffs_entity[0].legal_representative -> pLegal
common.plaintiffs_entity[0].position -> pPosition
common.plaintiffs_entity[0].phone -> pPhone
common.plaintiffs_entity[0].uscc -> pUscc
common.plaintiffs_entity[0].entity_type -> pTypeLLC (有限责任公司=true)
common.plaintiffs_entity[0].ownership_type -> pOwnerPrivate (民营=true)
```

### 被告自然人信息
```
common.defendants_natural[0].name -> dName
common.defendants_natural[0].gender -> dMale/dFemale
common.defendants_natural[0].birth_date -> dBirth
common.defendants_natural[0].nation -> dNation
common.defendants_natural[0].domicile_addr -> dAddr
common.defendants_natural[0].id_no -> dIdNo
common.defendants_natural[0].phone -> dPhone
```

### 被告2（如存在）
```
common.defendants_natural[1].name -> d2Name
common.defendants_natural[1].gender -> d2Male/d2Female
...（其他字段同上）
```

### 委托代理人
```
common.agents[0].name -> agent1Name
common.agents[0].unit -> agent1Unit
common.agents[0].position -> agent1Title
common.agents[0].phone -> agent1Phone
common.agents[0].authorization -> agent1Special/agent1General
```

### 物业费相关
```
property_service.owed_property_fee_amount -> feeAmount
property_service.owed_penalty_amount -> penaltyAmount
property_service.claim_penalty_to_actual_payment_date -> payableToEndNo
common.claims_common.claim_litigation_fee -> claimFeeYes
common.claims_common.claim_total_amount -> claimTotal
```

### 管辖保全
```
common.jurisdiction_and_preservation.has_jurisdiction_clause -> noJurisdiction (取反)
common.jurisdiction_and_preservation.has_pre_litigation_preservation -> noPreservation (取反)
```

### 事实理由
```
property_service.contract_name -> factContractName
property_service.contract_sign_date + contract_sign_location -> factContract
property_service.contract_party_property_service_provider -> factPropCompany
property_service.property_owner -> factOwner
property_service.property_location -> factLocation
property_service.property_area -> factArea
property_service.property_fee_standard -> factFeeStd
property_service.service_start_date -> factStartYear + factStartMonth + factStartDay
property_service.service_end_date -> factEndYear + factEndMonth + factEndDay
property_service.service_continued_after_expiry -> factServiceContinue
property_service.payment_method -> factPayMethod
property_service.penalty_standard -> factPenaltyStd
property_service.owed_property_fee_amount -> owedAmount
property_service.owed_property_fee_calc -> owedCalc
property_service.owed_penalty_amount -> penaltyAmount2
property_service.owed_penalty_calc -> penaltyCalc
property_service.collection_status -> factCollection
property_service.record_filing_status -> factRecord
property_service.request_basis_law -> factClaimLaw1/2/3
property_service.request_basis_contract -> factClaimContract
property_service.evidence_list -> factEvidence
```

### 具状信息
```
common.filing_info.drafter_name -> plaintiff
common.filing_info.drafter_sign_or_seal -> legalRepSign
common.filing_info.filing_date -> signDate
```

## 金融借款合同纠纷映射

### 原告信息
```
common.plaintiffs_entity[0].name -> fLenderName
common.plaintiffs_entity[0].addr -> fLenderAddr
common.plaintiffs_entity[0].legal_representative -> fLegalRep
common.plaintiffs_entity[0].position -> fLegalRepPosition
```

### 被告信息
```
common.defendants_entity[0].name -> fBorrowerName
common.defendants_entity[0].addr -> fBorrowerAddr
financial_loan.guarantor -> guarantorName
```

### 借款信息
```
financial_loan.principal_agreed -> fPrincipalAgreed
financial_loan.principal_actual -> fPrincipalActual
financial_loan.loan_start_date -> loanStartYear + loanStartMonth + loanStartDay
financial_loan.loan_end_date -> loanEndYear + loanEndMonth + loanEndDay
financial_loan.loan_matured -> maturedYes
financial_loan.interest_rate_normal -> fInterestRate
financial_loan.interest_rate_overdue -> fOverdueRate
financial_loan.penalty_rate -> fPenaltyRate
```

### 还款情况
```
financial_loan.repayment_method -> fRepayEqualPrincipalInterest/fRepayEqualPrincipal/fRepayOneTime/fRepayMonthlyInterest
financial_loan.repaid_principal -> fRepaidPrincipal
financial_loan.repaid_interest -> fRepaidInterest
financial_loan.interest_paid_to_date -> fInterestPaidToDate
financial_loan.is_overdue -> overdueYes
```

### 诉讼请求
```
financial_loan.claim_principal_amount -> fPrincipalAmount
financial_loan.claim_interest_penalty_compound_amount -> fInterestAmount + fPenaltyAmount + fCompoundAmount
financial_loan.claim_interest_to_actual_payment_date -> payableToEnd
financial_loan.claim_guarantee_right -> claimCollateral
financial_loan.claim_creditor_cost -> claimExpense
```

### 担保信息
```
financial_loan.has_collateral_contract -> collateralContract
financial_loan.collateral_type -> collateralType
financial_loan.collateral_desc -> collateralDesc
financial_loan.has_guarantee_contract -> guaranteeContract
financial_loan.guarantee_type -> guaranteeJoint/guaranteeGeneral
financial_loan.is_max_collateral -> maxCollateral
financial_loan.has_registration -> registrationYes
financial_loan.registration_no -> registrationNo
```

---

# 三、后处理函数

```python
def post_process_extraction(data: dict) -> dict:
    """后处理提取结果，映射到表单字段"""
    
    result = {}
    case_type = data.get("case_type", "")
    
    if case_type == "物业服务合同纠纷":
        # 映射物业字段
        common = data.get("common", {})
        prop = data.get("property_service", {})
        
        # 原告法人
        plaintiffs = common.get("plaintiffs_entity", [])
        if plaintiffs:
            p = plaintiffs[0]
            result.update({
                "pName": p.get("name", ""),
                "pAddr": p.get("addr", ""),
                "pRegAddr": p.get("reg_addr", ""),
                "pLegal": p.get("legal_representative", ""),
                "pPosition": p.get("position", ""),
                "pPhone": p.get("phone", ""),
                "pUscc": p.get("uscc", ""),
                "pTypeLLC": p.get("entity_type") == "有限责任公司",
                "pOwnerPrivate": p.get("ownership_type") == "民营"
            })
        
        # 被告自然人
        defendants = common.get("defendants_natural", [])
        if defendants:
            d = defendants[0]
            result.update({
                "dName": d.get("name", ""),
                "dMale": d.get("gender") == "男",
                "dFemale": d.get("gender") == "女",
                "dBirth": d.get("birth_date", ""),
                "dNation": d.get("nation", ""),
                "dAddr": d.get("domicile_addr", ""),
                "dIdNo": d.get("id_no", ""),
                "dPhone": d.get("phone", "")
            })
        
        # 被告2
        if len(defendants) > 1:
            d2 = defendants[1]
            result.update({
                "d2Name": d2.get("name", ""),
                "d2Male": d2.get("gender") == "男",
                "d2Female": d2.get("gender") == "女",
                # ... 其他字段
            })
        
        # 代理人
        agents = common.get("agents", [])
        if agents:
            a1 = agents[0]
            result.update({
                "hasAgent": True,
                "agent1Name": a1.get("name", ""),
                "agent1Unit": a1.get("unit", ""),
                "agent1Title": a1.get("position", ""),
                "agent1Phone": a1.get("phone", ""),
                "agent1Special": "特别授权" in a1.get("authorization", ""),
                "agent1General": "一般授权" in a1.get("authorization", "")
            })
        
        # 物业费
        result.update({
            "feeAmount": prop.get("owed_property_fee_amount", ""),
            "penaltyAmount": prop.get("owed_penalty_amount", ""),
            "payableToEndNo": prop.get("claim_penalty_to_actual_payment_date", False),
            "claimFeeYes": common.get("claims_common", {}).get("claim_litigation_fee", False),
            "claimTotal": common.get("claims_common", {}).get("claim_total_amount", "")
        })
        
        # 事实理由
        result.update({
            "factContractName": prop.get("contract_name", ""),
            "factPropCompany": prop.get("contract_party_property_service_provider", ""),
            "factOwner": prop.get("property_owner", ""),
            "factLocation": prop.get("property_location", ""),
            "factArea": prop.get("property_area", ""),
            "factFeeStd": prop.get("property_fee_standard", ""),
            "factServiceContinue": prop.get("service_continued_after_expiry", ""),
            "factPayMethod": prop.get("payment_method", ""),
            "factPenaltyStd": prop.get("penalty_standard", ""),
            "owedAmount": prop.get("owed_property_fee_amount", ""),
            "owedCalc": prop.get("owed_property_fee_calc", ""),
            "penaltyAmount2": prop.get("owed_penalty_amount", ""),
            "penaltyCalc": prop.get("owed_penalty_calc", ""),
            "factRecord": prop.get("record_filing_status", "")
        })
        
        # 具状信息
        filing = common.get("filing_info", {})
        result.update({
            "plaintiff": filing.get("drafter_name", ""),
            "legalRepSign": filing.get("drafter_sign_or_seal", ""),
            "signDate": filing.get("filing_date", "")
        })
    
    elif case_type == "金融借款合同纠纷":
        # 映射金融字段
        common = data.get("common", {})
        loan = data.get("financial_loan", {})
        
        # 原告
        plaintiffs = common.get("plaintiffs_entity", [])
        if plaintiffs:
            p = plaintiffs[0]
            result.update({
                "fLenderName": p.get("name", ""),
                "fLenderAddr": p.get("addr", ""),
                "fLegalRep": p.get("legal_representative", ""),
                "fLegalRepPosition": p.get("position", "")
            })
        
        # 被告
        defendants = common.get("defendants_entity", [])
        if defendants:
            d = defendants[0]
            result.update({
                "fBorrowerName": d.get("name", ""),
                "fBorrowerAddr": d.get("addr", "")
            })
        
        # 借款信息
        result.update({
            "fPrincipalAmount": loan.get("claim_principal_amount", ""),
            "fPrincipalAgreed": loan.get("principal_agreed", ""),
            "fPrincipalActual": loan.get("principal_actual", ""),
            "maturedYes": loan.get("loan_matured", False),
            "fInterestRate": loan.get("interest_rate_normal", ""),
            "fOverdueRate": loan.get("interest_rate_overdue", ""),
            "fPenaltyRate": loan.get("penalty_rate", ""),
            "overdueYes": loan.get("is_overdue", False)
        })
        
        # 还款情况
        repayment_method = loan.get("repayment_method", "")
        result.update({
            "fRepayEqualPrincipalInterest": "等额本息" in repayment_method,
            "fRepayEqualPrincipal": "等额本金" in repayment_method,
            "fRepayOneTime": "一次还本" in repayment_method or "到期" in repayment_method,
            "fRepaidPrincipal": loan.get("repaid_principal", ""),
            "fRepaidInterest": loan.get("repaid_interest", "")
        })
        
        # 诉讼请求
        result.update({
            "payableToEnd": loan.get("claim_interest_to_actual_payment_date", False),
            "claimCollateral": loan.get("claim_guarantee_right", False),
            "claimExpense": loan.get("claim_creditor_cost", False)
        })
        
        # 担保信息
        guarantee_type = loan.get("guarantee_type", "")
        result.update({
            "collateralContract": loan.get("has_collateral_contract", False),
            "guaranteeContract": loan.get("has_guarantee_contract", False),
            "guaranteeJoint": "连带" in guarantee_type,
            "guaranteeGeneral": "一般" in guarantee_type,
            "maxCollateral": loan.get("is_max_collateral", False),
            "registrationYes": loan.get("has_registration", False)
        })
    
    return result
```

---

# 四、使用示例

## 完整流程

```python
# 1. 调用大模型提取
raw_data = call_llm(prompt_with_text)

# 2. 解析JSON
import json
data = json.loads(raw_data)

# 3. 后处理映射
form_data = post_process_extraction(data)

# 4. 填充表单
for field, value in form_data.items():
    if hasattr(form, field):
        setattr(form, field, value)
```

## 质量检查

```python
def validate_extraction(data: dict) -> list:
    """验证提取结果完整性"""
    errors = []
    case_type = data.get("case_type", "")
    
    # 检查必填字段
    common = data.get("common", {})
    
    if not common.get("plaintiffs_entity") and not common.get("plaintiffs_natural"):
        errors.append("缺少原告信息")
    
    if not common.get("defendants_entity") and not common.get("defendants_natural"):
        errors.append("缺少被告信息")
    
    if case_type == "物业服务合同纠纷":
        prop = data.get("property_service", {})
        if not prop.get("contract_name"):
            errors.append("缺少物业合同名称")
    
    elif case_type == "金融借款合同纠纷":
        loan = data.get("financial_loan", {})
        if not loan.get("loan_contract_name"):
            errors.append("缺少借款合同名称")
    
    return errors
```

---

**文档版本**: v2.0 完整版  
**最后更新**: 2026-04-11  
**维护者**: PLIC 开发团队
