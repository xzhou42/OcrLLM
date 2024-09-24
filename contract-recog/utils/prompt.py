# COLLECTION_PROMPT = """
# 请从下面的使用"#####"包围的文字中提取信息：
# #####
# {ocr_result}
# #####
# 请提取出下面的信息，
#  "collateralLoanContract": 编号栏有“浙泰商银”四个字，则该字段的值为“是”，否则为"否"。
#  "mainContractNumber":编号信息中，从"浙泰商银"开始的内容。比如："浙泰商银(保借)字第 (011111111)号"，该字段取值不要包括"浙泰商银"前面的内容。
#  "contractStartDate":合同起始日期,借款期限中的起始日期，格式为XXXX年XX月XX日，不要有多余的字。
#  "contractEndDate":合同到期日期,借款期限中的到期日期，格式为XXXX年XX月XX日，不要有多余的字。
#  "businessCurrency":业务币种,借款金额中的币种信息（如，人民币、美元、欧元），不要包括金额信息。
#  "amountInWords":借款金额大写，不要包括币种信息。
#  "contractAmount"：借款金额的小写形式，不要包括币种信息。比如大写金额是"叁拾万元整"，对应的该字段的值就是"300000.00"。
#  "purposeOfFunds":资金用途,借款用途。
#  "monthlyInterestRate":只要固定月利率的数值，不用带百分号。
#  "annualInterestRate":只要年利率的数值，不用带百分号。
#  "LPRQuoteDate":报价日, 格式为XXXX年XX月XX日。
#  "LPRPeriod":LPR利率是一年期还是五年期？如：一年或者五年。
#  "LPRQuoteRate":LPR利率。
#  "adjustmentPoints"：借款年利率在LPR利率的基础上是如何变化的（格式如：减5.123400%、加6.123400%）。
#  "repaymentMethod": 贷款资金发放与支付方式。
#  "entrustedPayment": 是否受托支付。（请回答是或否，如：否）。如果文本中没有提及"贷款人受托支付"，则为否。
#  以json的方式返回，请直接给出对应的key、value，不需要给出注释格式的判断逻辑。
#  对于每一个问题，请只给出你的答案，不要给出你的说明、注释。
# """


# COLLECTION_PROMPT = """
# 请从下面的使用"#####"包围的文字中提取信息：
# 对于每一个问题，请只给出你的答案，不要给出你的说明、注释。
# #####
# {ocr_result}
# #####
# 请提取出下面的信息：
#  "version_no":版本号是多少。
#  "collateralLoanContract": 编号栏有“浙泰商银”四个字，则该字段的值为“是”，否则为"否"。
#  "mainContractNumber":返回完整的编号信息,冒号":"之后，号之前的信息。
#  "contractStartDate":合同起始日期,借款期限中的起始日期，格式为XXXX年XX月XX日，不要有多余的字。
#  "contractEndDate":合同到期日期,借款期限中的到期日期，格式为XXXX年XX月XX日，不要有多余的字。
#  "businessCurrency":业务币种,借款金额中的币种信息（如，人民币、美元、欧元），不要包括金额信息。
#  "amountInWords":借款金额大写，不要包括币种信息。
#  "contractAmount"：借款金额的小写形式，不要包括币种信息。比如大写金额是"叁拾万元整"，对应的该字段的值就是"300000.00"。
#  "purposeOfFunds":资金用途,借款用途。
#  "monthlyInterestRate":只要固定月利率的数值，不用带百分号。
#  "annualInterestRate":只要年利率的数值，不用带百分号。
#  "LPRQuoteDate":报价日, 格式为XXXX年XX月XX日。
#  "LPRPeriod":LPR利率是一年期还是五年期？如：一年或者五年。
#  "LPRQuoteRate":LPR利率。
#  "adjustmentPoints"：LPR加减点后面的数字是多少。
#  "repaymentMethod": 贷款资金发放与支付方式。
#  "entrustedPayment": 是否受托支付。（请回答是或否，如：否）。如果文本中没有提及"贷款人受托支付"，则为否。
#
#
#  以json的方式返回，请直接给出对应的key、value，不需要给出注释格式的判断逻辑。
#  对于每一个问题，请只给出你的答案，不要给出你的说明、注释。
# """


COLLECTION_PROMPT = """
请从下面的使用"#####"包围的文字中提取信息,对于每一个问题，请只给出你的答案，不要给出你的说明、注释，对于未识别到的字段，返回空""：

#####
{ocr_result}
#####

请提取出下面的信息：
{keys_describe}

 以json的方式返回，请直接给出对应的key、value，不需要给出注释格式的判断逻辑。
 对于每一个问题，请只给出你的答案，不要给出你的说明、注释。
"""



export_describe = """
 "GRNT_LOAN_CTR_IND": 编号栏有“保借”两个字，则该字段的值为“是”，否则为"否"。
 "MAIN_CTR_NO":返回完整的编号信息,冒号":"之后，号之前的信息。
 "CTR_BGN_DT":合同起始日期,借款期限中的起始日期，格式为XXXX年XX月XX日，不要有多余的字。
 "CTR_MTU_DT":合同到期日期,借款期限中的到期日期，格式为XXXX年XX月XX日，不要有多余的字。
 "BSN_CCY":借款金额的币种，如果是人民币，则显示为人民币。
 "BRWR_CTR_UPPER_AMT":借款金额大写，不要包括币种信息。
 "CTR_AMT"：借款金额的小写形式，不要包括币种信息。比如大写金额是"叁拾万元整"，对应的该字段的值就是"300000.00"。
 "CPT_USG_RMK":资金用途,借款用途。
 "EXEC_MON_IR":只要固定月利率的数值，不用带百分号。
 "EXEC_YEAR_IR":只要年利率的数值，不用带百分号。
 "LPR_QUO_DT":报价日, 格式为XXXX年XX月XX日。
 "LPR_TRM_TYP":LPR利率是一年期还是五年期？如：一年或者五年。
 "LPR_QUO_INTR_RAT":LPR利率,不要带上加减点数。
 "INCS_DECS_PNT_NUM"：LPR加减点后面的数字是多少。
 "RPAY_PRCP_SETL_INTR_MOD": 贷款资金发放与支付方式。
 "ETRS_PAY_IND": 是否受托支付。（请回答是或否，如：否）。如果文本中没有提及"贷款人受托支付"，则为否。"""