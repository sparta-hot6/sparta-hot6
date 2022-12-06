CREATE DATABASE hotsix;

USE hotsix;

CREATE TABLE user
(
    id               int PRIMARY KEY AUTO_INCREMENT,
    name             varchar(30) UNIQUE NOT NULL,
    login_id         varchar(30) UNIQUE NOT NULL,
    password         varchar(30)        NOT NULL,
    profile_image    varchar(100),
    background_image varchar(100)
);

CREATE TABLE post
(
    id        int PRIMARY KEY AUTO_INCREMENT,
    post_text varchar(30) NOT NULL,
    user_id   int,
    image     varchar(100),
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

INSERT
INTO user (id, name, login_id, password)
VALUES (1, '테스트1', 'test_id_01', 'test1'),
       (2, '테스트2', 'test_id_02', 'test2')

INSERT
INTO post (id, post_text, user_id)
VALUES (1, '테스트1의 게시글입니다.', 1),
       (2, '테스트2의 게시글입니다.', 2)

INSERT
INTO comment (id, user_id, text, post_id)
VALUES (1, 2, '테스트2가 테스트1의 글에 남긴 댓글입니다.', 1),
       (2, 1, '테스트1이 테스트2의 글에 남긴 댓글입니다.', 2)