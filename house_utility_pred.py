import streamlit as st
import pickle
import os

def main():
    st.title("Buying House Prediction")

    @st.cache_data
    def load_summaries():
        base_dir = os.path.dirname(__file__)
        pkl_path = os.path.join(base_dir, "type_price_summaries.pkl")
        with open(pkl_path, "rb") as f:
            return pickle.load(f)

    type_price_summaries = load_summaries()

    locations = sorted({loc for loc, _ in type_price_summaries})
    property_types = sorted({btype for _, btype in type_price_summaries})

    # Add "All" options at the front
    locations.insert(0, "All Locations")
    property_types.insert(0, "All Types")

    st.write("### Step 1: Enter the Money you can Spare Yearly for Mortgage (in million Rupiah)")
    annual_money = st.number_input("Annual spare money (Juta Rupiah)", min_value=0, step=50)

    st.write("### Step 2: Select your Preferred Location") 
    selected_location = st.selectbox("Location", locations)

    st.write("### Step 3: Select the Property Type you want")
    selected_type = st.selectbox("Property Type", property_types)

    if annual_money > 0:
        budget = annual_money * 20
        st.write(f"Your estimated house budget is: **{budget:,} Juta Rupiah**")

        price_bins = [0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 4000, 6000, float('inf')]
        bin_labels = ['<250', '250-500', '500-750', '750-1000', '1000-1250', '1250-1500',
                      '1500-1750', '1750-2000', '2000-2500', '2500-3000', '3000-4000', '4000-6000', '>6000']

        target_bin = None
        for i in range(len(price_bins) - 1):
            if price_bins[i] < budget <= price_bins[i + 1]:
                target_bin = bin_labels[i]
                break
        if target_bin is None:
            target_bin = '>6000'

        st.success(f"Based on your budget, you can afford houses in the **{target_bin} Juta** price range.")

        found_any = False
        for (loc, btype), summary_df in type_price_summaries.items():
            loc_match = (selected_location == "All Locations" or loc.lower() == selected_location.lower())
            type_match = (selected_type == "All Types" or btype.lower() == selected_type.lower())
            if loc_match and type_match and target_bin in summary_df.index:
                found_any = True
                st.write(f"#### {btype} - {loc}")
                st.dataframe(summary_df.loc[[target_bin]])

        if not found_any:
            st.warning("Sorry, no data available for your budget, location, and selected property type.")
    else:
        st.info("Please enter your annual spare money to see property suggestions.")
