CREATE TABLE `user_details` (
  `seq_no` int AUTO_INCREMENT,
  `user_id` varchar(20) PRIMARY KEY,
  `password` varchar(20),
  `name` varchar(20),
  `age` date,
  `city` varchar(20)
);

CREATE TABLE `post_type` (
  `post_type` varchar(30) PRIMARY KEY
);

CREATE TABLE `user_post` (
  `user_id` varchar(20),
  `post_id` varchar(30) PRIMARY KEY,
  `post_stamp` datetime,
  `post_type` varchar(30),
  `like_count` int,
  `comment_ref_id` varchar(30)
);

CREATE TABLE `comment_table` (
  `comment_id` varchar(30) PRIMARY KEY,
  `commenter_id` varchar(20),
  `time_stamp` datetime,
  `comment_content` varchar(256)
);

ALTER TABLE `user_details` ADD FOREIGN KEY (`user_id`) REFERENCES `comment_table` (`commenter_id`);

ALTER TABLE `user_details` ADD FOREIGN KEY (`user_id`) REFERENCES `user_post` (`user_id`);

ALTER TABLE `post_type` ADD FOREIGN KEY (`post_type`) REFERENCES `user_post` (`post_type`);

ALTER TABLE `user_post` ADD FOREIGN KEY (`comment_ref_id`) REFERENCES `comment_table` (`comment_id`);
