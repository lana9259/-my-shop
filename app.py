import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="فروشگاه من", layout="wide")

st.markdown("""
<style>
body { direction: rtl; }
.product-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🛍️ فروشگاه من")

if "products" not in st.session_state:
    st.session_state.products = []

tab1, tab2 = st.tabs(["🔍 جستجو و خرید", "➕ اضافه کردن محصول"])

with tab2:
    st.subheader("اضافه کردن محصول جدید")
    name = st.text_input("نام محصول")
    price = st.number_input("قیمت (تومان)", min_value=0, step=1000)
    image_url = st.text_input("لینک عکس محصول")
    description = st.text_area("توضیحات محصول")
    buy_link = st.text_input("لینک خرید")

    if st.button("اضافه کردن"):
        if name and price and image_url:
            st.session_state.products.append({
                "name": name,
                "price": price,
                "image_url": image_url,
                "description": description,
                "buy_link": buy_link
            })
            st.success(f"محصول {name} اضافه شد!")
        else:
            st.error("لطفاً نام، قیمت و لینک عکس را وارد کنید")

with tab1:
    search = st.text_input("🔍 جستجوی محصول...")

    if st.session_state.products:
        filtered = [p for p in st.session_state.products
                   if search.lower() in p["name"].lower()] if search else st.session_state.products

        if filtered:
            cols = st.columns(3)
            for i, product in enumerate(filtered):
                with cols[i % 3]:
                    try:
                        response = requests.get(product["image_url"], timeout=5)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, use_column_width=True)
                    except:
                        st.image("https://via.placeholder.com/300", use_column_width=True)

                    st.markdown(f"**{product['name']}**")
                    st.markdown(f"💰 {product['price']:,} تومان")
                    st.markdown(f"{product['description']}")
                    if product['buy_link']:
                        st.markdown(f"[🛒 خرید]({product['buy_link']})")
                    st.markdown("---")
        else:
            st.info("محصولی یافت نشد")
    else:
        st.info("هنوز محصولی اضافه نشده. از تب بالا محصول اضافه کنید")
