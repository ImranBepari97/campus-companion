from CampusCompanion import db
import models

def populate():
    admin1 = models.CCUser("admin1@soton.ac.uk", "admin", True)
    admin2 = models.CCUser("admin2@soton.ac.uk", "admin", True)
    db.session.add(admin1)
    db.session.add(admin2)
    db.session.commit()
