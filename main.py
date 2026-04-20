# -*- coding: utf-8 -*-
"""
诉前智检 (PLIC) 后端服务
支持案由：金融借款合同纠纷、物业服务合同纠纷
支持智能提取：
  1. 腾讯元器（默认，已配置）
  2. OpenAI（需配置 OPENAI_API_KEY）
启动方式：uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import re
import json
import os
import requests

# ==================== 腾讯元器配置 ====================
YQ_APPKEY = "i9pv6CRbCyMGLbQ4YxL4sHS4R8ER6iJa"  # appkey
YQ_APPID = "2042436439992732864"                    # appid
YQ_API_URL = "https://yuanqi.tencent.com/openapi/v1/agent/chat/completions"

def call_yuanqi(message: str) -> Dict[str, Any]:
    """调用腾讯元器智能体"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {YQ_APPKEY}"
    }
    payload = {
        "assistant_id": YQ_APPID,
        "user_id": "plic_user",
        "stream": False,
        "messages": [{
            "role": "user",
            "content": [{"type": "text", "text": message}]
        }]
    }
    try:
        resp = requests.post(YQ_API_URL, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        return {"error": True, "message": resp.text}
    except Exception as e:
        return {"error": True, "message": str(e)}

# 尝试导入 OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI SDK not installed. Run: pip install openai")

app = FastAPI(title="诉前智检API")

# 允许跨域（前端调试）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 请求模型 ====================
class CaseRequest(BaseModel):
    case_type: str  # "finance" 或 "property"
    text: str       # 案情描述

# ==================== 金融借款合同纠纷规则引擎 ====================
def extract_finance_elements(text: str) -> Dict[str, Any]:
    """从文本中抽取金融借款关键要素（基于正则模拟）"""
    elements = {
        "lender": "贷款机构",      # 贷款人
        "borrower": "借款人",
        "principal": 0.0,         # 本金
        "interest_rate": 0.0,     # 年利率(%)
        "loan_date": "未明确",
        "due_date": "未明确",
        "repayment_status": "未明确",
        "overdue_status": "未逾期",
        "evidence": []
    }
    # 借款人识别
    borrower_match = re.search(r"借款人[：:]\s*([^，,。；\n]+)", text)
    if not borrower_match:
        borrower_match = re.search(r"向\s*([^，,。；\n]{2,8})\s*发放贷款", text)
    if borrower_match:
        elements["borrower"] = borrower_match.group(1).strip()
    # 本金
    principal_match = re.search(r"(\d+(?:\.\d+)?)\s*万?元?[的金利]", text)
    if principal_match:
        val = float(principal_match.group(1))
        if "万" in text[principal_match.start():principal_match.end()+2]:
            val *= 10000
        elements["principal"] = val
    # 利率
    rate_match = re.search(r"年利率\s*(\d+(?:\.\d+)?)\s*%", text)
    if rate_match:
        elements["interest_rate"] = float(rate_match.group(1))
    # 日期
    date_match = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", text)
    if date_match:
        elements["loan_date"] = date_match.group(1)
    due_match = re.search(r"到期日[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日)", text)
    if due_match:
        elements["due_date"] = due_match.group(1)
    # 逾期判断
    if "逾期" in text or "未还" in text or "违约" in text:
        elements["overdue_status"] = "已逾期"
        elements["repayment_status"] = "未足额还款"
    # 证据
    if "借款合同" in text:
        elements["evidence"].append("借款合同")
    if "放款凭证" in text or "转账" in text:
        elements["evidence"].append("放款凭证")
    if "催收" in text:
        elements["evidence"].append("催收记录")
    return elements

def finance_rule_engine(elements: Dict) -> Dict:
    """金融借款规则：被告、管辖、诉请"""
    defendant = elements["borrower"]
    court = "被告住所地人民法院（若合同有约定则从约定）"
    # 简单管辖逻辑
    if "北京" in elements.get("borrower", "") or "上海" in elements.get("borrower", ""):
        court = f"{defendant[:2]}市相关基层人民法院"
    claims = [
        f"请求判令被告{defendant}偿还原告借款本金{elements['principal']:.2f}元" if elements['principal'] else "请求判令被告偿还借款本金（具体金额以合同为准）",
        "请求判令被告支付利息及逾期利息（按合同约定计算）",
        "请求判令被告承担本案全部诉讼费用"
    ]
    return {
        "defendant": defendant,
        "court": court,
        "claims": claims
    }

def generate_finance_complaint(elements: Dict, rules: Dict) -> str:
    """生成金融借款要素式起诉状（文本格式）"""
    complaint = f"""【要素式民事起诉状 · 金融借款合同纠纷】

原告（贷款人）：{elements['lender']}
被告（借款人）：{rules['defendant']}

诉讼请求：
{chr(10).join(f"{i+1}. {c}" for i,c in enumerate(rules['claims']))}

事实与要素：
1. 贷款事实：{elements['loan_date']}，原告向被告发放贷款{elements['principal']:.2f}元，约定年利率{elements['interest_rate']}%，到期日{elements['due_date']}。
2. 还款情况：{elements['repayment_status']}，目前{elements['overdue_status']}。
3. 证据材料：{', '.join(elements['evidence']) if elements['evidence'] else '合同、转账记录等'}。
4. 管辖依据：根据《民事诉讼法》及合同约定，本案应由{rules['court']}管辖。

证据清单（建议提交）：
□ 借款合同/借据
□ 银行放款凭证
□ 还款记录及催收函件
□ 当事人身份证明

风险提示：请确保原件留存，逾期利息计算方式需与合同一致。
"""
    return complaint

# ==================== 物业服务合同纠纷规则引擎 ====================
def extract_property_elements(text: str) -> Dict[str, Any]:
    """抽取物业合同纠纷要素"""
    elements = {
        "property_company": "物业公司",
        "owner": "业主",
        "house_info": "未提供",
        "debt_period": "未明确",
        "debt_amount": 0.0,
        "service_quality": "正常",
        "collection_records": False,
        "evidence": []
    }
    # 物业公司
    prop_match = re.search(r"([^，,。；\n]{2,12}物业公司)", text)
    if prop_match:
        elements["property_company"] = prop_match.group(1)
    # 业主
    owner_match = re.search(r"业主\s*([^，,。；\n]{2,6})", text)
    if not owner_match:
        owner_match = re.search(r"([^，,。；\n]{2,6})名下房屋", text)
    if owner_match:
        elements["owner"] = owner_match.group(1)
    # 欠费金额
    amount_match = re.search(r"(\d+(?:\.\d+)?)\s*元?[的欠物]", text)
    if amount_match:
        elements["debt_amount"] = float(amount_match.group(1))
    # 欠费期间
    period_match = re.search(r"(\d{4}年\d{1,2}月至\d{4}年\d{1,2}月)", text)
    if period_match:
        elements["debt_period"] = period_match.group(1)
    # 服务情况
    if "服务不达标" in text or "质量问题" in text:
        elements["service_quality"] = "存在争议"
    # 催收记录
    if "催收" in text:
        elements["collection_records"] = True
        elements["evidence"].append("催收记录")
    if "物业服务合同" in text:
        elements["evidence"].append("物业服务合同")
    if "欠费明细" in text:
        elements["evidence"].append("欠费明细")
    return elements

def property_rule_engine(elements: Dict) -> Dict:
    """物业合同规则：被告、管辖、诉请"""
    defendant = elements["owner"]
    court = "不动产所在地人民法院（即物业所在地法院）"
    claims = [
        f"请求判令被告{elements['owner']}支付拖欠的物业服务费{elements['debt_amount']:.2f}元" if elements['debt_amount'] else "请求判令被告支付拖欠的物业服务费",
        "请求判令被告支付违约金（按合同约定计算）",
        "请求判令被告承担本案全部诉讼费用"
    ]
    return {
        "defendant": defendant,
        "court": court,
        "claims": claims
    }

def generate_property_complaint(elements: Dict, rules: Dict) -> str:
    """生成物业服务合同要素式起诉状"""
    complaint = f"""【要素式民事起诉状 · 物业服务合同纠纷】

原告（物业公司）：{elements['property_company']}
被告（业主）：{rules['defendant']}

诉讼请求：
{chr(10).join(f"{i+1}. {c}" for i,c in enumerate(rules['claims']))}

事实与要素：
1. 服务关系：原告为{elements['house_info']}所在小区提供物业服务，被告系该小区业主。
2. 欠费情况：{elements['debt_period']}期间，被告拖欠物业费共计{elements['debt_amount']:.2f}元。
3. 服务履行：{elements['service_quality']}，原告已按约提供服务。
4. 催收情况：{'已多次催收' if elements['collection_records'] else '催收记录需补充'}。
5. 管辖依据：根据《民事诉讼法》第33条，因不动产纠纷提起的诉讼，由不动产所在地人民法院管辖，即{rules['court']}。

证据清单（建议提交）：
□ 物业服务合同
□ 欠费明细表
□ 催收通知书/记录
□ 业主身份证明

风险提示：若业主提出服务质量抗辩，需准备服务达标证据。
"""
    return complaint

# ==================== 统一接口 ====================
@app.post("/api/generate")
async def generate_case(request: CaseRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="案情描述不能为空")

    if request.case_type == "finance":
        elements = extract_finance_elements(text)
        rules = finance_rule_engine(elements)
        complaint = generate_finance_complaint(elements, rules)
        return {
            "defendant": rules["defendant"],
            "court": rules["court"],
            "elements": elements,
            "complaint": complaint,
            "claims": rules["claims"]
        }
    elif request.case_type == "property":
        elements = extract_property_elements(text)
        rules = property_rule_engine(elements)
        complaint = generate_property_complaint(elements, rules)
        return {
            "defendant": rules["defendant"],
            "court": rules["court"],
            "elements": elements,
            "complaint": complaint,
            "claims": rules["claims"]
        }
    else:
        raise HTTPException(status_code=400, detail="案由类型错误，请选择 finance 或 property")

# ==================== 测试用例接口 ====================
@app.get("/api/test-cases")
async def get_test_cases():
    """获取基于真实判决书的测试用例"""
    test_cases = [
        {
            "id": 1,
            "name": "世茂天成物业诉陈思聪物业费纠纷案",
            "case_type": "property",
            "input": "世茂天成物业服务集团有限公司烟台分公司起诉陈思聪，要求支付2019年1月至2020年12月期间的物业费共计3650元，并支付违约金。陈思聪房屋位于烟台市芝罘区XX路。",
            "expected_output": {
                "defendant": "陈思聪",
                "court": "烟台市芝罘区人民法院（不动产所在地）",
                "debt_amount": 3650
            }
        },
        {
            "id": 2,
            "name": "A公司B公司物业合同纠纷案",
            "case_type": "property",
            "input": "A物业公司起诉B公司，要求支付2020年1月至2021年12月期间的物业服务费28000元及违约金。B公司物业位于北京市朝阳区XX大厦。",
            "expected_output": {
                "defendant": "B公司",
                "court": "北京市朝阳区人民法院（不动产所在地）",
                "debt_amount": 28000
            }
        },
        {
            "id": 3,
            "name": "银行张三借款纠纷案",
            "case_type": "finance",
            "input": "某银行于2024年1月1日向借款人张三发放贷款500000元，约定年利率4.2%，到期日2027年1月1日。张三自2025年1月起未还款，构成逾期。银行持有借款合同、放款凭证、催收记录。",
            "expected_output": {
                "defendant": "张三",
                "principal": 500000,
                "interest_rate": 4.2
            }
        }
    ]
    return {"test_cases": test_cases}

# ==================== 腾讯元器智能提取接口 ====================
class ExtractRequest(BaseModel):
    case_type: str  # "finance" 或 "property"
    text: str       # 要提取的文本

@app.post("/api/extract")
async def smart_extract(request: ExtractRequest):
    """
    使用腾讯元器智能体提取起诉状中的所有要素
    """
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="文本不能为空")

    # 构建提示词，让腾讯元器提取所有要素
    if request.case_type == "property":
        prompt = f"""请从以下物业服务合同纠纷起诉状中提取所有要素，返回JSON格式。

起诉状文本：
{text}

请提取以下所有字段（没有的留空字符串或null）：
{{
    "pName": "原告名称",
    "pAddr": "住所地",
    "pRegAddr": "注册地",
    "pLegal": "法定代表人",
    "pPosition": "职务",
    "pPhone": "联系电话",
    "pUscc": "统一社会信用代码",
    "pTypeLLC": true/false,  // 是否有限责任公司
    "pOwnerPrivate": true/false,  // 是否民营
    "hasAgent": true/false,
    "agent1Name": "代理人1姓名",
    "agent1Unit": "代理人1单位",
    "agent1Title": "代理人1职务",
    "agent1Special": true/false,
    "agent1General": true/false,
    "agent2Name": "代理人2姓名",
    "agent2Unit": "代理人2单位",
    "agent2Title": "代理人2职务",
    "agent2Special": true/false,
    "agent2General": true/false,
    "dName": "被告1姓名",
    "dMale": true/false,
    "dFemale": true/false,
    "dBirth": "被告1出生日期",
    "dNation": "民族",
    "dAddr": "住址",
    "dIdNo": "身份证号",
    "dPhone": "电话",
    "d2Name": "被告2姓名",
    "d2Male": true/false,
    "d2Female": true/false,
    "d2Birth": "被告2出生日期",
    "d2Nation": "民族",
    "d2Addr": "住址",
    "d2IdNo": "身份证号",
    "d2Phone": "电话",
    "feeEndDate": "物业费截止日期",
    "feeAmount": "物业费金额",
    "penaltyAmount": "违约金金额",
    "payableToEndNo": true/false,  // 是否不请求至清偿日
    "claimFeeYes": true/false,
    "claimTotal": "标的总额",
    "noJurisdiction": true/false,
    "noPreservation": true/false,
    "factContractName": "合同名称",
    "factContract": "合同信息",
    "factPropCompany": "物业服务公司",
    "factOwner": "所有权人",
    "factLocation": "坐落位置",
    "factArea": "建筑面积",
    "factFeeStd": "物业费标准",
    "factStartYear": "服务开始年",
    "factStartMonth": "服务开始月",
    "factStartDay": "服务开始日",
    "factEndYear": "服务结束年",
    "factEndMonth": "服务结束月",
    "factEndDay": "服务结束日",
    "factServiceContinue": "事实服务延续说明",
    "factPayMethod": "支付方式",
    "factPenaltyStd": "违约金标准",
    "owedAmount": "欠付金额",
    "owedCalc": "计算方式",
    "penaltyAmount2": "应付违约金",
    "penaltyCalc": "违约金计算方式",
    "factCollection": "催缴情况",
    "factCollectionDate": "最后催收日期",
    "factOther": "其他说明",
    "factRecord": "备案情况",
    "factClaimLaw1": "法律依据1",
    "factClaimLaw2": "法律依据2",
    "factClaimLaw3": "法律依据3",
    "factClaimContract": "合同依据",
    "factEvidence": "证据清单",
    "plaintiff": "具状人",
    "legalRepSign": "法定代表人签字",
    "signDate": "日期",
    "hasContactChange": true/false,  // 是否有联系方式变更
    "contactChangeDate": "变更日期",
    "contactChangeReason": "变更原因",
    "newPhone": "新电话",
    "newAddr": "新地址"
}}

只返回JSON，不要其他解释。"""
    else:
        prompt = f"""请从以下金融借款合同纠纷起诉状中提取所有要素，返回JSON格式。

起诉状文本：
{text}

请提取以下所有字段：
{{
    "fLenderName": "贷款人/原告名称",
    "fBorrowerName": "借款人/被告名称",
    "fBorrowerAddr": "借款人地址",
    "fPrincipalAmount": "借款本金",
    "fInterestRate": "年利率",
    "rateYes": true/false,
    "payableToEndNo": true/false,
    "claimFeeYes": true/false,
    "noJurisdiction": true/false,
    "noPreservation": true/false,
    "maturedYes": true/false,
    "overdueYes": true/false,
    "repayOneTime": true/false,
    "evidence": "证据清单"
}}

只返回JSON，不要其他解释。"""

    # 调用腾讯元器
    response = call_yuanqi(prompt)

    if response.get("error"):
        return {
            "success": False,
            "error": f"腾讯元器调用失败: {response.get('message')}",
            "data": {}
        }

    try:
        # 解析腾讯元器响应
        choices = response.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content", "")
            # 提取JSON
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                data = json.loads(json_match.group())
                return {"success": True, "data": data, "raw": content}

        return {
            "success": True,
            "data": {},
            "raw": str(response)
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON解析失败: {str(e)}",
            "data": {}
        }


@app.get("/api/config")
async def get_config():
    """获取配置信息"""
    return {
        "provider": "tencent_yuanqi",
        "yq_enabled": bool(YQ_APPKEY and YQ_APPID),
        "openai_enabled": bool(os.environ.get("OPENAI_API_KEY")) if OPENAI_AVAILABLE else False
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("PLIC - 诉前智检系统")
    print("=" * 50)
    print("API Endpoints:")
    print("  POST /api/generate - 生成起诉状")
    print("  POST /api/extract  - 腾讯元器智能提取")
    print("  GET  /api/config   - 查看配置")
    print()
    print("智能体已配置: 腾讯元器")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8001)
