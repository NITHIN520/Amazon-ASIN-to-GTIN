# 🔍 UPC / GTIN Crawler

> **Automated GTIN extraction from Amazon product pages — Purpose-built to eliminate manual barcode mapping.**

---

## 🧩 The Problem It Solves

Previously, mapping GTINs (Global Trade Item Numbers / UPC barcodes) between a **retailer's product catalog** and a **client's product data** was a fully manual process:

- Analysts had to open each retailer product page one by one
- Cross-reference the product's **name**, **image**, and **details** against the client's data
- Manually identify and record the matching GTIN

This was **time-consuming, error-prone, and unscalable** — especially across thousands of products.

---

## ⚡ What This Crawler Does

This tool automates the hardest part of that workflow.

It crawls Amazon's **Product Detail Pages (PDPs)** and extracts the **UPC / GTIN** directly from the page — the same barcode that was previously being looked up manually.

The output is a clean **`Product ID ↔ GTIN`** mapping table saved to Excel.

```
product_id    →    upc_1         upc_2 (if multiple)
B09V1T3QMN         622356587587
B08N5WRWNW         195949000027
...
```

---

## 🔄 Workflow Integration

This crawler is **Step 1** in a larger automation pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   data/input.xlsx          Retailer PDPs         data/output.xlsx│
│   (ASINs / Product IDs)  ──────────────────►  (Product × GTIN) │
│                              UPC Crawler                        │
│                                   │                             │
│                                   ▼                             │
│                     ITools-GTIN-Autopilot-CIQ                   │
│               (Automated GTIN mapping & ingestion)              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

The `output.xlsx` from this crawler feeds directly into **[ITools-GTIN-Autopilot-CIQ](https://github.com/NithinG)** — a separate automation also built by me — which handles the full GTIN mapping and ingestion into the CIQ system, completely hands-free.

---

## 🛒 Supported Retailer

| Retailer | Supported |
|----------|-----------|
| **Amazon** | ✅ Full support |

> Amazon is one of the world's largest retailers, carrying virtually every major consumer product. GTINs extracted here cover a vast majority of the product universe, making this a highly effective tool for large-scale catalog operations.

---

## 🚀 How to Run

### 1. Prepare Input

Add your product ASINs to `data/input.xlsx` with a column named `product_id`:

| product_id |
|------------|
| B09V1T3QMN |
| B08N5WRWNW |

### 2. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 3. Install Dependencies *(first time only)*

```bash
.venv/bin/python3 -m pip install -r requirements.txt
.venv/bin/python3 -m playwright install chromium
```

### 4. Run

```bash
.venv/bin/python3 src/Final-Scraper.py
```

Or simply use the `RUN` shortcut file:

```bash
bash RUN
```

---

## ⚙️ How It Works

- Uses **Playwright** to launch a real Chromium browser with a **persistent session** (stored in `user_data/`) to avoid bot detection
- Simulates human-like behavior — random delays, mouse movements, page scrolling
- Extracts UPC codes using **3 extraction strategies**:
  1. Direct UPC label detection
  2. Product information table rows
  3. Detail bullets section (`#detailBullets_feature_div`)
- Automatically **saves progress every 5 products** so no data is lost on interruption
- Adds a **cooling break every 10 products** to avoid rate limiting

---

## 📁 Project Structure

```
UPC-GTIN Crawler/
├── src/
│   └── Final-Scraper.py    # Main crawler script
├── data/
│   ├── input.xlsx           # Input: ASINs to crawl
│   └── output.xlsx          # Output: Product × GTIN mapping
├── user_data/               # Persistent browser session (auto-managed)
├── .venv/                   # Python virtual environment
├── requirements.txt
└── RUN                      # One-line run command
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `playwright` | Browser automation |
| `pandas` | Excel read/write |
| `openpyxl` | Excel engine |

---

## 💡 Impact

| Before | After |
|--------|-------|
| Manual image & name comparison | Automated GTIN extraction |
| Hours per batch | Minutes per batch |
| Human error risk | Consistent & accurate |
| No downstream automation possible | Feeds directly into ITools-GTIN-Autopilot-CIQ |

---

## 👤 Author

Built by **Nithin G** as part of the CIQ product data automation suite.

---

> *This tool is purpose-built for internal catalog operations. Amazon's product pages are the source of truth for GTIN data — this crawler simply reads what's publicly displayed on the page.*
