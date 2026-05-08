import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Trợ Lý Sức Khỏe AI",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# --- CUSTOM CSS (Làm đẹp giao diện) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    div[data-testid="stExpander"] {
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        background: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TẢI MÔ HÌNH (Giữ nguyên đường dẫn và logic) ---
working_dir = os.path.dirname(os.path.abspath(__file__))

diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
kidney_model = pickle.load(open(f'{working_dir}/saved_models/kidney_model.sav', 'rb'))

kidney_fill = pickle.load(open(f'{working_dir}/saved_models/kidney_fill_values.pkl', 'rb'))
num_fill = kidney_fill['numeric']
cat_fill = kidney_fill['categorical']

# --- THANH ĐIỀU HƯỚNG BÊN TRÁI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2773/2773531.png", width=80)
    st.title("Menu Chính")
    selected = option_menu(
        'Hệ Thống Dự Đoán Bệnh',
        [
            'Dự đoán Tiểu đường',
            'Dự đoán Bệnh tim',
            'Dự đoán Parkinson',
            'Dự đoán Bệnh thận'
        ],
        icons=['activity', 'heart', 'person', 'droplet'],
        menu_icon='hospital-fill',
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#007bff"},
        }
    )

# ==========================
# TRANG DỰ ĐOÁN TIỂU ĐƯỜNG
# ==========================
if selected == 'Dự đoán Tiểu đường':
    st.markdown("<h1 style='text-align: center;'>Chẩn đoán Bệnh Tiểu Đường 🩸</h1>", unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1: Pregnancies = st.text_input('Số lần mang thai')
        with col2: Glucose = st.text_input('Chỉ số Đường huyết (Glucose)')
        with col3: BloodPressure = st.text_input('Chỉ số Huyết áp')
        with col1: SkinThickness = st.text_input('Độ dày nếp gấp da (Triceps)')
        with col2: Insulin = st.text_input('Chỉ số Insulin')
        with col3: BMI = st.text_input('Chỉ số BMI (Trọng lượng/Chiều cao)')
        with col1: DiabetesPedigreeFunction = st.text_input('Chỉ số Di truyền Tiểu đường')
        with col2: Age = st.text_input('Tuổi')

    diab_diagnosis = ''
    if st.button('Kiểm tra Kết quả Tiểu đường'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        user_input = [float(x) for x in user_input]
        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            st.error('⚠️ Kết quả: Người này có nguy cơ bị tiểu đường')
        else:
            st.success('✅ Kết quả: Người này không bị tiểu đường')

# ==========================
# TRANG DỰ ĐOÁN BỆNH TIM
# ==========================
if selected == 'Dự đoán Bệnh tim':
    st.markdown("<h1 style='text-align: center;'>Chẩn đoán Bệnh Tim Mạch ❤️</h1>", unsafe_allow_html=True)

    with st.expander("Thông số sinh tồn", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1: age = st.text_input('Tuổi')
        with col2: sex = st.text_input('Giới tính (1=Nam, 0=Nữ)')
        with col3: cp = st.text_input('Loại đau thắt ngực (0-3)')
        with col1: trestbps = st.text_input('Huyết áp lúc nghỉ ngơi')
        with col2: chol = st.text_input('Chỉ số Cholesterol (mg/dl)')
        with col3: fbs = st.text_input('Đường huyết khi đói > 120 mg/dl (1=Đúng, 0=Sai)')

    with st.expander("Kết quả lâm sàng", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1: restecg = st.text_input('Kết quả Điện tâm đồ lúc nghỉ ngơi')
        with col2: thalach = st.text_input('Nhịp tim tối đa đạt được')
        with col3: exang = st.text_input('Đau thắt ngực do tập thể dục (1=Có, 0=Không)')
        with col1: oldpeak = st.text_input('Đoạn ST chênh xuống do tập thể dục')
        with col2: slope = st.text_input('Độ dốc đoạn ST đỉnh tập thể dục')
        with col3: ca = st.text_input('Số lượng mạch máu chính (0-3)')
        with col1: thal = st.text_input('Thal: 0=Bình thường; 1=Khuyết tật cố định; 2=Khuyết tật có thể đảo ngược')

    if st.button('Kiểm tra Kết quả Bệnh tim'):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        user_input = [float(x) for x in user_input]
        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            st.error('⚠️ Kết quả: Người này có nguy cơ mắc bệnh tim')
        else:
            st.success('✅ Kết quả: Người này không mắc bệnh tim')

# ==========================
# TRANG DỰ ĐOÁN PARKINSON
# ==========================
if selected == "Dự đoán Parkinson":
    st.markdown("<h1 style='text-align: center;'>Chẩn đoán Bệnh Parkinson 🧠</h1>", unsafe_allow_html=True)
    st.info("Nhập các thông số đo giọng nói (MDVP):")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        fo = st.text_input('MDVP:Fo(Hz)'); RAP = st.text_input('MDVP:RAP'); APQ3 = st.text_input(
            'Shimmer:APQ3'); HNR = st.text_input('HNR'); D2 = st.text_input('D2')
    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)'); PPQ = st.text_input('MDVP:PPQ'); APQ5 = st.text_input(
            'Shimmer:APQ5'); RPDE = st.text_input('RPDE'); PPE = st.text_input('PPE')
    with col3:
        flo = st.text_input('MDVP:Flo(Hz)'); DDP = st.text_input('Jitter:DDP'); APQ = st.text_input(
            'MDVP:APQ'); DFA = st.text_input('DFA')
    with col4:
        Jitter_pct = st.text_input('MDVP:Jitter(%)'); Shimmer = st.text_input('MDVP:Shimmer'); DDA = st.text_input(
            'Shimmer:DDA'); spread1 = st.text_input('spread1')
    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)'); Shimmer_dB = st.text_input(
            'MDVP:Shimmer(dB)'); NHR = st.text_input('NHR'); spread2 = st.text_input('spread2')

    if st.button("Kiểm tra Kết quả Parkinson"):
        user_input = [fo, fhi, flo, Jitter_pct, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA,
                      NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
        user_input = [float(x) for x in user_input]
        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            st.error("⚠️ Kết quả: Người này mắc bệnh Parkinson")
        else:
            st.success("✅ Kết quả: Người này không mắc bệnh Parkinson")

# ==========================
# TRANG DỰ ĐOÁN BỆNH THẬN
# ==========================
if selected == 'Dự đoán Bệnh thận':
    st.markdown("<h1 style='text-align: center;'>Chẩn đoán Bệnh Thận Mãn Tính 💧</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Chỉ số Máu & Sinh tồn", "Kết quả Xét nghiệm", "Bệnh lý kèm theo"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            age = st.text_input('Tuổi')
            bp = st.text_input('Huyết áp (BP)')
            sg = st.text_input('Tỷ trọng nước tiểu (SG)')
            al = st.text_input('Albumin (AL)')
            su = st.text_input('Đường trong nước tiểu (Sugar)')
        with col2:
            bgr = st.text_input('Đường huyết ngẫu nhiên')
            bu = st.text_input('Ure máu')
            sc = st.text_input('Creatinine huyết thanh')
            sod = st.text_input('Natri (Sodium)')
            pot = st.text_input('Kali (Potassium)')

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            rbc = st.text_input('Hồng cầu (0=Bthường, 1=Bthường nhẹ)')
            pc = st.text_input('Tế bào mủ (0/1)')
            pcc = st.text_input('Cụm tế bào mủ (0/1)')
            ba = st.text_input('Vi khuẩn (0/1)')
            hemo = st.text_input('Huyết sắc tố (Hemoglobin)')
        with col2:
            pcv = st.text_input('Thể tích khối hồng cầu (PCV)')
            wc = st.text_input('Số lượng bạch cầu')
            rc = st.text_input('Số lượng hồng cầu')

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            htn = st.text_input('Cao huyết áp (0/1)')
            dm = st.text_input('Đái tháo đường (0/1)')
            cad = st.text_input('Bệnh mạch vành (0/1)')
        with col2:
            appet = st.text_input('Ăn uống (0=Kém, 1=Ngon miệng)')
            pe = st.text_input('Phù chân (0/1)')
            ane = st.text_input('Thiếu máu (0/1)')

    if st.button('Kiểm tra Kết quả Bệnh Thận'):
        try:
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
                st.error('⚠️ Kết quả: Người này có dấu hiệu mắc bệnh thận')
            else:
                st.success('✅ Kết quả: Người này không mắc bệnh thận')
        except Exception:
            st.warning('Vui lòng nhập đầy đủ các thông số ở dạng số (ví dụ: 0 hoặc 1 cho các lựa chọn Có/Không)')