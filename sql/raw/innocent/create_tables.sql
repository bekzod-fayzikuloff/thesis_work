/*
###############
# USERS TABLE #
###############
*/

CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    username VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(120) NOT NULL,
    CONSTRAINT validate_email
                        CHECK ( email ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$' ),
    PRIMARY KEY (id)
);
/*
##################
# PROFILES TABLE #
##################
*/
CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL NOT NULL,
    description VARCHAR(1000) NULL,
    user_id INT UNIQUE,
    CONSTRAINT user_fk
                        FOREIGN KEY (user_id)
                        REFERENCES users(id),
    PRIMARY KEY (id)
);

/*
##################
# FOLLOWERS TABLE #
##################
*/
CREATE TABLE IF NOT EXISTS followers (
    id SERIAL NOT NULL,
    follower_id INT NOT NULL,
    follow_to_id INT NOT NULL,

    CONSTRAINT follower_fk
                        FOREIGN KEY (follower_id)
                        REFERENCES profiles(id),

    CONSTRAINT follow_to_fk
                    FOREIGN KEY (follow_to_id)
                    REFERENCES profiles(id),

    UNIQUE (follower_id, follow_to_id),
    PRIMARY KEY (id)
);

/*
###############
# POSTS TABLE #
###############
*/
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL NOT NULL,
    description VARCHAR(1000) NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creator_id INT,
    CONSTRAINT creator_fk
                        FOREIGN KEY (creator_id)
                        REFERENCES profiles(id),
    PRIMARY KEY (id)
);

/*
#####################
# MEDIA_TYPES TABLE #
#####################
*/
CREATE TABLE IF NOT EXISTS media_types(
    id SERIAL NOT NULL,
    type_name VARCHAR(120) NOT NULL,
    extension VARCHAR(40) NOT NULL,
    PRIMARY KEY (id)
);

/*
#######################
# POST_CONTENTS TABLE #
#######################
*/
CREATE TABLE IF NOT EXISTS post_contents(
    id SERIAL NOT NULL,
    path VARCHAR(120) NOT NULL,
    post_id INT NOT NULL,
    media_type_id INT NOT NULL,

    CONSTRAINT post_fk
                    FOREIGN KEY (post_id)
                    REFERENCES posts(id),
    CONSTRAINT media_type_fk
                    FOREIGN KEY (media_type_id)
                    REFERENCES media_types(id),

    PRIMARY KEY (id)
);


/*
##################
# REACTION TABLE #
##################
*/

CREATE TABLE IF NOT EXISTS reactions (
    id SERIAL NOT NULL,
    positive BOOLEAN,
    is_active BOOLEAN DEFAULT FALSE,
    reacted_by_id INT NOT NULL,
    post_id INT NOT NULL,
    CONSTRAINT reacted_by_fk
                        FOREIGN KEY (reacted_by_id)
                        REFERENCES profiles(id),
    CONSTRAINT post_fk
                        FOREIGN KEY (post_id)
                        REFERENCES posts(id),
    PRIMARY KEY (id)
);

/*
#################
# COMMENT TABLE #
#################
*/

CREATE TABLE IF NOT EXISTS comments (
    id SERIAL NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    creator_id INT NOT NULL ,
    post_id INT NOT NULL,
    answer_comment_id INT NULL,

    CONSTRAINT creator_fk
                        FOREIGN KEY (creator_id)
                        REFERENCES profiles(id),
    CONSTRAINT post_fk
                        FOREIGN KEY (post_id)
                        REFERENCES posts(id),
    CONSTRAINT answer_comment_fk
                        FOREIGN KEY (answer_comment_id)
                        REFERENCES comments(id),

    PRIMARY KEY (id)
);


/*
##############
# CHAT TABLE #
##############
*/
CREATE TABLE IF NOT EXISTS chats (
    id SERIAL NOT NULL,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000) NULL,
    chat_uuid VARCHAR(50) NULL,
    created DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (id)
);

/*
######################
# CHAT_MEMBERS TABLE #
######################
*/
CREATE TABLE IF NOT EXISTS chat_members (
    id SERIAL NOT NULL,
    member_id INT NOT NULL,
    chat_id INT NOT NULL,

    CONSTRAINT member_fk
                        FOREIGN KEY (member_id)
                        REFERENCES profiles(id),
    CONSTRAINT chat_fk
                        FOREIGN KEY (chat_id)
                        REFERENCES chats(id),

    UNIQUE (member_id, chat_id),
    PRIMARY KEY (id)
);

/*
#################
# MESSAGE TABLE #
#################
*/
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL NOT NULL,
    content VARCHAR(2000),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    sender_id INT NOT NULL,
    chat_id INT NOT NULL,

    CONSTRAINT sender_fk
                        FOREIGN KEY (sender_id)
                        REFERENCES profiles(id),
    CONSTRAINT chat_fk
                        FOREIGN KEY (chat_id)
                        REFERENCES chats(id),
    PRIMARY KEY (id)
);
