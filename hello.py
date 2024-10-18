import aiohttp
import asyncio
from faker import Faker

# Initialize the Faker instance
fake = Faker()

# Define the URL where requests will be sent
URL = 'http://localhost:8000/api/submit/'  # Change to your actual endpoint

async def send_request(session):
    # Generate fake data
    username = fake.user_name()
    email = fake.email()
    password = fake.password()

    # Create the payload
    payload = {
        'username': username,
        'email': email,
        'password': password,
    }

    async with session.post(URL, json=payload) as response:
        # Print the response status (you can handle the response further if needed)
        print(f'Sent: {payload} | Response: {response.status}')

async def main():
    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks for sending requests
        tasks = [send_request(session) for _ in range(100000)]
        
        # Use asyncio.gather to run tasks concurrently
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
