import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64
import json
import uuid

st.set_page_config(page_title="فروشگاه من", layout="wide", page_icon="🛍️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Vazirmatn', sans-serif !important; direction: rtl; }

body { background: #f8f9ff; }

.main { padding: 0 !important; }

/* Header */
.shop-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
    border-radius: 0 0 30px 30px;
}
.shop-header h1 { font-size: 2.5rem; font-weight: 800; margin: 0; }
.shop-header p { font-size: 1rem; opacity: 0.85; margin: 0.5rem 0 0; }

/* Product Card */
.product-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    margin-bottom: 1.5rem;
    border: 1px solid #f0f0f0;
}
.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(102,126,234,0.2);
}
.product-img-container {
    width: 100%;
    height: 220px;
    overflow: hidden;
    background: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
}
.product-img-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.product-info {
    padding: 1rem;
}
.product-name {
    font-size: 1rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 0.3rem;
    line-height: 1.4;
}
.product-desc {
    font-size: 0.8rem;
    color: #666;
    margin-bottom: 0.8rem;
    line-height: 1.6;
}
.product-price {
    font-size: 1.2rem;
    font-weight: 800;
    color: #667eea;
    margin-bottom: 1rem;
}
.product-category {
    background: #f0f0ff;
    color: #667eea;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 0.8rem;
}
.btn-buy {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white !important;
    padding: 0.5rem 1.2rem;
    border-radius: 25px;
    text-decoration: none !important;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
    transition: opacity 0.2s;
}
.btn-buy:hover { opacity: 0.85; }

/* Stats bar */
.stats-bar {
    background: white;
    border-radius: 16px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    display: flex;
    gap: 2rem;
    align-items: center;
    flex-wrap: wrap;
}
.stat-item {
    text-align: center;
}
.stat-number { font-size: 1.5rem; font-weight: 800; color: #667eea; }
.stat-label { font-size: 0.75rem; color: #888; }

/* Form styling */
.form-container {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

/* Search bar */
.search-container {
    background: white;
    border-radius: 16px;
    padding: 1rem 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 1.5rem;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #aaa;
}
.empty-state .icon { font-size: 4rem; margin-bottom: 1rem; }
.empty-state h3 { color: #888; font-weight: 600; }

/* Edit/Delete buttons */
.action-btn {
    border: none;
    padding: 4px 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 4px;
}

/* Badge */
.badge-new {
    background: #ff6b6b;
    color: white;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 700;
    margin-right: 5px;
}

/* Tab customization */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: white;
    padding: 8px;
    border-radius: 16px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
}

/* Divider */
.section-divider {
    border: none;
    border-top: 2px solid #f0f0f0;
    margin: 1.5rem 0;
}

.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Vazirmatn', sans-serif !important;
}

.success-msg {
    background: #e8f5e9;
    border-right: 4px solid #4caf50;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    color: #2e7d32;
    font-weight: 600;
    margin: 0.5rem 0;
}
.error-msg {
    background: #ffebee;
    border-right: 4px solid #f44336;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    color: #c62828;
    font-weight: 600;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Initialize Session State ──────────────────────────────────────────────
if "products" not in st.session_state:
    st.session_state.products = []
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None
if "view_product" not in st.session_state:
    st.session_state.view_product = None

# ─── Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="shop-header">
    <h1>🛍️ فروشگاه من</h1>
    <p>بهترین محصولات با بهترین قیمت</p>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 فروشگاه", "➕ افزودن محصول", "⚙️ مدیریت محصولات"])

# ══════════════════════════════════════════════════════════════════
#  TAB 1: SHOP / SEARCH
# ══════════════════════════════════════════════════════════════════
with tab1:

    # Stats
    total = len(st.session_state.products)
    categories = list(set(p.get("category","") for p in st.session_state.products if p.get("category","")))
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown(f"""<div style="text-align:center;background:white;padding:1rem;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:1.8rem;font-weight:800;color:#667eea">{total}</div>
        <div style="font-size:0.8rem;color:#888">محصول</div></div>""", unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""<div style="text-align:center;background:white;padding:1rem;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:1.8rem;font-weight:800;color:#667eea">{len(categories)}</div>
        <div style="font-size:0.8rem;color:#888">دسته‌بندی</div></div>""", unsafe_allow_html=True)
    with col_s3:
        avg_price = int(sum(p.get("price",0) for p in st.session_state.products)/total) if total else 0
        st.markdown(f"""<div style="text-align:center;background:white;padding:1rem;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:1.8rem;font-weight:800;color:#667eea">{avg_price:,}</div>
        <div style="font-size:0.8rem;color:#888">میانگین قیمت (تومان)</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Search & Filter
    col_search, col_filter, col_sort = st.columns([3, 1.5, 1.5])
    with col_search:
        search = st.text_input("", placeholder="🔍 جستجوی محصول...", label_visibility="collapsed")
    with col_filter:
        all_cats = ["همه دسته‌ها"] + list(set(p.get("category","سایر") for p in st.session_state.products))
        cat_filter = st.selectbox("", all_cats, label_visibility="collapsed")
    with col_sort:
        sort_by = st.selectbox("", ["جدیدترین", "ارزان‌ترین", "گران‌ترین"], label_visibility="collapsed")

    # Filter products
    filtered = st.session_state.products.copy()
    if search:
        filtered = [p for p in filtered if search.lower() in p["name"].lower() or search.lower() in p.get("description","").lower()]
    if cat_filter != "همه دسته‌ها":
        filtered = [p for p in filtered if p.get("category","سایر") == cat_filter]
    if sort_by == "ارزان‌ترین":
        filtered = sorted(filtered, key=lambda x: x.get("price",0))
    elif sort_by == "گران‌ترین":
        filtered = sorted(filtered, key=lambda x: x.get("price",0), reverse=True)
    else:
        filtered = list(reversed(filtered))

    st.markdown(f"<p style='color:#888;font-size:0.85rem;margin-bottom:1rem'>{len(filtered)} محصول یافت شد</p>", unsafe_allow_html=True)

    if not st.session_state.products:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🛍️</div>
            <h3>هنوز محصولی اضافه نشده</h3>
            <p>از تب «افزودن محصول» شروع کنید</p>
        </div>
        """, unsafe_allow_html=True)
    elif not filtered:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🔍</div>
            <h3>محصولی یافت نشد</h3>
            <p>عبارت جستجو یا فیلتر را تغییر دهید</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, product in enumerate(filtered):
            with cols[i % 3]:
                # Image
                img_html = ""
                if product.get("image_data"):
                    img_html = f'<img src="data:image/jpeg;base64,{product["image_data"]}" style="width:100%;height:220px;object-fit:cover">'
                elif product.get("image_url"):
                    img_html = f'<img src="{product["image_url"]}" style="width:100%;height:220px;object-fit:cover" onerror="this.src=\'https://via.placeholder.com/400x220?text=No+Image\'">'
                else:
                    img_html = '<div style="width:100%;height:220px;background:#f0f0ff;display:flex;align-items:center;justify-content:center;font-size:3rem">🛍️</div>'

                discount_badge = ""
                if product.get("original_price") and product["original_price"] > product["price"]:
                    pct = int((1 - product["price"]/product["original_price"])*100)
                    discount_badge = f'<span class="badge-new">%{pct} تخفیف</span>'

                buy_btn = ""
                if product.get("buy_link"):
                    buy_btn = f'<a href="{product["buy_link"]}" target="_blank" class="btn-buy">🛒 خرید</a>'

                original_price_html = ""
                if product.get("original_price") and product["original_price"] > product["price"]:
                    original_price_html = f'<span style="text-decoration:line-through;color:#aaa;font-size:0.85rem;margin-right:8px">{int(product["original_price"]):,}</span>'

                st.markdown(f"""
                <div class="product-card">
                    <div style="position:relative">
                        {img_html}
                        <div style="position:absolute;top:10px;right:10px">{discount_badge}</div>
                    </div>
                    <div class="product-info">
                        <div class="product-category">{product.get("category","سایر")}</div>
                        <div class="product-name">{product["name"]}</div>
                        <div class="product-desc">{product.get("description","")[:80]}{"..." if len(product.get("description",""))>80 else ""}</div>
                        <div class="product-price">{original_price_html}{int(product["price"]):,} تومان</div>
                        {buy_btn}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 2: ADD PRODUCT
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown("### ➕ افزودن محصول جدید")
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        name = st.text_input("نام محصول *", placeholder="مثال: پیراهن کتان سفید")
        price = st.number_input("قیمت (تومان) *", min_value=0, step=10000, format="%d")
        original_price = st.number_input("قیمت قبل از تخفیف (اختیاری)", min_value=0, step=10000, format="%d",
                                          help="اگر محصول تخفیف دارد، قیمت اصلی را اینجا بنویسید")
        category = st.selectbox("دسته‌بندی *", ["پوشاک زنانه", "پوشاک مردانه", "پوشاک بچگانه",
                                                  "کفش و کیف", "اکسسوری", "ورزشی", "سایر"])

    with col_f2:
        description = st.text_area("توضیحات محصول", placeholder="ویژگی‌های محصول را بنویسید...", height=120)
        buy_link = st.text_input("لینک خرید (اختیاری)", placeholder="https://...")
        stock = st.number_input("موجودی انبار", min_value=0, step=1, value=10)

    st.markdown("#### 📷 تصویر محصول")
    img_method = st.radio("روش افزودن تصویر:", ["آپلود از گوشی/کامپیوتر", "لینک تصویر از اینترنت"], horizontal=True)

    image_data = None
    image_url = ""

    if img_method == "آپلود از گوشی/کامپیوتر":
        uploaded = st.file_uploader("تصویر محصول را انتخاب کنید", type=["jpg","jpeg","png","webp"])
        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            img.thumbnail((800, 800))
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=85)
            image_data = base64.b64encode(buf.getvalue()).decode()
            st.image(img, caption="پیش‌نمایش تصویر", width=250)
    else:
        image_url = st.text_input("لینک تصویر", placeholder="https://example.com/image.jpg")
        if image_url:
            try:
                st.image(image_url, caption="پیش‌نمایش", width=250)
            except:
                st.warning("تصویر قابل نمایش نیست")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1,3])
    with col_btn1:
        if st.button("✅ افزودن محصول", type="primary", use_container_width=True):
            if not name:
                st.markdown('<div class="error-msg">❌ نام محصول را وارد کنید</div>', unsafe_allow_html=True)
            elif price <= 0:
                st.markdown('<div class="error-msg">❌ قیمت را وارد کنید</div>', unsafe_allow_html=True)
            elif not image_data and not image_url:
                st.markdown('<div class="error-msg">❌ تصویر محصول را اضافه کنید</div>', unsafe_allow_html=True)
            else:
                new_product = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "price": price,
                    "original_price": original_price if original_price > 0 else None,
                    "category": category,
                    "description": description,
                    "buy_link": buy_link,
                    "stock": stock,
                    "image_data": image_data,
                    "image_url": image_url
                }
                st.session_state.products.append(new_product)
                st.markdown(f'<div class="success-msg">✅ محصول «{name}» با موفقیت اضافه شد!</div>', unsafe_allow_html=True)
                st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  TAB 3: MANAGE PRODUCTS
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### ⚙️ مدیریت محصولات")

    if not st.session_state.products:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📦</div>
            <h3>محصولی برای مدیریت وجود ندارد</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Edit mode
        if st.session_state.editing_id:
            product = next((p for p in st.session_state.products if p["id"] == st.session_state.editing_id), None)
            if product:
                st.markdown(f"#### ✏️ ویرایش: {product['name']}")
                st.markdown('<div class="form-container">', unsafe_allow_html=True)

                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    e_name = st.text_input("نام محصول", value=product["name"], key="e_name")
                    e_price = st.number_input("قیمت (تومان)", value=int(product["price"]), step=10000, key="e_price")
                    e_orig = st.number_input("قیمت قبل از تخفیف", value=int(product.get("original_price") or 0), step=10000, key="e_orig")
                    e_cat = st.selectbox("دسته‌بندی", ["پوشاک زنانه", "پوشاک مردانه", "پوشاک بچگانه",
                                                        "کفش و کیف", "اکسسوری", "ورزشی", "سایر"],
                                         index=["پوشاک زنانه","پوشاک مردانه","پوشاک بچگانه",
                                                "کفش و کیف","اکسسوری","ورزشی","سایر"].index(product.get("category","سایر")), key="e_cat")
                with col_e2:
                    e_desc = st.text_area("توضیحات", value=product.get("description",""), key="e_desc")
                    e_link = st.text_input("لینک خرید", value=product.get("buy_link",""), key="e_link")
                    e_stock = st.number_input("موجودی", value=int(product.get("stock",0)), key="e_stock")

                e_img_url = st.text_input("لینک تصویر جدید (اختیاری)", value=product.get("image_url",""), key="e_img")
                e_upload = st.file_uploader("یا تصویر جدید آپلود کنید", type=["jpg","jpeg","png","webp"], key="e_upload")

                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("💾 ذخیره تغییرات", type="primary", use_container_width=True):
                        idx = next(i for i, p in enumerate(st.session_state.products) if p["id"] == st.session_state.editing_id)
                        st.session_state.products[idx]["name"] = e_name
                        st.session_state.products[idx]["price"] = e_price
                        st.session_state.products[idx]["original_price"] = e_orig if e_orig > 0 else None
                        st.session_state.products[idx]["category"] = e_cat
                        st.session_state.products[idx]["description"] = e_desc
                        st.session_state.products[idx]["buy_link"] = e_link
                        st.session_state.products[idx]["stock"] = e_stock
                        if e_upload:
                            img = Image.open(e_upload).convert("RGB")
                            img.thumbnail((800,800))
                            buf = BytesIO()
                            img.save(buf, format="JPEG", quality=85)
                            st.session_state.products[idx]["image_data"] = base64.b64encode(buf.getvalue()).decode()
                            st.session_state.products[idx]["image_url"] = ""
                        elif e_img_url:
                            st.session_state.products[idx]["image_url"] = e_img_url
                            st.session_state.products[idx]["image_data"] = None
                        st.session_state.editing_id = None
                        st.success("✅ تغییرات ذخیره شد")
                        st.rerun()
                with col_cancel:
                    if st.button("❌ انصراف", use_container_width=True):
                        st.session_state.editing_id = None
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

        else:
            # Product list table
            for product in reversed(st.session_state.products):
                col_img, col_info, col_actions = st.columns([1, 4, 2])

                with col_img:
                    if product.get("image_data"):
                        st.markdown(f'<img src="data:image/jpeg;base64,{product["image_data"]}" style="width:80px;height:80px;object-fit:cover;border-radius:10px">', unsafe_allow_html=True)
                    elif product.get("image_url"):
                        st.markdown(f'<img src="{product["image_url"]}" style="width:80px;height:80px;object-fit:cover;border-radius:10px" onerror="this.src=\'https://via.placeholder.com/80\'">', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="width:80px;height:80px;background:#f0f0ff;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:2rem">🛍️</div>', unsafe_allow_html=True)

                with col_info:
                    st.markdown(f"**{product['name']}**")
                    st.markdown(f"<span style='color:#667eea;font-weight:700'>{int(product['price']):,} تومان</span> &nbsp;|&nbsp; <span style='color:#888'>{product.get('category','')}</span> &nbsp;|&nbsp; موجودی: {product.get('stock',0)}", unsafe_allow_html=True)
                    if product.get("description"):
                        st.markdown(f"<span style='color:#aaa;font-size:0.8rem'>{product['description'][:60]}...</span>", unsafe_allow_html=True)

                with col_actions:
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("✏️ ویرایش", key=f"edit_{product['id']}", use_container_width=True):
                            st.session_state.editing_id = product["id"]
                            st.rerun()
                    with col_del:
                        if st.button("🗑️ حذف", key=f"del_{product['id']}", use_container_width=True):
                            st.session_state.products = [p for p in st.session_state.products if p["id"] != product["id"]]
                            st.rerun()

                st.markdown('<hr style="border:1px solid #f0f0f0;margin:0.5rem 0">', unsafe_allow_html=True)

        # Bulk actions
        if st.session_state.products and not st.session_state.editing_id:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ حذف همه محصولات", type="secondary"):
                st.session_state.products = []
                st.rerun()
