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
VALUES (1, '테스트1', 'test_id_01', '$2b$12$3u8I4oywtcOuLoCzedjvCu0OWCfR5Dq1l/huAmrQKz7dCvX1EmmFi'),
       (2, '테스트2', 'test_id_02', '$2b$12$3u8I4oywtcOuLoCzedjvCu0OWCfR5Dq1l/huAmrQKz7dCvX1EmmFi');

INSERT
INTO post (id, post_text, user_id)
VALUES (1, '테스트1의 게시글입니다.', 1),
       (2, '테스트2의 게시글입니다.', 2),
       (3, '테스트3의 게시글 입니다', 1),
       (4, '테스트4의 게시글 입니다', 2),
       (5, '테스트5의 게시글 입니다', 1),
       (6, '테스트6의 게시글 입니다', 2),
       (7, '테스트7의 게시글 입니다', 1),
       (8, '테스트8의 게시글 입니다', 2),
       (9, '테스트9의 게시글 입니다', 1),
       (10, '테스트10의 게시글 입니다', 2),
       (11, '테스트11의 게시글 입니다', 1),
       (12, '테스트12의 게시글 입니다', 2),
       (13, '테스트13의 게시글 입니다', 1),
       (14, '테스트14의 게시글 입니다', 2),
       (15, '테스트15의 게시글 입니다', 1),
       (16, '테스트16의 게시글 입니다', 2),
       (17, '테스트17의 게시글 입니다', 1),
       (18, '테스트18의 게시글 입니다', 2),
       (19, '테스트19의 게시글 입니다', 1),
       (20, '테스트20의 게시글 입니다', 2);


INSERT
INTO comment (user_id, text, post_id)
VALUES (2, '테스트2가 테스트1의 글에 남긴 댓글입니다.', 1),
       (1, '테스트1이 테스트2의 글에 남긴 댓글입니다.', 2);

