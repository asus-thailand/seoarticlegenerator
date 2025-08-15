# streamlit_final_seo_app.py

import streamlit as st
import google.generativeai as genai

# ==============================================================================
# --- ส่วนตั้งค่า API Key และหน้าเว็บ ---
# ==============================================================================
st.set_page_config(page_title="Final SEO Checklist Writer", page_icon="🏆", layout="wide")

# จัดการ API Key
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except (KeyError, FileNotFoundError):
    st.warning("⚠️ ไม่พบ API Key ใน Secrets")
    GEMINI_API_KEY = st.text_input("กรุณาใส่ Google AI API Key ของคุณ:", type="password")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================================
# --- หน้าตาของแอปพลิเคชัน ---
# ==============================================================================
st.title("🏆 Final SEO Checklist Writer")
st.markdown("เครื่องมือสร้างสรรค์เนื้อหาพร้อม SEO Checklist ฉบับสมบูรณ์แบบ All-in-One")

# --- ฟอร์มสำหรับรับข้อมูลจากผู้ใช้ ---
with st.form("final_form"):
    st.header("1. กำหนดข้อมูลพื้นฐาน")
    topic_input = st.text_input("หัวข้อบทความ (Topic)", placeholder="เช่น เปรียบเทียบเทคนิคการปลูกผม FUE VS FUT")
    keyphrase_input = st.text_input("คีย์เวิร์ดหลัก (Focus Keyphrase)", placeholder="เช่น ปลูกผม FUE")
    
    st.header("2. กำหนดคุณสมบัติ E-E-A-T")
    author_persona = st.text_input("สวมบทบาทเป็นใคร (Author Persona)", placeholder="เช่น ผู้เชี่ยวชาญด้านการแพทย์")
    target_audience = st.text_input("เขียนให้ใครอ่าน (Target Audience)", placeholder="เช่น คนที่หาข้อมูลเกี่ยวกับ ปลูกผม")

    st.header("3. กำหนดความยาว")
    word_count_input = st.number_input("ความยาวที่ต้องการ (คำ)", min_value=300, value=800, step=100)

    submitted = st.form_submit_button("🏆 สร้าง SEO Checklist ทั้งหมด!")

# ==============================================================================
# --- ส่วนประมวลผลและแสดงผลลัพธ์ ---
# ==============================================================================
if submitted:
    if not GEMINI_API_KEY or not topic_input or not keyphrase_input or not author_persona:
        st.warning("⚠️ กรุณากรอกข้อมูลในช่อง 'หัวข้อ', 'คีย์เวิร์ด' และ 'สวมบทบาทเป็นใคร' ให้ครบถ้วน")
    else:
        with st.spinner(f"AI ในบทบาท '{author_persona}' กำลังสร้างผลงาน Final..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # --- Final Mega Prompt ---
                final_mega_prompt = f"""
                คุณคือ SEO Content Strategist และนักเขียนบทความมืออาชีพระดับสูงสุด ภารกิจของคุณคือสร้าง SEO Elements ทั้งหมดสำหรับหน้าเว็บ 1 หน้า ให้สอดคล้องกับกฎ SEO และ E-E-A-T ทุกข้ออย่างสมบูรณ์แบบ

                **ข้อมูลหลัก:**
                - Topic: {topic_input}
                - Focus Keyphrase: "{keyphrase_input}"
                - Author Persona: "{author_persona}"
                - Target Audience: "{target_audience}"
                - Target Length: ประมาณ {word_count_input} คำ

                **กฎการสร้าง SEO Elements (ต้องทำทุกข้อ):**

                1.  **URL Slug:** สร้าง URL Slug ที่เป็นมิตรกับ SEO โดยใช้ "{keyphrase_input}" (ใช้ภาษาอังกฤษ ตัวพิมพ์เล็ก คั่นด้วยขีด)
                2.  **Image Filename:** สร้างชื่อไฟล์รูปภาพหลักสำหรับบทความนี้ ควรเกี่ยวข้องกับ "{topic_input}" และ "{keyphrase_input}" (ใช้ภาษาอังกฤษ ตัวพิมพ์เล็ก คั่นด้วยขีด) พร้อมนามสกุล .jpg
                3.  **Meta Title:** ต้องมี "{keyphrase_input}" อยู่ตอนต้น, ยาวไม่เกิน 60 ตัวอักษร
                4.  **Meta Keywords:** สร้างรายการ Meta Keywords ที่เกี่ยวข้องกับ "{topic_input}" ประมาณ 5-7 คำ คั่นด้วยจุลภาค (,)
                5.  **Meta Description:** ต้องมี "{keyphrase_input}", ยาว 120-155 ตัวอักษร
                6.  **Article Body & Other SEOs:** เขียนบทความตามหลัก E-E-A-T พร้อมทั้งแนะนำ Image Alt Text และตำแหน่งการวาง Links (Internal/Outbound)

                **รูปแบบผลลัพธ์ที่ต้องการ (Output Format):**
                [SLUG_START]
                (URL Slug)
                [SLUG_END]
                [IMAGE_FILENAME_START]
                (Image Filename)
                [IMAGE_FILENAME_END]
                [META_TITLE_START]
                (Meta Title)
                [META_TITLE_END]
                [META_KEYWORDS_START]
                (Meta Keywords)
                [META_KEYWORDS_END]
                [META_DESC_START]
                (Meta Description)
                [META_DESC_END]
                [ARTICLE_BODY_START]
                (เนื้อหาบทความทั้งหมด พร้อมคำแนะนำ Image Alt Text และ Links)
                [ARTICLE_BODY_END]
                """

                response = model.generate_content(final_mega_prompt)
                full_text = response.text
                
                # แยกส่วนผลลัพธ์
                slug = full_text.split('[SLUG_START]')[1].split('[SLUG_END]')[0].strip()
                image_filename = full_text.split('[IMAGE_FILENAME_START]')[1].split('[IMAGE_FILENAME_END]')[0].strip()
                title = full_text.split('[META_TITLE_START]')[1].split('[META_TITLE_END]')[0].strip()
                keywords = full_text.split('[META_KEYWORDS_START]')[1].split('[META_KEYWORDS_END]')[0].strip()
                description = full_text.split('[META_DESC_START]')[1].split('[META_DESC_END]')[0].strip()
                article = full_text.split('[ARTICLE_BODY_START]')[1].split('[ARTICLE_BODY_END]')[0].strip()

                st.success("🎉 สร้าง Final SEO Checklist สำเร็จ!")
                
                # แสดงผลลัพธ์
                st.subheader("✅ SEO Checklist (สำหรับนำไปใช้ใน CMS ของคุณ)")
                
                st.text_input("1. URL Slug", value=slug)
                st.text_input("2. ชื่อภาพ (Image Filename)", value=image_filename)
                st.text_input("3. Title", value=title)
                st.text_input("4. Meta Keywords", value=keywords)
                st.text_area("5. Meta Description", value=description, height=150)

                st.subheader("✍️ Article Body")
                st.markdown(article)
                st.info("💡 **หมายเหตุ:** อย่าลืมมองหาคำแนะนำสำหรับใส่ Links และ Alt Text ในบทความ")

            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")