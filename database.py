import os
import json

DATA_PATH="data"

PROFILE_FILE=os.path.join(
    DATA_PATH,
    "student_profile.json"
)


def ensure():

    os.makedirs(DATA_PATH,exist_ok=True)


def load_profile():

    ensure()

    if not os.path.exists(PROFILE_FILE):

        profile={

            "name":"Student",
            "difficulty":"easy",
            "weak_topics":[],
            "quiz_scores":[],
            "xp":0,
            "achievements":[]
        }

        save_profile(profile)

        return profile

    with open(PROFILE_FILE,"r") as f:

        return json.load(f)



def save_profile(profile):

    ensure()

    with open(PROFILE_FILE,"w") as f:

        json.dump(profile,f,indent=2)



def add_score(score):

    profile=load_profile()

    profile["quiz_scores"].append(score)

    profile["xp"]+=score

    if score>80:

        profile["achievements"].append(
            "⭐ High Performer"
        )

    save_profile(profile)

    return profile
