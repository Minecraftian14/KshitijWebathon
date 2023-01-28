import os


useSimpleTech = True

exportedSecretKey = os.environ['DJANGO_SECRET_KEY']
exportedDevMode = True
exportedMongoDBPassword = os.environ['MONGO_DB_ATLAS_PASSWORD']


def export_default_database(base_dir):
    # if useSimpleTech:
    if False:
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": base_dir / "dev_db"
        }
    return {
        "ENGINE": "djongo",
        "NAME": "dev_db",
        "CLIENT": {
            "host": f"mongodb+srv://Minecraftian14:{exportedMongoDBPassword}@developmentcluster.ep377hf.mongodb.net/?retryWrites=true&w=majority"
        }
    }
