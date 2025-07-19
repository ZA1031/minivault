import requests
import argparse
import sys

API_URL = "http://localhost:8000"

def send_prompt(prompt: str):
    try:
        response = requests.post(f"{API_URL}/generate", json={"prompt": prompt})
        if response.status_code == 200:
            data = response.json()
            print(f"\n🧠 Response:\n{data['response']}")
        else:
            print(f"❌ Error {response.status_code}:\n{response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to the API. Is the server running?")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def check_status():
    try:
        response = requests.get(f"{API_URL}/status")
        if response.status_code == 200:
            print("\n📊 System Status:")
            for k, v in response.json().items():
                print(f"  {k}: {v}")
        else:
            print(f"❌ Error {response.status_code}:\n{response.text}")
    except Exception as e:
        print(f"❌ Failed to get status: {e}")
        sys.exit(1)

def main():  # ✅ Add this
    parser = argparse.ArgumentParser(description="MiniVault CLI")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--prompt",
        type=str,
        help="Prompt to send to the local MiniVault API"
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Check system status (memory, uptime, GPU)"
    )

    args = parser.parse_args()

    if args.status:
        check_status()
    else:
        send_prompt(args.prompt)

if __name__ == "__main__":
    main()
