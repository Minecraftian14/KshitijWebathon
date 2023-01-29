import os


useSimpleTech = True

exportedSecretKey = os.environ['DJANGO_SECRET_KEY']
exportedDevMode = True
exportedMongoDBPassword = os.environ['MONGO_DB_ATLAS_PASSWORD']


def export_default_database(base_dir):
    return {
        "ENGINE": "djongo",
        "NAME": "dev_db",
        "CLIENT": {
            "host": f"mongodb+srv://Minecraftian14:{exportedMongoDBPassword}@developmentcluster.ep377hf.mongodb.net/?retryWrites=true&w=majority"
        }
    }
