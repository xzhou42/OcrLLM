import streamlit as st
import anthropic
import json
import requests
url = "http://localhost:7862/guarLnAnalyze"
serial_no = "123456"  # 替换为实际的 serial_no
tsk_id = "task_001"  # 替换为实际的 tsk_id


with st.sidebar:
    image_path="images/robot.png"
    st.image(image_path, caption='合同识别模型助手', use_column_width=True)
    "[View the source code](https://github.com/xzhou42/OcrLLM/tree/main/OcrLLM_Streamlit)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/xzhou42/OcrLLM/tree/main/contract-recog)"


st.title("📝 制式合同关键字段识别")
# 注入自定义 CSS 样式
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# col1, col2 = st.columns([1,1])
# with col1:
#     uploaded_file = st.file_uploader("上传合同图片", type=("png", "jpg"))
#     response = ''
#     if uploaded_file is not None:
#         # 展示图片
#         st.image(uploaded_file, caption='上传的图片', use_column_width=True)
#         files = {"file": uploaded_file}
#         data = {"serial_no": serial_no, "tsk_id": tsk_id}
#
#
#         # 发送 POST 请求
#         response = requests.post(url, files=files, data=data)
#         response.encoding='utf-8'
#
# with col2:
#     # print("response content:",response.text)
#     # st.title("识别结果:")
#     st.markdown("#### 识别结果：")
#     try:
#         st.json(response.text)
#     except:
#         st.write("识别结果为空")
#
#     question = st.text_input(
#         "待识别字段",
#         placeholder='',
#         disabled=not uploaded_file,
#     )
#
#     if uploaded_file and question and not anthropic_api_key:
#         st.info("Please add your Anthropic API key to continue.")
#
#     if uploaded_file and question and anthropic_api_key:
#         article = uploaded_file.read().decode()
#         prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
#         {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""
#
#         client = anthropic.Client(api_key=anthropic_api_key)
#         response = client.completions.create(
#             prompt=prompt,
#             stop_sequences=[anthropic.HUMAN_PROMPT],
#             model="claude-v1",  # "claude-2" for Claude 2 model
#             max_tokens_to_sample=100,
#         )
#         st.write("### Answer")
#         st.write(response.completion)
#
import streamlit as st
import requests

# 假设已导入其他必要的库
# ...

# 创建两列
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("上传合同图片", type=("png", "jpg"))
    response = ''
    if uploaded_file is not None:
        # 展示图片并尝试使其居中
        st.image(uploaded_file, caption='上传的图片', use_column_width=True)

    keys_describe = """"GRNT_LOAN_CTR_IND": 编号栏有“保借”两个字，则该字段的值为“是”，否则为"否"。
    "MAIN_CTR_NO":返回完整的编号信息,冒号":"之后，号之前的信息。
    "LN_NM":贷款人姓名是什么。
    "LN_ID":贷款人身份证号。
    "LD_NM":借款人（全称）是什么。
    "CTR_BGN_DT":合同起始日期,借款期限中的起始日期，格式为XXXX年XX月XX日，不要有多余的字。
    "CTR_MTU_DT":合同到期日期,借款期限中的到期日期，格式为XXXX年XX月XX日，不要有多余的字。
    "BSN_CCY":借款金额的币种，如果是人民币，则显示为人民币。
    "BRWR_CTR_UPPER_AMT":借款金额中文，不要包括币种信息。
    "CTR_AMT"：借款金额的小写形式，不要包括币种信息。比如大写金额是"叁拾万元整"，对应的该字段的值就是"300000.00"。
    "CPT_USG_RMK":资金用途,借款用途。
    "LPR_QUO_DT":报价日, 格式为XXXX年XX月XX日。
    "LPR_TRM_TYP":LPR利率是一年期还是五年期？如：一年或者五年。
    "RPAY_PRCP_SETL_INTR_MOD":贷款资金发放与支付方式。
    "ETRS_PAY_IND":是否受托支付。（请回答是或否，如：否）。如果文本中没有提及"贷款人受托支付"，则为否。"""

    txt = st.text_area(label = "字段说明",placeholder = keys_describe, height=300)

    # 添加 CSS 样式
    st.markdown(
        """
        <style>
            div[data-testid="stTextInput"] input {
                height: 50px;  /* 设置输入框的高度 */
                padding: 10px; /* 增加内边距 */
            }
        </style>
        """,
        unsafe_allow_html=True
    )


with col2:
    # 居中显示标题和 JSON 数据




    try:
        files = {"file": uploaded_file}
        data = {"serial_no": serial_no, "tsk_id": tsk_id, "keys_describe": keys_describe}
        with st.spinner("加载中"):
            response = requests.post(url, files=files, data=data)
        response.encoding='utf-8'
        st.write("")

        st.markdown(
            """
            <style>
            .bordered-container {
                border: 2px solid #000000;  /* 黑色边框 */
                padding: 10px;              /* 内边距 */
                border-radius: 5px;         /* 边框圆角 */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);  /* 阴影效果 */
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        if response.text:
            st.markdown(
                """
                <div class="bordered-container">
                    <h4>识别结果</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.json(response.text)

    except:
        st.text("识别为空")

