import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import ollama

# Cấu hình trang web
st.set_page_config(page_title="Hệ Thống Trợ Lý Sức Khỏe",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Lấy đường dẫn thư mục hiện tại
working_dir = os.path.dirname(os.path.abspath(__file__))

# Tải các model đã lưu
try:
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
    parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
    kidney_model = pickle.load(open(f'{working_dir}/saved_models/kidney_model.sav', 'rb'))
    kidney_fill = pickle.load(open(f'{working_dir}/saved_models/kidney_fill_values.pkl', 'rb'))
    num_fill = kidney_fill['numeric']
    cat_fill = kidney_fill['categorical']
except Exception as e:
    st.error(f"Lỗi khi tải mô hình: {e}")

# Thanh điều hướng bên trái
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100)
    selected = option_menu(
        'Hệ thống dự đoán đa bệnh',
        [
            'Dự đoán bệnh Tiểu đường',
            'Dự đoán bệnh Tim',
            'Dự đoán bệnh Parkinson',
            'Dự đoán bệnh Thận',
            'Trợ lý AI sức khỏe'
        ],
        menu_icon='hospital-fill',
        icons=['activity', 'heart-pulse', 'person-walking', 'droplet-fill','robot'],
        default_index=0
    )
    st.info("Hướng dẫn: Vui lòng nhập đầy đủ các chỉ số xét nghiệm để có kết quả chính xác nhất.")

# ------------------------------------------------------------------
# ==========================
# DỰ ĐOÁN BỆNH TIỂU ĐƯỜNG
# ==========================
if selected == 'Dự đoán bệnh Tiểu đường':
    st.title('🩺 Dự đoán bệnh Tiểu đường')
    st.divider()

    # --- NHÓM 1: THÔNG TIN CƠ BẢN & CƠ THỂ ---
    st.subheader("👤 Thông tin cơ bản & Chỉ số cơ thể")
    col1, col2, col3 = st.columns(3)

    with col1:
        Age = st.text_input('Tuổi', placeholder='Ví dụ: 30')
        Pregnancies = st.text_input('Số lần mang thai', placeholder='Ví dụ: 2',
                                    help="Tổng số lần mang thai (nhập 0 nếu là nam giới)")

    with col2:
        BMI = st.text_input('Chỉ số BMI', placeholder='Ví dụ: 22.5',
                            help="Chỉ số khối cơ thể (Cân nặng / Chiều cao bình phương)")
        DiabetesPedigreeFunction = st.text_input('Phả hệ Tiểu đường (DPF)', placeholder='Ví dụ: 0.5',
                                                 help="Chỉ số khả năng mắc bệnh dựa trên lịch sử gia đình (Diabetes Pedigree Function)")

    with col3:
        SkinThickness = st.text_input('Độ dày nếp gấp da (mm)', placeholder='Ví dụ: 20',
                                      help="Độ dày nếp gấp da vùng cơ tam đầu (Triceps skin fold thickness)")

    st.divider()

    # --- NHÓM 2: CHỈ SỐ XÉT NGHIỆM ---
    st.subheader("🔬 Chỉ số xét nghiệm lâm sàng")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        Glucose = st.text_input('Nồng độ Glucose', placeholder='Ví dụ: 120',
                                help="Nồng độ Glucose trong huyết tương sau 2 giờ thử nghiệm dung nạp glucose đường uống")

    with col_b:
        Insulin = st.text_input('Chỉ số Insulin', placeholder='Ví dụ: 80',
                                help="Nồng độ Insulin trong huyết thanh sau 2 giờ (mu U/ml)")

    with col_c:
        BloodPressure = st.text_input('Huyết áp (mm Hg)', placeholder='Ví dụ: 70',
                                      help="Chỉ số huyết áp tâm trương (Diastolic blood pressure)")

    # --- XỬ LÝ DỰ ĐOÁN ---
    st.write("")  # Tạo khoảng trống
    if st.button('Kiểm tra kết quả Tiểu đường'):
        try:
            # Thứ tự user_input phải khớp chính xác với thứ tự biến mà model đã train:
            # [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DPF, Age]
            user_input = [
                Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                BMI, DiabetesPedigreeFunction, Age
            ]

            # Chuyển đổi sang kiểu số float
            user_input = [float(x) for x in user_input]

            # Dự đoán
            diab_prediction = diabetes_model.predict([user_input])

            if diab_prediction[0] == 1:
                st.error(
                    'Kết quả: ⚠️ Người này có khả năng cao mắc bệnh Tiểu đường.')
            else:
                st.success('Kết quả: ✅ Người này hiện tại không có dấu hiệu mắc bệnh Tiểu đường.')

        except ValueError:
            st.warning("⚠️ Vui lòng nhập đầy đủ các thông số dưới dạng số (Ví dụ: 20 hoặc 22.5).")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")

# ------------------------------------------------------------------
# ==========================
# DỰ ĐOÁN BỆNH TIM
# ==========================
if selected == 'Dự đoán bệnh Tim':
    st.title('❤️ Dự đoán bệnh Tim')
    st.divider()

    # --- NHÓM 1: THÔNG TIN CƠ BẢN & HUYẾT ÁP ---
    st.subheader("👤 Thông tin cơ bản & Huyết áp")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Tuổi', placeholder='Ví dụ: 45')
        sex = st.text_input('Giới tính', placeholder='Nam: 1, Nữ: 0', help="Nhập 1 cho Nam và 0 cho Nữ")

    with col2:
        trestbps = st.text_input('Huyết áp lúc nghỉ (trestbps)', placeholder='Ví dụ: 120',
                                 help="Huyết áp tâm trương đo khi nghỉ ngơi (mm Hg)")
        fbs = st.text_input('Đường huyết lúc đói (fbs)', placeholder='> 120mg/dl: 1, Ngược lại: 0',
                            help="Chỉ số đường huyết lúc đói có lớn hơn 120 mg/dl không? (1 = Có; 0 = Không)")

    with col3:
        chol = st.text_input('Chỉ số Cholesterol', placeholder='Ví dụ: 200',
                             help="Nồng độ Cholesterol trong huyết thanh (mg/dl)")

    st.divider()

    # --- NHÓM 2: TRIỆU CHỨNG & ĐIỆN TÂM ĐỒ (ECG) ---
    st.subheader("🩺 Triệu chứng & Điện tâm đồ")
    col4, col5, col6 = st.columns(3)

    with col4:
        cp = st.text_input('Loại đau thắt ngực (cp)', placeholder='Nhập từ 0 - 3',
                           help="0: Điển hình, 1: Không điển hình, 2: Đau không do tim, 3: Không triệu chứng")
        exang = st.text_input('Đau thắt ngực khi vận động (exang)', placeholder='Có: 1, Không: 0',
                              help="Tình trạng đau thắt ngực có xuất hiện khi gắng sức không? (1 = Có; 0 = Không)")

    with col5:
        restecg = st.text_input('Kết quả điện tâm đồ (restecg)', placeholder='Nhập 0, 1 hoặc 2',
                                help="0: Bình thường, 1: Bất thường sóng ST-T, 2: Phì đại thất trái")

    with col6:
        thalach = st.text_input('Nhịp tim tối đa (thalach)', placeholder='Ví dụ: 150',
                                help="Nhịp tim cao nhất đạt được trong quá trình kiểm tra")

    st.divider()

    # --- NHÓM 3: CHỈ SỐ KIỂM TRA GẮNG SỨC (ST SEGMENT) ---
    st.subheader("📉 Chỉ số chuyên sâu & Gắng sức")
    col7, col8, col9 = st.columns(3)

    with col7:
        oldpeak = st.text_input('Độ hạ đoạn ST (Oldpeak)', help="Độ hạ đoạn ST gây ra bởi vận động so với lúc nghỉ")
        slope = st.text_input('Độ dốc đoạn ST (Slope)', help="0: Dốc lên, 1: Đi ngang, 2: Dốc xuống")

    with col8:
        ca = st.text_input('Số mạch chính (ca)', placeholder='Nhập từ 0 - 3',
                           help="Số lượng các mạch máu chính (0-3) được soi dưới tia X")
        thal = st.text_input('Chỉ số Thal', placeholder='Nhập từ 0 - 3',
                             help="0: Bình thường, 1: Khiếm khuyết cố định, 2: Khiếm khuyết có thể đảo ngược")

    # --- XỬ LÝ DỰ ĐOÁN ---
    st.write("")
    if st.button('Kiểm tra kết quả bệnh Tim'):
        try:
            # Thứ tự user_input phải khớp chính xác với Model:
            # [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

            # Chuyển đổi sang số thực
            user_input = [float(x) for x in user_input]

            # Dự đoán từ model
            heart_prediction = heart_disease_model.predict([user_input])

            if heart_prediction[0] == 1:
                st.error('⚠️ Kết quả: Người này có dấu hiệu mắc bệnh Tim. Cần sớm tham khảo ý kiến bác sĩ chuyên khoa.')
            else:
                st.success('✅ Kết quả: Người này hiện tại không có dấu hiệu mắc bệnh Tim.')

        except ValueError:
            st.warning("⚠️ Vui lòng nhập đầy đủ các thông số dưới dạng số. Kiểm tra lại các ô nhập liệu.")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi hệ thống: {e}")

# ------------------------------------------------------------------
# TRANG DỰ ĐOÁN PARKINSON
# ------------------------------------------------------------------
if selected == "Dự đoán bệnh Parkinson":
    st.title("🧠 Dự đoán bệnh Parkinson")
    st.info("Các chỉ số dưới đây được đo lường thông qua bản ghi âm giọng nói của người bệnh.")
    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('Tần số trung bình - Fo(Hz)', help="Tần số cơ bản trung bình của giọng nói")
        RAP = st.text_input('Độ rung RAP', help="MDVP:RAP - Chỉ số đo sự biến đổi tần số")
        APQ3 = st.text_input('Độ rè APQ3', help="Shimmer:APQ3 - Biến đổi biên độ trong 3 chu kỳ")
        HNR = st.text_input('Độ trong HNR', help="Tỷ lệ hài âm trên nhiễu (HNR cao là giọng trong)")
        D2 = st.text_input('Chỉ số D2', help="Đo tính chất động học của giọng nói")

    with col2:
        fhi = st.text_input('Tần số cao nhất - Fhi(Hz)', help="Tần số cơ bản lớn nhất")
        PPQ = st.text_input('Độ rung PPQ', help="MDVP:PPQ - Chỉ số biến đổi tần số qua 5 chu kỳ")
        APQ5 = st.text_input('Độ rè APQ5', help="Shimmer:APQ5 - Biến đổi biên độ trong 5 chu kỳ")
        RPDE = st.text_input('Độ phức tạp RPDE', help="Đo độ phức tạp của chu kỳ giọng nói")
        PPE = st.text_input('Độ hỗn loạn PPE', help="Chỉ số Entropy cao độ (PPE) - Rất quan trọng trong chẩn đoán")

    with col3:
        flo = st.text_input('Tần số thấp nhất - Flo(Hz)', help="Tần số cơ bản nhỏ nhất")
        DDP = st.text_input('Độ rung DDP', help="Jitter:DDP")
        APQ = st.text_input('Độ rè APQ', help="MDVP:APQ")
        DFA = st.text_input('Chỉ số DFA', help="Phân tích dao động giọng nói")

    with col4:
        Jitter_percent = st.text_input('Độ rung (%)', help="MDVP:Jitter(%)")
        Shimmer = st.text_input('Độ rè Shimmer', help="MDVP:Shimmer")
        DDA = st.text_input('Độ rè DDA', help="Shimmer:DDA")
        spread1 = st.text_input('Độ biến thiên 1', help="spread1: Biến thiên cao độ phi tuyến tính dạng 1")

    with col5:
        Jitter_Abs = st.text_input('Độ rung (Abs)', help="MDVP:Jitter(Abs)")
        Shimmer_dB = st.text_input('Độ rè (dB)', help="MDVP:Shimmer(dB)")
        NHR = st.text_input('Tỷ lệ nhiễu NHR', help="Tỷ lệ nhiễu trên hài âm")
        spread2 = st.text_input('Độ biến thiên 2', help="spread2: Biến thiên cao độ phi tuyến tính dạng 2")

    if st.button("Kiểm tra kết quả Parkinson"):
        try:
            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                          RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                          APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
            user_input = [float(x) for x in user_input]
            parkinsons_prediction = parkinsons_model.predict([user_input])

            if parkinsons_prediction[0] == 1:
                st.error("Kết quả: ⚠️ Người này có dấu hiệu mắc bệnh Parkinson")
            else:
                st.success("Kết quả: ✅ Người này không mắc bệnh Parkinson")
        except ValueError:
            st.warning("Vui lòng nhập các chỉ số Parkinson hợp lệ.")

# ------------------------------------------------------------------
# ==========================
# DỰ ĐOÁN BỆNH THẬN (KIDNEY)
# ==========================
if selected == 'Dự đoán bệnh Thận':
    st.title('💧 Dự đoán bệnh Thận mãn tính')
    st.info("Đây là các chỉ số xét nghiệm máu và nước tiểu.")
    st.divider()

    # --- NHÓM 1: THÔNG TIN CƠ BẢN & NƯỚC TIỂU ---
    st.subheader("📋 Chỉ số cơ bản & Nước tiểu")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Tuổi')
        bp = st.text_input('Huyết áp (bp)', help="Huyết áp lúc nghỉ (mm/Hg)")
        sg = st.text_input('Tỷ trọng nước tiểu (sg)', help="Chỉ số Specific Gravity: Đo khả năng cô đặc nước tiểu (thường 1.005 - 1.025)")

    with col2:
        al = st.text_input('Chỉ số Albumin (al)', help="Mức độ protein trong nước tiểu (0-5, 0 là bình thường)")
        su = st.text_input('Chỉ số Đường (su)', help="Mức độ đường trong nước tiểu (0-5)")
        rbc = st.text_input('Hồng cầu (rbc)', placeholder="Nhập 0 hoặc 1", help="0: Bất thường, 1: Bình thường")

    with col3:
        pc = st.text_input('Tế bào mủ (pc)', placeholder="Nhập 0 hoặc 1", help="Sự hiện diện của tế bào mủ (0: Bất thường, 1: Bình thường)")
        pcc = st.text_input('Cụm tế bào mủ (pcc)', placeholder="Nhập 0 hoặc 1", help="0: Không có cụm, 1: Có cụm tế bào mủ")
        ba = st.text_input('Vi khuẩn (ba)', placeholder="Nhập 0 hoặc 1", help="Vi khuẩn trong nước tiểu (0: Không có, 1: Có)")

    st.divider()

    # --- NHÓM 2: CHỈ SỐ XÉT NGHIỆM MÁU ---
    st.subheader("🩸 Chỉ số xét nghiệm máu")
    col4, col5, col6 = st.columns(3)

    with col4:
        bgr = st.text_input('Đường huyết ngẫu nhiên (bgr)', help="Nồng độ đường trong máu (mgs/dl)")
        bu = st.text_input('Ure máu (bu)', help="Nồng độ Ure trong máu (mgs/dl)")
        sc = st.text_input('Creatinine huyết thanh (sc)', help="Chỉ số quan trọng nhất đánh giá chức năng lọc của thận (mgs/dl)")

    with col5:
        sod = st.text_input('Natri (sod)', help="Nồng độ Natri trong máu (mEq/L)")
        pot = st.text_input('Kali (pot)', help="Nồng độ Kali trong máu (mEq/L)")
        hemo = st.text_input('Hemoglobin (hemo)', help="Huyết sắc tố trong máu (gms)")

    with col6:
        pcv = st.text_input('Thể tích khối hồng cầu (pcv)', help="Tỷ lệ thể tích hồng cầu trên tổng thể tích máu")
        wc = st.text_input('Số lượng bạch cầu (wc)', help="Đơn vị: cells/cumm")
        rc = st.text_input('Số lượng hồng cầu (rc)', help="Đơn vị: millions/cmm")

    st.divider()

    # --- NHÓM 3: TIỀN SỬ BỆNH LÝ & TRIỆU CHỨNG ---
    st.subheader("🏥 Tiền sử & Triệu chứng")
    col7, col8, col9 = st.columns(3)

    with col7:
        htn = st.text_input('Tăng huyết áp (htn)', placeholder="Nhập 0 hoặc 1", help="0: Không, 1: Có")
        dm = st.text_input('Tiểu đường (dm)', placeholder="Nhập 0 hoặc 1", help="0: Không, 1: Có")

    with col8:
        cad = st.text_input('Bệnh mạch vành (cad)', placeholder="Nhập 0 hoặc 1", help="0: Không, 1: Có")
        appet = st.text_input('Ăn uống (appet)', placeholder="Nhập 0 hoặc 1", help="0: Kém, 1: Ngon miệng")

    with col9:
        pe = st.text_input('Phù chân (pe)', placeholder="Nhập 0 hoặc 1", help="0: Không phù, 1: Có phù chân")
        ane = st.text_input('Thiếu máu (ane)', placeholder="Nhập 0 hoặc 1", help="0: Không thiếu máu, 1: Có thiếu máu")

    # --- NÚT DỰ ĐOÁN & XỬ LÝ KẾT QUẢ ---
    st.write("") # Tạo khoảng trống
    if st.button('Kiểm tra kết quả bệnh Thận'):
        try:
            # Thu thập dữ liệu theo đúng thứ tự mảng đầu vào của model
            user_input = [
                float(age) if age != '' else num_fill['age'],
                float(bp) if bp != '' else num_fill['bp'],
                float(sg) if sg != '' else num_fill['sg'],
                float(al) if al != '' else num_fill['al'],
                float(su) if su != '' else num_fill['su'],
                float(rbc) if rbc != '' else cat_fill['rbc'],
                float(pc) if pc != '' else cat_fill['pc'],
                float(pcc) if pcc != '' else cat_fill['pcc'],
                float(ba) if ba != '' else cat_fill['ba'],
                float(bgr) if bgr != '' else num_fill['bgr'],
                float(bu) if bu != '' else num_fill['bu'],
                float(sc) if sc != '' else num_fill['sc'],
                float(sod) if sod != '' else num_fill['sod'],
                float(pot) if pot != '' else num_fill['pot'],
                float(hemo) if hemo != '' else num_fill['hemo'],
                float(pcv) if pcv != '' else num_fill['pcv'],
                float(wc) if wc != '' else num_fill['wc'],
                float(rc) if rc != '' else num_fill['rc'],
                float(htn) if htn != '' else cat_fill['htn'],
                float(dm) if dm != '' else cat_fill['dm'],
                float(cad) if cad != '' else cat_fill['cad'],
                float(appet) if appet != '' else cat_fill['appet'],
                float(pe) if pe != '' else cat_fill['pe'],
                float(ane) if ane != '' else cat_fill['ane'],
            ]

            pred = kidney_model.predict([user_input])

            if pred[0] == 1:
                st.error('Kết quả: ⚠️ Người này có dấu hiệu mắc bệnh Thận mãn tính.')
            else:
                st.success('Kết quả: ✅ Người này không có dấu hiệu mắc bệnh Thận.')

        except ValueError:
            st.warning("Vui lòng nhập số hợp lệ vào các ô chỉ số.")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi hệ thống: {e}")

# ==========================
# TRANG TRỢ LÝ AI SỨC KHỎE
# ==========================
if selected == 'Trợ lý AI sức khỏe':
    st.title("🤖 Trợ lý Sức khỏe AI")
    st.markdown("---")

    # Đổi sang model qwen2:1.5b để tiếng Việt chuẩn hơn
    AI_MODEL = "qwen2:1.5b"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                # 1. Chỉ lấy tối đa 5 tin nhắn gần nhất để tránh nhiễu model nhỏ
                recent_messages = st.session_state.messages[-5:]

                response = ollama.chat(
                    model=AI_MODEL,
                    messages=[
                        {
                            'role': 'system',
                            'content': (
                                "Bạn là bác sĩ ảo chuyên nghiệp. Nhiệm vụ của bạn là cung cấp thông tin y khoa chính xác, ngắn gọn.\n"
                                "QUY TẮC BẮT BUỘC:\n"
                                "1. Không lặp lại ý đã nói.\n"
                                "2. Luôn trả lời theo định dạng sau:\n"
                                "- **Giải thích:** (1-2 câu về tình trạng)\n"
                                "- **Nguyên nhân phổ biến:** (Liệt kê gạch đầu dòng)\n"
                                "- **Lời khuyên:** (Cần làm gì ngay và khi nào gặp bác sĩ)\n"
                                "3. Nếu không biết, hãy nói: 'Tôi không có đủ dữ liệu, hãy tham khảo ý kiến bác sĩ chuyên khoa'."
                            )
                        },
                        *recent_messages
                    ],
                    stream=True,
                    options={
                        'temperature': 0.2,       # Giảm xuống 0.2 để cực kỳ nghiêm túc, tránh sáng tạo linh tinh
                        'top_p': 0.8,
                        'repeat_penalty': 1.2,    # QUAN TRỌNG: Ngăn chặn việc lặp lại từ và ý (1.1 - 1.5 là ổn)
                        'presence_penalty': 0.6,  # Khuyến khích model đưa ra ý mới
                        'num_ctx': 2048,          # Giới hạn ngữ cảnh để model tập trung
                    }
                )

                for chunk in response:
                    content = chunk['message']['content']
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")

                # Hậu xử lý: Xóa bỏ các ký tự thừa nếu model tự ý thêm vào
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"⚠️ Lỗi: {str(e)}")