> Note: Small updates are not included 

**⛏️ Snapshot**: Testing versions, very rare \
**⚒️ Alpha**: Things are subject to break. An experimental version \
**✨ Beta**: Stuffs are still unstable and needs further feedbacks and works \
**🚀 Pre-Release**: Preparing to make a release, needs testing and even more feedback \
**⭐ Release**: The stable version, everything is working fine. It *could* contain bugs but it shouldn't

# ⛏️ v1.3.10x-SNAPSHOTS | Snapshots
- Fix many bugs
- Make some small changes to match the pycord documentation
- Test many upcoming features

# 🚀 v1.3.9 | Pre-Release
- Make a command group `msgcount` and make these features grouped to it:
    - `guide`, explain what is message count feature and how to set it up
    - `toggle`, turn message count feature on/off (off by default)
    - `get`, renamed from `/staff_message_count`
    - `delete`, delete the message count data of your server
- Add description to slash command parameters
- Update README.md outdated information
- Preparing for the 3rd release

# ⚒️ v1.3.8 | Alpha
- Experimental version of the third release. Things are still in progress and might break.

# ✨ v1.3.2 | Beta
- Fix the `/staff_message_count` command, now required mention everyone permission is on (as the command pings the users)

# ✨ v1.3.1 | Beta
- Fix some small, important bugs

# ✨ v1.3.0 | Beta
- Update & fix the MongoDB functions
- Add custom exceptions for my code
- Fix a small bug in the MongoDB functions
- New slash commend (exclusive feature, only available for 1 of my server): `/staff_message_count`, returns how many messages the staffs sent in the past week

# ⭐ v1.2.0 | Release 
- Add MongoDB functions (to help people that remix the project)
- Update README
- New slash command: `/guess_the_number`, everything in the name and default guess range is 1-10

# ⭐ v1.0.0 | Release
*This is written after it's released, may contain misinformation*
- Becomes a major version as everything is tested and working perfectly. This is the first release yay!. From now on, every feature needs to be tested before the release.
- Bot renamed and redesigned to "MicroMightyBot"

- Adds connection to MongoDB
- Fix bugs
- Rename `/roll_dice` to `/roll_a_dice`
- Rename `/roll_dice_custom` to `/roll_custom_dice`

# 🚀 v0.3.0 | Pre-Release
*This is written after it's released, may contain misinformation*
- Add basic setup for the bot
- New slash command: `/roll`, this returns a random number from 1-6
- New slash command: `/roll_custom`, this returns a random number from a custom range