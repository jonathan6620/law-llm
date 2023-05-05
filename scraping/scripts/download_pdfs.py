import httpx
import asyncio
from typing import List
import nest_asyncio

nest_asyncio.apply()

base_url = 'https://www.legislation.gov.uk/ukpga/'
output_dir = 'pdfs/'
timeout = 100

async def fetch_data(url: str, timeout: float = 10.0):
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            return response
    except httpx.ReadTimeout:
        print(f'exceed timeout of {timeout} for url: {url}')
        return None
        
        
async def download_data(urls: List[str]):
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch_data(url))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    
    
async def write_response_to_pdf(response: httpx.Response, destination: str):
    with open(destination, "wb") as fp:
        fp.write(response.content)
    return 


for year in range(1980, 2024):
    for index in range(1, 100):
        query = f'{base_url}{year}/{index}/data.pdf'
        destination = f'{output_dir}/uk-gov-bill-{year}-{index}.pdf'
        result = asyncio.run(fetch_data(query, timeout))

        if result is None or result.status_code == 404:
            continue
        
        print(f'Writing: {query}')
        asyncio.run(write_response_to_pdf(result, destination))
