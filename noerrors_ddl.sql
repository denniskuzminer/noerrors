CREATE table if not exists users (
	user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY ( user_id )
)

CREATE table if not exists favorites (
	favorite_id INT NOT NULL AUTO_INCREMENT,
    favorite_coin_name VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY ( favorite_id ),
    FOREIGN KEY ( user_id ) REFERENCES users(user_id)
)