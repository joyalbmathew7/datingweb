# Dating App

## Authentication
POST /api/v1/auth/register/
POST /api/v1/auth/login/
POST /api/v1/auth/refresh/
GET  /api/v1/auth/me/

## Profiles
POST  /api/v1/profiles/
GET   /api/v1/profiles/me/
PATCH /api/v1/profiles/me/

## Discovery
GET /api/v1/discovery/

Filters:
- gender
- interested_in
- relationship_status
- country
- state
- city

## Interactions
POST /api/v1/interactions/
Actions:
- LIKE
- PASS
- UNLIKE

## Matches
GET /api/v1/interactions/matches/

## Chat
GET  /api/v1/chats/
GET  /api/v1/chats/<conversation_uuid>/messages/
POST /api/v1/chats/<conversation_uuid>/messages/

## Block
POST /api/v1/interactions/block/
POST /api/v1/interactions/unblock/

Behavior:
- Conversation remains after blocking
- Old messages remain
- New messages are blocked
- Unblocking allows messaging again

## Future
- Notifications
- WebSockets / real-time chat
- Images
- Audio
- Video



------------------------------------------------------------------------------

I am building a dating app.

TECH STACK
- Backend: Django 6.0.7 + Django REST Framework
- Authentication: JWT
- Frontend: React (planned/being built)
- Database: SQLite for development

CURRENT DJANGO APPS
- accounts
- profiles
- locations
- common
- discovery
- interactions
- matches
- chats

COMPLETED FEATURES
1. Authentication / JWT
2. User profiles
3. Profile photos
4. Discovery
5. Gender/interested_in/location filters
6. Randomized discovery ordering
7. LIKE
8. PASS
9. UNLIKE
10. Automatic mutual LIKE → Match
11. Match list
12. Conversations
13. Text messages
14. Block / Unblock

CHAT DESIGN
Match
  ↓
Conversation (OneToOne with Match)
  ↓
Message (ForeignKey to Conversation)

IMPORTANT BLOCK BEHAVIOR
- Blocking does NOT delete the conversation.
- Blocking does NOT delete old messages.
- Existing chat history remains visible.
- Blocked users cannot send new messages.
- Unblocking allows messaging again.
- This rule must also work with WebSockets.

CURRENT TASK
We are implementing WebSocket chat using Django Channels.

Channels has been installed/configured.
settings.py has:
    "channels"
and:
    ASGI_APPLICATION = "config.asgi.application"

config/asgi.py already exists and currently contains the normal Django ASGI setup.

NEXT STEP
Continue from here.
Do NOT rebuild the completed features.
Next, configure Django Channels/WebSocket routing and create the chat consumer.
Keep the project simple and explain each step because I understand the project flow/logic better than detailed coding.