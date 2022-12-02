CREATE DATABASE hotsix;

USE hotsix;

CREATE TABLE user
(
    id               int PRIMARY KEY AUTO_INCREMENT,
    name             varchar(30) UNIQUE NOT NULL,
    login_id         varchar(30) UNIQUE NOT NULL,
    password         varchar(30)        NOT NULL,
    profile_image    LONGBLOB,
    background_image LONGBLOB
);

CREATE TABLE post
(
    id        int PRIMARY KEY AUTO_INCREMENT,
    post_text varchar(30) NOT NULL,
    user_id   int,
    image     LONGBLOB,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE comment
(
    id      int PRIMARY KEY AUTO_INCREMENT,
    user_id int,
    text    varchar(30) NOT NULL,
    post_id int,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (post_id) REFERENCES post (id)
);