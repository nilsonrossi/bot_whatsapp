-- `process-engine`.customer definition

CREATE TABLE `process-engine`.`customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profile_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(100) NOT NULL,
  `gender_opt` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- `process-engine`.flow definition

CREATE TABLE `process-engine`.`flow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `start_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `end_date` datetime DEFAULT NULL,
  `instance_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `flow_FK` (`customer_id`),
  CONSTRAINT `flow_FK` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;