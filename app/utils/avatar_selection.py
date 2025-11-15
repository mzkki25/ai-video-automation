AVATARS = [
    {
        "name": "Mas Indo",
        "voice_id": "08e816816f5f496e8757268f2e0b633a",
        "talking_photo_id": "76db764087a14ff683b6964c6ca62537",
        "avatar_url": "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/mas_indo.jpg"
    },
    {
        "name": "Ci Chindo",
        "voice_id": "d7d6ae6ac0f64d1a9b1a8b26760096eb",
        "talking_photo_id": "cae19979cd0e4203b2bcc702eaead13d",
        "avatar_url": "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/ci_chindo.jpg"
    },
    {
        "name": "Ko Chindo",
        "voice_id": "5df1a994b0ae425dbe7f71c6d8dd2563",
        "talking_photo_id": "ea33ba36a756400e8f9c131f955cd6b8",
        "avatar_url": "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/ko_chindo.png"
    },
    {
        "name": "Mba Indo",
        "voice_id": "1b81540177114ec4bfda2a7a514e0e6b",
        "talking_photo_id": "8183274ca6d947aa8c9ba7ccd5f3fdea",
        "avatar_url": "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/mba_indo.jpg"
    }
]

def get_all_avatars():
    return AVATARS

def avatar_selection(avatar_name):
    for avatar in AVATARS:
        if avatar["name"] == avatar_name:
            return avatar
    return None
        