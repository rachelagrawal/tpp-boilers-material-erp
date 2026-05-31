class Config:
    SECRET_KEY = "tpp_boilers_secret"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root@localhost/material_erp"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False