import asyncio
import httpx
import json

async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=20)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"❌ Lỗi khi gọi API: {e}")
            return None

async def fetch_all_data(base_url):
    all_items = []
    page = 1

    while True:
        url = f"{base_url}?page={page}"
        print(f"🔄 Đang lấy dữ liệu từ trang {page}...")
        data = await fetch_data(url)

        if not data or not data.get("items"):
            print("⚠️ Không có dữ liệu trả về, kết thúc.")
            break

        total_pages = data.get("pagination", {}).get("totalPages", 1)
        all_items.extend(data["items"])

        if page >= total_pages:
            print("✅ Đã lấy hết tất cả các trang.")
            break

        page += 1

    print(f"✅ Tổng số phim lấy được: {len(all_items)}")
    return all_items

def save_to_json(items, filename="phim_moi_cap_nhat.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"📁 Đã lưu dữ liệu vào file: {filename}")

async def main():
    base_url = "https://ophim1.com/danh-sach/phim-moi-cap-nhat"
    items = await fetch_all_data(base_url)
    save_to_json(items)

if __name__ == "__main__":
    asyncio.run(main())
