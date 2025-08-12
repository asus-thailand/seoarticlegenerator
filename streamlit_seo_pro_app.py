import streamlit as st
import google.generativeai as genai
import time

# ==============================================================================
# --- ส่วนตั้งค่า API Key และหน้าเว็บ ---
# ==============================================================================

st.set_page_config(page_title="SEO Pro Article Writer", page_icon="✍️", layout="wide")

# จัดการ API Key อย่างปลอดภัย
# เมื่อ Deploy จริง เราจะใช้ st.secrets
# แต่เพื่อให้ทดลองบนเครื่องได้ง่าย จะให้กรอกผ่านหน้าเว็บได้ด้วย
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except (KeyError, FileNotFoundError):
    st.warning("⚠️ ไม่พบ API Key ในระบบ Secrets ของ Streamlit")
    GEMINI_API_KEY = st.text_input("กรุณาใส่ Google AI API Key ของคุณที่นี่เพื่อทดลองใช้งาน:", type="password", help="คุณสามารถสร้าง API Key ได้ฟรีที่ Google AI Studio")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================================
# --- หน้าตาของแอปพลิเคชัน ---
# ==============================================================================

st.title("✍️ SEO Pro Article Writer")
st.markdown("เครื่องมือสร้างบทความคุณภาพสูง ที่ปรับให้เหมาะกับ SEO ตามหลักเกณฑ์ที่คุณต้องการ")

# --- ฟอร์มสำหรับรับข้อมูลจากผู้ใช้ ---
with st.form("pro_article_form"):
    st.subheader("กรอกข้อมูลเพื่อสร้างบทความ")
    
    topic_input = st.text_input(
        "1. หัวข้อบทความ (Topic)",
        placeholder="เช่น ประโยชน์ของวิตามินซีต่อผิว, วิธีการทำงานของโบท็อกซ์"
    )
    
    keyphrase_input = st.text_input(
        "2. คีย์เวิร์ดหลักที่ต้องการโฟกัส (Focus Keyphrase)",
        placeholder="เช่น วิตามินซี, โบท็อกซ์ คืออะไร"
    )

    word_count_input = st.number_input(
        "3. ความยาวที่ต้องการ (คำ)",
        min_value=300,
        max_value=2500,
        value=500,
        step=100,
        help="ปลั๊กอิน SEO ส่วนใหญ่แนะนำความยาวขั้นต่ำ 300 คำ"
    )

    # ปุ่มสำหรับส่งฟอร์ม
    submitted = st.form_submit_button("🚀 สร้างบทความ SEO Pro!")

# ==============================================================================
# --- ส่วนประมวลผลและแสดงผลลัพธ์ ---
# ==============================================================================

if submitted:
    # ตรวจสอบความพร้อมของข้อมูล
    if not GEMINI_API_KEY:
        st.error("❌ กรุณาใส่ API Key ของคุณก่อนเริ่มใช้งาน")
    elif not topic_input or not keyphrase_input:
        st.warning("⚠️ กรุณากรอกทั้ง 'หัวข้อบทความ' และ 'คีย์เวิร์ดหลัก'")
    else:
        with st.spinner(f"AI กำลังเขียนบทความ SEO ระดับโปรในหัวข้อ '{topic_input}'... กรุณารอสักครู่..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # --- Mega Prompt เวอร์ชัน SEO Pro ---
                mega_prompt = f"""
                คุณคือ SEO Content Strategist และนักเขียนบทความมืออาชีพ ภารกิจของคุณคือการเขียนบทความ 1 บทความ, Meta Title 1 รายการ, และ Meta Description 1 รายการ โดยต้องปฏิบัติตามกฎ SEO ต่อไปนี้อย่างเคร่งครัด:

                **ข้อมูลหลัก:**
                - **หัวข้อหลักของบทความ (Topic):** {topic_input}
                - **คีย์เวิร์ดหลักที่ต้องโฟกัส (Focus Keyphrase):** "{keyphrase_input}"
                - **ความยาวบทความที่ต้องการ (Target Length):** ประมาณ {word_count_input} คำ (ห้ามต่ำกว่า 300 คำ)

                **กฎการเขียน SEO ที่ต้องปฏิบัติตาม:**
                1. **กฎสำหรับ Meta Title:** ต้องมี "{keyphrase_input}" อยู่, ยาวไม่เกิน 60 ตัวอักษร, และดึงดูดให้คลิก
                2. **กฎสำหรับ Meta Description:** ต้องมี "{keyphrase_input}" อยู่, ยาว 120-155 ตัวอักษร, และกระตุ้นให้อยากอ่าน
                3. **กฎสำหรับเนื้อหาบทความ (Article Body):**
                   - **Text Length:** เนื้อหาต้องยาวอย่างน้อย {max(300, word_count_input)} คำ
                   - **Keyphrase in Introduction:** ต้องใส่ "{keyphrase_input}" ในย่อหน้าแรก
                   - **Keyphrase Density & Distribution:** ต้องกระจาย "{keyphrase_input}" ให้ทั่วถึงทั้งบทความอย่างเป็นธรรมชาติ (ประมาณ 2-5 ครั้ง)
                   - **Keyphrase in Subheadings:** ต้องมี "{keyphrase_input}" หรือคำใกล้เคียงในหัวข้อย่อย (H2/H3) อย่างน้อย 1-2 ครั้ง
                   - **Readability & Structure:** ต้องอ่านง่าย, ใช้ย่อหน้าสั้นๆ, และมีโครงสร้างชัดเจน (บทนำ, H2/H3, สรุป)

                **รูปแบบผลลัพธ์ที่ต้องการ:**
                จงสร้างผลลัพธ์ในรูปแบบเฉพาะด้านล่างนี้เท่านั้น โดยใช้ตัวคั่นที่ไม่ซ้ำกัน:
                [META_TITLE_START]
                (Meta Title ที่คุณสร้าง)
                [META_TITLE_END]
                [META_DESC_START]
                (Meta Description ที่คุณสร้าง)
                [META_DESC_END]
                [ARTICLE_BODY_START]
                (เนื้อหาบทความทั้งหมดที่คุณสร้างตามกฎ)
                [ARTICLE_BODY_END]
                """

                # เรียกใช้งาน AI
                response = model.generate_content(mega_prompt)
                full_text = response.text
                
                # แยกส่วนผลลัพธ์
                title = full_text.split('[META_TITLE_START]')[1].split('[META_TITLE_END]')[0].strip()
                description = full_text.split('[META_DESC_START]')[1].split('[META_DESC_END]')[0].strip()
                article = full_text.split('[ARTICLE_BODY_START]')[1].split('[ARTICLE_BODY_END]')[0].strip()

                st.success("🎉 สร้างบทความ SEO Pro สำเร็จ!")
                
                # แสดงผลลัพธ์
                st.subheader("📄 Meta Title")
                st.code(title, language='text')

                st.subheader("📝 Meta Description")
                st.code(description, language='text')

                st.subheader("✍️ Article Body")
                st.markdown(article)

            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")

# --- ส่วนท้ายเว็บ ---
st.markdown("---")
st.write("สร้างโดย คู่หูเขียนโค้ดของคุณ | ขับเคลื่อนโดย Google Gemini & Streamlit")