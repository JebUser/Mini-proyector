import bcrypt

#Generates hashed_password
def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Generate the hash of the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password