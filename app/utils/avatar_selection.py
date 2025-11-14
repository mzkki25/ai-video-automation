def avatar_selection(avatar_name):
    if avatar_name == "Mas Indo":
        voice_id = "08e816816f5f496e8757268f2e0b633a"
        photo_talking_id = "76db764087a14ff683b6964c6ca62537"
        link_avatar_url = "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/mas_indo.jpg"
    elif avatar_name == "Ci Chindo":
        voice_id = "d7d6ae6ac0f64d1a9b1a8b26760096eb"
        photo_talking_id = "cae19979cd0e4203b2bcc702eaead13d"
        link_avatar_url = "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/ci_chindo.jpg"
    elif avatar_name == "Ko Chindo":
        voice_id = "5df1a994b0ae425dbe7f71c6d8dd2563"
        photo_talking_id = "ea33ba36a756400e8f9c131f955cd6b8"
        link_avatar_url = "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/ko_chindo.png"
    elif avatar_name == "Mba Indo":
        voice_id = "1b81540177114ec4bfda2a7a514e0e6b"
        photo_talking_id = "8183274ca6d947aa8c9ba7ccd5f3fdea"
        link_avatar_url = "https://ai-automation.tos-ap-southeast-3.bytepluses.com/avatar_list/mba_indo.jpg"
    
    return {
        "avatar_name": avatar_name,
        "voice_id": voice_id,
        "photo_talking_id": photo_talking_id,
        "link_avatar_url": link_avatar_url
    }
        