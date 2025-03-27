import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from crawl4ai import AsyncWebCrawler

#SITEMAP_URL = "http://www.tranglo.com/page-sitemap.xml" from https://www.tranglo.com/sitemap_index.xml
SITEMAP_URL = "http://www.tranglo.com/category-sitemap.xml"
OUTPUT_FILE = "tranglo_category.txt"

def extract_sitemap_urls(sitemap_content):
    """Extract URLs from sitemap XML content."""
    root = ET.fromstring(sitemap_content)
    return [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]

async def fetch_sitemap():
    """Fetch sitemap content."""
    async with aiohttp.ClientSession() as session:
        async with session.get(SITEMAP_URL) as response:
            return await response.text()

async def crawl_urls(urls):
    """Crawl each URL and save content."""
    async with AsyncWebCrawler() as crawler:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for url in urls:
                print(f"Crawling: {url}")
                result = await crawler.arun(url)
                f.write(f"URL: {url}\n\n")
                f.write(result.markdown + "\n\n" + "="*80 + "\n\n")

async def main():
    print("Fetching sitemap...")
    sitemap_content = await fetch_sitemap()
    urls = extract_sitemap_urls(sitemap_content)
    print(f"Found {len(urls)} URLs.")
    await crawl_urls(urls)
    print("Crawling complete. Output saved")

if __name__ == "__main__":
    asyncio.run(main())
