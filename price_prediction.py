import streamlit as st
import pandas as pd
import joblib
import os

def main():
    # Load model and expected columns
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model = joblib.load(os.path.join(script_dir, "best_xgb_model_house.pkl"))
        model_columns = joblib.load(os.path.join(script_dir, "model_columns.pkl"))
    except FileNotFoundError:
        st.error("Model files not found. Please ensure both model files are in the correct directory.")
        return

    st.title("🏠 House Price Prediction")
    st.write("Fill in the property details to get a price prediction")

    # Input sections
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            bedroom = st.number_input("Number of Bedrooms", min_value=0, step=1)
            bathroom = st.number_input("Number of Bathrooms", min_value=0, step=1)
            garage = st.number_input("Number of Garages", min_value=0, step=1)
            land_area = st.number_input("Land Area (m²)", min_value=0.0)
            building_area = st.number_input("Building Area (m²)", min_value=0.0)

        with col2:
            tenor = st.number_input("Tenor (Years)", min_value=1, max_value=30, step=1)
            is_luxury = st.selectbox("Is it a luxury property?", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            building_land_ratio = st.number_input("Building-to-Land Ratio", min_value=0.0, max_value=5.0, step=0.01)
            area_efficiency = st.number_input("Area Efficiency", min_value=0.0, max_value=1.0, step=0.01)
            total_rooms = st.number_input("Total Rooms", min_value=0, step=1)

        # Categorical inputs
        location = st.selectbox("Location", sorted([
            'Sleman', 'Tangerang Selatan', 'Bogor', 'Jakarta Utara', 'Jakarta Pusat', 'Depok', 'Tangerang', 'Semarang',
            'Jakarta Selatan', 'Badung', 'Yogyakarta', 'Magelang', 'Jakarta Barat', 'Jakarta Timur', 'Bekasi',
            'Sidoarjo', 'Surabaya', 'Bandung', 'Bantul', 'Gianyar', 'Cimahi', 'Gresik', 'Cikarang', 'Denpasar', 'Malang',
            'Karawang', 'Medan', 'Batam', 'Tabanan', 'Karangasem', 'Mojokerto', 'Gunung Kidul', 'Cirebon', 'Purwokerto',
            'Bandung Barat', 'Kediri', 'Lampung Selatan', 'Palembang', 'Subang', 'Bandar Lampung', 'Sumedang',
            'Lombok Barat', 'Deli Serdang', 'Balikpapan', 'Cianjur', 'Solo', 'Bangkalan', 'Purwodadi', 'Bukittinggi',
            'Banyuwangi', 'Banggai', 'Purwakarta', 'Cilegon', 'Jember', 'Banyumas', 'Buleleng', 'Makassar', 'Serang',
            'Blitar', 'Tasikmalaya', 'Kendal', 'Kulon Progo', 'Magetan', 'Sukabumi', 'Karanganyar', 'Pekalongan',
            'Jembrana', 'Lombok Timur', 'Tulungagung', 'Batang', 'Pasuruan', 'Lumajang', 'Probolinggo', 'Madiun',
            'Ponorogo', 'Bojonegoro', 'Nganjuk', 'Pamekasan', 'Madura', 'Ciamis', 'Tuban', 'Temanggung', 'Lebak',
            'Sragen', 'Sukoharjo', 'Gowa', 'Majene', 'Bontang', 'Mempawah', 'Lampung Utara', 'Jayapura', 'Biak Numfor',
            'Nabire', 'Lombok Tengah', 'Mataram', 'Lombok Utara', 'Ngawi', 'Bondowoso', 'Bone', 'Wajo', 'Palu',
            'Pare-Pare', 'Gorontalo', 'Banjar', 'Kuantan Singingi', 'Labuhan Batu', 'Serdang Bedagai',
            'Indragiri Hulu', 'Nagan Raya', 'Asahan', 'Simalungun', 'Batu-Bara', 'Lhokseumawe', 'Langsa', 'Pelalawan',
            'Aceh Besar', 'Pangkal Pinang', 'Kota Waringin Timur', 'Tanjung Jabung Timur', 'Jambi', 'Lahat', 'Solok',
            'Metro', 'Pontianak', 'Samarinda', 'Banjar Baru', 'Kubu Raya', 'Tanah Bumbu', 'Tabalong', 'Kutai Timur',
            'Lubuk Linggau', 'Musi Rawas', 'Bengkulu', 'Muaro Jambi', 'Sumbawa Barat', 'Dompu', 'Bima', 'Merauke',
            'Keerom', 'Sorong Selatan', 'Lampung Tengah', 'Tulang Bawang', 'Banyuasin', 'Ogan Ilir', 'Sarolangun',
            'Pagar Alam', 'Maros', 'Kampar', 'Boyolali', 'Majalengka', 'Palopo', 'Bangka', 'Pematang Siantar',
            'Pekanbaru', 'Manado', 'Palangkaraya', 'Banjarmasin', 'Padang', 'Garut', 'Kendari', 'Singkawang', 'Pemalang',
            'Tanjung Pinang', 'Surakarta', 'Klaten', 'Batu', 'Pasaman', 'Tanah Datar', 'Tebo', 'Belitung', 'Kepahiang',
            'Lampung Timur', 'Kupang', 'Lamongan', 'Cilacap', 'Wonogiri', 'Jepara', 'Kuningan', 'Indramayu',
            'Rejang Lebong', 'Pandeglang', 'Jombang', 'Tegal', 'Bener Meriah', 'Prabumulih', 'Situbondo',
            'Minahasa Utara', 'Bangli', 'Toba Samosir', 'Berau', 'Manggarai', 'Maluku Tengah', 'Pati', 'Sampang',
            'Klungkung', 'Dumai', 'Kepulauan Seribu', 'Salatiga', 'Pesawaran', 'Barru', 'Demak', 'Rembang', 'Cikampek',
            'Kabupaten Bandung', 'Brebes', 'Penajam Paser Utara', 'Anyer', 'Ambon', 'Rokan Hilir', 'Wonosobo',
            'Manggarai Barat', 'Bitung', 'Blora', 'Kutai Kartanegara', 'Nusa Lembongan', 'Tebing Tinggi',
            'Bone Bolango', 'Melawi', 'Semarapura', 'Kepulauan Talaud', 'Kabupaten Kudus', 'Muna', 'Ambarawa',
            'Pangandaran', 'Ternate', 'Lampung Barat', 'Grobogan', 'Sumba Barat', 'Karimun', 'Purbalingga', 'Kebumen',
            'Muko Muko', 'Selayar', 'Bulukumba', 'Landak', 'Pacitan', 'Banjarnegara', 'Bintan', 'Langkat', 'Sumbawa',
            'Tana Toraja', 'Nunukan', 'Muara Enim', 'Trenggalek', 'Sidenreng Rappang', 'Kolaka', 'Ketapang',
            'Banda Aceh', 'Timor Tengah Utara', 'Wakatobi', 'Tapanuli Selatan', 'Pringsewu', 'Purworejo', 'Bulungan',
            'Kota Waringin Barat', 'Ogan Komering Ilir', 'Sambas', 'Padang Pariaman', 'Minahasa', 'Tomohon',
            'Pangkajene', 'Natuna', 'Bombana', 'Australia', 'Sumba Barat Daya'
        ]))

        property_type = st.selectbox("Property Type", [
            'tanah', 'rumah', 'apartemen', 'kavling', 'villa',
            'kost', 'ruko', 'house', 'gudang', 'apartment'
        ])

        area_category = st.selectbox("Area Category", [
            'tiny', 'small', 'medium', 'large', 'Uncategorized'
        ])

        submitted = st.form_submit_button("Predict Price")

    if submitted:
        # Initialize input_data dictionary with numeric + selected categorical inputs
        input_data = {
            'bedroom': bedroom,
            'bathroom': bathroom,
            'garage': garage,
            'land_area': land_area,
            'building_area': building_area,
            'Tenor (Years)': tenor,
            'is_luxury': is_luxury,
            'building_land_ratio': building_land_ratio,
            'area_efficiency': area_efficiency,
            'Total_rooms': total_rooms
        }

        # One-hot encode categorical inputs
        for col in model_columns:
            if col.startswith("location_"):
                if f"location_{location}" == col:
                    input_data[col] = 1
                else:
                    input_data[col] = 0
            elif col.startswith("type_"):
                if f"type_{property_type}" == col:
                    input_data[col] = 1
                else:
                    input_data[col] = 0
            elif col.startswith("area_category_"):
                if f"area_category_{area_category}" == col:
                    input_data[col] = 1
                else:
                    input_data[col] = 0
            else:
                if col not in input_data:
                    input_data[col] = 0

        # Convert input data to DataFrame for prediction
        input_encoded = pd.DataFrame([input_data], columns=model_columns)

        # Predict
        try:
            prediction = model.predict(input_encoded)[0]
            st.success(f"## Predicted Price: {prediction:,.0f} Million Rupiah (Rp {prediction:,.0f} Miliar)")


            # Debug info
            with st.expander("Debug Info"):
                st.write("Model expects these columns:", model_columns)
                st.write("Non-zero input features:", input_encoded.loc[:, input_encoded.iloc[0] != 0])
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
            st.write(input_encoded)

if __name__ == "__main__":
    main()
