# Iteration One
auth_register_test assumptions: 
- clear_v1 function is working

channels_listall_v1_test assumptions: 
- clear_v1 function is working
- channels_create_v1 function is working
- auth_register_v1 function is working
- assumed empty fields do not occur

auth_register_v1 assumptions:
- u_id = number of users in list before appending latest user
- all input variables must be strings (throw input error otherwise, as per the types specified by the assignment)
- spaces in first_name and last_name are allowed, but it cannot all be spaces
- left and right spaces are stripped
- spaces are not allowed in passwords, except trailing and leading spaces, which are stripped
- spaces are not allowed in emails, except trailing and leading spaces, which are stripped

auth_login_v1 assumptions:
- there must be characters other than spaces in both email and password
- leading and / or trailing white space for both fields allows successful login
- other white space is not allowed

auth_register_v1 assumptions:
- registering a user automatically logs in that user

channel_invite_v1:
- list of errors are in this order:
1. AccessError if auth_user_id does not exist
2. InputError if channel_id does not exist (channel was never created)
3. AccessError if auth_user_id is not a member of the channel
4. InputError if u_id either does not exist or is already a member of the channel

channel_join_v1 assumptions:
- Owner of streams can join any channel without an invite
- Owner of streams cannot join as an owner_member, only as a normal member unless they have been invited by the channel's owner

# Iteration Two

In a DM:
- empty list of u_ids -> acceptable, user can make a dm by themselves
- global owner cannot access dm details without joining
- global owner cannot access dms messages without joining

Changing profile:
- you cannot change your handle to your current handle. This will throw an error as it is not a change.
- you cannot change your email to your current email. This will throw an error as it is not a change.
- you cannot change your name to your current name. This will throw an error as it is not a change.



# Iteration Three
messages/sendlater assumptions:
- User will not log out after queuing a message or dm via message_sendlater

standup/start assumptions:
- User will not log out after beginning a standup

search assumptions:
- Search is case insensitive (i.e. searching for Dog will yield i.e. dog, Dog, dOg, doG)