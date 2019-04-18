x = {
    "desc":"You wake up in your bed and remember nothing",
    "choices":["Check your phone", "Check your computer"],
    "next_scenes":{
        "1":{
            "desc":"Your phone is locked. You don't know the password",
            "choices":["Go back"],
            "art":None,
            "next_scenes":{}
        },
        "2":{
            "desc":"You use your computer that you left open",
            "choices":["Check google maps, Check social media, Check email"],
            "art":None,
            "next_scenes":{}
        }
    },
    "art":None
}

y = x['next_scenes']
print(y)
# y['next_scenes']