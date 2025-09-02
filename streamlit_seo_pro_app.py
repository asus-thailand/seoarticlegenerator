# streamlit_final_boss_app.py

import streamlit as st
import google.generativeai as genai

# ==============================================================================
# --- ส่วนตั้งค่า API Key และหน้าเว็บ ---
# ==============================================================================
st.set_page_config(page_title="Final Boss SEO Writer", page_icon="👑", layout="wide")

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
st.title("👑 Final Boss: SEO Publishing Kit Generator")
st.markdown("เครื่องมือสร้าง 'ชุดข้อมูลสำหรับเผยแพร่' ที่สมบูรณ์แบบสำหรับ Yoast SEO")

with st.form("final_boss_form"):
    st.header("Phase 1: Strategic Input (ข้อมูลเชิงกลยุทธ์จากคุณ)")
    
    col1, col2 = st.columns(2)
    with col1:
        topic_input = st.text_input("หัวข้อบทความ (Topic)", placeholder="เปรียบเทียบคาร์ซีท All-in-One")
        keyphrase_input = st.text_input("คีย์เวิร์ดหลักตรงตัว (Exact Focus Keyphrase)", placeholder="คาร์ซีทเด็กแรกเกิด")
        word_count_input = st.number_input("ความยาวที่ต้องการ (คำ)", min_value=300, value=1000, step=100)

    with col2:
        author_persona = st.text_input("สวมบทบาทเป็นใคร (Author Persona)", placeholder="ผู้เชี่ยวชาญด้านผลิตภัณฑ์สำหรับเด็ก")
        target_audience = st.text_input("เขียนให้ใครอ่าน (Target Audience)", placeholder="คุณพ่อคุณแม่มือใหม่")
        internal_link_ideas = st.text_area("ไอเดียสำหรับลิงก์ภายใน (Internal Links)", placeholder="เช่น: บทความเรื่อง 'วิธีเลือกคาร์ซีทให้ปลอดภัย', 'รีวิวคาร์ซีท 5 รุ่นยอดนิยม'")

    submitted = st.form_submit_button("👑 สร้าง Publishing Kit!")

# ==============================================================================
# --- ส่วนประมวลผล ---
# ==============================================================================
if submitted:
    if not all([GEMINI_API_KEY, topic_input, keyphrase_input, author_persona]):
        st.warning("⚠️ กรุณากรอกข้อมูลในช่อง 'หัวข้อ', 'คีย์เวิร์ด' และ 'สวมบทบาทเป็นใคร' ให้ครบถ้วน")
    else:
        with st.spinner(f"AI Co-Editor กำลังร่าง Publishing Kit..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                final_boss_prompt = f"""
                Act as a world-class SEO Content Strategist and Editor. Your task is to generate a complete "Publishing Kit" for a single web page based on the provided strategic inputs. You must strictly adhere to all Yoast SEO Premium rules and E-E-A-T principles.

                **STRATEGIC INPUTS:**
                - **Topic:** {topic_input}
                - **Exact Focus Keyphrase:** "{keyphrase_input}"
                - **Author Persona:** "{author_persona}"
                - **Target Audience:** "{target_audience}"
                - **Target Word Count:** Approximately {word_count_input} words.
                - **Internal Link Context:** The website has existing articles about: "{internal_link_ideas}".

                **TASK: Generate the following elements in the specified XML-like format.**

                <publishing_kit>

                <metadata>
                    <seo_title>Generate an SEO Title. It MUST start with the exact keyphrase "{keyphrase_input}". Total length must be 55-60 characters.</seo_title>
                    <meta_description>Generate a Meta Description. It MUST contain the exact keyphrase "{keyphrase_input}". Total length MUST be between 140 and 156 characters.</meta_description>
                    <url_slug>Generate a URL-friendly slug containing the keyphrase "{keyphrase_input}". Use lowercase English words separated by hyphens.</url_slug>
                </metadata>

                <content_body>
                    <article>
                    Write a comprehensive article based on the strategic inputs.
                    **Strict Rules:**
                    1.  **Length:** Must be at least {max(300, word_count_input)} words.
                    2.  **E-E-A-T:** Write from the perspective of the "{author_persona}" for the "{target_audience}", demonstrating clear Experience, Expertise, Authoritativeness, and Trust.
                    3.  **Keyphrase in Introduction:** The exact keyphrase "{keyphrase_input}" MUST appear naturally within the first paragraph.
                    4.  **Keyphrase Density/Distribution:** The exact keyphrase "{keyphrase_input}" MUST appear 3-6 times, distributed evenly across the introduction, body, and conclusion.
                    5.  **Keyphrase in Subheadings:** The exact keyphrase "{keyphrase_input}" or a very close synonym MUST appear in at least two H2 or H3 subheadings.
                    6.  **Internal Links:** Naturally integrate 1-2 internal links to the topics mentioned in the Internal Link Context. Use the format `[[anchor text|INTERNAL SUGGESTION: Link to the article about...]]`.
                    7.  **Outbound Links:** Naturally integrate 1-2 outbound links to high-authority, non-commercial sources (like Wikipedia, research institutions, or government sites). Use the format `[[anchor text|OUTBOUND SUGGESTION: Link to a reputable source about...]]`.
                    </article>
                </content_body>

                <asset_checklist>
                    <image_suggestions>
                        <image>
                            <description>Suggest a relevant, high-quality image for the article.</description>
                            <alt_text>Write a descriptive alt text for this image that includes the exact keyphrase "{keyphrase_input}".</alt_text>
                        </image>
                        <image>
                            <description>Suggest a second, different type of image (e.g., an infographic, a comparison table).</description>
                            <alt_text>Write a descriptive alt text for this second image that includes a synonym or variation of the keyphrase "{keyphrase_input}".</alt_text>
                        </image>
                    </image_suggestions>
                </asset_checklist>

                </publishing_kit>
                """

                response = model.generate_content(final_boss_prompt)
                full_text = response.text
                
                # ใช้ Regular Expression เพื่อดึงข้อมูลจากแท็ก XML
                def extract_tag(tag, text):
                    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
                    return match.group(1).strip() if match else f"[{tag} not found]"

                title = extract_tag('seo_title', full_text)
                description = extract_tag('meta_description', full_text)
                slug = extract_tag('url_slug', full_text)
                article = extract_tag('article', full_text)
                images = extract_tag('image_suggestions', full_text)


                st.success("🎉 Publishing Kit พร้อมใช้งานแล้ว!")
                
                # แสดงผลลัพธ์
                st.subheader("Phase 2: AI Generated Publishing Kit")
                st.markdown("นำข้อมูลชุดนี้ไปใช้ใน WordPress หรือ CMS ของคุณ")
                
                with st.container(border=True):
                    st.markdown("#### **Metadata**")
                    st.text_input("SEO Title", value=title)
                    st.text_area("Meta Description", value=description, height=100)
                    st.text_input("URL Slug", value=slug)

                with st.container(border=True):
                    st.markdown("#### **Content Body**")
                    st.markdown(article)
                    st.info("💡 **คำแนะนำ:** มองหาข้อความในวงเล็บ `[[...]]` เพื่อใส่ลิงก์ Internal/Outbound")

                with st.container(border=True):
                    st.markdown("#### **Asset Checklist (สำหรับรูปภาพ)**")
                    st.text_area("Image & Alt Text Suggestions", value=images, height=200)

            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
                st.text(full_text) # แสดงผลลัพธ์ดิบเพื่อดีบัก