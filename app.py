import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. CẤU HÌNH TRANG WEB (TAB BROWSER) ---
st.set_page_config(
    page_title="AI Agency Super Sales",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS TÙY CHỈNH GIAO DIỆN (CHO SANG TRỌNG) ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        height: 3em;
        font-weight: bold;
        border-radius: 10px;
    }
    .reportview-container {background: #f0f2f6}
    div.block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# --- 3. THANH SIDEBAR (KHU VỰC CÀI ĐẶT CỦA SẾP) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=50)
    st.title("⚙️ CẤU HÌNH BỘ NÃO")
    st.markdown("---")
    
    # Nhập API Key
    api_key = st.text_input("1. Nhập Gemini API Key", type="password", help="Lấy key tại aistudio.google.com")
    
    # KHU VỰC QUAN TRỌNG NHẤT: TÙY CHỈNH PROMPT
    st.subheader("2. Nạp dữ liệu & Quy trình")
    st.info("💡 Mẹo: Copy file giá, quy trình xử lý khiếu nại của từng khách hàng (Don Chicken/Hoa Tường Vy) dán vào đây.")
    
    default_prompt = """VAI TRÒ:
Bạn là Trợ lý Sales AI chuyên nghiệp, chốt đơn đỉnh cao.

NHIỆM VỤ:
- Đọc tin nhắn hoặc hình ảnh khách gửi.
- Đưa ra 3 phương án trả lời (Ngắn gọn, Thuyết phục, Upsell).

DỮ LIỆU SẢN PHẨM & GIÁ (Ví dụ):
- Combo Gà Sốt Cay: 199k
- Combo Gà Phô Mai: 250k
- Bia tươi: 30k/ly

QUY TẮC ỨNG XỬ:
- Luôn xưng hô "Dạ/Vâng" và "Anh/Chị".
- Nếu khách chê đắt -> Nhấn mạnh vào chất lượng/số lượng.
- Nếu khách hỏi địa chỉ -> Gửi địa chỉ + Google Maps."""

    # Ô nhập Prompt tùy chỉnh (Lưu vào session state để không bị mất khi reload)
    system_prompt = st.text_area("Dán Prompt vào đây:", value=default_prompt, height=400)

# --- 4. GIAO DIỆN CHÍNH (KHU VỰC LÀM VIỆC CỦA NHÂN VIÊN) ---
st.title("🤖 AI AGENCY SALES ASSISTANT")
st.caption("Công cụ hỗ trợ phản hồi khách hàng đa kênh (Zalo/FB/Tiktok)")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Dữ liệu đầu vào (Input)")
    st.markdown("Copy ảnh màn hình đoạn chat hoặc gõ nội dung khách hỏi vào đây.")
    
    # Tab chọn loại dữ liệu cho gọn
    tab1, tab2 = st.tabs(["🖼️ Tải Ảnh Chat/Sản Phẩm", "✍️ Nhập Văn Bản"])
    
    with tab1:
        uploaded_file = st.file_uploader("Chọn ảnh...", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Ảnh đã tải lên", width=300)
            
    with tab2:
        user_text = st.text_area("Nội dung khách nhắn:", height=150, placeholder="Ví dụ: Khách bảo gà hôm nay hơi mặn, shop đền bù sao?")

    # NÚT BẤM KÍCH HOẠT
    generate_btn = st.button("🚀 PHÂN TÍCH & TRẢ LỜI NGAY")

with col2:
    st.subheader("📤 Kết quả tư vấn (Output)")
    
    if generate_btn:
        if not api_key:
            st.error("❌ Chưa nhập API Key ở cột bên trái sếp ơi!")
        elif not system_prompt:
            st.warning("⚠️ Chưa nạp dữ liệu não bộ (Prompt)!")
        elif not uploaded_file and not user_text:
            st.warning("⚠️ Chưa có thông tin khách hàng (Ảnh hoặc Text)!")
        else:
            with st.spinner("AI đang đọc dữ liệu & suy nghĩ..."):
                try:
                    # Gọi Google Gemini
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    
                    # Ghép Prompt hệ thống + Dữ liệu khách hàng
                    full_request = [system_prompt]
                    if user_text:
                        full_request.append(f"TIN NHẮN KHÁCH HÀNG:\n{user_text}")
                    if uploaded_file:
                        image = Image.open(uploaded_file)
                        full_request.append(image)
                    
                    # Gửi yêu cầu
                    response = model.generate_content(full_request)
                    
                    # Hiển thị kết quả đẹp
                    st.success("✅ Đã có 3 phương án xử lý:")
                    st.markdown(response.text)
                    
                    # Khu vực Copy nhanh
                    st.text_area("Copy nội dung để gửi khách:", value=response.text, height=300)
                    
                except Exception as e:
                    st.error(f"Lỗi hệ thống: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by Agency Team | Powered by Google Gemini 1.5 Flash")
