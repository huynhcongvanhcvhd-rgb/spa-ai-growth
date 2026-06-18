import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import json
from datetime import datetime
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="SPA AI GROWTH",
    page_icon="💆‍♀️",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #fafafa;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.hero-box {
    background: linear-gradient(135deg,#fff5f2,#ffffff);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 20px;
    border: 1px solid #ffe3db;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #2d2d2d;
}

.hero-subtitle {
    font-size: 18px;
    color: #666;
    margin-top: 10px;
}

.stButton > button {
    background: linear-gradient(135deg,#ff6b6b,#ff8e72);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
col1, col2 = st.columns([1,4])

with col1:
    st.image("vuongtrang.png", width=120)

with col2:
    st.markdown("""
    <h1 style='margin-bottom:0px;color:#d63384;'>
    VƯƠNG TRANG SPA AI
    </h1>
    <p style='font-size:18px;color:#666;'>
    Trang tạo ra công cụ này giúp chủ Spa biết hôm nay đăng gì, viết gì và quay gì để tăng cơ hội có khách.
    </p>
    """, unsafe_allow_html=True)

st.divider()
""", unsafe_allow_html=True)

if not api_key:
    st.error("Chưa tìm thấy OPENAI_API_KEY trong file .env.")
    st.stop()

client = OpenAI(api_key=api_key)
def show_result(result, file_name):
    st.markdown(result)

    st.download_button(
        label="📥 Tải nội dung về máy",
        data=result,
        file_name=file_name,
        mime="text/plain"
    )
def save_history(title, content):
    try:
        history = []

        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                history = json.load(f)

        history.insert(
            0,
            {
                "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "title": title,
                "content": content
            }
        )

        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    except:
        pass  
def load_spa_profile():
    if os.path.exists("spa_profile.json"):
        with open("spa_profile.json", "r", encoding="utf-8") as f:
            return json.load(f)

    return {
        "ten_spa": "",
        "hotline": "",
        "dia_chi": "",
        "dich_vu": ""
    }  
def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Lỗi AI: {e}"

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
spa_profile = load_spa_profile()
tab1, tab2, tab3, tab4, tab5 = st.tabs(
[
    "📅 Hôm Nay Đăng Gì",
    "📸 Viết Content Từ Ảnh",
    "🎬 Quay Video Gì Hôm Nay",
    "📚 Lịch Sử",
    "🏢 Hồ Sơ Spa"
]
)

with tab1:
    st.header("📅 Hôm Nay Đăng Gì?")

    dich_vu = st.text_input(
        "Dịch vụ muốn quảng bá",
        placeholder="Ví dụ: Trị mụn, Triệt lông, Giảm mỡ, Chăm sóc da..."
    )

    uu_dai = st.text_input(
        "Ưu đãi nếu có",
        placeholder="Ví dụ: Giảm 30%, soi da miễn phí, combo 399k..."
    )
    phong_cach = st.selectbox(
    "Chọn phong cách nội dung",
    [
        "Chạm cảm xúc",
        "Chuyên gia",
        "Bán hàng mạnh",
        "Kể chuyện khách hàng",
        "Khuyến mãi",
        "Xây thương hiệu cá nhân"
    ]
    )
    if st.button("Tạo nội dung hôm nay", type="primary"):

        if not dich_vu:
            st.warning("Bạn hãy nhập dịch vụ trước.")
        else:
            prompt = f"""
Bạn là "Bộ Não Marketing Spa" chuyên sâu, có kinh nghiệm xây chiến dịch nội dung cho spa, thẩm mỹ viện, beauty clinic và academy spa.

Mục tiêu không phải chỉ viết content.
Mục tiêu là giúp chủ spa biết hôm nay nên đăng gì để tăng cơ hội có khách inbox, đặt lịch, hỏi giá hoặc để lại bình luận.
THÔNG TIN SPA:
- Tên Spa: {spa_profile.get("ten_spa", "")}
- Hotline: {spa_profile.get("hotline", "")}
- Địa chỉ: {spa_profile.get("dia_chi", "")}
- Dịch vụ chính: {spa_profile.get("dich_vu", "")}
THÔNG TIN ĐẦU VÀO:
- Dịch vụ cần quảng bá: {dich_vu}
- Ưu đãi hiện có: {uu_dai}
- Phong cách nội dung cần viết: {phong_cach}

TƯ DUY MARKETING BẮT BUỘC:
Hãy viết dựa trên công thức:
NỖI ĐAU → HẬU QUẢ → ĐỒNG CẢM → GIẢI PHÁP → LÝ DO TIN → CTA

Khi viết, phải tự phân tích:
1. Khách hàng đang đau điều gì?
2. Họ sợ điều gì?
3. Họ đã từng thử sai điều gì?
4. Họ cần nghe câu nào để cảm thấy được thấu hiểu?
5. Điều gì khiến họ muốn inbox ngay?

QUY TẮC VIẾT:
- Viết như người làm spa thật, không viết như AI.
- Có cảm xúc, có sự đồng cảm, có tính thuyết phục.
- Không dùng văn quá sáo rỗng kiểu: "Hãy đến với chúng tôi để trải nghiệm dịch vụ tốt nhất".
- Không cam kết quá đà như khỏi 100%, hết mụn vĩnh viễn, giảm cân thần tốc.
- Không dùng từ ngữ vi phạm quảng cáo y tế.
- Phù hợp để đăng Facebook cá nhân, fanpage spa, Zalo hoặc TikTok caption.
- Ngôn ngữ gần gũi, dễ hiểu, có khả năng kéo khách inbox.

YÊU CẦU THEO PHONG CÁCH:
Nếu phong cách là "Chạm cảm xúc":
- Tập trung vào nỗi tự ti, sự mệt mỏi, áp lực ngoại hình và mong muốn thay đổi.

Nếu phong cách là "Chuyên gia":
- Tập trung vào phân tích nguyên nhân, sai lầm thường gặp, góc nhìn chuyên môn dễ hiểu.

Nếu phong cách là "Bán hàng mạnh":
- Tập trung vào lợi ích, ưu đãi, sự khan hiếm, lý do nên đặt lịch hôm nay.

Nếu phong cách là "Kể chuyện khách hàng":
- Viết theo dạng một câu chuyện trước - sau của khách hàng, nhưng không bịa kết quả quá đà.

Nếu phong cách là "Khuyến mãi":
- Nhấn mạnh chương trình ưu đãi nhưng vẫn có lý do thuyết phục, không chỉ giảm giá.

Nếu phong cách là "Xây thương hiệu cá nhân":
- Viết như chủ spa đang chia sẻ thật lòng từ kinh nghiệm làm nghề.

HÃY TRẢ KẾT QUẢ THEO ĐÚNG CẤU TRÚC SAU:

# 1. HÔM NAY NÊN ĐĂNG GÌ?
Gợi ý 1 hướng nội dung nên đăng hôm nay.
Nói rõ vì sao hướng này có khả năng kéo khách.

# 2. 5 TIÊU ĐỀ VIRAL
Viết 5 tiêu đề khác nhau.
Mỗi tiêu đề phải đánh vào một góc:
- Nỗi đau
- Sai lầm
- Tò mò
- Kết quả mong muốn
- Lời cảnh tỉnh nhẹ

# 3. BÀI FACEBOOK HOÀN CHỈNH
Viết 1 bài Facebook từ 300-450 từ.
Cấu trúc bài:
- Hook mở đầu mạnh
- Chạm đúng nỗi đau khách hàng
- Phân tích vấn đề
- Đưa ra giải pháp
- Lý do nên tin
- CTA cuối bài

# 4. PHIÊN BẢN NGẮN ĐĂNG ZALO
Viết 1 bài ngắn 80-120 từ.

# 5. 5 CTA CHỐT KHÁCH
Viết 5 CTA khác nhau:
- CTA comment
- CTA inbox
- CTA đặt lịch
- CTA nhận tư vấn
- CTA nhận ưu đãi

# 6. 10 HASHTAG
Viết 10 hashtag phù hợp ngành spa.

# 7. 5 Ý TƯỞNG VIDEO NGẮN
Mỗi ý tưởng gồm:
- Tên video
- Hook 3 giây đầu
- Nội dung nên quay
- Lời thoại gợi ý
- CTA cuối video

# 8. GỢI Ý HÌNH ẢNH ĐI KÈM
Gợi ý 3 kiểu ảnh nên đăng cùng nội dung này.

Viết hoàn toàn bằng tiếng Việt.
"""
            with st.spinner("AI đang tạo nội dung..."):
                result = ask_ai(prompt)
                show_result(result, "hom_nay_dang_gi.txt")
                save_history("Hôm nay đăng gì", result)
with tab2:
    st.header("📸 Viết Content Từ Ảnh")

    phong_cach_anh = st.selectbox(
        "Chọn phong cách chiến dịch",
        [
            "Chạm cảm xúc",
            "Bán hàng",
            "Chuyên gia",
            "Feedback khách hàng",
            "Xây thương hiệu cá nhân",
            "Tuyển học viên spa"
        ]
    )

    uploaded_file = st.file_uploader(
        "Tải ảnh spa, ảnh feedback, ảnh dịch vụ hoặc ảnh poster lên",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Ảnh đã tải lên", use_container_width=True)

        if st.button("Phân tích ảnh và tạo chiến dịch", type="primary"):
            image_base64 = encode_image(uploaded_file)

            text = f"""
Bạn là Bộ Não Marketing Spa V2.
THÔNG TIN SPA:
- Tên Spa: {spa_profile.get("ten_spa", "")}
- Hotline: {spa_profile.get("hotline", "")}
- Địa chỉ: {spa_profile.get("dia_chi", "")}
- Dịch vụ chính: {spa_profile.get("dich_vu", "")}
Phong cách chiến dịch:
{phong_cach_anh}

Nhiệm vụ:
Phân tích ảnh người dùng tải lên và biến ảnh đó thành một chiến dịch marketing hoàn chỉnh cho chủ spa.

Mục tiêu cuối cùng:
Giúp chủ spa có nội dung đăng bài để tăng cơ hội kéo khách inbox, comment, hỏi giá hoặc đặt lịch.

TƯ DUY MARKETING BẮT BUỘC:
Hãy phân tích theo công thức:
NỖI ĐAU → HẬU QUẢ → ĐỒNG CẢM → GIẢI PHÁP → LÝ DO TIN → CTA

QUY TẮC VIẾT:
- Viết như người làm marketing spa thật.
- Không viết chung chung.
- Không dùng văn AI máy móc.
- Không cam kết quá đà như khỏi 100%, hết mụn vĩnh viễn, giảm cân thần tốc.
- Nội dung phải thực tế, dễ dùng, phù hợp để đăng Facebook, Zalo, TikTok/Reels.

Hãy trả kết quả theo đúng cấu trúc:

# 1. AI NHÌN THẤY GÌ TRONG ẢNH
Mô tả ngắn gọn nội dung ảnh.

# 2. ĐIỂM MẠNH MARKETING CỦA ẢNH
Phân tích vì sao ảnh này có thể dùng để kéo khách.

# 3. ĐIỂM YẾU CỦA ẢNH
Góp ý thật ngắn: ảnh còn thiếu gì để bán hàng tốt hơn.

# 4. NÊN ĐĂNG THEO HƯỚNG NÀO
Gợi ý 3 hướng đăng khác nhau.

# 5. BÀI FACEBOOK
Viết 1 bài Facebook hoàn chỉnh 250-350 từ.

# 6. BÀI ZALO NGẮN
Viết 1 bài ngắn 80-120 từ.

# 7. CAPTION TIKTOK/REELS
Viết caption ngắn, dễ kéo tương tác.

# 8. KỊCH BẢN LỒNG THOẠI VIDEO 30 GIÂY
Viết lời thoại để người dùng lồng vào video.

# 9. 5 CTA
Viết 5 CTA khác nhau.

# 10. 10 HASHTAG
Viết 10 hashtag phù hợp.

# 11. PROMPT TẠO ẢNH MỞ RỘNG
Viết 1 prompt tạo ảnh AI liên quan đến nội dung ảnh.

# 12. PROMPT VEO VIDEO
Viết 1 prompt tạo video 9:16 bằng Veo, phù hợp nội dung ảnh.

Viết hoàn toàn bằng tiếng Việt.
"""

            with st.spinner("AI đang phân tích ảnh và tạo chiến dịch..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": text
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image_base64}"
                                        }
                                    }
                                ]
                            }
                        ]
                    )

                    result = response.choices[0].message.content
                    show_result(result, "chien_dich_tu_anh.txt")
                    save_history("Chiến dịch từ ảnh", result)
                except Exception as e:
                    st.error("Có lỗi khi phân tích ảnh.")
                    st.code(str(e))

with tab3:
    st.header("🎬 Quay Video Gì Hôm Nay?")

    chu_de = st.text_input(
        "Nhập chủ đề video",
        placeholder="Ví dụ: Trị mụn, Giảm mỡ bụng, Triệt lông, Đào tạo học viên spa..."
    )

    kieu_video = st.selectbox(
        "Chọn kiểu video muốn quay",
        [
            "Video kéo khách inbox",
            "Video chuyên gia giải thích",
            "Video chạm nỗi đau",
            "Video feedback khách hàng",
            "Video quy trình dịch vụ",
            "Video chủ spa xây thương hiệu cá nhân",
            "Video khuyến mãi"
        ]
    )

    thoi_luong = st.selectbox(
        "Chọn thời lượng video",
        [
            "30 giây",
            "45 giây",
            "60 giây"
        ]
    )

    if st.button("Tạo kịch bản quay video", type="primary"):

        if not chu_de:
            st.warning("Bạn hãy nhập chủ đề video trước.")
        else:
            prompt = f"""
Bạn là AI Đạo Diễn Video Spa, chuyên lên kịch bản video ngắn cho chủ spa quay bằng điện thoại.
THÔNG TIN SPA:
- Tên Spa: {spa_profile.get("ten_spa", "")}
- Hotline: {spa_profile.get("hotline", "")}
- Địa chỉ: {spa_profile.get("dia_chi", "")}
- Dịch vụ chính: {spa_profile.get("dich_vu", "")}
MỤC TIÊU:
Giúp chủ spa biết hôm nay phải quay gì, quay ở đâu, quay góc nào, nói gì, để tăng cơ hội có khách inbox, comment, hỏi giá hoặc đặt lịch.

THÔNG TIN ĐẦU VÀO:
- Chủ đề video: {chu_de}
- Kiểu video: {kieu_video}
- Thời lượng mong muốn: {thoi_luong}

TƯ DUY MARKETING BẮT BUỘC:
Kịch bản phải đi theo công thức:
HOOK 3 GIÂY → NỖI ĐAU → GIẢI THÍCH → GIẢI PHÁP → LÝ DO TIN → CTA

QUY TẮC:
- Viết thực tế cho chủ spa bận rộn.
- Quay được bằng điện thoại.
- Không cần ekip chuyên nghiệp.
- Không yêu cầu thiết bị phức tạp.
- Không nói quá công dụng như khỏi 100%, hết mụn vĩnh viễn, giảm mỡ thần tốc.
- Ưu tiên cảnh quay thật trong spa: phòng soi da, giường spa, máy móc, tay chuyên viên, khách hàng, bảng giá, sản phẩm, feedback, chủ spa nói chuyện.
- Nếu không có khách thật, hãy đưa phương án thay thế bằng ảnh feedback, tay chuyên viên, sản phẩm hoặc chủ spa tự nói.

HÃY TRẢ KẾT QUẢ THEO CẤU TRÚC SAU:

# 1. Ý TƯỞNG VIDEO CHÍNH
Nói rõ video này nên đánh vào nỗi đau nào và vì sao dễ kéo khách.

# 2. HOOK 3 GIÂY ĐẦU
Viết 5 câu hook khác nhau để người dùng chọn.

# 3. KỊCH BẢN QUAY TỪNG CẢNH
Chia video thành 5-7 cảnh.

Mỗi cảnh bắt buộc có:
- Thời lượng
- Bối cảnh
- Góc quay
- Hành động cần quay
- Lời thoại hoặc chữ hiện trên màn hình
- Ghi chú dựng video

# 4. LỜI THOẠI HOÀN CHỈNH
Viết nguyên một đoạn lời thoại liền mạch để người dùng có thể đọc/lồng tiếng.

# 5. TEXT CHÈN TRÊN VIDEO
Viết từng dòng text ngắn để chèn vào video.

# 6. CAPTION ĐĂNG VIDEO
Viết caption phù hợp đăng Facebook Reels/TikTok.

# 7. CTA CUỐI VIDEO
Viết 5 CTA khác nhau.

# 8. SHOT LIST CẦN QUAY
Liệt kê ngắn gọn tất cả cảnh cần quay để chủ spa mở ra là quay theo.

# 9. PHIÊN BẢN KHÔNG MUỐN LỘ MẶT
Đưa kịch bản thay thế nếu chủ spa không muốn xuất hiện trước camera.

# 10. PROMPT VEO TẠO VIDEO AI
Viết 1 prompt tiếng Anh để tạo video 9:16 bằng Veo, nội dung phù hợp chủ đề này.

Viết hoàn toàn bằng tiếng Việt, riêng prompt Veo viết bằng tiếng Anh.
"""

            with st.spinner("AI đang tạo kịch bản quay video..."):
                result = ask_ai(prompt)
                show_result(result, "kich_ban_quay_video.txt")
                save_history("Kịch bản video", result)
with tab4:

    st.header("📚 Lịch sử nội dung")

    if os.path.exists("history.json"):

        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)

        for item in history:

            with st.expander(
                f"{item['time']} - {item['title']}"
            ):
                st.markdown(item["content"])

    else:
        st.info("Chưa có nội dung nào được lưu.")
with tab5:

    st.header("🏢 Hồ Sơ Spa")

    ten_spa = st.text_input(
        "Tên Spa",
        value="Lucy Spa Beauty & Academy"
    )

    hotline = st.text_input(
        "Hotline",
        value="0766132239"
    )

    dia_chi = st.text_area(
        "Địa chỉ",
        value="35 An Thượng 27 - Đà Nẵng"
    )

    dich_vu = st.text_area(
        "Dịch vụ chính",
        value="""
Trị mụn
Triệt lông
Giảm béo
Đào tạo spa
"""
    )

    if st.button("💾 Lưu Hồ Sơ"):

        profile = {
            "ten_spa": ten_spa,
            "hotline": hotline,
            "dia_chi": dia_chi,
            "dich_vu": dich_vu
        }

        with open(
            "spa_profile.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                profile,
                f,
                ensure_ascii=False,
                indent=2
            )

        st.success("Đã lưu hồ sơ spa")