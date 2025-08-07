#!/usr/bin/env python3

import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/test_user"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Listen for initial connection message
            initial_msg = await websocket.recv()
            print(f"📨 Initial message: {initial_msg}")
            
            # Send story generation request
            test_request = {
                "type": "generate_story",
                "data": "dragon, castle, magic"
            }
            
            print(f"🚀 Sending request: {test_request}")
            await websocket.send(json.dumps(test_request))
            
            # Listen for responses
            print("\n📡 Waiting for responses...")
            timeout_counter = 0
            
            while timeout_counter < 30:  # 30 second timeout
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    print(f"📨 Response: {response}")
                    
                    # Parse and analyze the response
                    try:
                        parsed = json.loads(response)
                        msg_type = parsed.get("type")
                        
                        if msg_type == "story_complete":
                            print(f"✅ STORY RECEIVED! Length: {len(parsed.get('data', ''))}")
                            print(f"📖 Story preview: {parsed.get('data', '')[:100]}...")
                        elif msg_type == "turn_complete":
                            print("✅ Turn completed, breaking...")
                            break
                        elif msg_type == "error":
                            print(f"❌ Error: {parsed.get('message')}")
                            break
                            
                    except json.JSONDecodeError:
                        print(f"⚠️  Non-JSON response: {response}")
                        
                except asyncio.TimeoutError:
                    timeout_counter += 1
                    print(f"⏱️  Waiting... ({timeout_counter}/30)")
                    
            print("\n🏁 Test completed")
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket()) 