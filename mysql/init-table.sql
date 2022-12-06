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

INSERT
    INTO post (post_text)
VALUES
('테스트3의 게시글 입니다'),
('테스트4의 게시글 입니다'),
('테스트5의 게시글 입니다'),
('테스트6의 게시글 입니다'),
('테스트7의 게시글 입니다'),
('테스트8의 게시글 입니다'),
('테스트9의 게시글 입니다'),
('테스트10의 게시글 입니다'),
('테스트11의 게시글 입니다'),
('테스트12의 게시글 입니다'),
('테스트13의 게시글 입니다'),
('테스트14의 게시글 입니다'),
('테스트15의 게시글 입니다'),
('테스트16의 게시글 입니다'),
('테스트17의 게시글 입니다'),
('테스트18의 게시글 입니다'),
('테스트19의 게시글 입니다'),
('테스트20의 게시글 입니다')
