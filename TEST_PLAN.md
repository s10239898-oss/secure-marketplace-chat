# 🔍 Socket.IO Room Fix - Test Plan

## 🎯 Objective
Verify that deterministic room naming fixes bidirectional communication between buyers and sellers.

## 🧪 Test Scenarios

### 1. Room Naming Determinism Test
**Goal**: Verify both users always join the same room regardless of who joins first

**Steps**:
1. Start the application: `python app.py`
2. Open two browser tabs
3. Tab 1: Login as `buyer1`, select `seller1`, click chat
4. Tab 2: Login as `seller1`, select `buyer1`, click chat
5. Check server logs for room names
6. **Expected**: Both users join the same room: `buyer1_seller1`

**Reverse Order Test**:
1. Tab 1: Login as `seller1`, select `buyer1`, click chat
2. Tab 2: Login as `buyer1`, select `seller1`, click chat
3. **Expected**: Same room name: `buyer1_seller1`

### 2. Bidirectional Message Test
**Goal**: Verify both users receive messages

**Steps**:
1. Both users join the same chat room
2. Buyer sends: "Hello seller"
3. **Expected**: 
   - Buyer sees their own message
   - Seller receives buyer's message
   - AI replies to both users
4. Seller sends: "Hello buyer"
5. **Expected**:
   - Seller sees their own message
   - Buyer receives seller's message
   - No AI reply (seller to buyer doesn't trigger AI)

### 3. AI Response Visibility Test
**Goal**: Verify AI replies appear for both users

**Steps**:
1. Buyer sends message to seller
2. **Expected**:
   - Buyer sees AI reply
   - Seller sees AI reply
   - AI reply marked with `is_ai: true`

### 4. Room Membership Debug Test
**Goal**: Verify debug logging shows correct room membership

**Steps**:
1. Monitor server console logs
2. Join multiple users to different rooms
3. **Expected**: 
   - Room membership logs show correct users
   - No duplicate room entries
   - Clean disconnect handling

### 5. Reconnection Test
**Goal**: Verify reconnection doesn't create duplicate rooms

**Steps**:
1. User joins chat room
2. Refresh browser (reconnect)
3. **Expected**:
   - User rejoins same room
   - No duplicate room entries
   - Chat history loads correctly

## 🔍 Debug Log Analysis

### Expected Log Patterns
```
🔗 Client connected: [SID]
🔐 Login attempt: buyer1
✅ Login successful: buyer1 (SID: [SID])
🚪 buyer1 wants to join chat with seller1
✅ buyer1 joined room: buyer1_seller1
📚 Sent chat history for buyer1 <-> seller1
🏠 ROOM MEMBERSHIP DEBUG:
  Room 'buyer1_seller1': 2 clients
👤 ACTIVE USERS: ['buyer1', 'seller1']
🔗 USER-ROOMS: {'buyer1': ['buyer1_seller1'], 'seller1': ['buyer1_seller1']}
```

### Message Flow Logs
```
💬 Message: buyer1 -> seller1: 'Hello seller'
🏠 Sending to room: buyer1_seller1
✅ Message saved to database
📤 Message emitted to room: buyer1_seller1
🤖 Generating AI response for seller1
✅ AI response generated: 'Hello! How can I help you today?'
📤 AI response emitted to room: buyer1_seller1
```

## 🚀 Production Tests

### 1. Systemd Service Test
**Steps**:
```bash
# Check service status
sudo systemctl status secure-chat

# Check logs
sudo journalctl -u secure-chat -f

# Restart service
sudo systemctl restart secure-chat
```

**Expected**: Service starts without errors, logs show proper room handling

### 2. Tor Hidden Service Test
**Steps**:
1. Access via Tor hidden service URL
2. Test chat functionality through Tor
3. **Expected**: All features work through Tor

### 3. Load Test
**Steps**:
1. Multiple simultaneous users (5+ buyers + 5+ sellers)
2. Concurrent messaging
3. **Expected**: No room conflicts, all messages delivered

## 🐛 Common Issues & Solutions

### Issue: Users in different rooms
**Symptoms**: 
- Messages not received
- AI replies only visible to one user

**Debug Check**:
```bash
# Look for these logs
🏠 ROOM MEMBERSHIP DEBUG:
  Room 'buyer1_seller1': 1 client  # Should be 2
  Room 'seller1_buyer1': 1 client  # Should not exist
```

**Solution**: Verify deterministic room naming is working

### Issue: Duplicate room joins
**Symptoms**:
- Multiple room entries for same user
- Message duplication

**Debug Check**:
```bash
ℹ️ buyer1 already in room: buyer1_seller1
```

**Solution**: Reconnection handling is working

### Issue: AI not responding
**Symptoms**:
- No AI replies
- AI error messages

**Debug Check**:
```bash
❌ AI response error: [error details]
```

**Solution**: Check API key and model configuration

## ✅ Success Criteria

### Must Pass
- [ ] Both users always join same room (`buyer1_seller1`)
- [ ] Bidirectional messaging works
- [ ] AI replies visible to both users
- [ ] No duplicate room creation
- [ ] Clean reconnection handling
- [ ] Debug logs show correct state

### Should Pass
- [ ] Systemd service runs without errors
- [ ] Tor hidden service works
- [ ] Multiple concurrent users work
- [ ] Message persistence works

## 🔧 Troubleshooting Commands

### Check Room State
```python
# Add temporary debug endpoint
@app.route("/debug/rooms")
def debug_rooms():
    rooms = {}
    for room_name, members in socketio.server.manager.get_rooms().items():
        if room_name not in ['__default__']:
            rooms[room_name] = len(members)
    return jsonify({
        "rooms": rooms,
        "active_users": list(active_users.keys()),
        "user_rooms": user_rooms
    })
```

### Manual Room Test
```javascript
// Browser console test
socket.emit('join_chat', {username: 'buyer1', partner: 'seller1'});
socket.emit('send_message', {sender: 'buyer1', receiver: 'seller1', message: 'test'});
```

## 📊 Performance Monitoring

### Key Metrics
- Room creation rate
- Message delivery latency
- Concurrent users per room
- Reconnection frequency

### Monitoring Commands
```bash
# Monitor Socket.IO connections
watch -n 1 "curl http://localhost:5001/debug/rooms"

# Monitor system resources
htop
iostat -x 1
```

## 🎉 Final Verification

After all tests pass:
1. Deploy to production
2. Monitor for 24 hours
3. Check system logs for any room conflicts
4. Verify user experience is smooth

The deterministic room naming should completely eliminate the one-sided communication issue.
